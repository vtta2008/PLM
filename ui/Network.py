# -*- coding: utf-8 -*-
"""

Script Name: Network.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import os, json, uuid

from datetime import datetime
from urllib import parse
import defer

# PyQt5
from PyQt5.QtCore import QTimer, QUrl
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest

# Plt
import appData as app
from appData.config import config


# -------------------------------------------------------------------------------------------------------------
""" Configure the current level to make it disable certain log """

logger = app.logger

# -------------------------------------------------------------------------------------------------------------
API_BASE = "https://api.telegram.org/bot{token}/{method}"
API_FILE = "https://api.telegram.org/file/bot{token}/{file_path}"


class NotificationItem:
    """The item shown in the notification."""

    MEDIA_TYPE_IMAGE = 'image'
    MEDIA_TYPE_AUDIO = 'audio'

    def __init__(self, message_id, text=None, sent_at=None,
                 extfile_path=None, media_type=None, useful=True):
        self.message_id = message_id
        self.useful = useful
        self.text = text
        self.sent_at = sent_at
        self.extfile_path = extfile_path
        self.media_type = media_type

    @classmethod
    @defer.inline_callbacks
    def _from_update(cls, update):
        """Create from a telegram message."""
        try:
            msg = update['message']
        except KeyError:
            logger.warning("Unknown update type: %r", update)
            return

        # only allow messages from a specific user (set in the first message, can be reset
        # through config)
        from_id = msg['from']['id']
        allowed_user = config.USER_ALLOWED
        if allowed_user is None:
            # user not configured yet, let's set it now
            logger.info("Setting allowed user id to %r", from_id)
            config.USER_ALLOWED = from_id
            config.save()
        else:
            # check user is allowed
            if allowed_user != from_id:
                logger.warning("Ignoring message from user not allowed: %r", from_id)
                return

        if 'text' in msg:
            text = msg['text']
            info = dict(text=text)

        elif 'photo' in msg:
            # grab the content of the biggest photo only
            photo = max(msg['photo'], key=lambda photo: photo['width'])
            extfile_path = yield download_file(photo['file_id'])
            media_type = cls.MEDIA_TYPE_IMAGE
            text = msg['caption'] if 'caption' in msg else None
            info = dict(extfile_path=extfile_path, media_type=media_type, text=text)

        elif 'voice' in msg:
            # get the audio file
            extfile_path = yield download_file(msg['voice']['file_id'])
            media_type = cls.MEDIA_TYPE_AUDIO
            info = dict(extfile_path=extfile_path, media_type=media_type)

        else:
            logger.warning("Message type not supported: %s", msg)
            return

        update_id = int(update['update_id'])
        sent_at = datetime.fromtimestamp(msg['date'])
        defer.return_value(cls(sent_at=sent_at, message_id=update_id, **info))

    @classmethod
    @defer.inline_callbacks
    def from_update(cls, update):
        """Securely parse from update, or return a not useful item."""
        try:
            item = yield cls._from_update(update)
        except Exception as exc:
            logger.exception("Problem parsing message from update: %s", exc)
            item = None

        if item is None:
            # bad parsing, crash in _from_update, user not allowed, etc
            update_id = int(update['update_id'])
            item = cls(message_id=update_id, useful=False)
        defer.return_value(item)

    def __str__(self):
        return "<Message [{}] {} {!r} ({}, {!r})>".format(
            self.message_id, self.sent_at, self. text, self.media_type, self.extfile_path)

class NetworkError(Exception):
    """Problems in the network."""


class _Downloader(object):
    """An asynch downloader that fires a deferred with data when done."""

    def __init__(self, url, file_path=None):
        if file_path is None:
            self.file_handler = None
            self.file_downloaded_size = None
        else:
            self.file_handler = open(file_path, "wb")
            self.file_downloaded_size = 0

        self._qt_network_manager = QNetworkAccessManager()

        self.deferred = defer.Deferred()
        self.deferred._store_it_because_qt_needs_or_wont_work = self
        request = QNetworkRequest(QUrl(url))

        self.req = self._qt_network_manager.get(request)
        self.req.error.connect(self.error)
        self.req.finished.connect(self.end)
        if self.file_handler is not None:
            self.req.downloadProgress.connect(self._save_partial)

        # program the eventual unlock
        QTimer.singleShot(10000, self.unlock)  # ten seconds should be more than enough (?)

    def _save_partial(self, dloaded, total):
        """Save partially downloaded content."""
        new_data = self.req.readAll()
        self.file_downloaded_size += len(new_data)
        self.file_handler.write(new_data)

    def unlock(self):
        """Unlock the downloader, no matter what."""
        if self.deferred.called:
            # exited normally or with error... but not locked!
            return

        error_message = "Downloader locked! Unlocking..."
        logger.warning(error_message)
        self.deferred.errback(ValueError(error_message))

    def error(self, error_code):
        """Request finished (*maybe*) on error."""
        error_message = "Downloader error {}: {}".format(error_code, self.req.errorString())
        logger.warning(error_message)
        if not self.deferred.called:
            self.deferred.errback(NetworkError(error_message))

    def end(self):
        """Send data through the deferred, if wasn't fired before."""
        if self.file_handler is None:
            result = self.req.read(self.req.bytesAvailable())
        else:
            result = self.file_downloaded_size
            self.file_handler.close()

        if result and not self.deferred.called:
            self.deferred.callback(result)


def build_baseapi_url(method, **kwargs):
    """Build the proper url to hit the API."""
    token = config.BOT_AUTH_TOKEN
    url = API_BASE.format(token=token, method=method)
    if kwargs:
        url += '?' + parse.urlencode(kwargs)
    return url


def build_fileapi_url(file_path):
    """Build the proper url to hit the API."""
    token = config.BOT_AUTH_TOKEN
    url = API_FILE.format(token=token, file_path=file_path)
    return url


@defer.inline_callbacks
def download_file(file_id):
    """Download the file content from Telegram."""
    url = build_baseapi_url('getFile', file_id=file_id)
    logger.debug("Getting file path, file_id=%s", file_id)
    downloader = _Downloader(url)
    encoded_data = yield downloader.deferred

    logger.debug("getFile response encoded data len=%d", len(encoded_data))
    data = json.loads(encoded_data.decode('utf8'))
    if not data.get('ok'):
        logger.warning("getFile result is not ok: %s", encoded_data)
        return

    remote_path = data['result']['file_path']
    url = build_fileapi_url(remote_path)
    file_path = os.path.join(app.DB_PTH, uuid.uuid4().hex + '-' + os.path.basename(remote_path))
    logger.debug("Getting file content, storing in %r", file_path)
    downloader = _Downloader(url, file_path)
    downloaded_size = yield downloader.deferred

    logger.debug("Downloaded file content, size=%d", downloaded_size)
    defer.return_value(file_path)


class MessagesGetter:
    """Get messages."""

    def __init__(self, new_items_callback, last_id_callback):
        self.new_items_callback = new_items_callback
        self.last_id_callback = last_id_callback

    @defer.inline_callbacks
    def _process(self, encoded_data):
        """Process received info."""
        logger.debug("Process encoded data len=%d", len(encoded_data))
        data = json.loads(encoded_data.decode('utf8'))
        if data.get('ok'):
            results = data['result']
            logger.debug("Telegram results ok! len=%d", len(results))
            items = []
            for item in results:
                logger.debug("Processing result: %s", item)
                ni = yield NotificationItem.from_update(item)
                items.append(ni)
            if items:
                self.new_items_callback(items)
        else:
            logger.warning("Telegram result is not ok: %s", data)

    def go(self):
        """Get the info from Telegram."""
        last_id = self.last_id_callback()
        kwargs = {}
        if last_id is not None:
            kwargs['offset'] = last_id + 1
        url = build_baseapi_url('getUpdates', **kwargs)
        logger.debug("Getting updates, kwargs=%s", kwargs)

        def _re_get(error):
            """Capture all results; always re-issue self.go, if error raise it."""
            polling_time = 1000 * config.POLLING_TIME
            logger.debug("Re get, error=%s polling_time=%d", error, polling_time)
            QTimer.singleShot(polling_time, self.go)
            if error is not None:
                error.raise_exception()

        self._downloader = _Downloader(url)
        self._downloader.deferred.add_callback(self._process)
        self._downloader.deferred.add_callbacks(_re_get, _re_get)


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 16/06/2018 - 2:26 AM
# © 2017 - 2018 DAMGteam. All rights reserved