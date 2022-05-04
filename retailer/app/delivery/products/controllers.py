from fastapi import Depends, APIRouter

from app.delivery.products.deps import ProductListPagingParams, product_paging_params
from app.dto.products import ShopProductsListDTO, ShopProductDTO
from app.services import ProductsService

router = APIRouter(
    prefix="/product",
    tags=["product"],
)


@router.get("", response_model=ShopProductDTO)
async def get(
    product_id: int, shop_id: int, product_service: ProductsService = Depends()
) -> ShopProductDTO:
    return await product_service.get(product_id, shop_id)


@router.get(".list", response_model=ShopProductsListDTO)
async def get_list(
    shop_id: int,
    paging_params: ProductListPagingParams = Depends(product_paging_params),
) -> ShopProductsListDTO:
    return ShopProductsListDTO(
        products=[
            ShopProductDTO(
                id=1,
                photo="https://media.istockphoto.com/photos/close-up-of-steaming-cup-of-coffee-or-tea-on-vintage-table-early-on-picture-id1137365972?s=612x612",
                name="Random Name #1",
                description="Probably the most random thing you have ever seen!",
                price=100,
                category="Category1",
            ),
            ShopProductDTO(
                id=2,
                photo="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSwTNyJU1T0rmUUnCottIoWbwHfQqjBvkVpwSvwh4r3LPoUN5TBqEE9aOcgquwwl0MUgYc&usqp=CAU",
                name="Random Name #2",
                description="Hello World!",
                price=100,
                category="Category2",
            ),
            ShopProductDTO(
                id=3,
                name="Random Name #3",
                description="Hello World!",
                photo="https://st.depositphotos.com/2632165/3063/i/600/depositphotos_30638835-stock-photo-coffee.jpg",
                price=100,
                category="Category2",
            ),
            ShopProductDTO(
                id=4,
                name="Random Name #4",
                description="Hello World!",
                photo="https://cdn.pixabay.com/photo/2017/05/12/08/29/coffee-2306471__340.jpg",
                price=100,
                category="Category2",
            ),
            ShopProductDTO(
                id=5,
                name="Random Name #5",
                description="Hello World!",
                price=100,
                category="Category1",
            ),
            ShopProductDTO(
                id=6,
                name="Random Name #2",
                description="Hello World!",
                price=100,
                category="Category1",
            ),
            ShopProductDTO(
                id=7,
                name="Random Name #2",
                description="Hello World!",
                price=100,
                category="Category2",
            ),
        ],
        total=7,
    )
