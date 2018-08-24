import base64
import os
import os.path
import json
import shlex
from distutils.version import StrictVersion
from datetime import datetime

import six

from dock import errors, tls

if six.PY2:
    from urllib import splitnport
else:
    from urllib.parse import splitnport

DEFAULT_HTTP_HOST = "127.0.0.1"
DEFAULT_UNIX_SOCKET = "http+unix://var/run/docker.sock"
DEFAULT_NPIPE = 'npipe:////./pipe/docker_engine'

BYTE_UNITS = {
    'b': 1,
    'k': 1024,
    'm': 1024 * 1024,
    'g': 1024 * 1024 * 1024
}


def create_ipam_pool(*args, **kwargs):
    raise errors.DeprecatedMethod(
        'utils.create_ipam_pool has been removed. Please use a '
        'docker.types.IPAMPool object instead.'
    )


def create_ipam_config(*args, **kwargs):
    raise errors.DeprecatedMethod(
        'utils.create_ipam_config has been removed. Please use a '
        'docker.types.IPAMConfig object instead.'
    )


def decode_json_header(header):
    data = base64.b64decode(header)
    if six.PY3:
        data = data.decode('utf-8')
    return json.loads(data)


def compare_version(v1, v2):
    """Compare docker versions

    >>> v1 = '1.9'
    >>> v2 = '1.10'
    >>> compare_version(v1, v2)
    1
    >>> compare_version(v2, v1)
    -1
    >>> compare_version(v2, v2)
    0
    """
    s1 = StrictVersion(v1)
    s2 = StrictVersion(v2)
    if s1 == s2:
        return 0
    elif s1 > s2:
        return -1
    else:
        return 1


def version_lt(v1, v2):
    return compare_version(v1, v2) > 0


def version_gte(v1, v2):
    return not version_lt(v1, v2)


def _convert_port_binding(binding):
    result = {'HostIp': '', 'HostPort': ''}
    if isinstance(binding, tuple):
        if len(binding) == 2:
            result['HostPort'] = binding[1]
            result['HostIp'] = binding[0]
        elif isinstance(binding[0], six.string_types):
            result['HostIp'] = binding[0]
        else:
            result['HostPort'] = binding[0]
    elif isinstance(binding, dict):
        if 'HostPort' in binding:
            result['HostPort'] = binding['HostPort']
            if 'HostIp' in binding:
                result['HostIp'] = binding['HostIp']
        else:
            raise ValueError(binding)
    else:
        result['HostPort'] = binding

    if result['HostPort'] is None:
        result['HostPort'] = ''
    else:
        result['HostPort'] = str(result['HostPort'])

    return result


def convert_port_bindings(port_bindings):
    result = {}
    for k, v in six.iteritems(port_bindings):
        key = str(k)
        if '/' not in key:
            key += '/tcp'
        if isinstance(v, list):
            result[key] = [_convert_port_binding(binding) for binding in v]
        else:
            result[key] = [_convert_port_binding(v)]
    return result


def convert_volume_binds(binds):
    if isinstance(binds, list):
        return binds

    result = []
    for k, v in binds.items():
        if isinstance(k, six.binary_type):
            k = k.decode('utf-8')

        if isinstance(v, dict):
            if 'ro' in v and 'mode' in v:
                raise ValueError(
                    'Binding cannot contain both "ro" and "mode": {}'
                    .format(repr(v))
                )

            bind = v['bind']
            if isinstance(bind, six.binary_type):
                bind = bind.decode('utf-8')

            if 'ro' in v:
                mode = 'ro' if v['ro'] else 'rw'
            elif 'mode' in v:
                mode = v['mode']
            else:
                mode = 'rw'

            result.append(
                six.text_type('{0}:{1}:{2}').format(k, bind, mode)
            )
        else:
            if isinstance(v, six.binary_type):
                v = v.decode('utf-8')
            result.append(
                six.text_type('{0}:{1}:rw').format(k, v)
            )
    return result


def convert_tmpfs_mounts(tmpfs):
    if isinstance(tmpfs, dict):
        return tmpfs

    if not isinstance(tmpfs, list):
        raise ValueError(
            'Expected tmpfs value to be either a list or a dict, found: {}'
            .format(type(tmpfs).__name__)
        )

    result = {}
    for mount in tmpfs:
        if isinstance(mount, six.string_types):
            if ":" in mount:
                name, options = mount.split(":", 1)
            else:
                name = mount
                options = ""

        else:
            raise ValueError(
                "Expected item in tmpfs list to be a string, found: {}"
                .format(type(mount).__name__)
            )

        result[name] = options
    return result


def convert_service_networks(networks):
    if not networks:
        return networks
    if not isinstance(networks, list):
        raise TypeError('networks parameter must be a list.')

    result = []
    for n in networks:
        if isinstance(n, six.string_types):
            n = {'Target': n}
        result.append(n)
    return result


def parse_repository_tag(repo_name):
    parts = repo_name.rsplit('@', 1)
    if len(parts) == 2:
        return tuple(parts)
    parts = repo_name.rsplit(':', 1)
    if len(parts) == 2 and '/' not in parts[1]:
        return tuple(parts)
    return repo_name, None


# Based on utils.go:ParseHost http://tinyurl.com/nkahcfh
# fd:// protocol unsupported (for obvious reasons)
# Added support for http and https
# Protocol translation: tcp -> http, unix -> http+unix
def parse_host(addr, is_win32=False, tls=False):
    proto = "http+unix"
    port = None
    path = ''

    if not addr and is_win32:
        addr = DEFAULT_NPIPE

    if not addr or addr.strip() == 'unix://':
        return DEFAULT_UNIX_SOCKET

    addr = addr.strip()
    if addr.startswith('http://'):
        addr = addr.replace('http://', 'tcp://')
    if addr.startswith('http+unix://'):
        addr = addr.replace('http+unix://', 'unix://')

    if addr == 'tcp://':
        raise errors.DockerException(
            "Invalid bind address format: {0}".format(addr)
        )
    elif addr.startswith('unix://'):
        addr = addr[7:]
    elif addr.startswith('tcp://'):
        proto = 'http{0}'.format('s' if tls else '')
        addr = addr[6:]
    elif addr.startswith('https://'):
        proto = "https"
        addr = addr[8:]
    elif addr.startswith('npipe://'):
        proto = 'npipe'
        addr = addr[8:]
    elif addr.startswith('fd://'):
        raise errors.DockerException("fd protocol is not implemented")
    else:
        if "://" in addr:
            raise errors.DockerException(
                "Invalid bind address protocol: {0}".format(addr)
            )
        proto = "https" if tls else "http"

    if proto in ("http", "https"):
        address_parts = addr.split('/', 1)
        host = address_parts[0]
        if len(address_parts) == 2:
            path = '/' + address_parts[1]
        host, port = splitnport(host)

        if port is None:
            raise errors.DockerException(
                "Invalid port: {0}".format(addr)
            )

        if not host:
            host = DEFAULT_HTTP_HOST
    else:
        host = addr

    if proto in ("http", "https") and port == -1:
        raise errors.DockerException(
            "Bind address needs a port: {0}".format(addr))

    if proto == "http+unix" or proto == 'npipe':
        return "{0}://{1}".format(proto, host).rstrip('/')
    return "{0}://{1}:{2}{3}".format(proto, host, port, path).rstrip('/')


def parse_devices(devices):
    device_list = []
    for device in devices:
        if isinstance(device, dict):
            device_list.append(device)
            continue
        if not isinstance(device, six.string_types):
            raise errors.DockerException(
                'Invalid device type {0}'.format(type(device))
            )
        device_mapping = device.split(':')
        if device_mapping:
            path_on_host = device_mapping[0]
            if len(device_mapping) > 1:
                path_in_container = device_mapping[1]
            else:
                path_in_container = path_on_host
            if len(device_mapping) > 2:
                permissions = device_mapping[2]
            else:
                permissions = 'rwm'
            device_list.append({
                'PathOnHost': path_on_host,
                'PathInContainer': path_in_container,
                'CgroupPermissions': permissions
            })
    return device_list


def kwargs_from_env(ssl_version=None, assert_hostname=None, environment=None):
    if not environment:
        environment = os.environ
    host = environment.get('DOCKER_HOST')

    # empty string for cert path is the same as unset.
    cert_path = environment.get('DOCKER_CERT_PATH') or None

    # empty string for tls verify counts as "false".
    # Any value or 'unset' counts as true.
    tls_verify = environment.get('DOCKER_TLS_VERIFY')
    if tls_verify == '':
        tls_verify = False
    else:
        tls_verify = tls_verify is not None
    enable_tls = cert_path or tls_verify

    params = {}

    if host:
        params['base_url'] = (
            host.replace('tcp://', 'https://') if enable_tls else host
        )

    if not enable_tls:
        return params

    if not cert_path:
        cert_path = os.path.join(os.path.expanduser('~'), '.docker')

    if not tls_verify and assert_hostname is None:
        # assert_hostname is a subset of TLS verification,
        # so if it's not set already then set it to false.
        assert_hostname = False

    params['tls'] = tls.TLSConfig(
        client_cert=(os.path.join(cert_path, 'cert.pem'),
                     os.path.join(cert_path, 'key.pem')),
        ca_cert=os.path.join(cert_path, 'ca.pem'),
        verify=tls_verify,
        ssl_version=ssl_version,
        assert_hostname=assert_hostname,
    )

    return params


def convert_filters(filters):
    result = {}
    for k, v in six.iteritems(filters):
        if isinstance(v, bool):
            v = 'true' if v else 'false'
        if not isinstance(v, list):
            v = [v, ]
        result[k] = v
    return json.dumps(result)


def datetime_to_timestamp(dt):
    """Convert a UTC datetime to a Unix timestamp"""
    delta = dt - datetime.utcfromtimestamp(0)
    return delta.seconds + delta.days * 24 * 3600


def parse_bytes(s):
    if isinstance(s, six.integer_types + (float,)):
        return s
    if len(s) == 0:
        return 0

    if s[-2:-1].isalpha() and s[-1].isalpha():
        if s[-1] == "b" or s[-1] == "B":
            s = s[:-1]
    units = BYTE_UNITS
    suffix = s[-1].lower()

    # Check if the variable is a string representation of an int
    # without a units part. Assuming that the units are bytes.
    if suffix.isdigit():
        digits_part = s
        suffix = 'b'
    else:
        digits_part = s[:-1]

    if suffix in units.keys() or suffix.isdigit():
        try:
            digits = int(digits_part)
        except ValueError:
            raise errors.DockerException(
                'Failed converting the string value for memory ({0}) to'
                ' an integer.'.format(digits_part)
            )

        # Reconvert to long for the final result
        s = int(digits * units[suffix])
    else:
        raise errors.DockerException(
            'The specified value for memory ({0}) should specify the'
            ' units. The postfix should be one of the `b` `k` `m` `g`'
            ' characters'.format(s)
        )

    return s


def normalize_links(links):
    if isinstance(links, dict):
        links = six.iteritems(links)

    return ['{0}:{1}'.format(k, v) for k, v in sorted(links)]


def parse_env_file(env_file):
    """
    Reads a line-separated environment file.
    The format of each line should be "key=value".
    """
    environment = {}

    with open(env_file, 'r') as f:
        for line in f:

            if line[0] == '#':
                continue

            line = line.strip()
            if not line:
                continue

            parse_line = line.split('=', 1)
            if len(parse_line) == 2:
                k, v = parse_line
                environment[k] = v
            else:
                raise errors.DockerException(
                    'Invalid line in environment file {0}:\n{1}'.format(
                        env_file, line))

    return environment


def split_command(command):
    if six.PY2 and not isinstance(command, six.binary_type):
        command = command.encode('utf-8')
    return shlex.split(command)


def format_environment(environment):
    def format_env(key, value):
        if value is None:
            return key
        if isinstance(value, six.binary_type):
            value = value.decode('utf-8')

        return u'{key}={value}'.format(key=key, value=value)
    return [format_env(*var) for var in six.iteritems(environment)]


def format_extra_hosts(extra_hosts, task=False):
    # Use format dictated by Swarm API if container is part of a task
    if task:
        return [
            '{} {}'.format(v, k) for k, v in sorted(six.iteritems(extra_hosts))
        ]

    return [
        '{}:{}'.format(k, v) for k, v in sorted(six.iteritems(extra_hosts))
    ]


def create_host_config(self, *args, **kwargs):
    raise errors.DeprecatedMethod(
        'utils.create_host_config has been removed. Please use a '
        'docker.types.HostConfig object instead.'
    )


#!/usr/bin/env python3
# coding=utf-8
"""
Script Name: utils.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    Here is where a lot of function need to use multiple times overall
"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import
""" Import """

# Python
import os, sys, requests, platform, subprocess, winshell, yaml, json, linecache, re, datetime, time, uuid, win32api, pprint

__all__ = ['attr_type', 'auto_convert', 'camel_case_to_lower_case_underscore', 'camel_case_to_title', 'clean_name',
            'is_bool', 'is_dict', 'is_list', 'is_none', 'is_number', 'is_string', 'list_attr_types',
            'lower_case_underscore_to_camel_case', 'is_newer', 'test_func']

# PyQt5
from PyQt5.QtCore   import Qt, QRectF, QRect, QSize
from PyQt5.QtGui    import QColor, QFont, QFontMetrics

# PLM
from core       import __envKey__, __pkgsReq__
from core       import LOGO_DIR, WEB_ICON_DIR, TAG_DIR, AVATAR_DIR
from core       import KEYPACKAGE
from core       import IsADirectoryError, FileNotFoundError


from core.Loggers   import Loggers
logger = Loggers(__name__)
report = logger.report

import base64
import os
import os.path
import json
import shlex
from distutils.version import StrictVersion
from datetime import datetime

import six

from .. import errors
from .. import tls

if six.PY2:
    from urllib import splitnport
else:
    from urllib.parse import splitnport

# -------------------------------------------------------------------------------------------------------------
""" Destop tool """

def create_shotcut(target, icon, shortcut, description):
    winshell.CreateShortcut(
        Path=os.path.join(winshell.desktop(), shortcut),
        Target=target,
        Icon=(icon, 0),
        Description=description
    )

def create_folder(pth, mode=0o770):
    if not pth or os.path.exists(pth):
        return []

    (head, tail) = os.path.split(pth)
    res = create_folder(head, mode)
    try:
        original_umask = os.umask(0)
        os.makedirs(pth, mode)
    except:
        os.chmod(pth, mode)
    finally:
        os.umask(original_umask)
    res += [pth]
    return res

def obj_properties_setting(directory, mode):
    if platform.system() == "Windows" or platform.system() == "Darwin":
        if mode == "h":
            if platform.system() == "Windows":
                subprocess.call(["attrib", "+H", directory])
            elif platform.system() == "Darwin":
                subprocess.call(["chflags", "hidden", directory])
        elif mode == "s":
            if platform.system() == "Windows":
                subprocess.call(["attrib", "-H", directory])
            elif platform.system() == "Darwin":
                subprocess.call(["chflags", "nohidden", directory])
        else:
            report("ERROR: (Incorrect Command) Valid commands are 'HIDE' and 'UNHIDE' (both are not case sensitive)")
    else:
        report("ERROR: (Unknown Operating System) Only Windows and Darwin(Mac) are Supported")

def batch_obj_properties_setting(listObj, mode):

    for obj in listObj:
        if os.path.exists(obj):
            obj_properties_setting(obj, mode)
        else:
            report('Could not find the specific path: %s' % obj)

# -------------------------------------------------------------------------------------------------------------
""" Error handle """

def handle_path_error(directory=None):
    if not os.path.exists(directory) or directory is None:
        try:
            raise IsADirectoryError("Path is not exists: {directory}".format(directory=directory))
        except IsADirectoryError as error:
            raise('Caught error: ' + repr(error))

def raise_exception():

    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)

    report("--------------------------------------------------------------------------------- \n"
            "Tracking from:   {0} \n"
            "At line number:  {1} \n"
            "Details code:    {2} \n"
            "{3} \n"
            "---------------------------------------------------------------------------------".format(os.path.basename(filename), lineno, line.strip(), exc_obj))
    return

def print_variable(varName, varData):
    print('###-------------------------------------------------------------------------------###')
    print('-------- CHECK VARIABLE: {0}'.format(varName))
    print('------------ File location: {0}'.format(__file__))
    print('------------ Variable type: {0}'.format(type(varName)))
    print(' ')
    print('-------- VARIABLE CONTENT')
    print(' ')

    pprint.pprint(varData)

    print(' ')
    print('-------- END CHECK')
    print('###-------------------------------------------------------------------------------###')

# -------------------------------------------------------------------------------------------------------------
""" Python """

def install_py_packages(name):
    """
    Install python package via command prompt
    :param name: name of component
    :return:
    """
    # report('Using pip to install %s' % name)
    if os.path.exists(name):
        subprocess.Popen('python %s install' % name)
    else:
        subprocess.Popen('python -m pip install %s' % name, shell=True).wait()

def install_require_package(package=__pkgsReq__):
    try:
        import package
    except ImportError as err:
        report("installing {0}".format(package))
        command = "start python -m pip install {0}".format(package)
        p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        status = p.wait()
        report("Command output: {0}".format(output))

def uninstall_all_required_package():
    for pkg in __pkgsReq__:
        try:
            subprocess.Popen("python -m pip uninstall %s" % pkg)
        except FileNotFoundError:
            subprocess.Popen("pip uninstall %s" % pkg)
            __pkgsReq__.remove(pkg)

    if len(__pkgsReq__)==0:
        return True
    else:
        return False

def get_py_env_var(key, path):
    try:
        pth = os.getenv(key)
        if pth == None or pth == '':
            report('install new environment variable')
            os.environ[key] = path
    except KeyError:
        report('install new environment variable')
        os.environ[key] = path
    else:
        pass

# -------------------------------------------------------------------------------------------------------------
""" Command Prompt """

def cmd_execute_py(name, path):
    """
    Executing a python file
    :param name: python file name
    :param path: path to python file
    :return: executing in command prompt
    """
    report("Executing {name} from {path}".format(name=name, path=path))
    pth = os.path.join(path, name)
    if os.path.exists(pth):
        subprocess.call([sys.executable, pth])

def system_call(args, cwd="."):
    report("Running '{}' in '{}'".format(str(args), cwd))
    subprocess.call(args, cwd=cwd)
    pass

def run_cmd(pth):
    subprocess.Popen(pth)

def open_cmd():
    os.system("start /wait cmd")

# -------------------------------------------------------------------------------------------------------------
""" Find Path """

def get_all_path_from_dir(directory):
    """
        This function will generate the file names in a directory
        tree by walking the tree either top-down or bottom-up. For each
        directory in the tree rooted at directory top (including top itself),
        it yields a 3-tuple (dirpath, dirnames, filenames).
    """
    filePths = []   # List which will store all of the full file paths.
    dirPths = []    # List which will store all of the full folder paths.

    # Walk the tree.
    for root, directories, files in os.walk(directory, topdown=False):
        for filename in files:
            filePths.append(os.path.join(root, filename))  # Add to file list.
        for folder in directories:
            dirPths.append(os.path.join(root, folder)) # Add to folder list.
    return [filePths, dirPths]

def get_file_path(directory):
    handle_path_error(directory)
    return get_all_path_from_dir(directory)[0]

def get_folder_path(directory):
    handle_path_error(directory)
    return get_all_path_from_dir(directory)[1]

def get_base_folder(path):
    return os.path.dirname(path)

def get_base_name(path):
    return os.path.basename(path)

def get_app_icon(size=32, iconName="AboutPlt"):
    iconPth = os.path.join(os.getenv(__envKey__), 'imgs', 'icons', "x" + str(size))
    return os.path.join(iconPth, iconName + ".icon.png")

def get_logo_icon(size=32, name="DAMG"):
    if name == "Logo":
        logoPth = os.path.join(LOGO_DIR, 'Plm', 'icons')
    elif name == 'DAMG':
        logoPth = os.path.join(LOGO_DIR, 'DAMGteam', 'icons')
    else:
        logoPth = os.path.join(LOGO_DIR, 'Plt', 'icons')
    return os.path.join(logoPth, str(size) + "x" + str(size) + ".png")

def get_web_icon(name):
    icons = [i for i in get_file_path(WEB_ICON_DIR) if ".icon" in i]
    for i in icons:
        if name in i:
            return i

def get_avatar_icon(name):
    avatars = [a for a in get_file_path(AVATAR_DIR) if '.avatar' in a]
    for a in avatars:
        if name in a:
            return a

def get_tag_icon(name):
    tags = [t for t in get_file_path(TAG_DIR) if '.tag' in t]
    for t in tags:
        if name in t:
            return t

def generate_alternative_color(color, av):
    lightness = color.lightness()
    mult = float(lightness)/255
    return mult

def convert_to_QColor(data=None, alternate=False, av=20):
    if len(data) == 3:
        color = QColor(data[0], data[1], data[2])
        if alternate:
            mult = generate_alternative_color(color, av)
            color = QColor(max(0, data[0]-(av*mult)), max(0, data[1]-(av*mult)), max(0, data[2]-(av*mult)))
        return color
    elif len(data) == 4:
        color = QColor(data[0], data[1], data[2], data[3])
        if alternate:
            mult = generate_alternative_color(color, av)
            color = QColor(max(0, data[0]-(av*mult)), max(0, data[1]-(av*mult)), max(0, data[2]-(av*mult)), data[3])
        return color
    else:
        report('Color from configuration is not recognized : ', data)
        report('Can only be [R, G, B] or [R, G, B, A]')
        report('Using default color !')
        color = QColor(120, 120, 120)
        if alternate:
            color = QColor(120-av, 120-av, 120-av)
        return color

def get_pointer_bounding_box(pointerPos, bbSize):
    point = pointerPos
    mbbPos = point
    point.setX(point.x() - bbSize / 2)
    point.setY(point.y() - bbSize / 2)
    size = QSize(bbSize, bbSize)
    bb = QRect(mbbPos, size)
    bb = QRectF(bb)
    return bb

# -------------------------------------------------------------------------------------------------------------
""" Read, Write, Edit json/yaml/config info """

def data_handler(type='json', mode='r', filePath=None, data={}):
    info = {}
    if type == 'json':
        if mode == 'r' or mode == 'r+':
            with open(filePath, mode) as f:
                info = json.load(f)
        elif mode == 'w' or mode == 'w+':
            with open(filePath, mode) as f:
                info = json.dump(data, f, indent=4)
        else:
            with open(filePath, mode) as f:
                info = json.dump(data, f, indent=4)
    else:
        if mode == 'r' or mode == 'r+':
            with open(filePath, mode) as f:
                info = yaml.load(f)
        elif mode == 'w' or mode == 'w+':
            with open(filePath, mode) as f:
                info = yaml.dump(data, f, default_flow_style=False)
        else:
            with open(filePath, mode) as f:
                info = yaml.dump(data, f, default_flow_style=False)
    return info

def swap_list_index(inputList, oldIndex, newIndex):
    if oldIndex == -1:
        oldIndex = len(inputList)-1
    if newIndex == -1:
        newIndex = len(inputList)
    value = inputList[oldIndex]
    inputList.pop(oldIndex)
    inputList.insert(newIndex, value)

def load_config(filePath):
    with open(filePath, 'r') as myfile:
        fileString = myfile.read()
        cleanString = re.sub('//.*?\n|/\*.*?\*/', '', fileString, re.S)                 # remove comments
        data = json.loads(cleanString)
    return data

def save_data(filePath, data):
    f = open(filePath, "w")
    f.write(json.dumps(data, sort_keys = True, indent = 4, ensure_ascii=False))
    f.close()

def load_data(filePath):
    with open(filePath) as json_file:
        j_data = json.load(json_file)
    json_file.close()
    return j_data

# -------------------------------------------------------------------------------------------------------------
""" Collecting info user """

def get_user_location():

    package = KEYPACKAGE
    pythonVersion = sys.version
    windowOS = platform.system()
    windowVersion = platform.version()

    sysOpts = package['sysOpts']
    cache = os.popen2("SYSTEMINFO")
    source = cache[1].read()

    sysInfo = {}

    sysInfo['python'] = pythonVersion
    sysInfo['os'] = windowOS + "|" + windowVersion
    sysInfo['pcUser'] = platform.node()
    sysInfo['operating system'] = platform.system() + "/" + platform.platform()
    sysInfo['python version'] = platform.python_version()

    values = {}

    for opt in sysOpts:
        values[opt] = [item.strip() for item in re.findall("%s:\w*(.*?)\n" % (opt), source, re.IGNORECASE)][0]
    for item in values:
        sysInfo[item] = values[item]

    return sysInfo

def get_screen_resolution():
    resW = win32api.GetSystemMetrics(0)
    resH = win32api.GetSystemMetrics(1)
    return resW, resH

def get_window_taskbar_size():
    resW, resH = get_screen_resolution()
    monitors = win32api.EnumDisplayMonitors()
    display1 = win32api.GetMonitorInfo(monitors[0][0])
    tbH = resH - display1['Work'][3]
    tbW = resW
    return tbW, tbH

def get_local_pc_info():
    r = requests.get('https://api.ipdata.co').json()
    info = dict()
    for key in r:
        k = (str(key))
        for c in ['ip', 'city', 'country_name']:
            if k == c:
                info[k] = str(r[key])
            else:
                info[k] = 'unknown'

    return info['ip'], info['city'], info['country_name']

def get_layout_size(layout):
    sizeW = layout.frameGeometry().width()
    sizeH = layout.frameGeometry().height()
    return sizeW, sizeH

def get_text_size(text, painter=None):
    if not painter:
        metrics = QFontMetrics(QFont())
    else:
        metrics = painter.fontMetrics()
    size = metrics.size(Qt.TextSingleLine, text)
    return size

# ----------------------------------------------------------------------------------------------------------- #
""" Encode, decode, convert """

def codec_name(codec):
    try:
        name = str(codec.name(), encoding='ascii')          # Python v3.
    except TypeError:
        name = str(codec.name())                            # Python v2.
    return name

def text_to_utf8(input):
    return input.encode('utf-8')

def text_to_hex(text):
    return ''.join(["%02X" % ord(x) for x in str(text)])

def hex_to_text(hex):
    bytes = []
    hexStr = ''.join(str(hex).split(" "))
    for i in range(0, len(hexStr), 2):
        bytes.append(chr(int(hexStr[i:i + 2], 16)))
    outPut = ''.join(bytes)
    return outPut

def str2bool(arg):
    return str(arg).lower() in ['true', 1, '1', 'ok', '2']

def bool2str(arg):
    if arg:
        return "True"
    else:
        return "False"

def get_datetime():
    datetime_stamp = str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y.%m.%d||%H:%M:%S'))
    return datetime_stamp

def getDate():
    datetimeLog = get_datetime()
    return datetimeLog.split('||')[0]

def getTime():
    datetimeLog = get_datetime()
    return datetimeLog.split('||')[1]

def getToken():
    return str(uuid.uuid4())

def getUnix():
    return (str(uuid.uuid4())).split('-')[-1]

# ----------------------------------------------------------------------------------------------------------- #
""" String """

def check_blank(data):
    if len(data) == 0 or data == "" or data is None:
        return False
    else:
        return True

def check_match(data1, data2):
    check = []
    if len(data1) == len(data2):
        for i in range(len(data1)):
            if data1[i] is data2[i]:
                continue
            else:
                check.append('False')
    else:
        check.append('False')

    if len(check) == 0:
        return True
    else:
        return False

# ----------------------------------------------------------------------------------------------------------- #
""" Math """

def check_odd(num):
    return str2bool(num%2)

def get_all_odd(numLst):
    return [i for i in numLst if check_odd(i)]

def get_all_even(numLst):
    return [i for i in numLst if not check_odd(i)]

# ----------------------------------------------------------------------------------------------------------- #
""" Clean up """

def del_key(key, dict = {}):
    try:
        del dict[key]
        report("key deleted: {key}".format(key=key))
    except KeyError:
        dict.pop(key, None)
        report("key poped: {key}".format(key=key))

def clean_file_ext(ext):
    fileNames = [f for f in get_file_path(os.getenv(__envKey__)) if ext in f] or []
    if not fileNames == []:
        for filePth in fileNames:
            os.remove(filePth)


# - Naming ----
def clean_name(text):
    """
    Return a cleaned version of a string - removes everything
    but alphanumeric characters and dots.

    :param str text: string to clean.
    :returns: cleaned string.
    :rtype: str
    """
    return re.sub(r'[^a-zA-Z0-9\n\.]', '_', text)


def camel_case_to_lower_case_underscore(text):
    """
    Split string by upper case letters.
    F.e. useful to convert camel case strings to underscore separated ones.

    :param str text: string to convert.
    :returns: formatted string.
    :rtype: str
    """
    words = []
    from_char_position = 0
    for current_char_position, char in enumerate(text):
        if char.isupper() and from_char_position < text:
            words.append(s[from_char_position:current_char_position].lower())
            from_char_position = current_char_position
    words.append(text[from_char_position:].lower())
    return '_'.join(words)


def camel_case_to_title(text):
    """
    Split string by upper case letters and return a nice name.

    :param str text: string to convert.
    :returns: formatted string.
    :rtype: str
    """
    words = []
    from_char_position = 0
    for current_char_position, char in enumerate(text):
        if char.isupper() and from_char_position < current_char_position:
            words.append(text[from_char_position:current_char_position].title())
            from_char_position = current_char_position
    words.append(text[from_char_position:].title())
    return ' '.join(words)


def lower_case_underscore_to_camel_case(text):
    """
    Convert string or unicode from lower-case underscore to camel-case.

    :param str text: string to convert.
    :returns: formatted string.
    :rtype: str
    """
    split_string = text.split('_')
    # use string's class to work on the string to keep its type
    class_ = text.__class__
    return split_string[0] + class_.join('', map(class_.capitalize, split_string[1:]))


# - Attribute Functions ----
def auto_convert(value):
    """
    Auto-convert a value to it's given type.
    """
    atype = attr_type(value)
    if atype == 'str':
        return str(value)

    if atype == 'bool':
        return bool(value)

    if atype == 'float':
        return float(value)

    if atype == 'int':
        return int(value)
    return value


def attr_type(value):
    """
    Determine the attribute type based on a value.
    Returns a string.

    For example:

        value = [2.1, 0.5]
        type = 'float2'

    :param value: attribute value.

    :returns: attribute type.
    :rtype: str
    """
    if is_none(value):
        return 'null'

    if is_list(value):
        return list_attr_types(value)

    else:
        if is_bool(value):
            return 'bool'

        if is_string(value):
            return 'str'

        if is_number(value):
            if type(value) is float:
                return 'float'

            if type(value) is int:
                return 'int'
    return 'unknown'


def list_attr_types(s):
    """
    Return a string type for the value.

    .. todo::
        - 'unknown' might need to be changed
        - we'll need a feature to convert valid int/str to floats
          ie:
            [eval(x) for x in s if type(x) in [str, unicode]]
    """
    if not is_list(s):
        return 'unknown'

    for typ in [str, int, float, bool]:
        if all(isinstance(n, typ) for n in s):
            return '%s%d' % (typ.__name__, len(s))

    if False not in list(set([is_number(x) for x in s])):
        return 'float%d' % len(s)
    return 'unknown'


def is_none(s):
    return type(s).__name__ == 'NoneType'


def is_string(s):
    return type(s) in [str, unicode]


def is_number(s):
    """
    Check if a string is a int/float
    """
    if is_bool(s):
        return False
    return isinstance(s, int) or isinstance(s, float)


def is_bool(s):
    """
    Returns true if the object is a boolean value.
    * Updated to support custom decoders.
    """
    return isinstance(s, bool) or str(s).lower() in ['true', 'false']


def is_list(s):
    """
    Returns true if the object is a list type.
    """
    return type(s) in [list, tuple]


def is_dict(s):
    """
    Returns true if the object is a dict type.
    """
    from collections import OrderedDict
    return type(s) in [dict, OrderedDict]


def is_newer(file1, file2):
    """
    Returns true if file1 is newer than file2.

    :param str file1: first file to compare.
    :param str file2: second file to compare.

    :returns: file1 is newer.
    :rtype: bool
    """
    if not os.path.exists(file1) or not os.path.exists(file2):
        return False

    time1 = os.path.getmtime(file1)
    time2 = os.path.getmtime(file2)
    return time1 > time2


# - Testing -----
def test_func(w, h):
    print
    '# width: %.2f, height: %.2f' % (float(w), float(h))


def nodeParse(node):
    t = node[u"type"]

    if t == u"Program":
        body = [parse(block) for block in node[u"body"]]
        return Program(body)

    elif t == u"VariableDeclaration":
        kind = node[u"kind"]
        declarations = [parse(declaration) for declaration in node[u"declarations"]]
        return VariableDeclaration(kind, declarations)

    elif t == u"VariableDeclarator":
        id = parse(node[u"id"])
        init = parse(node[u"init"])
        return VariableDeclarator(id, init)

    elif t == u"Identifier":
        return Identifier(node[u"name"])

    elif t == u"Literal":
        return Literal(node[u"value"])

    elif t == u"BinaryExpression":
        operator = node[u"operator"]
        left = parse(node[u"left"])
        right = parse(node[u"right"])
        return BinaryExpression(operator, left, right)
    else:
        raise ValueError("Invalid data structure.")


# ----------------------------------------------------------------------------------------------------------- #