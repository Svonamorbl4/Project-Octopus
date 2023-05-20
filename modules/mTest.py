import subprocess
import os
import paramiko
import asyncio

def mTest(username, hostname, password):
    command = 'echo Connection with Octopus is established! > TEST.oct'
    client = paramiko.SSHClient()
    key = paramiko.RSAKey.from_private_key_file('/home/svonamor/.ssh/id_rsa')
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=hostname, port=22, username=username, pkey=key, password=password)
    stdin, stdout, stderr = client.exec_command(command)
    res, err = stdout.read(), stderr.read()
    result = res if res else err
    return result
    client.close()
