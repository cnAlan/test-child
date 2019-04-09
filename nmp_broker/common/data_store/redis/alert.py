# coding: utf-8
from nmp_broker.common.database import redis_client

dingtalk_access_token_key = "dingtalk_access_token"


def get_dingtalk_access_token_from_cache() -> str:
    dingtalk_access_token = redis_client.get(dingtalk_access_token_key)
    dingtalk_access_token = dingtalk_access_token.decode()
    return dingtalk_access_token


def save_dingtalk_access_token_to_cache(access_token: str) -> None:
    redis_client.set(dingtalk_access_token_key, access_token)
    return


weixin_access_token_key = "weixin_access_token"


def get_weixin_access_token_from_cache() -> str or None:
    weixin_access_token = redis_client.get(weixin_access_token_key)
    if weixin_access_token is None:
        return None
    weixin_access_token = weixin_access_token.decode()
    return weixin_access_token


def save_weixin_access_token_to_cache(access_token: str) -> None:
    redis_client.set(weixin_access_token_key, access_token)
    return
