from math import sqrt
import os.path as osp
from string import ascii_uppercase
import re
import uuid

import numpy as np

from qtpy import QtCore
from qtpy import QtGui
from qtpy import QtWidgets


here = osp.dirname(osp.abspath(__file__))


def newIcon(icon):
    icons_dir = osp.join(here, 'icons')
    return QtGui.QIcon(osp.join(':/', icons_dir, '%s.png' % icon))


def newButton(text, icon=None, slot=None):
    b = QtWidgets.QPushButton(text)
    if icon is not None:
        b.setIcon(newIcon(icon))
    if slot is not None:
        b.clicked.connect(slot)
    return b


def newAction(parent, text, slot=None, shortcut=None, icon=None,
              tip=None, checkable=False, enabled=True):
    """Create a new action and assign callbacks, shortcuts, etc."""
    a = QtWidgets.QAction(text, parent)
    if icon is not None:
        a.setIcon(newIcon(icon))
    if shortcut is not None:
        if isinstance(shortcut, (list, tuple)):
            a.setShortcuts(shortcut)
        else:
            a.setShortcut(shortcut)
    if tip is not None:
        a.setToolTip(tip)
        a.setStatusTip(tip)
    if slot is not None:
        a.triggered.connect(slot)
    if checkable:
        a.setCheckable(True)
    a.setEnabled(enabled)
    return a


def addActions(widget, actions):
    for action in actions:
        if action is None:
            widget.addSeparator()
        elif isinstance(action, QtWidgets.QMenu):
            widget.addMenu(action)
        else:
            widget.addAction(action)


def labelValidator():
    return QtGui.QRegExpValidator(QtCore.QRegExp(r'^[^ \t].+'), None)


class struct(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


def distance(p):
    return sqrt(p.x() * p.x() + p.y() * p.y())


def distancetoline(point, line):
    p1, p2 = line
    p1 = np.array([p1.x(), p1.y()])
    p2 = np.array([p2.x(), p2.y()])
    p3 = np.array([point.x(), point.y()])
    if np.dot((p3 - p1), (p2 - p1)) < 0:
        return np.linalg.norm(p3 - p1)
    if np.dot((p3 - p2), (p1 - p2)) < 0:
        return np.linalg.norm(p3 - p2)
    return np.linalg.norm(np.cross(p2 - p1, p1 - p3)) / np.linalg.norm(p2 - p1)


def fmtShortcut(text):
    mod, key = text.split('+', 1)
    return '<b>%s</b>+<b>%s</b>' % (mod, key)

def getUUID():
    return str(uuid.uuid1())

def generate_label(bnr_type=None,label=None):
    if bnr_type == 'aisle':
        if label:
            first_letter = label[0]
            second_letter = label[1]
            num = int(label[-2:])
            if num == 99:
                second_letter = ascii_uppercase[ascii_uppercase.find(second_letter)+1]
                num = 00
            else:
                num = num + 1
            return first_letter + second_letter + str(num).zfill(2)
        else:
            return ascii_uppercase[0] * 2 + '00'
    else:
        if label:
            num = int(label[-4:])
            num = num + 1
            return bnr_type[0:2].upper() + str(int(num)).zfill(4)
        else:
            return bnr_type[0:2].upper() + '0000'
