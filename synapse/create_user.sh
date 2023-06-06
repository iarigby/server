SYNAPSE_USER=$1
ADMIN_OPTION=$2
SHARED_SECRET=$(grep -oP 'registration_shared_secret: "\K.+(?=")' synapse-data/homeserver.yaml)

if [[ -z "$SYNAPSE_USER" ]]
then
	echo "synapse_user must be provided as an argument"
	exit 1
fi

if [[ -z "$ADMIN_OPTION" ]]
then
	echo "admin must be provided as an argument"
	exit 1
fi

if [[ -z "$SHARED_SECRET" ]]
then
	echo "shared secret could not be found in synapse-data/homeserver.yaml"
	exit 1
fi

docker compose exec synapse register_new_matrix_user http://localhost:8008 \
	--user $SYNAPSE_USER --password default --$ADMIN_OPTION --shared-secret "$SHARED_SECRET"
