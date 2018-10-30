import redis
import re
from proxypool.error import PoolEmptyError
from proxypool.setting import REDIS_HOST, REDIS_KEY, REDIS_PASSWORD, REDIS_PORT
from proxypool.setting import MAX_SCORE, MIN_SCORE, INITIAL_SCORE
from random import choice


class RedisClient(object):
    def __init__(self, host = REDIS_HOST, port = REDIS_PORT, password = REDIS_PASSWORD):
        """
        初始化
        :param host: Redis 地址
        :param port: Redis 端口
        :param password: Redis 密码
        """
        self.db = redis.StrictRedis(host = host, port = port, password = password, decode_responses= True)

    def add(self, proxy, score = INITIAL_SCORE):
        """
        向Redis中添加代理，
        :param proxy: 代理
        :param score: 分数
        :return: 返回结果
        """
        # 剔除不符合规范你的代理
        if not re.match('\d+\.\d+\.\d+\.\d+\:\d+', proxy):
            print('代理不符合规范', proxy, '丢弃')
            return
        """
        zset(sorted set：有序集合)
        Redis zset 和 set 一样也是string类型元素的集合,且不允许重复的成员。
        不同的是每个元素都会关联一个double类型的分数。redis正是通过分数来为集合中的成员进行从小到大的排序。
        zset的成员是唯一的,但分数(score)却可以重复。
        
        zadd 命令
添      加元素到集合，元素在集合中存在则更新对应score
        """
        if not self.db.zscore(REDIS_KEY, proxy):
            return self.db.zadd(REDIS_KEY, score, proxy)

    def random(self):
        """
        获取有效代理，首先尝试获取最高分数代理，如果不存在，按照排名获取，否则异常
        :return: 返回代理
        """
        result = self.db.zrangebyscore(REDIS_KEY, MAX_SCORE, MAX_SCORE)
        if len(result):
            return choice(result)
        else:
            result = self.db.zrevrange(REDIS_KEY, 0, 100)
            if len(result):
                return choice(result)
            else:
                raise PoolEmptyError

    def decrease(self, proxy):
        """
        代理值减一分，小于最小值则删除
        :param proxy: 代理
        :return: 修改后的代理分数
        """
        score = self.db.zscore(REDIS_KEY, proxy)
        if score and score > MIN_SCORE:
            print('代理', proxy, '当前分数', score, '减1')
            return self.db.zincrby(REDIS_KEY, proxy, -1)
        else:
            print('代理', proxy, '当前分数', score, '移除')
            return self.db.zrem(REDIS_KEY, proxy)

    def exists(self, proxy):
        """
        判断是否存在
        :param proxy: 代理
        :return: 是否存在
        """
        return not self.db.zscore(REDIS_KEY, proxy) == None

    def max(self, proxy):
        """
        将代理设置为MAX_SCORE
        :param proxy: 代理
        :return: 设置结果
        """
        print('代理', proxy, '可用，设置为', MAX_SCORE)
        return self.db.zadd(REDIS_KEY, MAX_SCORE, proxy)

    def count(self):
        """
        获取数量
        :return: 数量
        """
        return self.db.zcard(REDIS_KEY)

    def all(self):
        """
        获取全部代理
        :return: 全部代理列表
        """
        return self.db.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)

    def batch(self, start, stop):
        """
        批量获取
        :param start: 开始索引
        :param stop: 结束索引
        :return: 代理列表
        """
        return self.db.zrevrange(REDIS_KEY, start, stop - 1)


if __name__ == '__main__':
    conn = RedisClient()
    result = conn.batch(680, 688)
    print(result)