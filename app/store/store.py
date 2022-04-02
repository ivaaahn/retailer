from core.settings import Settings, get_settings
from store.pg.connect import PgConnect


class Store:
    def __init__(self, settings: "Settings"):
        self.pg = PgConnect(settings.pg)


store = Store(get_settings())
