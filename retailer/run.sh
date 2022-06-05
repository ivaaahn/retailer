#!/bin/sh

alembic upgrade head
uvicorn app.application:app "--proxy-headers" --host '0.0.0.0' --port '8080' --loop uvloop --reload
