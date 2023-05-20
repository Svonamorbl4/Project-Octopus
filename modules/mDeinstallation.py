import paramiko
import asyncio

async def mDeinstallation(username, hostname, password, pkgName):
    # await asyncio.sleep(8)
    command = 'sudo -S apt remove -y ' + pkgName
    client = paramiko.SSHClient()
    key = paramiko.RSAKey.from_private_key_file('/home/svonamor/.ssh/id_rsa')
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=hostname, port=22, username=username, pkey=key, password=password)

    task = asyncio.create_task(mSubDeinstallation(command, client, password))
    await task

async def mSubDeinstallation(command, client, password):
    channel = client.get_transport().open_session()
    channel.get_pty()
    channel.settimeout(1)
    channel.exec_command(command)
    channel.send(password + '\n')
    channel.recv_exit_status()
    client.exec_command(command)
    channel.close()
    client.close()