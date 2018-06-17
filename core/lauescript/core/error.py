"""
Module for reporting of error messages.
"""
__author__ = 'Arrahed'

from socket import AF_INET, SOCK_STREAM, socket
from getpass import getuser
import os
import uuid
import hashlib
import json
import io
#from io import TextIOWrapper, BytesIO


clientSocket = None


def create_hash():
    """
    Creates a hash from user and machine specific information. The hash code can not
    be used to reconstruct any of those information and is completely anonymous.
    :return: String representation of the hash.
    """
    hashString = hashlib.md5(str(getuser()) + str(uuid.getnode()) + os.name).hexdigest()
    return hashString


def createReport(tb, comment='', fileContent=''):
    """
    Creates a JSON object from the traceback string a possible comment
    and filecontent.
    All personal information is removed and no private data is left in
    the report.
    :param tb: String representation of a traceback.
    :param comment: String representation of a comment.
    :param fileContent: 'String representation of one or more files.
    :return: String representation of the report including the JSON object and a hash.
    """
    userHash = create_hash()
    osName = os.name
    tb = cleanTb(tb)
    j = json.dumps({'userHash': userHash,
                    'os': osName,
                    'tb': tb,
                    'comment': comment,
                    'file': fileContent})
    mHash = hashlib.md5(j).hexdigest()
    return '{}***{}'.format(j, mHash)


def cleanTb(tb):
    """
    Removes data privacy related information from the traceback.
    :param tb: String representation of the most recent traceback.
    :return: String representation of the cleaned up traceback.
    """
    cleaned = []
    for line in tb.split('\n'):
        if ' File \"' in line and ' line ' in line:
            lLine = ''.join(line.partition('\"')[:-1])
            rLine = ''.join(line.rpartition('/')[1:])
            line = ''.join((lLine, rLine))
        cleaned.append(line)
    return '\n'.join(cleaned).replace('\'', '##').replace('\"', '##')


def convert_to_bytes(no):
    """
    Returns a 4 byte large representation of an integer.
    :param no: Integer
    :return: bytearray representation of input Integer.
    """
    result = bytearray()
    result.append(no & 255)
    for i in range(3):
        no >>= 8
        result.append(no & 255)
    return result


def connect(config):
    """
    Connects to a socket specified in the INI file.
    :param config: Reference to a plugin manager instance.
    :return:
    """
    global clientSocket
    clientSocket = socket(AF_INET, SOCK_STREAM)
    host = config.config.get('Errors', 'ServerAddress')
    port = config.config.getint('Errors', 'Port')
    clientSocket.settimeout(3)
    clientSocket.connect((host, port))


def sendReport(message, config):
    """
    Sends a message to the error server specified in the INI file.
    :param message: String representation of the message
    :param config: Reference to a plugin manager instance.
    :return: None
    """
    connect(config)
    #message = createReport(tb)
    message = message.encode('utf-8')
    bs = convert_to_bytes(len(message))
    message = io.TextIOWrapper(io.BytesIO(message))
    clientSocket.send(bs)
    chunk = message.read(1024)
    while chunk:
        clientSocket.send(chunk)
        chunk = message.read(1024)
    # printer('Report sent')
    _ = clientSocket.recv(1024).decode()
    # printer(answer)
    clientSocket.close()