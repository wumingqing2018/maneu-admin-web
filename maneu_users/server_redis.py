from django.core.cache import cache


def user_login_set(session_key, value):
    return cache.set(session_key, value, 600)


def user_login_get(session_key):
    return cache.get(session_key)


def user_login_ttl(session_key):
    return cache.ttl(session_key)


def user_login_del(session_key):
    return cache.delete(session_key)


def user_login_update(session_key):
    return cache.expire(session_key, timeout=600)


def user_login_verify(session_key):
    return cache.get_or_set(session_key, {'maneu_users': False}, 600)
