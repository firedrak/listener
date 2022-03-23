import redis
import sys
import subprocess
import time

# Sample command to use listener.py
# python3 listener.py redis_host

args = sys.argv[1:]
if args:
    redis_host = args[0]


class redisCli:

#     redis_host = '172.16.221.234'
    redis_host = redis_host
    redis_port = 6379

    REDIS_CLI = redis.StrictRedis(
        host=redis_host, port=redis_port, decode_responses=True)

    def should_i_start(self):
        return self.REDIS_CLI.get('should_i_start')

    def get_spider(self):
        return self.REDIS_CLI.get('spider')

    def set_should_i_start(self):
        self.REDIS_CLI.set('should_i_start', 'no')

subprocess.check_output(["rm", "-rf", "shell"])
subprocess.call(["git", "clone", "https://github.com/firedrak/shell.git"])

while True:
    time.sleep(2)
    if redisCli().should_i_start() == 'yes':
        spider_url = redisCli().get_spider()
        subprocess.call(["bash", "shell/shell.sh", f"{redis_host} {spider_url}"])
        break
print('Finished')
