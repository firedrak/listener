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

redis_host = redis_host
redis_port = 6379

REDIS_CLI = redis.StrictRedis(
    host=redis_host, port=redis_port, decode_responses=True)

def get_spider():
    return REDIS_CLI.rpop('spiders')

def get_active_process(listener_name):
    return REDIS_CLI.get(f'active_process_of_{host}')

def set_active_process(listener_name):
    return REDIS_CLI.set(f'active_process_of_{host}', 0)

def inc_active_process(listener_name):
    REDIS_CLI.incr(f'active_process_of_{host}')

def decr_active_process(listener_name):
    REDIS_CLI.decr(f'active_process_of_{host}')

def start_executor(redis_host, spider_url):
    subprocess.call(["python3", "crawler/crawler.py", f"{redis_host} {spider_url}"])
    decr_active_process(listener_name)

subprocess.check_output(["rm", "-rf", "crawler"])
subprocess.call(["git", "clone", "https://github.com/firedrak/crawler.git"])

processes = []
set_active_process(listener_name)

while True:
    if int(get_active_process(listener_name)) <= max_processes: 
        if get_spider():
            spider_url = get_spider()
            inc_active_process(listener_name)
            processe = Process(target = start_executor, args = (redis_host, spider_url))
            processe.start()
            processes.append(processe)
    time.sleep(1)
