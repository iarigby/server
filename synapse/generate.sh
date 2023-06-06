SYNAPSE_SERVER_NAME=$1

if [[ -z "$SYNAPSE_SERVER_NAME" ]]
then
	echo "synapse server name is required as argument"
	exit 1
fi

docker compose run -e SYNAPSE_SERVER_NAME=$SYNAPSE_SERVER_NAME -e SYNAPSE_REPORT_STATS=yes synapse generate

