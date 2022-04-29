from fastapi import Depends, APIRouter

from app.delivery.shop.deps import ShopListPagingParams
from app.delivery.shop.deps import shop_paging_params
from app.dto.shop import ShopRespDTO, ShopListRespDTO, ShopAddressDTO

router = APIRouter(
    prefix="/shop",
    tags=["shop"],
)


@router.get("", response_model=ShopRespDTO)
async def get_shop(
    id: int,
):
    return ShopRespDTO(
        id=id,
        address=ShopAddressDTO(
            id=id,
            city="Москва",
            street="Авиамоторная",
            house=2,
        ),
    )


@router.get(".list", response_model=ShopListRespDTO)
async def get_list(paging_params: ShopListPagingParams = Depends(shop_paging_params)):
    return ShopListRespDTO(
        shops=[
            ShopRespDTO(
                id=1,
                address=ShopAddressDTO(id=1, city="Москва", street="Набережная", house="25А"),
            ),
            ShopRespDTO(
                id=2,
                address=ShopAddressDTO(id=2, city="Москва", street="Советская", house=48),
            ),
            ShopRespDTO(
                id=3,
                address=ShopAddressDTO(id=2, city="Москва", street="Ленина", house=41),
            ),
            ShopRespDTO(
                id=4,
                address=ShopAddressDTO(id=2, city="Москва", street="Карла-Маркса", house=121),
            ),
            ShopRespDTO(
                id=5,
                address=ShopAddressDTO(id=2, city="Москва", street="Зеленая", house=10),
            ),
            ShopRespDTO(
                id=6,
                address=ShopAddressDTO(id=2, city="Москва", street="3-я Парковая", house=7),
            ),
        ],
        total=6,
    )
