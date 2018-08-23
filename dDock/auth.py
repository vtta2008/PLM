# -*- coding: utf-8 -*-
"""

Script Name: auth.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import

import json
import logging
import os
import random

from dDock import constants
from dDock import errors, utils

log = logging.getLogger(__name__)


class BuildApiMixin(object):
    def build(self, path=None, tag=None, quiet=False, fileobj=None,
              nocache=False, rm=False, timeout=None,
              custom_context=False, encoding=None, pull=False,
              forcerm=False, dockerfile=None, container_limits=None,
              decode=False, buildargs=None, gzip=False, shmsize=None,
              labels=None, cache_from=None, target=None, network_mode=None,
              squash=None, extra_hosts=None, platform=None, isolation=None):

        remote = context = None
        headers = {}
        container_limits = container_limits or {}
        if path is None and fileobj is None:
            raise TypeError("Either path or fileobj needs to be provided.")
        if gzip and encoding is not None:
            raise errors.DockerException(
                'Can not use custom encoding if gzip is enabled'
            )

        for key in container_limits.keys():
            if key not in constants.CONTAINER_LIMITS_KEYS:
                raise errors.DockerException(
                    'Invalid container_limits key {0}'.format(key)
                )

        if custom_context:
            if not fileobj:
                raise TypeError("You must specify fileobj with custom_context")
            context = fileobj
        elif fileobj is not None:
            context = utils.mkbuildcontext(fileobj)
        elif path.startswith(('http://', 'https://',
                              'git://', 'github.com/', 'git@')):
            remote = path
        elif not os.path.isdir(path):
            raise TypeError("You must specify a directory to build in path")
        else:
            dockerignore = os.path.join(path, '.dockerignore')
            exclude = None
            if os.path.exists(dockerignore):
                with open(dockerignore, 'r') as f:
                    exclude = list(filter(
                        lambda x: x != '' and x[0] != '#',
                        [l.strip() for l in f.read().splitlines()]
                    ))
            dockerfile = process_dockerfile(dockerfile, path)
            context = utils.tar(
                path, exclude=exclude, dockerfile=dockerfile, gzip=gzip
            )
            encoding = 'gzip' if gzip else encoding

        u = self._url('/build')
        params = {
            't': tag,
            'remote': remote,
            'q': quiet,
            'nocache': nocache,
            'rm': rm,
            'forcerm': forcerm,
            'pull': pull,
            'dockerfile': dockerfile,
        }
        params.update(container_limits)

        if buildargs:
            params.update({'buildargs': json.dumps(buildargs)})

        if shmsize:
            if utils.version_gte(self._version, '1.22'):
                params.update({'shmsize': shmsize})
            else:
                raise errors.InvalidVersion(
                    'shmsize was only introduced in API version 1.22'
                )

        if labels:
            if utils.version_gte(self._version, '1.23'):
                params.update({'labels': json.dumps(labels)})
            else:
                raise errors.InvalidVersion(
                    'labels was only introduced in API version 1.23'
                )

        if cache_from:
            if utils.version_gte(self._version, '1.25'):
                params.update({'cachefrom': json.dumps(cache_from)})
            else:
                raise errors.InvalidVersion(
                    'cache_from was only introduced in API version 1.25'
                )

        if target:
            if utils.version_gte(self._version, '1.29'):
                params.update({'target': target})
            else:
                raise errors.InvalidVersion(
                    'target was only introduced in API version 1.29'
                )

        if network_mode:
            if utils.version_gte(self._version, '1.25'):
                params.update({'networkmode': network_mode})
            else:
                raise errors.InvalidVersion(
                    'network_mode was only introduced in API version 1.25'
                )

        if squash:
            if utils.version_gte(self._version, '1.25'):
                params.update({'squash': squash})
            else:
                raise errors.InvalidVersion(
                    'squash was only introduced in API version 1.25'
                )

        if extra_hosts is not None:
            if utils.version_lt(self._version, '1.27'):
                raise errors.InvalidVersion(
                    'extra_hosts was only introduced in API version 1.27'
                )

            if isinstance(extra_hosts, dict):
                extra_hosts = utils.format_extra_hosts(extra_hosts)
            params.update({'extrahosts': extra_hosts})

        if platform is not None:
            if utils.version_lt(self._version, '1.32'):
                raise errors.InvalidVersion(
                    'platform was only introduced in API version 1.32'
                )
            params['platform'] = platform

        if isolation is not None:
            if utils.version_lt(self._version, '1.24'):
                raise errors.InvalidVersion(
                    'isolation was only introduced in API version 1.24'
                )
            params['isolation'] = isolation

        if context is not None:
            headers = {'Content-Type': 'application/tar'}
            if encoding:
                headers['Content-Encoding'] = encoding

        self._set_auth_headers(headers)

        response = self._post(
            u,
            data=context,
            params=params,
            headers=headers,
            stream=True,
            timeout=timeout,
        )

        if context is not None and not custom_context:
            context.close()

        return self._stream_helper(response, decode=decode)

    @utils.minimum_version('1.31')
    def prune_builds(self):
        url = self._url("/build/prune")
        return self._result(self._post(url), True)

    def _set_auth_headers(self, headers):
        if not self._auth_configs:
            log.debug("No auth config in memory - loading from filesystem")
            self._auth_configs = auth.load_config()
        if self._auth_configs:
            auth_cfgs = self._auth_configs
            auth_data = {}
            if auth_cfgs.get('credsStore'):
                for registry in auth_cfgs.get('auths', {}).keys():
                    auth_data[registry] = auth.resolve_authconfig(
                        auth_cfgs, registry,
                        credstore_env=self.credstore_env,
                    )
            else:
                for registry in auth_cfgs.get('credHelpers', {}).keys():
                    auth_data[registry] = auth.resolve_authconfig(
                        auth_cfgs, registry,
                        credstore_env=self.credstore_env
                    )
                for registry, creds in auth_cfgs.get('auths', {}).items():
                    if registry not in auth_data:
                        auth_data[registry] = creds

                if auth.INDEX_NAME in auth_data:
                    auth_data[auth.INDEX_URL] = auth_data[auth.INDEX_NAME]

            log.debug(
                'Sending auth config ({0})'.format(
                    ', '.join(repr(k) for k in auth_data.keys())
                )
            )

            headers['X-Registry-Config'] = auth.encode_header(
                auth_data
            )
        else:
            log.debug('No auth config found')


def process_dockerfile(dockerfile, path):
    if not dockerfile:
        return (None, None)

    abs_dockerfile = dockerfile
    if not os.path.isabs(dockerfile):
        abs_dockerfile = os.path.join(path, dockerfile)

    if (os.path.splitdrive(path)[0] != os.path.splitdrive(abs_dockerfile)[0] or
            os.path.relpath(abs_dockerfile, path).startswith('..')):

        with open(abs_dockerfile, 'r') as df:
            return (
                '.dockerfile.{0:x}'.format(random.getrandbits(160)),
                df.read()
            )

    if dockerfile == abs_dockerfile:

        dockerfile = os.path.relpath(abs_dockerfile, path)
    return (dockerfile, None)

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 23/08/2018 - 11:08 AM
# © 2017 - 2018 DAMGteam. All rights reserved