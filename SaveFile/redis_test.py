#_*_coding:utf-8_*_
#author:wangxinchao

from redis import StrictRedis,ConnectionPool

class redisSpider(object):
    def __init__(self):
        self.redis = StrictRedis(host='localhost',db=2,password=None, port=6379)

    def _save(self):
        self.redis.set('wangxinchao','dafadaf')

    def _give(self):
        res = self.redis.get('wangxinchao')
        print(res)
    
    def __exit(self):
        res = self.redis.exists('wangxinchao')
        if res:
            self.redis.delete('wangxinchao')
        print(res)
    def _ops(self):
        print(self.redis.keys('w*'))
        self.redis.rename('wangxinchao1','wangxinhchao')
        print(self.redis.keys('w*'))

    def _main(self):
        self._ops()
        # self._save()
        # self._give()
        # self.__exit()
        # self._give()
if __name__ == '__main__':
    redis = redisSpider()
    redis._main()
