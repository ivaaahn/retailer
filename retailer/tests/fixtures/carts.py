import pytest

from retailer.app.dto.api.cart import CartRespDTO
from retailer.app.dto.api.products import CartProductDTO, ShopProductsListDTO
from retailer.app.dto.db.products import (
    DBCartInfoDTO,
    DBCartProductDTO,
    DBShopProductListDTO,
)
from retailer.app.services import ProductsService
from retailer.app.services.carts import CartService
from retailer.tests.builders.db.cart_product import CartApiBuilder
from retailer.tests.mocks import CartsRepoMock


@pytest.fixture
def default_cart_built(
    default_products_list_built: DBShopProductListDTO,
) -> DBCartInfoDTO:
    return DBCartInfoDTO(
        products=[
            DBCartProductDTO(
                product_id=p.id,
                qty=p.id,
            )
            for p in default_products_list_built.products
        ]
    )


@pytest.fixture
def default_cart_resp_built(
    default_products_list_s3_patched_built: ShopProductsListDTO,
    default_cart_built: DBCartInfoDTO,
) -> CartRespDTO:
    products = default_products_list_s3_patched_built.products
    cart_raw = default_cart_built.products

    res: list[CartProductDTO] = [
        CartProductDTO(
            product=product,
            qty=cart_product.qty,
            price=product.price * cart_product.qty,
        )
        for product, cart_product in zip(products, cart_raw)
    ]

    return CartRespDTO(
        products=res,
        total_price=sum(p.price for p in res),
    )


@pytest.fixture
def cart_service(
    carts_repo_mock: CartsRepoMock,
    products_service: ProductsService,
) -> CartService:
    return CartService(
        carts_repo=carts_repo_mock,
        products_service=products_service,
    )


@pytest.fixture
def cart_api_builder() -> CartApiBuilder:
    return CartApiBuilder()
