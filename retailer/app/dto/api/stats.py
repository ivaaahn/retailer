from datetime import date

from pydantic import BaseModel, Field


class StatEntityDTO(BaseModel):
    shop_id: int = Field(title="Идентификатор магазина")
    shop_orders_qty: int = Field(
        title="Общее количество заказов в магазине за период"
    )
    shop_total_profit: float = Field(title="Общий доход в магазине за период")
    shop_address: str = Field(title="Адрес магазина")
    client_name: str = Field(title="Полное имя лучшего клиента")
    client_orders_qty: int = Field(
        title="Количество заказов клиента за период"
    )
    client_spend: float = Field(title="Сумма, потраченная клиентом за период")


class StatRespDTO(BaseModel):
    best_shops: list[StatEntityDTO] = Field(
        title="Список самых доходных магазинов", default_factory=list
    )


class StatReqDTO(BaseModel):
    count: int = Field(title="Количество магазинов")
    data_from: date = Field(title="Дата начала периода")
    data_to: date = Field(title="Дата окончания периода")
