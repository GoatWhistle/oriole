from shared.exceptions import TimingException


class TaskStartBeforeModuleStartException(TimingException):
    detail = "Task start deadline cannot be earlier than module start deadline."


class TaskEndAfterModuleEndException(TimingException):
    detail = "Task end deadline cannot be later than module end deadline."
