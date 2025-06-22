from shared.exceptions import NotFoundException


class ModuleNotFoundException(NotFoundException):
    detail: str = "Module not found"
