import asyncio
import json

import aiohttp
import random
import time
from dataclasses import dataclass

import matplotlib.pyplot as plt
import numpy as np
import requests

URL = "http://127.0.0.1:8080/api/products/{}"
URL_2 = "/api/products/{}"


COUNT = 5000
COUNT_NESTED = 1
PRODUCT_ID_MAX = 1108
SHOP_ID_MAX = 500
TIME_SEC = 10


@dataclass
class ReqParams:
    product_id: int
    shop_id: int


def _generate_params() -> ReqParams:
    return ReqParams(
        product_id=random.randint(1, PRODUCT_ID_MAX),
        shop_id=random.randint(1, SHOP_ID_MAX),
    )



async def make_async_request() -> float:
    params: ReqParams = _generate_params()
    start = time.perf_counter_ns()

    async with aiohttp.request(
            method="GET",
            url=URL.format(params.product_id),
            params={"shop_id": str(params.shop_id)}
    ) as resp:
        end = time.perf_counter_ns()

    return end - start

def make_request() -> float:
    params: ReqParams = _generate_params()

    # requests.get(URL.format(params.product_id), params={"shop_id": params.shop_id})

    start = time.perf_counter_ns()
    requests.get(URL.format(params.product_id), params={"shop_id": params.shop_id})
    end = time.perf_counter_ns()

    return end - start


def visualize(results: list[float], results_2: list[float]):
    plt.clf()

    plt.xlabel("Время под нагрузкой, мин")
    plt.ylabel("Кол-во запросов в минуту, шт")
    plt.grid(axis="y", color="gray", linewidth=0.5)

    x, y, z = [], [], []
    # r = np.array(results[1:])
    # l = [x for x in r if r.mean() - 2*r.std() < x < r.mean() + 2*r.std()]
    # print(np.array(l).mean())
    for xv, yv, zv in zip(range(1, len(results)+1), results, results_2):
        x.append(xv)
        y.append(yv)
        z.append(zv)

    plt.plot(x, y, label="С кэшированием")
    plt.plot(x, z, label="Без кэширования")

    plt.legend()
    plt.savefig("measures.svg", format="svg")
    plt.show()


def test(count: int):
    res: list[float] = []
    for idx in range(count):
        t = make_request() * 1e-6
        res.append(t)
        if idx % 1000 == 0:
            print(f"{idx=} | {round(t, 4)} spr")

    visualize(res)


async def test_async(timeout: int = 10, threads: int = 8):
    res: list[float] = []
    # counter: int = 0

    baked = [[make_async_request() for _ in range(threads)] for _ in range(1000)]

    start_time = time.time()
    i = 0
    while True:
        t = await asyncio.gather(*baked[i])
        i += 1
        res.extend(t)
        curr_time = time.time()
        if curr_time > start_time + timeout:
            print(curr_time - start_time)
            break
    ms = [t * 1e-6 for t in res]


    print(f"{i * 8} requests per {timeout} seconds => {i * 8 / 10} average rps")
    visualize(ms)


if __name__ == "__main__":
    # test(count=COUNT)
    # asyncio.run(test_async())
    #
    # p_generated = [_generate_params() for _ in range(30000)]
    #
    # gen = [
    #     {
    #         "path": URL_2.format(g.product_id) + f"?shop_id={g.shop_id}",
    #         "method": "GET",
    #     }
    #     for g in p_generated
    # ]
    #
    # with open("/home/ivaaahn/dev/retailer/retailer/tests/cache/wrk/data/requests.json", "w") as f:
    #     json.dump(gen, f)

    visualize(
        [
            12775, 13937, 14247, 14321, 15174, 15290, 16198,
        ],
        [
            13362, 13542, 13373, 13135, 12896, 13448, 13167,
        ]
    )