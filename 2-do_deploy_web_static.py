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
'''
fabric script to distribute an archive to web servers
----NEEDS TO REVISIT SCRIPT
'''

import os
from datetime import datetime
from fabric.api import env, local, put, run, runs_once


env.hosts = ['18.205.38.219', '34.138.16.188']


def do_deploy(archive_path):
    """Distributes an archive to a web server.
    Args:
        archive_path (str): The path of the archive to distribute.
    Returns:
        If the file doesn't exist at archive_path or an error occurs - False.
        Otherwise - True.
    """
    if not os.path.isdir("versions"):
        os.mkdir("versions")
    cur_time = datetime.now()
    output = "versions/web_static_{}{}{}{}{}{}.tgz".format(
        cur_time.year,
        cur_time.month,
        cur_time.day,
        cur_time.hour,
        cur_time.minute,
        cur_time.second
    )
    try:
        print("Packing web_static to {}".format(output))
        local("tar -cvzf {} web_static".format(output))
        archize_size = os.stat(output).st_size
        print("web_static packed: {} -> {} Bytes".format(output, archize_size))
    except Exception:
        output = None
    return output


def do_deploy(archive_path):
    """Deploys the static files to the host servers.
    Args:
        archive_path (str): The path to the archived static files.
    """
    if not os.path.exists(archive_path):
        return False
    file_name = os.path.basename(archive_path)
    folder_name = file_name.replace(".tgz", "")
    folder_path = "/data/web_static/releases/{}/".format(folder_name)
    success = False
    try:
        put(archive_path, "/tmp/{}".format(file_name))
        run("mkdir -p {}".format(folder_path))
        run("tar -xzf /tmp/{} -C {}".format(file_name, folder_path))
        run("rm -rf /tmp/{}".format(file_name))
        run("mv {}web_static/* {}".format(folder_path, folder_path))
        run("rm -rf {}web_static".format(folder_path))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(folder_path))
        print('New version deployed!')
        success = True
    except Exception:
        success = False
    return 


