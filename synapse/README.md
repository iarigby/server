# Synapse Matrix Server

## Setup
### nginx
```sh
docker compose -f docker-compose-certbot.yml up webserver -d
docker compose -f docker-compose-certbot.yml run --rm  certbot certonly --webroot --webroot-path /var/www/certbot/ -d mx.kernelpanicdisco.dev
docker compose -f docker-compose-certbot.yml down webserver
```
### synapse
- **don't forget to open ports**

```sh
sh genereate.sh DOMAIN_NAME
```

## Launch
sunapse will launch on port 8008
```sh
docker compose up
```

## Create Users
password will be 'default'
```
sh create_user.sh USERNAME (admin|no-admin)
```
