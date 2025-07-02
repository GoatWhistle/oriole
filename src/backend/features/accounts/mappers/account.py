from features.groups.models import Account
from features.groups.schemas import AccountRead
from features.users.models import UserProfile
from features.users.schemas import UserProfileRead


def build_account_read(account: Account, user_profile: UserProfile) -> AccountRead:
    return AccountRead(
        user_profile=UserProfileRead.model_validate(user_profile),
        role=account.role,
    )


def build_account_read_list(
    accounts: list[Account],
    user_profiles: list[UserProfile],
) -> list[AccountRead]:
    profiles_by_user_id = {profile.user_id: profile for profile in user_profiles}

    result = []
    for account in accounts:
        profile = profiles_by_user_id.get(account.user_id)
        if profile:
            result.append(build_account_read(account, profile))
    return result
