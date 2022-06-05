import csv
from dataclasses import asdict


def write(data: list, filename: str):
    if not data:
        return

    with open(filename, "w") as fd:
        fieldnames = [str(key) for key in asdict(data[0])]
        writer = csv.DictWriter(fd, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows([asdict(item) for item in data])


def read(filename: str) -> list[dict]:
    with open(filename, "r", newline="") as fd:
        reader = csv.DictReader(fd)
        reader.__iter__()

        result = [item for item in reader]
    return result
