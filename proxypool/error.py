class PoolEmptyError(Exception):
    """
    新建一个异常类继承自Exception，
    用于在代理用完的时候报异常
    """
    def __init__(self):
        Exception.__init__(self)

    def __str__(self):
        return repr('代理池已经用完')