from core.settings import Settings, get_settings
from store.pg.connect import PgConnect
from store.rmq import RMQConnect


class Store:
    def __init__(self, settings: "Settings"):
        self.pg = PgConnect(settings.pg)
        self.rmq = RMQConnect(settings.rmq)


store = Store(get_settings())
