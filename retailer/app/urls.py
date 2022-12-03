from fastapi import FastAPI

from retailer.app.delivery.urls import setup_routes as setup_api_routes

__all__ = ("setup_routes",)


def setup_routes(app: FastAPI):
    setup_api_routes(app)
