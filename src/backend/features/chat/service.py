from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from starlette.websockets import WebSocket, WebSocketDisconnect
from .manager import connection_manager
from .models import Message
import json


async def handle_websocket(
    websocket: WebSocket, group_id: int, user_id: int, session: AsyncSession
):
    await connection_manager.connect(websocket, group_id, user_id)

    try:
        history_stmt = (
            select(Message)
            .where(Message.group_id == group_id)
            .order_by(Message.timestamp)
        )
        result = await session.execute(history_stmt)
        messages = result.scalars().all()

        msg_dict = {msg.id: msg for msg in messages}

        history_payload = [
            {
                "user_id": msg.sender_id,
                "message": msg.text,
                "timestamp": msg.timestamp.isoformat(),
                "message_id": msg.id,
                "reply_to": msg.reply_to,
                "reply_to_text": (
                    msg_dict[msg.reply_to].text if msg.reply_to in msg_dict else None
                ),
            }
            for msg in messages
        ]
        await websocket.send_text(
            json.dumps({"type": "history", "messages": history_payload})
        )

        while True:
            raw_data = await websocket.receive_text()
            try:
                data = json.loads(raw_data)
                if data.get("type") == "edit":
                    new_text = data.get("new_text")
                    message_id = data.get("message_id")
                    updated_message = await update_message(
                        user_id=user_id,
                        new_text=new_text,
                        session=session,
                        message_id=message_id,
                    )
                    if updated_message:
                        upd_msg = {
                            "user_id": user_id,
                            "message": new_text,
                            "timestamp": updated_message.timestamp.isoformat(),
                            "connectionId": data.get("connectionId"),
                            "message_id": message_id,
                        }
                        await connection_manager.broadcast(
                            group_id=group_id, message=json.dumps(upd_msg)
                        )
                        continue
                if data.get("type") == "delete":
                    deleted_message_id = data.get("message_id")
                    deleted = await delete_message(
                        message_id=deleted_message_id, session=session, user_id=user_id
                    )
                    if deleted:
                        del_msg = {
                            "type": "delete",
                            "deleted_message_id": deleted_message_id,
                            "connectionId": data.get("connectionId"),
                        }
                        await connection_manager.broadcast(
                            group_id=group_id, message=json.dumps(del_msg)
                        )
                        continue
                text = data.get("message", "")
                if not text:
                    continue

                timestamp = datetime.now(timezone.utc)
                reply_to = data.get("reply_to")
                reply_to_text = data.get("reply_to_text")
                message = Message(
                    text=text,
                    group_id=group_id,
                    sender_id=user_id,
                    timestamp=timestamp,
                    reply_to=reply_to,
                )
                session.add(message)
                await session.commit()

                msg = {
                    "user_id": user_id,
                    "message": text,
                    "timestamp": timestamp.isoformat(),
                    "connectionId": data.get("connectionId"),
                    "message_id": message.id,
                    "reply_to": reply_to,
                    "reply_to_text": reply_to_text,
                }
                await connection_manager.broadcast(group_id, json.dumps(msg))

            except json.JSONDecodeError:
                print("[websocket] Invalid JSON")

    except WebSocketDisconnect:
        await connection_manager.disconnect(group_id, websocket)


async def update_message(
    user_id: int,
    message_id: int,
    session: AsyncSession,
    new_text: str,
):
    message = await session.get(Message, message_id)
    if message and message.sender_id == user_id:
        message.text = new_text
        await session.commit()
        return message
    return None


async def delete_message(
    user_id: int,
    message_id: int,
    session: AsyncSession,
):
    message = await session.get(Message, message_id)
    if message and message.sender_id == user_id:
        await session.delete(message)
        await session.commit()
        return message
    return None


"""

async def get_user_groups(
    session: AsyncSession,
    user_id: int,
) -> list[GroupRead]:
    await check_user_exists(session, user_id)

    accounts = await account_crud.get_accounts_by_user_id(session, user_id)
    if not accounts:
        return []

    group_ids = [account.group_id for account in accounts]

    groups = await group_crud.get_groups_by_ids(session, group_ids)
    all_group_accounts = await account_crud.get_accounts_in_groups(session, group_ids)
    modules = await module_crud.get_modules_by_group_ids(session, group_ids)

    tasks = await task_crud.get_tasks_by_module_ids(
        session, [module.id for module in modules]
    )

    user_replies = await user_reply_crud.get_user_replies(
        session, [account.id for account in accounts], [task.id for task in tasks]
    )

    user_profiles = await user_profile_crud.get_user_profiles_by_user_ids(
        session, [account.user_id for account in all_group_accounts]
    )

    return mapper.build_group_read_list(
        groups, all_group_accounts, user_profiles, modules, tasks, user_replies
    )
@router.get(
    "/",
    response_model=list[GroupRead],
    status_code=status.HTTP_200_OK,
)
async def get_user_groups(
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    return await service.get_user_groups(session, user_id)
    
    
    
    from features.groups.mappers import build_account_read_list
from features.groups.models import Group, Account
from features.groups.schemas import GroupRead, AccountRead
from features.modules.mappers import build_module_read_list
from features.modules.models import Module
from features.modules.schemas import ModuleRead
from features.tasks.models import Task, UserReply
from features.users.models import UserProfile


def build_group_read(
    group: Group,
    accounts: list[Account],
    user_profiles: list[UserProfile],
    modules: list[Module] | None = None,
    tasks: list[Task] | None = None,
    user_replies: list[UserReply] | None = None,
) -> GroupRead:
    modules = modules or []
    tasks = tasks or []
    user_replies = user_replies or []

    account_reads: list[AccountRead] = build_account_read_list(accounts, user_profiles)

    module_reads: list[ModuleRead] = build_module_read_list(
        modules=modules,
        tasks=tasks,
        user_replies=user_replies,
    )

    return GroupRead(
        id=group.id,
        title=group.title,
        description=group.description,
        accounts=account_reads,
        modules=module_reads,
    )


def build_group_read_list(
    groups: list[Group],
    accounts: list[Account],
    user_profiles: list[UserProfile],
    modules: list[Module],
    tasks: list[Task],
    user_replies: list[UserReply],
) -> list[GroupRead]:
    accounts_by_group_id: dict[int, list[Account]] = {}
    for account in accounts:
        accounts_by_group_id.setdefault(account.group_id, []).append(account)

    modules_by_group_id: dict[int, list[Module]] = {}
    for module in modules:
        modules_by_group_id.setdefault(module.group_id, []).append(module)

    tasks_by_module_id: dict[int, list[Task]] = {}
    for task in tasks:
        tasks_by_module_id.setdefault(task.module_id, []).append(task)

    group_read_list: list[GroupRead] = []

    for group in groups:
        group_accounts = accounts_by_group_id.get(group.id, [])
        group_modules = modules_by_group_id.get(group.id, [])

        account_reads: list[AccountRead] = build_account_read_list(
            group_accounts, user_profiles
        )

        group_module_ids = {module.id for module in group_modules}
        group_tasks = [task for task in tasks if task.module_id in group_module_ids]

        module_reads = build_module_read_list(group_modules, group_tasks, user_replies)

        group_read_list.append(
            GroupRead(
                title=group.title,
                description=group.description,
                id=group.id,
                accounts=account_reads,
                modules=module_reads,
            )
        )

    return group_read_list
"""
