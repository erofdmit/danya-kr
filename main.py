from fastapi import APIRouter, FastAPI
from fastapi.staticfiles import StaticFiles
from consts import DATABASE_URL
from routers.data_router import data_router
from routers.input_router import input_router
from routers.metrics_router import metrics_router
from settings import settings
import os

path_static = './'
path_static = os.path.join(path_static, 'static')


def create_app():
    app = FastAPI(
        title='Smirnov DB',
        version='0.0.0',
        openapi_version='3.1.0',
        docs_url='/docs',
        openapi_url='/docs/openapi.json'
    )
    app.mount("/static", StaticFiles(directory=path_static), name="static")
    main_routers: tuple[APIRouter, ...] = (
        data_router,
        input_router,
        metrics_router
    )

    for router in main_routers:
        app.include_router(
            router=router,
            prefix=settings.ROOT_PATH
        )

    return app

