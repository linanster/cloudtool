from flask import request, g
from functools import wraps
#
from app.lib.mylogger import logger
#
def afterrequestlog(func):
    @wraps(func)
    def inner(response):
        request_addr = request.headers.get('X-Real-IP') or request.remote_addr
        username = g.get('user').username if g.get('user') else ''
        logger.info('{} {} - FROM {} - By {} - Response: {}'.format(request.method, request.url, request_addr, username, response.status))
        return func(response)
    return inner

