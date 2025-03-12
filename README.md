# Demo View
http://66.42.56.128:8004/docs

## deployment
- install requirements
```
python -m venv env
source env/bin/activate
cd project
python -m pip install -r requirements.txt
```
- init db
```
# mirrors--tencent
vi /etc/docker/daemon.json
{
"registry-mirrors": [
"https://docker.m.daocloud.io",
"https://dockerproxy.com",
"https://docker.mirrors.ustc.edu.cn",
"https://docker.nju.edu.cn"
]
}
# 
docker-compose up -d --build
docker-compose exec web aerich init -t app.db.TORTOISE_ORM
docker-compose exec web aerich init-db
```
