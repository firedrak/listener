import redis
import sys
import subprocess
from multiprocessing import Process


# Sample command to use listener.py
# python3 listener.py redis_host

args = sys.argv[1:]
if args:
    redis_host = args[0]
    max_processes = int(args[1])

active_processes = 0

class redisCli:

#     redis_host = '172.16.221.234'
    redis_host = redis_host
    redis_port = 6379

    REDIS_CLI = redis.StrictRedis(
        host=redis_host, port=redis_port, decode_responses=True)

    def get_spider(self):
        return self.REDIS_CLI.rpop('spiders')


def start_executor(redis_host, spider_url):
    subprocess.call(["bash", "shell/shell.sh", f"{redis_host} {spider_url}"])
    active_processes -= 1

subprocess.check_output(["rm", "-rf", "shell"])
subprocess.call(["git", "clone", "https://github.com/firedrak/shell.git"])

processes = []

while True:
    if active_processes <= max_processes: 
        if redisCli().get_spider():
            spider_url = redisCli().get_spider()
            processe = Process(target = start_executor, args = (redis_host, spider_url))
            active_processes += 1
            processe.start()
            processes.append(processe)

