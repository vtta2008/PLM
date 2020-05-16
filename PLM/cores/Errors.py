# -*- coding: utf-8 -*-
"""

Script Name: Errors.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# PLM
from PLM.api.damg                    import DAMGERROR


class NodePropertyError(DAMGERROR): pass


class NodeWidgetError(DAMGERROR): pass


class NodeRegistrationError(DAMGERROR): pass


class PortRegistrationError(DAMGERROR): pass


class NodeMenuError(DAMGERROR): pass


class IconNotFound(DAMGERROR): pass


class ActionKeyConfigError(DAMGERROR): pass


class ActionRegisterError(DAMGERROR): pass


class ButtonRegisterError(DAMGERROR): pass


class ToolbarNameError(DAMGERROR): pass


class LayoutComponentError(DAMGERROR): pass


class ThreadNotFoundError(DAMGERROR): pass


class WorkerNotFoundError(DAMGERROR): pass


class TaskNotFoundError(DAMGERROR): pass


class CreateThreadError(DAMGERROR): pass


class CreateWorkerError(DAMGERROR): pass


class CreateTaskError(DAMGERROR): pass


class DirectoryError(DAMGERROR): pass


class EnsureValueError(ValueError):

    """Exception which gets raised by ensure_valid."""

    def __init__(self, obj):
        try:
            self.reason = obj.errorString()
        except AttributeError:
            self.reason = None
        err = "{} is not valid".format(obj)
        if self.reason:
            err += ": {}".format(self.reason)
        super(EnsureValueError, self).__init__(err)

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 4/12/2019 - 1:22 AM
# © 2017 - 2018 DAMGteam. All rights reserved