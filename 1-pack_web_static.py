#!/usr/bin/python3
"""
Generate .tgz files
"""
from datetime import datetime as dt
from fabric.api import local


def do_pack():
    """ generate .tgz file"""
    archived = dt.now()
    path = "versions/web_static_{}{}{}{}{}{}".format(
        archived.year, archived.month, archived.day,
        archived.hour, archived.minute, archived.second)
    try:
        local(
            "mkdir -p versions && tar -cvzf versions/{}.tgz web_static".format(
                path))
    except Exception:
        return None
    else:
        return path
