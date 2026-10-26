"""
Django settings for maneu project.

Django 3.0 | 项目：maneu
"""

import os


# ============================================================================
# 路径配置
# ============================================================================
# BASE_DIR 指向 manage.py 所在目录（即项目根目录）
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# ============================================================================
# 安全与调试配置
# ============================================================================
# 参考文档：https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/
#
# ⚠️ 生产环境必改：
#   - DEBUG = False
#   - SECRET_KEY 从环境变量读取，不要硬编码
#   - ALLOWED_HOSTS 改为具体域名 / IP
#
# SECRET_KEY 缺省时用开发兜底值，避免环境变量未设置导致启动崩溃
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'dev-only-fallback')

# 调试模式：生产环境必须 False（否则会暴露路由、settings、源码堆栈）
DEBUG = True

# 允许访问的主机列表：生产环境应替换为具体域名 / IP
ALLOWED_HOSTS = ['*']


# ============================================================================
# 应用注册
# ============================================================================
INSTALLED_APPS = [
    # ---- Django 内置 ----
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # ---- 业务应用 ----
    'maneu',          # 主业务（认证、订单、报表核心）
    'maneu_admin',    # 管理员后台
    'maneu_index',    # 首页
    'maneu_order',    # 订单管理
    'maneu_report',   # 验光报告
    'maneu_store',    # 定制产品
]


# ============================================================================
# 中间件
# ============================================================================
# 注意顺序：
#   - AuthenticationMiddleware 必须先于自定义 JWT 中间件
#   - UserMiddleware 放在最后（依赖前面已初始化好的 request）
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # 自定义 JWT 鉴权中间件（需在最后）
    'common.UserMiddleware.UserMiddleware',
]


# ============================================================================
# 路由
# ============================================================================
ROOT_URLCONF = 'maneu.urls'


# ============================================================================
# 模板
# ============================================================================
# 参考文档：https://docs.djangoproject.com/en/3.0/ref/settings/#templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 项目级模板目录（额外目录，优先于 app 内 templates）
        'DIRS': [BASE_DIR + "/templates"],
        # 是否在各 app 的 templates/ 目录中查找模板
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# ============================================================================
# WSGI / ASGI 入口
# ============================================================================
WSGI_APPLICATION = 'maneu.wsgi.application'


# ============================================================================
# 数据库（MySQL）
# ============================================================================
# 参考文档：https://docs.djangoproject.com/en/3.0/ref/settings/#databases
#
# ⚠️ 用户名 / 密码从环境变量读取，生产环境不要硬编码
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'maneu',
        'HOST': '127.0.0.1',
        'PORT': 3306,
        'USER': os.environ.get('MYSQL_KEY_ID'),
        'PASSWORD': os.environ.get('MYSQL_KEY_SECRET'),
    }
}


# ============================================================================
# 密码强度校验
# ============================================================================
# 参考文档：https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        # 禁止密码与用户属性（用户名、邮箱等）过于相似
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        # 最小长度限制
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        # 禁止常见弱密码
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        # 禁止纯数字密码
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# ============================================================================
# 国际化与本地化
# ============================================================================
# 参考文档：https://docs.djangoproject.com/en/3.0/topics/i18n/
LANGUAGE_CODE = 'zh-hans'    # 简体中文
TIME_ZONE = 'Asia/Shanghai'  # 东八区
USE_I18N = True              # 启用翻译
USE_L10N = True              # 启用本地化格式（数字 / 日期等）
USE_TZ = False               # False = 使用 TIME_ZONE 本地时间；True = 存 UTC


# ============================================================================
# 静态文件
# ============================================================================
# 参考文档：https://docs.djangoproject.com/en/3.0/howto/static-files/
#
# ⚠️ STATIC_ROOT 目前是系统根目录 "/static/"，collectstatic 时需要 root 权限，
#    生产环境建议改为：STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
STATIC_ROOT = "/static/"
STATIC_FILES_DIRS = [os.path.join(BASE_DIR, "static")]


# ============================================================================
# JWT 配置（PyJWT）
# ============================================================================
# 说明：
#   - 所有需要登录的接口，路径中含 AUTH_URL_KEYWORDS 的会被 UserMiddleware 拦截
#   - SECRET_KEY 与 Django SECRET_KEY 一致；建议生产环境独立配 JWT_SECRET_KEY
JWT_CONFIG = {
    # 签名密钥（缺省从环境变量读取，兜底值仅用于开发）
    'SECRET_KEY': os.environ.get('DJANGO_SECRET_KEY', 'dev-only-fallback'),

    # 签名算法
    'ALGORITHM': 'HS256',

    # 签发者（写在 payload.iss 中，解码时一并校验）
    'ISSUER': 'maneu',

    # Token 有效期（秒）
    'ACCESS_TOKEN_LIFETIME':  30,             # 1 小时
    'REFRESH_TOKEN_LIFETIME': 60 * 60 * 24 * 7,    # 7 天

    # 请求头格式：Authorization: Bearer <token>
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'AUTH_HEADER_TYPES': ('Bearer',),

    # ⭐ 路径含以下关键词 → 需要登录；其他一律放行
    'AUTH_URL_KEYWORDS': ['/auth/'],
}


# ============================================================================
# Redis 缓存
# ============================================================================
# 用途：JWT 黑名单、短信验证码、微信 access_token、其他业务缓存
#
# ⚠️ LOCATION 当前用 db=1，注意与 db=0 区分，避免和其他服务冲突
#     如需密码：redis://:your_password@127.0.0.1:6379/1
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",

        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",

            # Redis 密码（如启用）
            # "PASSWORD": "your_redis_password",

            # 读写超时（秒）
            "SOCKET_TIMEOUT": 5,

            # 数据压缩（节省内存，django-redis 会自动解压）
            "COMPRESSOR": "django_redis.compressors.zlib.ZlibCompressor",

            # 连接池
            "CONNECTION_POOL_KWARGS": {
                "max_connections": 100,       # 最大连接数
                "health_check_interval": 30,  # 健康检查间隔（秒）
            },
        },

        # 所有缓存 key 前缀，避免与其他项目冲突
        "KEY_PREFIX": "maneu",
    }
}