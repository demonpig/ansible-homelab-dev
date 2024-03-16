#!/usr/bin/env python

import os
import argparse
import subprocess

RUNTIME_NAME = os.path.basename(os.path.dirname(os.path.realpath(__file__))).replace('-', '_')
IMAGE_NAME = 'localhost/docker-almalinux9-ansible:latest'

def parse_args(name: str, *args, **kwargs):
    parser = argparse.ArgumentParser(prog=name, **kwargs)
    parser.add_argument('-s', '--stop', action='store_true', default=False)
    parser.add_argument('-d', '--delete', action="store_true", default=False)
    parser.add_argument('--docker', action='store_true', default=False)
    parser.add_argument('--podman', action='store_true', default=False)
    parser.add_argument('--lima', action='store_true', default=True)
    return parser.parse_args()

def run_cmd(cmd: list):
    return subprocess.run(cmd, stdout=subprocess.PIPE)

# not good code design but its just something that is fast and simple
# these functions are going to handle both delete and create

def handle_docker(stop: bool = False, delete: bool = False):
    if stop or delete:
        # make sure this list stays in the same order: stop, delete
        delete_cmds = [
            ['docker', 'container', 'stop', RUNTIME_NAME]
        ]
        
        if stop and not delete:
            run_cmd(delete_cmds[0])
        else:
            for cmd in delete_cmds:
                run_cmd(cmd)
        return

    # Creating the docker container
    create_cmds = [
        [
            'docker', 'run', '-d', '-it', '--rm', '--privileged',
            '-v', '/sys/fs/cgroup:/sys/fs/cgroup:rw',
            '-v', './:/project:rw',
            '-w', '/project',
            '--name', RUNTIME_NAME,
            IMAGE_NAME
        ]
    ]

    for cmd in create_cmds:
        run_cmd(cmd)

def handle_podman(stop: bool = False, delete: bool = False):
    pass

def handle_lima(stop: bool = False, delete: bool = False):
    if stop or delete:
        # make sure this list stays in the same order: stop, delete
        delete_cmds = [
            ['limactl', 'stop', RUNTIME_NAME],
            ['limactl', 'delete', RUNTIME_NAME]
        ]
        
        if stop and not delete:
            run_cmd(delete_cmds[0])
        else:
            for cmd in delete_cmds:
                run_cmd(cmd)
        return

    # Creating the lima vm
    create_cmds = [
        [
            'limactl', 'create', '--tty=false',
            '--name', RUNTIME_NAME,
            os.path.dirname(__file__) + '/lima-config.yml'
        ],
        [
            'limactl', 'start', RUNTIME_NAME
        ]
    ]

    for cmd in create_cmds:
        run_cmd(cmd)

if __name__ == "__main__":
    args = parse_args(name=os.path.basename(__file__))

    if args.lima and not args.docker and not args.podman:
        handle_lima(stop=args.stop, delete=args.delete)
    if args.docker and not args.podman:
        handle_docker(stop=args.stop, delete=args.delete)
    if args.podman:
        handle_podman(stop=args.stop, delete=args.delete)