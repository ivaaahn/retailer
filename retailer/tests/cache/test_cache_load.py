import asyncio
import random
import time
from dataclasses import asdict, dataclass

import matplotlib.pyplot as plt
from aiohttp import ClientResponse, ClientSession

URL = "http://127.0.0.1:8080/api/product"


async def requester(client: ClientSession, params: dict) -> ClientResponse:
    async with client.get(URL, params=params) as resp:
        return resp


@dataclass
class ReqParams:
    product_id: int
    shop_id: int


def _generate_params() -> dict:
    return asdict(
        ReqParams(
            product_id=random.randint(1, 100),
            shop_id=random.randint(1, 100),
        )
    )


async def multi_requester(client: ClientSession, count: int = 10) -> float:
    params = _generate_params()

    tasks1 = [requester(client, params=params) for _ in range(10)]

    start = time.perf_counter()
    for t in tasks1:
        await t
    end = time.perf_counter()

    return (end - start) / 10


def visualize(results: list[float]):
    plt.clf()

    plt.xlabel("Итерация (номер)")
    plt.ylabel("Время, мс")
    plt.grid(axis="y", color="gray", linewidth=0.5)

    x, y = [], []
    for idx, m in enumerate(results):
        x.append(idx)
        y.append(m)

    plt.plot(x, y)

    plt.savefig("measures.png")
    plt.show()


async def test(count: int):
    async with ClientSession() as client:
        res = []
        for idx in range(count):
            t = await multi_requester(client)
            res.append(t)
            print(f"{idx=} | {round(t, 4)} spr")

        visualize(res)


async def main():
    await test(1000)


if __name__ == "__main__":
    asyncio.run(main())
