import redis
import sys, time
import subprocess
from multiprocessing import Process


# Sample command to use listener.py
# python3 listener.py redis_host max_processes listener_name

args = sys.argv[1:]
if args:
    redis_host = args[0]
    max_processes = int(args[1])
    listener_name = args[2]

redis_port = 6379

REDIS_CLI = redis.StrictRedis(
    host=redis_host, port=redis_port, decode_responses=True)

def llen_spider():
    return REDIS_CLI.llen('spiders')

def get_spider():
    return REDIS_CLI.rpop('spiders')

def get_active_process(listener_name):
    return REDIS_CLI.get(f'active_process_of_{listener_name}')

def set_active_process(listener_name):
    return REDIS_CLI.set(f'active_process_of_{listener_name}', 0)

def inc_active_process(listener_name):
    REDIS_CLI.incr(f'active_process_of_{listener_name}')

def decr_active_process(listener_name):
    REDIS_CLI.decr(f'active_process_of_{listener_name}')

def start_executor(redis_host, spider_url):
    subprocess.call(["bash", "shell/shell.sh"], stdout=FNULL)
    subprocess.call(["time", "python3", "crawler/main.py", redis_host, spider_url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    decr_active_process(listener_name)

subprocess.check_output(["sudo", "rm", "-rf", "shell"])
subprocess.call(["git", "clone", "https://github.com/firedrak/shell.git"])

processes = []
set_active_process(listener_name)

while True:
    if int(get_active_process(listener_name)) <= max_processes: 
        if llen_spider():
            spider_url = get_spider()
            print('Crawling started')
            inc_active_process(listener_name)
            processe = Process(target = start_executor, args = (redis_host, spider_url))
            processe.start()
            processes.append(processe)
    time.sleep(1)
