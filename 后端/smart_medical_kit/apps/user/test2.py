import jwt
import requests


class OpenId(object):
    """获取openid类"""

    def __init__(self, jscode):
        self.url = 'https://api.weixin.qq.com/sns/jscode2session'

        self.app_id = 'wx7be9912ef8a9650c'
        self.app_secret = '9074257c19c86bdc574b000c3900d3b1'
        self.jscode = jscode

    def get_openid(self):
        url = self.url + "?appid=" + self.app_id + "&secret=" + self.app_secret + "&js_code=" + self.jscode + "&grant_type=authorization_code"
        res = requests.get(url)
        try:
            # 文档说unionid可以不用，就先对openid和session_key进行JWT加密生成token
            openid = res.json()['openid']  # 用户唯一标识
            session_key = res.json()['session_key']  # 会话密钥
            unionid = res.json()['unionid']  # 用户在开放平台的唯一标识符，在满足 UnionID 下发条件的情况下会返回，详见 UnionID 机制说明。
        except KeyError:
            return 'fail'
        else:
            return openid, session_key


class GetOpenID(object):
    """返回openid"""

    def __init__(self, jscode):
        self.jscode = jscode

    def get_token(self):
        openid, session_key = OpenId(self.jscode).get_openid()
        token_dict = {
            'openid': openid,
            'session_key': session_key
        }
        headers = {
            'alg': "HS256",  # 声明所使用的算法
        }
        jwt_token = jwt.encode(token_dict,  # payload, 有效载体
                               "zhananbudanchou9527269",  # 进行加密签名的密钥
                               algorithm="HS256",  # 指明签名算法方式, 默认也是HS256
                               headers=headers  # json web token 数据结构包含两部分, payload(有效载体), headers(标头)
                               ).decode('utf-8')  # python3 编码后得到 bytes, 再进行解码(指明解码的格式), 得到一个str
        return jwt_token


class GetToken(object):
    """
    上面两个是测试，这个是真正用的
    """
    def __init__(self, jscode):
        self.url = 'https://api.weixin.qq.com/sns/jscode2session'
        self.app_id = 'wx7be9912ef8a9650c'
        self.app_secret = '9074257c19c86bdc574b000c3900d3b1'
        self.jscode = jscode

    def get_openid(self):
        url = self.url + "?appid=" + self.app_id + "&secret=" + self.app_secret + "&js_code=" + self.jscode + "&grant_type=authorization_code"
        res = requests.get(url)
        try:
            # 文档说unionid可以不用，就先对openid和session_key进行JWT加密生成token
            openid = res.json()['openid']  # 用户唯一标识
            session_key = res.json()['session_key']  # 会话密钥
            unionid = res.json()['unionid']  # 用户在开放平台的唯一标识符，在满足 UnionID 下发条件的情况下会返回，详见 UnionID 机制说明。

            token_dict = {
                'openid': openid,
                'session_key': session_key
            }
            headers = {
                'alg': "HS256",  # 声明所使用的算法
            }
            jwt_token = jwt.encode(token_dict,  # payload, 有效载体
                                   "zhananbudanchou9527269",  # 进行加密签名的密钥
                                   algorithm="HS256",  # 指明签名算法方式, 默认也是HS256
                                   headers=headers  # json web token 数据结构包含两部分, payload(有效载体), headers(标头)
                                   ).decode('utf-8')  # python3 编码后得到 bytes, 再进行解码(指明解码的格式), 得到一个str
            return jwt_token
        except KeyError:
            return 'fail'
