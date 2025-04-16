from ..Helpers.Helpers import Helpers

class User:
    def __init__(self, name: str, account_balance: float) -> None:
        self.__id__:str = Helpers.random_key(5)
        self.name:str = name
        self.account_balance:float = account_balance