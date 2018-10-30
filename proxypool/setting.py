# Redis 数据库
REDIS_HOST= '127.0.0.1'
REDIS_PORT = 6379
REDIS_PASSWORD = None
REDIS_KEY = 'proxies'


# web API
API_HOST = '0.0.0.0'
API_PORT = 5555

# 代理分数
# 最大分数
MAX_SCORE = 100
# 最小分数
MIN_SCORE = 0
# 初始分数
INITIAL_SCORE = 10

VALID_STATUS_CODES = [200, 302]
# 代理池数量界限
POOL_UPPER_THRESHOLD = 50000

# 检查周期
TESTER_CYCLE= 20
# 获取周期
GETTER_CYCLE= 300

# 测试API，建议抓哪个网站测哪个
TEST_URL = 'http://www.baidu.com'

# 最大批测试量
BATCH_TEST_SIZE = 10


# 开关
TESTER_ENABLED = True
GETTER_ENABLED = True
API_ENABLED = True
