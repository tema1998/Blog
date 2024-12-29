# Blog with chat

## URL
[http://tema1998.ru/](http://tema1998.ru/)

### Built with

* ![Docker][Docker]
* ![Nginx][Nginx]
* ![Django][Django]
* ![PostgreSQL][PostgreSQL]
* ![Redis][Redis]
* ![Daphne][Daphne]
* ![Certbot][Certbot]


Functions |
-- |
`Follow/unfollow people` |
`Share photos with your friends` |
`Edit/delete posts` |
`View friends posts` |
`Like posts` |
`Write comments` |
`Like comments` |
`Turn off/on comments` |
`Add posts to favorites` |
`Chat with friends` |

Functions 'Follow/unfollow', 'Like/dislike', 'Add posts to favorites' implemented using **JS**(*without page refresh*).

## Environment
Use .env.example to create .env with your parameters.

## Run development server

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Run docker
```
docker build -t tb_docker .
docker-compose up --build
```
## Stop:
```
docker stop $(docker ps -q)
```
## Deploying
Set your domain name instead of tema1998.ru in project.
Create a folder for certificates:
```
mkdir data
mkdir data/certbot
mkdir data/certbot/conf
mkdir data/certbot/www
mkdir data/certbot/conf/live/
mkdir data/certbot/conf/live/your-domain.ru/
```
Get certificate SSL through Certbot.(Turn off SSL, daphne and run.) In the second console run:
```
docker-compose run --rm --entrypoint "\
certbot certonly --webroot -w /var/www/certbot \
  --email your-email@mail.ru \
  -d your-site.ru \
  --rsa-key-size 2048 \
  --agree-tos \
  --force-renewal" certbot
```
Turn on SSL and daphne(don't forget to configure it)

[Docker]: https://img.shields.io/badge/docker-000000?style=for-the-badge&logo=docker&logoColor=blue
[Django]: https://img.shields.io/badge/django-000000?style=for-the-badge&logo=django&logoColor=white
[PostgreSQL]: https://img.shields.io/badge/postgresql-000000?style=for-the-badge&logo=postgresql&logoColor=blue
[Celery]: https://img.shields.io/badge/celery-000000?style=for-the-badge&logo=celery&logoColor=green
[Redis]: https://img.shields.io/badge/redis-000000?style=for-the-badge&logo=redis&logoColor=red
[Nginx]: https://img.shields.io/badge/nginx-000000?style=for-the-badge&logo=nginx&logoColor=green
[Daphne]: https://img.shields.io/badge/daphne-000000?style=for-the-badge&logo=daphne&logoColor=green
[Certbot]: https://img.shields.io/badge/certbot-000000?style=for-the-badge&logo=certbot&logoColor=green
