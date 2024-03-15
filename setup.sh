#!/bin/sh

# stand up a simple container with this project mounted into it
IMAGE="${IMAGE:-localhost/docker-almalinux9-ansible:latest}"

_CONTAINER_CMD=""
command -v docker > /dev/null && _CONTAINER_CMD="docker"
command -v podman > /dev/null && _CONTAINER_CMD="podman"

_CONTAINER_NAME="$(basename $(dirname $(realpath $0)))"
_CONTAINER_CMD_OPTIONS="-it --rm -d --privileged --name $_CONTAINER_NAME"


_DOWN_CMDS=( "s" "stop" "down" "destroy" )
for i in "${_DOWN_CMDS[@]}"; do
    if [[ "$i" == "$1" ]]; then
        $_CONTAINER_CMD container stop $_CONTAINER_NAME
        exit 0
    fi
done

# check for 'container' environment variable
# this should indicate to us if we are inside of the container
_INSIDE_CONTAINER="$(env | grep -o 'container=')"
if [[ ! -z $_INSIDE_CONTAINER ]]; then
    # we shouldn't do anything if we are inside the container
    exit 0
fi 

$_CONTAINER_CMD run $_CONTAINER_CMD_OPTIONS \
    -v /sys/fs/cgroup:/sys/fs/cgroup:rw \
    -v ./:/project:rw \
    -w /project \
    $IMAGE

$_CONTAINER_CMD exec -it $_CONTAINER_NAME bash