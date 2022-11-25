import argparse
import logging
import logging.config
import sys
import requests
from requests import get
from typing import List
from io import StringIO
import io
import docker
import socket
# --------------------------------------------------------------------- #
# Define ntfy url
request_url = sys.argv[1]
# --------------------------------------------------------------------- #
# get_hostname

def get_hostname():
    """ get_hostname """
    hostname = str(socket.gethostname())
    return hostname
hostname = get_hostname()
    

# --------------------------------------------------------------------- #


def main(argv):
    buffer = StringIO()
    sys.stdout = buffer

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--container-name',
        metavar='container_name',
        required=True,
        help='(Partial) name of the container',
        type=str
    )

    args = parser.parse_args(argv)

    try:
        client: docker.DockerClient = docker.from_env()

        containers: List[docker.models.containers.Container] = client.containers.list(
            all=True,
            filters={'name': args.container_name}
        )

        for container in containers:
            res = client.api.inspect_container(container.id)

            # if the container is running, check the health status (if it exists)
            if container.status == 'running':
                if 'Health' in res['State'] and res['State']['Health']['Status'] == 'unhealthy':
                    last_log = res['State']['Health']['Log'][-1]['Output'].strip()
                    # logger.error('container "%s" is unhealthy, last log entry: "%s"', container.name, last_log)
                    requests.post("request_url", data=(f'container {container.name} on {hostname} is unhealthy, last log entry: {last_log}'))
            elif container.status != 'running':
                requests.post("request_url", data=(f'container {container.name} on {hostname} has status {container.status}'))


        if len(containers) == 0:
            requests.post("request_url", data=(f'no container(s) with name {container.name} found on {hostname}'))
    except docker.errors.NotFound:
        # logger.error('Container "%s" not found', args.container_name)
        requests.post("request_url", data=(f'Container {container.name} on {hostname} not found'))
        
    except docker.errors.DockerException as exc:
        # logger.error('Docker host seems to be down: %s', exc)
        requests.post("request_url", data=(f'Docker host on {hostname} seems to be down: {exc}'))


if __name__ == '__main__':
    logging.config.dictConfig({
        'version': 1,
        'disable_existing_loggers': False,
        'loggers': {
            '': {
                'level': 'INFO',
            },
        }
    })
    sys.exit(main(sys.argv[1:]))
