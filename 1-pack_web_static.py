#!/usr/bin/python3
"""
Generate .tgz files
"""
from os import path
from datetime import datetime as dt
from fabric.api import local


def do_pack():
    """ generate .tgz file"""
    archived = dt.now()
    if not path.isdir("versions"):
        if local("mkdir -p versions").failed is True:
            return None
    p = "versions/web_static_{}{}{}{}{}{}".format(
        archived.year, archived.month, archived.day,
        archived.hour, archived.minute, archived.second)
    if local("tar -cvzf versions/{}.tgz web_static".format(
            p)).failed is True:
        return None
    return p
