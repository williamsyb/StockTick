
import weakref

# import redis
#
#
# class RedisCache(object):
#     _spam_cache = weakref.WeakValueDictionary()
#
#     def __new__(cls, host, port):
#         if (host, port) in cls._spam_cache:
#             return cls._spam_cache[(host, port)]
#         else:
#             self = object.__new__(cls)
#             cls._spam_cache[(host, port)] = self
#             return self
#
#     def __init__(self, host, port):
#         pool = redis.ConnectionPool(host=host, port=port)
#         self.client = redis.Redis(connection_pool=pool, decode_responses=True)
