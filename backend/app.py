''' Main App '''

import os
import multiprocessing
from starlette.datastructures import URL
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
from starlette.responses import RedirectResponse

from src.models.base_model import declare_base, database, engine

from src.routers.category import main as category_router
from src.routers.product import main as product_router
from src.routers.unit import main as unit_router
from src.routers.firststock import main as first_stock_router
from src.routers.supplier import main as supplier_router
from src.routers.stock import main as stock_router
from src.routers.stockdetail import main as stockdetail_router
from src.routers.user import main as user_router
from src.routers.customer import ROUTER as customer_router
from src.routers.salesman import ROUTER as sales_router
from src.routers.customerorder import ROUTER as order_router
from src.routers.orderdetail import ROUTER as orderdetail_router
from src.routers.fackturer import ROUTER as fackturer_router
from src.routers.fackturerdetail import ROUTER as fackturerdetail_router

app = FastAPI(title=os.environ.get('APP_TITLE'))
app.mount("/yoga", StaticFiles(directory="yoga"), name="yoga")

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.on_event('startup')
async def startup():
    ''' Start endpoint '''
    async with engine.begin() as conn:
        await conn.run_sync(declare_base.metadata.create_all)

    await database.connect()


@app.on_event('shutdown')
async def shutdown():
    ''' Shutdown endpoint '''
    await database.disconnect()


@app.get('/')
async def root():
    ''' Goto root '''
    # return {'message': os.environ.get('DEF_MESSAGE')}
    return FileResponse('yoga/index.html')
    # return RedirectResponse(URL('yoga/'))

app.include_router(category_router.ROUTER)
app.include_router(product_router.ROUTER)
app.include_router(unit_router.ROUTER)
app.include_router(first_stock_router.ROUTER)
app.include_router(supplier_router.ROUTER)
app.include_router(stock_router.ROUTER)
app.include_router(stockdetail_router.ROUTER)
app.include_router(user_router.ROUTER)
app.include_router(customer_router)
app.include_router(sales_router)
app.include_router(order_router)
app.include_router(orderdetail_router)
app.include_router(fackturer_router)
app.include_router(fackturerdetail_router)

if __name__ == '__main__':
    multiprocessing.freeze_support()
    uvicorn.run('app:app',
                host=os.environ.get('SERVER_HOST'),
                port=int(str(os.environ.get('SERVER_PORT'))),
                reload=True,
                workers=1,
                debug=True)
