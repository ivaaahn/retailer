alembic upgrade head
uvicorn retailer.app.application:app --host '0.0.0.0' --port '8080' --reload