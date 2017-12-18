# pufomap-back
Backend para PufoMap

## System
$ sudo apt-get install binutils libproj-dev gdal-bin geos
> createdb pufomap

## Docker

docker build -t pufomap-db:1.0 -f Dockerfile_db .
docker run -d --name pufomap_db -p 5432:5432 -e POSTGRES_DB=pufomap -v /path/to/pufomap-back/data:/var/lib/postgresql/data pufomap-db:1.0
psql -h localhost -U postgres -d pufomap
