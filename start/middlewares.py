
# token加密解密
import jwt
import time
import config
import logging
logger = logging.getLogger('log')



def token_encode(open_id, access_token, expires_in):
    """
    加密token数据
    :param open_id: 用户openid
    :param access_token: 用户access_token信息
    :param expires_in: 用户超时时间
    :return:
    """
    d = {
        # 公有申明
        'exp': int(time.time()) + expires_in,  # token过期时间
        'iat': int(time.time()),  # token创建时间
        'iss': config.issuer,  # token的签发者

        # 私有声明
        'data': {
            'open_id': open_id,
            'access_token': access_token,
            'exp': expires_in,
            'timestamp': int(time.time())
        }
    }
    jwt_encode = jwt.encode(d, config.token_user, algorithm='HS256')
    return jwt_encode


def token_decode(token):
    """
    解析token加密
    :param token: 加密字符串
    :return:R
    """
    jwt_decode = None
    try:
        jwt_decode = jwt.decode(token, config.token_user, issuer=config.issuer, algorithms=['HS256'])
    except:
        logger.error('解析token失败')
    finally:
        return jwt_decode