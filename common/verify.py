import re
from typing import Optional, Union

"""
通用校验工具模块
提供常用格式（日期、手机号、UUID、MD5、验证码、微信code）的校验，
以及移动端/PC端的 User-Agent 识别功能。
"""

# ==================== 预编译正则表达式 ====================
# 日期时间格式: YYYY-MM-DD HH:MM:SS
REGEX_DATETIME = re.compile(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$')

# 中国大陆手机号码: 1开头，第二位3-9，后面9位数字
REGEX_MOBILE = re.compile(r'^1[3-9]\d{9}$')

# UUID 格式 (8-4-4-4-12)
REGEX_UUID = re.compile(
    r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fa-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$'
)

# MD5 格式: 32位十六进制数字（无横线）
REGEX_MD5 = re.compile(r'^\d{32}$')

# 6位数字验证码
REGEX_CODE_6 = re.compile(r'^\d{6}$')

# 微信小程序 code: 64位十六进制字符串
REGEX_WX_CODE = re.compile(r'^[0-9a-fA-F]{64}$')

# 移动端 User-Agent 匹配（长模式）
USER_AGENT_LONG_MATCHES = re.compile(
    r'googlebot-mobile|android|avantgo|blackberry|blazer|elaine|hiptop|ip(hone|od)|kindle|midp|mmp'
    r'|mobile|o2|opera mini|palm( os)?|pda|plucker|pocket|psp|smartphone|symbian|treo|up\.(browser|link)'
    r'|vodafone|wap|windows ce; (iemobile|ppc)|xiino|maemo|fennec',
    re.IGNORECASE
)

# 移动端 User-Agent 匹配（短模式，取前4个字符匹配）
USER_AGENT_SHORT_MATCHES = re.compile(
    r'1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)'
    r'|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)'
    r'|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw'
    r'|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8'
    r'|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit'
    r'|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)'
    r'|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji'
    r'|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|e\-|e\/|\-[a-w])|libw|lynx'
    r'|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(di|rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi'
    r'|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)'
    r'|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg'
    r'|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21'
    r'|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-'
    r'|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it'
    r'|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)'
    r'|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)'
    r'|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit'
    r'|wi(g |nc|nw)|wmlb|wonu|x700|xda(\-|2|g)|yas\-|your|zeto|zte\-',
    re.IGNORECASE
)


# ==================== 校验函数 ====================

def is_date(code: str) -> bool:
    """
    判断字符串是否符合日期时间格式（YYYY-MM-DD HH:MM:SS）。

    Args:
        code: 待校验的字符串。

    Returns:
        bool: 符合格式返回 True，否则返回 False。
    """
    return REGEX_DATETIME.match(code) is not None


def is_call(code: str) -> Optional[str]:
    """
    判断字符串是否为有效的中国大陆手机号码（1开头，第二位3-9，共11位数字）。
    原函数行为: 若符合则返回原字符串，否则返回 None。

    Args:
        code: 待校验的字符串。

    Returns:
        Optional[str]: 符合格式时返回原字符串，否则返回 None。
    """
    if REGEX_MOBILE.match(code):
        return code
    return None


def is_uuid(code: str) -> Optional[str]:
    """
    判断字符串是否为标准 UUID 格式（8-4-4-4-12，十六进制字母可大小写）。

    Args:
        code: 待校验的字符串。

    Returns:
        Optional[str]: 符合格式时返回原字符串，否则返回 None。
    """
    if REGEX_UUID.match(code):
        return code
    return None


def is_md5(code: str) -> Optional[str]:
    """
    判断字符串是否为 32 位 MD5 格式（32个十六进制数字，无横线）。

    Args:
        code: 待校验的字符串。

    Returns:
        Optional[str]: 符合格式时返回原字符串，否则返回 None。
    """
    if REGEX_MD5.match(code):
        return code
    return None


def is_code(code: str) -> Optional[str]:
    """
    判断字符串是否为 6 位数字验证码。

    Args:
        code: 待校验的字符串。

    Returns:
        Optional[str]: 符合格式时返回原字符串，否则返回 None。
    """
    if REGEX_CODE_6.match(code):
        return code
    return None


def is_code_wx(code: str) -> Optional[str]:
    """
    判断字符串是否为微信小程序 code（64位十六进制字符串）。

    Args:
        code: 待校验的字符串。

    Returns:
        Optional[str]: 符合格式时返回原字符串，否则返回 None。
    """
    if REGEX_WX_CODE.match(code):
        return code
    return None


def is_mobile(ua: str) -> bool:
    """
    根据 User-Agent 判断客户端是否为移动端设备。

    Args:
        ua: HTTP 请求头中的 User-Agent 字符串。

    Returns:
        bool: 移动端返回 True，PC端返回 False。

    Example:
        # 在 Django 视图中使用
        if is_mobile(request.META.get("HTTP_USER_AGENT", "")):
            return render(request, 'mobile_template.html')
        else:
            return render(request, 'pc_template.html')
    """
    if USER_AGENT_LONG_MATCHES.search(ua):
        return True
    # 取前4个字符进行短模式匹配
    user_agent_head = ua[:4]
    if USER_AGENT_SHORT_MATCHES.search(user_agent_head):
        return True
    return False