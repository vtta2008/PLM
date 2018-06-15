# -*- coding: utf-8 -*-
"""

Script Name: PingCheck.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import sys
import subprocess, re, shlex
import appindicator, glib, gtk, requests, signal, time, pynotify, threading, gobject

# PyQt5
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget

# Plt
import appData as app
from ui import uirc as rc
from utilities import utils as func

# -------------------------------------------------------------------------------------------------------------
""" Configure the current level to make it disable certain log """

logger = app.logger

# -------------------------------------------------------------------------------------------------------------
""" PingCheck """

APPINDICATOR_ID = 'ping-check'
PYNOTIFY_ID = 'ping-check'
ping_host_name = "google.com"

"""
PingCheck class - main class implementing the entire app-indicator
"""


class PingCheck:
    """
    Class constructor
    """

    def __init__(self):
        # param1: appindicator identifier
        # param2: appindicator default icon name
        # param3: appindicator category
        self.indicator = appindicator.Indicator(APPINDICATOR_ID, gtk.STOCK_NO, appindicator.CATEGORY_COMMUNICATIONS)

        # activate the status of the indicator
        self.indicator.set_status(appindicator.STATUS_ACTIVE)

        # initiate the pynotify using some unique app ID
        pynotify.init(PYNOTIFY_ID)

        # Build the menu
        self.build_menu()

        self.ping_timeout = 3

        self.update_interval = 5
        self.timeout_ID = 1
        # set the first radio menu item active
        self.menu_refresh_control_items[0].set_active(True)

        self.ping_paused = False

        self.show_notification("Ping Check",
                               "Now tracking the ping continuously! You can pause the tracking from the menu.")
        self.indicator.set_icon(gtk.STOCK_NO)
        self.indicator.set_label("--")

        self.update_ui()

    """
    Method to build the entire menu including the submenu as well
    """

    def build_menu(self):
        # trigger to build the menu
        self.menu = gtk.Menu()

        # create a menu item for showing about indicator section
        item_about = gtk.MenuItem("Ping Check Indicator")
        self.menu.append(item_about)

        # create menu item for adjusting the ping refresh time
        item_refresh_control = gtk.MenuItem("Adjust refresh time")
        self.menu_refresh_control = gtk.Menu()
        self.menu_refresh_control_items = []
        group = [None]
        time_interval_list = [5, 10, 20, 30]
        for i in time_interval_list:
            subitem = gtk.RadioMenuItem(group[0], str(i) + " seconds")
            subitem.connect('activate', self.adjust_update_interval)
            self.menu_refresh_control.append(subitem)
            self.menu_refresh_control_items.append(subitem)
            group = subitem.get_group()
        item_refresh_control.set_submenu(self.menu_refresh_control)
        self.menu.append(item_refresh_control)

        # create a menu item for pausing and resuming the ping operation
        item_pause = gtk.MenuItem("Pause")
        item_pause.connect('activate', self.pause_resume)
        self.menu.append(item_pause)

        # create a menu item for exiting the app
        item_exit = gtk.MenuItem("Exit")
        item_exit.connect('activate', self.exit_indicator)
        self.menu.append(item_exit)

        self.menu.show_all()
        self.indicator.set_menu(self.menu)

    """
    Main method implementing the ping functionality,
    returns the ping time if successful ping is observed,
    and False otherwise
    """

    def ping(self, host_name):
        # pings google.com and returns a dot . on success and an X on failure
        ping_command = "ping -i " + str(self.ping_timeout) + " -c 1 " + host_name
        process = subprocess.Popen(shlex.split(ping_command), stdout=subprocess.PIPE)
        output = process.stdout.read()
        matches = re.findall(r"time=[0-9]\w+", output)
        if len(matches):
            # print matches[0].split("=")[-1]
            return matches[0].split("=")[-1]
        else:
            return False

    # return check_output( ["sh", "-c", "{ timeout " + str( self.ping_timeout ) + " ping -w 3 -c 2 -i 1 google.com > /dev/null 2>&1 && echo -n . ; } || { echo -n X ; }"] )

    """
    Method which will be called every {update_interval} seconds by glib
    """

    def update_timeout(self):

        if not self.ping_paused:
            self.update_ui()

        # returning True so that it doesn't get exited from timeout_add_seconds function
        return True

    """
    Method responsible for updating the label and icon of the app-indicator
    """

    def update_ui(self):
        # set the loading text
        curr_label = self.indicator.get_label()
        self.indicator.set_label(curr_label + "(Loading)")

        # ping the host and get the response
        ping_response = self.ping(ping_host_name)

        print(ping_response, self.update_interval)

        ## TODO ##
        if ping_response == False:
            # if False is received, play connection_down sound
            # and change the icon to STOCK_STOP one
            self.indicator.set_icon(gtk.STOCK_NO)
            self.indicator.set_label("--")
        else:
            # otherwise, change to STOCK_ON icon.
            self.indicator.set_icon(gtk.STOCK_YES)
            self.indicator.set_label(str(ping_response) + " ms")

    """
    Method to implement the pause/resume feature
    """

    def pause_resume(self, source):
        # click on resume
        if self.ping_paused:
            self.ping_paused = False
            self.indicator.set_label("Resuming...")
            source.set_label("Pause")
            self.show_notification("Ping Check", "Ping checking has been resumed!")
            self.update_ui()
        # click on pause
        else:
            self.ping_paused = True
            curr_label = self.indicator.get_label()
            self.indicator.set_label(curr_label + "(Paused)")
            source.set_label("Resume")
            self.show_notification("Ping Check", "Ping checking has been paused!")

    """
    Method to implement the adjustment of update interval feature
    """

    def adjust_update_interval(self, source):
        # find the value of update_interval represented by the source that's selected
        new_update_interval = int(source.get_label().split()[0])

        # update the update_interval value with the new one
        self.update_interval = new_update_interval

        try:
            # remove the current timeout_add_seconds event using its event ID
            glib.source_remove(self.timeout_ID)
        except:
            pass

        # start a new timeout_add_seconds event and update the timeout_ID for later updates
        self.timeout_ID = glib.timeout_add_seconds(self.update_interval, self.update_timeout)

    """
    Generalized method for showing a notification using pynotify
    """

    def show_notification(self, title="Title", msg="Message", timeout=1000):
        notification = pynotify.Notification(title, msg)
        notification.set_timeout(timeout)
        notification.show()

    """
    Method for exiting the app-indicator
    """

    def exit_indicator(self, source):
        gtk.main_quit()
        self.show_notification("Ping Check", "Exiting the app-indicator.")

    """
    Main method for initializing the gtk
    """

    def main(self):
        gtk.main()


if __name__ == "__main__":
    # For making Ctrl+C do it's default action
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    indicator = PingCheck()
    indicator.main()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 15/06/2018 - 5:10 PM
# © 2017 - 2018 DAMGteam. All rights reserved