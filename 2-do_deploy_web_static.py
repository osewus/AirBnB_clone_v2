# #!/usr/bin/python3
# from fabric.api import *
# from datetime import datetime
# import os

# env.hosts = ['35.196.60.116', '54.221.176.56']
# env.user = 'ubuntu'


# def do_deploy(archive_path):
#     """ fabric script to deploy to a server """
#     if not os.path.exists(archive_path):
#         return False

#     filename = archive_path.split("/")
#     filename = filename[1]
#     fname = filename.split('.')
#     fname = fname[0]

#     newpath = '/data/web_static/releases/{}/'.format(fname)

#     try:
#         put(archive_path, "/tmp/")
#         run("mkdir -p {}".format(newpath))
#         run("tar -xzf /tmp/{} -C {}".format(filename, newpath))
#         run("rm /tmp/{}".format(filename))
#         run("mv {}web_static/* {}".format(newpath, newpath))
#         run("rm -rf {}web_static".format(newpath))
#         run("rm -rf /data/web_static/current")
#         run("ln -s {} /data/web_static/current".format(newpath))
#         return True
#     except:
#         return False

#!/usr/bin/python3
"""Fabric script (based on the file 1-pack_web_static.py)
that distributes an archive to your web servers,
using the function do_deploy
"""
import time
import os
from fabric.api import *
from fabric.operations import run, put


env.hosts = ['34.138.195.126', '35.185.8.133']
env.user = 'ubuntu'


def do_pack():
    """generates a .tgz archive"""
    try:
        local("mkdir -p versions")
        local("tar -cvzf versions/web_static_{:s}.tgz web_static/".
              format(time.strftime("%Y%m%d%H%M%S")))
        return "versions/web_static_{:s}.tgz".\
            format(time.strftime("%Y%m%d%H%M%S"))
    except BaseException:
        return None


def do_deploy(archive_path):
    """distributes an archive to my web servers"""
    if not os.path.exists(archive_path):
        return False
    try:
        # Upload archive
        put(archive_path, '/tmp/')

        # Create a target dir without the file extension
        timestamp = time.strftime("%Y%m%d%H%M%S")
        run(
            'sudo mkdir -p /data/web_static/releases/web_static_{:s}/'.
            format(timestamp))

        # uncompress archive to the targed dir
        run('sudo tar xzvf /tmp/web_static_{:s}.tgz --directory\
            /data/web_static/releases/web_static_{:s}/'.
            format(timestamp, timestamp))

        # delete the archive from the web server
        run('sudo rm /tmp/web_static_{:s}.tgz'.format(timestamp))

        # move contents into host web_static
        run('sudo mv /data/web_static/releases/web_static_{:s}/web_static/*\
            /data/web_static/releases/web_static_{}/'.format(
            timestamp, timestamp))

        # remove irrelevant web_static dir
        run('sudo rm -rf /data/web_static/releases/web_static_{}/web_static'.
            format(timestamp))

        # delete the initial symbolic link from the web server
        run('sudo rm -rf /data/web_static/current')

        # create a new symbolic link
        run('sudo ln -s /data/web_static/releases/web_static_{:s}/ \
            /data/web_static/current'.format(
            timestamp))
    except BaseException:
        return False
    # if all that succeeded, return True
    return True
