import subprocess

# for simple commands
subprocess.run(["scp", "svonamor@192.168.1.118:home/svonamor/Рабочий стол/Project Octopus/inventoryTest.txt", '/home/svonamor'])
# for complex commands, with many args, use string + `shell=True`:
cmd_str = "ls -l /tmp | awk '{print $3,$9}' | grep root"
subprocess.run(cmd_str, shell=True)

scp root@123.123.123.123:/home/test.txt /directory