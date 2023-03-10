from sys import argv
import os
import math
import requests
import random
import os.path


def deg2num(lat_deg, lon_deg, zoom):
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
    return (xtile, ytile)


def download_url(zoom, xtile, ytile):  
    url = "http://c.tile.openstreetmap.org/%d/%d/%d.png" % (zoom, xtile, ytile)
    dir_path = "tiles/%d/%d/" % (zoom, xtile)
    download_path = "tiles/%d/%d/%d.png" % (zoom, xtile, ytile)
    
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    
    if(not os.path.isfile(download_path)):
        print("downloading %r" % url)
        header = {'User-Agent': 'PostmanRuntime/7.28.4'}
        r = requests.get(url, headers=header)
        with open(download_path, 'wb') as f:
            f.write(r.content)
    else:
        print(f"skipped {url}")


def usage():
    print("Usage: ")
    print("osm_tiles_downloader <lat> <lon>")


def main(argv):
    try:
        script, lat, lon = argv
    except:
        usage()
        exit(2)

    maxzoom = 15 # redefine me if need so

    # from 0 to 6 download all
    for zoom in range(0,7,1):
        for x in range(0,2**zoom,1):
            for y in range(0,2**zoom,1):
                download_url(zoom, x, y)

    # from 6 to 15 ranges
    for zoom in range(7, int(maxzoom)+1, 1):
        xtile, ytile = deg2num(float(lat)-0.1, float(lon)-0.05, zoom)
        final_xtile, final_ytile = deg2num(float(lat)+0.1, float(lon)+0.05, zoom)

        print(f"{zoom}:{xtile}-{final_xtile}/{ytile}-{final_ytile}")
        for x in range(xtile, final_xtile + 1, 1):
            for y in range(ytile, final_ytile - 1, -1):                
                result = download_url(zoom, x, y)


if __name__ == '__main__':
    main(argv)
