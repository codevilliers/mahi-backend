CWD=$(pwd)

docker run \
    --tty \
    --interactive \
    --rm \
    --userns host \
    --user $(id -u $(whoami)) \
    --network=mahi_network \
    --publish 8000:8000/tcp \
    --mount type=bind,src=${CWD}/mahi_care,dst=/mahi_care \
    --mount type=bind,src=${CWD}/configurations,dst=/configurations \
    --mount type=bind,src=${CWD}/media_files,dst=/media_files \
    --name=mahi_care_dev \
    --network-alias	django_mahi_care \
    mahi-django:latest \
    python /mahi_care/manage.py runserver 0.0.0.0:8000
