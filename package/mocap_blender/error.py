class BaseError(Exception):
    def __init__(self, msg: str = "") -> None:
        super(BaseError).__init__()
        self.msg = msg

    def __str__(self) -> str:
        return f"[{self.__class__.__name__}] {self.msg}"


class MeshError(BaseError):
    def __init__(self, msg: str = "") -> None:
        super().__init__(msg)
