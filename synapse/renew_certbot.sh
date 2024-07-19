cd $HOME/server/synapse
docker compose stop nginx
docker compose -f docker-compose-certbot.yml down --remove-orphans
docker compose -f docker-compose-certbot.yml up webserver -d
docker compose -f docker-compose-certbot.yml run --rm  certbot certonly --webroot --webroot-path /var/www/certbot/ -d mx.kernelpanicdisco.dev
docker compose -f docker-compose-certbot.yml down --remove-orphans
docker compose up -d
