from app.delivery.auth.deps import get_current_active_user
from app.dto.api.cart import CartRespDTO
from app.dto.api.user import UserRespDTO
from app.services.carts.service import CartService
from fastapi import APIRouter, Depends, Query

router = APIRouter(
    prefix="/cart",
    tags=["cart"],
)


@router.get("", response_model=CartRespDTO)
async def get(
    cart_service: CartService = Depends(),
    shop_id: int = Query(..., title="Идентификатор магазина"),
    user: UserRespDTO = Depends(get_current_active_user),
) -> CartRespDTO:
    return await cart_service.get(user.email, shop_id)


@router.delete("", response_model=CartRespDTO)
async def delete(
    cart_service: CartService = Depends(),
    user: UserRespDTO = Depends(get_current_active_user),
) -> int:
    return await cart_service.clear_cart(user.email)


@router.patch("", response_model=CartRespDTO)
async def patch(
    shop_id: int = Query(..., title="Идентификатор магазина"),
    product_id: int = Query(..., title="Идентификатор продукта"),
    qty: int = Query(..., title="Количество (0 - удалить из корзины)", gt=-1),
    user: UserRespDTO = Depends(get_current_active_user),
    cart_service: CartService = Depends(),
) -> CartRespDTO:
    await cart_service.update_cart(
        email=user.email,
        product_id=product_id,
        qty=qty,
    )

    return await cart_service.get(user.email, shop_id)
