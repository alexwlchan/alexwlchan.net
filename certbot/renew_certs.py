#!/usr/bin/env python3
# -*- encoding: utf-8

import glob
import os
import subprocess

import yaml


def _get_new_certs(domain):
    subprocess.check_call([
        'certbot', 'certonly', '--webroot', '--webroot-path',
        '/site/%s' % domain, '-d', '%s,www.%s' % (domain, domain)
    ])


def _update_docker_compose(domain):
    # The layout of this folder is something like
    #
    #     alexwlchan.net
    #     alexwlchan.net-0001
    #     alexwlchan.net-0002
    #     alexwlchan.net-0003
    #     bijouopera.co.uk
    #     ...
    #
    # So for a given domain, we want to find the latest matching name.
    #
    matching = glob.glob('/etc/letsencrypt/live/%s*' % domain)
    assert len(matching) > 0
    latest_certs_dir = os.path.basename(sorted(matching)[-1])

    docker_compose = yaml.safe_load(open('/infra/docker-compose.yml'))
    volumes = docker_compose['services']['proxy']['volumes']

    # First remove the existing certbot volume
    docker_compose['services']['proxy']['volumes'] = [
        v for v in volumes if not v.endswith(':/certbot/%s' % domain)
    ]
    docker_compose['services']['proxy']['volumes'].append(
        '~/.certbot/config/archive/%s:/certbot/%s' % (latest_certs_dir, domain)
    )

    out_yaml = yaml.dump(docker_compose, default_flow_style=False)
    open('/infra/docker-compose.yml', 'w').write(out_yaml)


def renew_certs(domain):
    print('*** Renewing certs for %s' % domain)
    _get_new_certs(domain)
    _update_docker_compose(domain)

    print('*** Restarting the proxy container with new certificates')
    subprocess.check_call(['docker-compose', 'restart', 'proxy'], cwd='/infra')


if __name__ == '__main__':
    renew_certs('alexwlchan.net')
    renew_certs('bijouopera.co.uk')
