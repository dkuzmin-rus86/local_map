import os
import requests
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

BASE_DIR = os.path.realpath(os.path.dirname(__file__))
DEFAULT_IMAGE = 'static/0.png'

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/")
async def home():
    return {"message": "Первое приложение на FastAPI"}


@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    """ Get items data """
    context = {"request": request, "id": id}
    return templates.TemplateResponse("item.html", context)


@app.get("/map/", response_class=HTMLResponse)
async def map_page(request: Request):
    """ Map page"""
    context = {"request": request, "id": id}
    return templates.TemplateResponse("map.html", context)


def download_tiles(zoom, xtile, ytile):
    url = f"https://c.tile.openstreetmap.org/{zoom}/{xtile}/{ytile}.png"
    dir_path = f"{BASE_DIR}/tiles/{zoom}/{xtile}/"
    download_path = f"{BASE_DIR}/tiles/{zoom}/{xtile}/{ytile}.png"
    
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    
    if(not os.path.isfile(download_path)):
        print(f"downloading {url}")
        header = {'User-Agent': 'PostmanRuntime/7.28.4'}
        try:
            r = requests.get(url, headers=header)
            with open(download_path, 'wb') as f:
                f.write(r.content)
            return True
        except Exception as e:
            print(f'Error: {e}')
            return False


@app.get("/tiles/{zoom}/{x}/{y}.png", response_class=FileResponse)
async def tiles(request: Request, zoom, y, x):
    """ Get tiles """

    filename = f'{BASE_DIR}/tiles/{zoom}/{x}/{y}.png'
    if os.path.isfile(filename):
        return filename
    else:
        downloaded = download_tiles(zoom, x, y)
        if downloaded:
            return filename
        else:
            return FileResponse(DEFAULT_IMAGE)
