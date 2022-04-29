from fastapi import APIRouter

from app.dto.cart import CartRespDTO
from app.dto.products import ShopProductDTO, CartProductDTO

router = APIRouter(
    prefix="/cart",
    tags=["cart"],
)


@router.get("", response_model=CartRespDTO)
async def get() -> CartRespDTO:
    return CartRespDTO(
        products=[
            CartProductDTO(
                id=1,
                name="молоко",
                description="годен 3 дня после открытия",
                category="молочные продукты",
                price=88.5,
                qty=1,
            ),
            CartProductDTO(
                id=1,
                name="Морковь по корейски",
                category="закуски",
                price=99,
                qty=1,
            ),
        ],
        total_price=187.5,
    )


@router.patch("")
async def update(product_id: int, qty: int) -> CartRespDTO:
    return CartRespDTO(
        products=[
            CartProductDTO(
                id=product_id,
                name="молоко",
                description="годен 3 дня после открытия",
                category="молочные продукты",
                price=88.5,
                qty=qty,
            ),
            CartProductDTO(
                id=7,
                name="Морковь по корейски",
                category="закуски",
                price=99,
                qty=3,
            ),
        ],
        total_price=187.5,
    )
