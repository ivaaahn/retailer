import asyncio

from fastapi import Depends

from app.base.services import BaseService
from app.dto.api.cart import CartRespDTO
from app.dto.api.products import CartProductDTO
from app.dto.db.products import DBCartProductDTO
from app.repos.cart import CartsRepo
from app.services import ProductsService
from app.services.carts.interfaces import ICartsRepo

__all__ = ("CartService",)


class CartService(BaseService):
    def __init__(
        self,
        carts_repo: ICartsRepo = Depends(CartsRepo),
        products_service: ProductsService = Depends(),
    ):
        super().__init__()
        self._carts_repo = carts_repo
        self._products_service = products_service

    async def clear_cart(self, email: str) -> int:
        return await self._carts_repo.clear_cart(email)

    async def update_cart(self, email: str, product_id: int, qty: int):
        if qty == 0:
            await self._carts_repo.remove(email, product_id)
        else:
            await self._carts_repo.add_to_cart(
                email=email, dto=DBCartProductDTO(product_id, qty)
            )

    async def get(self, email: str, shop_id: int) -> CartRespDTO:
        cart_raw = await self._carts_repo.get(email)

        if not cart_raw.products:
            return CartRespDTO(products=[], total_price=0.0)

        total_price = 0.0
        products = await asyncio.gather(
            *[
                self._products_service.get(product_raw.product_id, shop_id)
                for product_raw in cart_raw.products
            ]
        )

        res: list[CartProductDTO] = []
        for product, cart_product_info in zip(products, cart_raw.products):
            total_product_price = product.price * cart_product_info.qty
            res.append(
                CartProductDTO(
                    product=product,
                    qty=cart_product_info.qty,
                    price=total_product_price,
                )
            )
            total_price += total_product_price

        return CartRespDTO(
            products=res,
            total_price=total_price,
        )
