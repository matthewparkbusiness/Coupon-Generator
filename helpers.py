import uuid

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

def format_money(amount: int, sign: bool = False) -> str:
    sign_str = "+" if amount >= 0 else "-"
    return f"{sign_str if sign else ''}${abs(amount) / 100:,.2f}"

DISPLAY_WIDTH = 70
NAMESPACE_ID = uuid.UUID("15820273928395740272882900047382")

