import paramiko
import asyncio
from scp import *
import os
import subprocess

async def mNginx(username, hostname, password):
    commandInstall = 'sudo -S apt install -y nginx'
    commandFirewall = 'sudo -S ufw allow "Nginx HTTP"'
    commandDir = 'sudo -S mkdir -p /var/www/octopus/html'
    commandOwn = 'sudo -S chown -R $USER:$USER /var/www/octopus/html'
    commandChmod = 'sudo -S chmod -R 755 /var/www/octopus'

    # commandNcPage = 'sudo -S nc -l -N 64000 > /var/www/octopus/html/index.html'
    #
    # commandNcInput = 'sudo -S cat /home/svonamor/Рабочий\ стол/Project\ Octopus/web/index.html | nc ' + hostname + ' 64000'
    #
    # commandNcSite = 'sudo -S nc -l -N 64001 > /etc/nginx/sites-available/octopus/'
    #
    # commandCfg = 'sudo -S cat /home/svonamor/Рабочий\ стол/Project\ Octopus/modules_configs/mNginx_config.cfg | nc ' + hostname + ' 64001'

    # commandRsync = 'sudo -S scp -P 2223 /home/svonamor/Рабочий\ стол/Project\ Octopus/web/index.html svonamor@192.168.1.218:/var/www/octopus.html'
    # commandRsyncCfg = 'sudo -S scp -P 2223 /home/svonamor/Рабочий\ стол/Project\ Octopus/web/modules_configs/mNginx_config.cfg svonamor@192.168.1.218:/etc/nginx/sites-available/octopus/'
    commandLink = 'sudo -S ln -s /etc/nginx/sites-available/octopus /etc/nginx/sites-enabled/'
    commandRestart = 'sudo -S systemctl restart nginx'
    #
    # with subprocess.Popen(["sudo", "-S", "cat", "/home/svonamor/Рабочий\ стол/Project\ Octopus/web/index.html", "|", "nc", "192.168.1.218", "64000"],
    #                       stdin=subprocess.PIPE,
    #                       stdout=subprocess.PIPE,
    #                       stderr=subprocess.PIPE) as proc:
    #     proc.communicate(bytes(password + '\n', "UTF-8"))
    #
    # with subprocess.Popen(["sudo", "-S", "cat", "/home/svonamor/Рабочий\ стол/Project\ Octopus/modules_configs/mNginx_config.cfg", "|", "nc", "192.168.1.218", "64001"],
    #                       stdin=subprocess.PIPE,
    #                       stdout=subprocess.PIPE,
    #                       stderr=subprocess.PIPE) as proc:
    #     proc.communicate(bytes(password + '\n', "UTF-8"))

    client = paramiko.SSHClient()
    key = paramiko.RSAKey.from_private_key_file('/home/svonamor/.ssh/id_rsa')
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=hostname, port=22, username=username, pkey=key, password=password)

    with SCPClient(client.get_transport()) as scp:
        scp.put('/home/svonamor/Рабочий стол/Project Octopus/web/index.html', '/var/www/octopus/html/index.html')

    with SCPClient(client.get_transport()) as scp:
        scp.put('/home/svonamor/Рабочий стол/Project Octopus/modules_configs/mNginx_config.cfg', '/etc/nginx/sites-available/octopus')

    taskInstall = asyncio.create_task(mSubNginx(commandInstall, client, password))
    await taskInstall

    taskFirewall = asyncio.create_task(mSubNginx(commandFirewall, client, password))
    await taskFirewall

    taskDir = asyncio.create_task(mSubNginx(commandDir, client, password))
    await taskDir

    taskOwn = asyncio.create_task(mSubNginx(commandOwn, client, password))
    await taskOwn

    taskChmod = asyncio.create_task(mSubNginx(commandChmod, client, password))
    await taskChmod

    # taskNcPage = asyncio.create_task(mSubNginx(commandNcPage, client, password))
    # await taskNcPage

    # taskCommandNcInput = asyncio.create_task(os.system(commandNcInput))
    # await taskCommandNcInput

    # taskCommandNcSite = asyncio.create_task(mSubNginx(commandNcSite, client, password))
    # await taskCommandNcSite

    # taskCommandCfg = asyncio.create_task(os.system(commandCfg))
    # await taskCommandCfg

    # taskCommandRsync= asyncio.create_task(mSubNginx(commandRsync, client, password))
    # await taskCommandRsync
    #
    # taskCommandRsyncCfg = asyncio.create_task(mSubNginx(commandRsyncCfg, client, password))
    # await taskCommandRsyncCfg
    #
    taskCommandLink= asyncio.create_task(mSubNginx(commandLink, client, password))
    await taskCommandLink

    taskCommandRestart = asyncio.create_task(mSubNginx(commandRestart, client, password))
    await taskCommandRestart

    client.close()

async def mSubNginx(command, client, password):
    channel = client.get_transport().open_session()
    channel.get_pty()
    channel.settimeout(1)
    channel.exec_command(command)
    channel.send(password + '\n')
    channel.recv_exit_status()
    client.exec_command(command)
    channel.close()