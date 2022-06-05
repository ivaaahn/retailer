import asyncio
import base64
import time
from asyncio import gather
from dataclasses import dataclass
from pprint import pprint
from typing import Any, Coroutine, NamedTuple

import aiofiles
import aiohttp
from bs4 import BeautifulSoup, BeautifulSoup as bs, PageElement

from scripts.faker.rw import write

COUNT = 10
PRODUCTS_FILE = "data/products.csv"
CATEGORIES_FILE = "data/product_categories.csv"

C_INDEX = 1

URL = "https://fitaudit.ru/categories/fds"


class ProductTemp(NamedTuple):
    name: str
    task: Coroutine[Any, Any, str]


@dataclass
class CategoryTemp:
    id: int
    name: str
    products: list[ProductTemp]


@dataclass
class Category:
    id: int
    name: str


@dataclass
class Product:
    name: str
    category_id: int
    photo: str | None = None
    description: str | None = None


async def generate(to_file: bool = False) -> None:
    soup = _parse_html(await _fetch_html(URL))
    cat, prod = await _parse_products(soup)
    pprint(cat)
    pprint(prod)

    #
    # temp_categories = _parse_categoris_names(main_page)
    # categories = [Category(c.id, c.name) for c in temp_categories]
    #
    # products: list[Product] = []
    #
    # unique_names = set()
    # for p in await _parse_products(temp_categories):
    #     if p.name not in unique_names:
    #         products.append(
    #             Product(
    #                 name=p.name,
    #                 category_id=p.category.id,
    #                 photo=p.photo,
    #                 description=p.description,
    #             )
    #         )
    #         unique_names.add(p.name)

    if to_file:
        write(cat, CATEGORIES_FILE)
        write(prod, PRODUCTS_FILE)


async def _fetch_html(url: str) -> str:
    async with aiohttp.ClientSession() as client:
        async with client.get(url) as resp:
            return await resp.text()

async def _parse_product_photo_mock(url: str, name: str) -> str | None:
    path = f"data/products/{name.replace(' ', '_').lower()}"
    return path[5:]

async def _parse_product_photo(url: str, name: str) -> str | None:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            while resp.status == 503:
                print(name, " page: ", resp.status)
                print("WAITING..........")
                await asyncio.sleep(10)
                resp = await session.get(url)

            print(name, " page: ", resp.status)
            product_soup = _parse_html(await resp.text())
            try:
                img_url_tail = product_soup.find(id="fixmixed")["data-image-src"]
            except TypeError:
                print("!!!!!!!!!TYPEERROR!!!!!!!!!!!!!!")
                print(name)
                print(product_soup.find(id="fixmixed"))
                print("!!!!!!!!!TYPEERROR!!!!!!!!!!!!!!")

            full_img_url = "https://fitaudit.ru/" + img_url_tail

        async with session.get(full_img_url) as resp:
            print(name, " photo: ", resp.status)
            if resp.status == 404:
                return None
            path = f"data/products/{name.replace(' ', '_').lower()}"
            f = await aiofiles.open(path, mode="wb")
            await f.write(await resp.read())
            await f.close()

        await asyncio.sleep(0.5)

    return path[5:]


def _parse_html(html: str) -> BeautifulSoup:
    return bs(html, "lxml")


def _parse_categories_names(soup: BeautifulSoup) -> list[str]:
    categories_class = "pr__ind_c pr__ind_c_mbottom fimlist__title_groups"

    headers = soup.find_all(class_=categories_class)

    return [header.text for header in headers]


def _parse_product_table(product_table: PageElement) -> list[ProductTemp]:
    return [
        ProductTemp(
            name=item["title"], task=_parse_product_photo(item["href"], item["title"])
        )
        for item in product_table.find_all("a", class_="vertical_pseudo")
    ]


async def _parse_products_photo(
    categories: list[CategoryTemp],
) -> list[tuple[str, ...]]:
    all_coros = [[p.task for p in category.products] for category in categories]
    return [
        await gather(*category_products_coros) for category_products_coros in all_coros
    ]


async def _parse_products(soup: BeautifulSoup) -> tuple[list[Category], list[Product]]:
    global C_INDEX
    categories_names: list[str] = _parse_categories_names(soup)

    products_separated_by_categories: list[CategoryTemp] = []

    for product_table, category_name in zip(
        soup.find_all(class_="fimlist fimlist__items"), categories_names
    ):
        products_separated_by_categories.append(
            CategoryTemp(
                id=C_INDEX,
                name=category_name,
                products=_parse_product_table(product_table),
            )
        )
        C_INDEX += 1
    products_photo_paths = await _parse_products_photo(
        categories=products_separated_by_categories
    )

    res_categories: list[Category] = []
    res_products: list[Product] = []

    for category, category_products_photo_paths in zip(
        products_separated_by_categories,
        products_photo_paths
    ):
        res_categories.append(Category(id=category.id, name=category.name))
        for product, product_photo_path in zip(
            category.products, category_products_photo_paths
        ):
            res_products.append(
                Product(
                    name=product.name, category_id=category.id, photo=product_photo_path
                )
            )
    return res_categories, res_products

if __name__ == "__main__":
    asyncio.run(generate(to_file=True))
