#!/usr/bin/python3
"""
Generate .tgz files
"""
from os import path
from datetime import datetime as dt
from fabric.api import local, put, run, env


env.user = "ubuntu"
env.hosts = ["3.236.145.87", "3.236.223.114"]


def do_pack():
    """ generate .tgz file"""
    archived = dt.utcnow()
    if path.isdir("versions") is False:
        if local("mkdir -p versions").failed is True:
            return None
    p = "versions/web_static_{}{}{}{}{}{}.tgz".format(
        archived.year, archived.month, archived.day,
        archived.hour, archived.minute, archived.second)
    if local("tar -cvzf {} web_static".format(
            p)).failed is True:
        return None
    return p


def do_deploy(archive_path):
    """ Deploy files to servers"""
    print("archive_path")
    if path.isfile("versions/{}".format(archive_path)) is False:
        return False
    result = put(
        "versions/{}".format(archive_path), "/tmp/{}".format(archive_path))
    if result.failed is True:
        return False
    extract_path = archive_path.split(".")[0]
    if run(
            "mkdir -p /data/web_static/releases/{}".format(
                extract_path)).failed is True:
        return False
    if run("tar -xf /tmp/{} -C /data/web_static/releases/{}".format(
            archive_path, extract_path)).failed is True:
        return False
    if run("rm -rf /tmp/{}".format(archive_path)).failed is True:
        return False
    if run(
        "rm /data/web_static/current && ln -sf /data/web_static/releases/{}"
            .format(extract_path)).failed is True:
        return False
    return True
