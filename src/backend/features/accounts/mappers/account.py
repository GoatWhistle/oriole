from features.accounts.models import Account
from features.accounts.schemas import AccountReadWithProfileData
from features.users.models import UserProfile


def build_account_read_with_profile_data(
    account: Account,
    user_profile: UserProfile,
) -> AccountReadWithProfileData:
    base_schemas = account.get_validation_schema()
    return base_schemas.to_with_profile_data(
        name=user_profile.name,
        surname=user_profile.surname,
        patronymic=user_profile.patronymic,
    )


def build_account_read_with_profile_data_list(
    accounts: list[Account],
    user_profiles: list[UserProfile],
) -> list[AccountReadWithProfileData]:
    profiles_by_user_id = {profile.user_id: profile for profile in user_profiles}

    result = []
    for account in accounts:
        profile = profiles_by_user_id.get(account.user_id)
        if profile:
            result.append(build_account_read_with_profile_data(account, profile))
    return result
