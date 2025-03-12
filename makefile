black:
	docker-compose exec web black .
isort:
	docker-compose exec web isort .
pytest:
	docker-compose exec web pytest .
docker_p:
	docker-compose exec web-db psql -U postgres
routine: 
	docker-compose exec web flake8 .
	docker-compose exec web black .
	docker-compose exec web isort .
	docker-compose exec web pytest .
rebuild:
	docker-compose up -d --build

# 更新数据库
# 更新本地
init_db_meta:
	docker-compose exec web aerich init -t app.db.TORTOISE_ORM
init_db:
	docker-compose exec web aerich init-db
# heroku
heroku_init_db_meta:
	heroku run aerich init --app young-chamber-41337 -t app.db.TORTOISE_ORM
heroku_init_db:
	heroku run aerich upgrade --app young-chamber-41337

heroku_p:
	heroku pg:psql  -a young-chamber-41337
heroku_reset:
	heroku pg:reset -a young-chamber-41337