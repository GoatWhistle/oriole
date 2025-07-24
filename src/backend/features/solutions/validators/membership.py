from features import Account, BaseSolution
from features.solutions.exceptions.membership import UserNotCreatorOfSolutionException


def check_user_is_creator_of_solution(
    account: Account,
    solution: BaseSolution,
):
    if account.id != solution.creator_id:
        raise UserNotCreatorOfSolutionException()
