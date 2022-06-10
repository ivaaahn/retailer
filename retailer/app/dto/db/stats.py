from dataclasses import dataclass


@dataclass
class DBStatOrdersDTO:
    shop_id: int
    shop_orders_qty: int
    shop_total_profit: float
    shop_address: str
    client_name: str
    client_orders_qty: int
    client_spend: float
