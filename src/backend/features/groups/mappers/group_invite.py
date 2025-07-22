from urllib.parse import urljoin

from fastapi import Request

from features.groups.models import GroupInvite
from features.groups.schemas import GroupInviteReadWithLink


def build_group_invite_read_with_link(
    group_invite: GroupInvite,
    request: Request,
) -> GroupInviteReadWithLink:
    base_schema = group_invite.get_validation_schema()
    base_url = str(request.base_url).rstrip("/")
    return base_schema.to_with_link(
        urljoin(
            base_url, f"/api/groups/{base_schema.space_id}/invites/{base_schema.code}"
        )
    )


def build_group_invite_read_with_link_list(
    group_invites: list[GroupInvite],
    request: Request,
) -> list[GroupInviteReadWithLink]:
    return [
        build_group_invite_read_with_link(group_invite, request)
        for group_invite in group_invites
    ]
