### Run server
```sh
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

http://127.0.0.1:8000/redoc
http://127.0.0.1:8000/docs


### Download all tiles
```sh
python osm_tiles_downloader.py 61.3148 63.3324
```

### Локальная карта
http://127.0.0.1:8000/map