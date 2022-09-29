#!/usr/bin/python3
"""
Generate .tgz files
"""
import sys
import os
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
    if local("tar -cvzf {} web_static/".format(
            p)).failed is True:
        return None
    return p


def do_deploy(archive_path):
    """ Deploy files to servers"""
    print("archive_path")
    if path.isfile("{}".format(archive_path)) is False:
        return False
    result = put("{}".format(
        archive_path), "/tmp/{}".format(
            archive_path.split("/")[1]))
    if result.failed is True:
        return False
    extract_path = archive_path.split("/")[1].split(".")[0]
    if run("rm -rf /data/web_static/releases/{}/".format(
            extract_path)).failed is True:
        return False
    if run(
            "mkdir -p /data/web_static/releases/{}".format(
                extract_path)).failed is True:
        return False
    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}".format(
            archive_path.split("/")[1], extract_path)).failed is True:
        return False
    if run("rm -rf /tmp/{}".format(archive_path.split("/")[1])).failed is True:
        return False
    part1 = "mv /data/web_static/releases/{}/web_static/*".format(extract_path)
    part2 = "/data/web_static/releases/{}/".format(extract_path)
    mv = "{} {}".format(part1, part2)
    if run(mv).failed is True:
        return False
    if run("rm -rf /data/web_static/current").failed is True:
        pass
    if run(
        "ln -sf /data/web_static/releases/{}/ /data/web_static/current"
            .format(extract_path)).failed is True:
        return False
    return True


def deploy():
    """ Deploy in one command """
    file_path = do_pack()
    if not file_path:
        return False
    return do_deploy(file_path)


def do_clean(number=0):
    """clean outdated versions"""
    n = int(number)
    paths = sorted([dt.strptime(
        os.path.abspath(x).split("_")[-1].split(
            ".")[0], "%Y%m%d%H%M%S") for x in os.listdir('./versions')], reverse=True)
    #if int(number) > 1 and int(number) < len(paths):
    if int(number) <= 1:
        return;
    if int(number) >= len(paths):
        return;
    paths = paths[n:]
    pa = ["" + str(int(x.strftime("%Y"))) +
            str(int(x.strftime("%m"))) +
            str(int(x.strftime("%d"))) +
            str(int(x.strftime("%H"))) +
            str(int(x.strftime("%M"))) +
            str(int(x.strftime("%S"))) for x in paths]
    for p in pa:
        local("rm -rf versions/web_static_{}.tgz".format(p))
        run("rm -rf /data/web_static/releases/web_static_{}".format(p))
