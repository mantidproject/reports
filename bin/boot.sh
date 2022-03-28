#! /bin/bash -e
# Starts the stack

function create_external_net(){
  network_name=nginx_net
  docker network inspect nginx_net >/dev/null 2>&1 || \
    docker network create --driver bridge nginx_net
}

SCRIPTPATH=$(cd "$(dirname "$0")"; pwd -P)
SOURCE_DIR=$(cd "$SCRIPTPATH" && cd .. && pwd -P)
PROJECT_NAME=reports

if [[ ! -f "$SOURCE_DIR/.env" ]]; then
  echo "Please copy and configure the .env file from blank.env"
  exit 1
fi

COMPOSE_ARGS="--file ${SOURCE_DIR}/docker-compose.yml"
if [[ $OSTYPE == "msys"* ]] || [[ $OSTYPE == 'darwin'* ]]; then
  # Use volume mounts to avoid permission issues
  COMPOSE_ARGS="${COMPOSE_ARGS} --file ${SOURCE_DIR}/docker-compose-use-docker-volume.yml"
else
  # Create empty directories, so they are not owned by root
  mkdir -p "${SOURCE_DIR}/pgdata"
fi

# Start external network
create_external_net
# Build services
docker-compose ${COMPOSE_ARGS} --project-name ${PROJECT_NAME} build
# Bring up the stack and detach
docker-compose ${COMPOSE_ARGS} --project-name ${PROJECT_NAME} up -d
