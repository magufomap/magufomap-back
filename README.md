# magufomap-back
Backend para MagufoMap

## System

```bash
$ sudo apt-get install binutils libproj-dev gdal-bin geos
> createdb magufomap
```

## Docker

```bash
$ docker build -t magufomap-db:1.0 -f Dockerfile_db .
$ docker run -d --name magufomap_db -p 5432:5432 -e POSTGRES_DB=magufomap -v /path/to/magufomap-back/data:/var/lib/postgresql/data magufomap-db:1.0
$ psql -h localhost -U postgres -d magufomap
```

## Filters

* severity_in=1,2,3,4
* tags__name__in=tag1,tag2,etc
* status__in=PUB,PEN
* in_bbox=-3.8638,40.2554,-3.5122,40.5816 # (min Lon, min Lat, max Lon, max Lat)
