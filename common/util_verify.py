"""
common/util_verify.py

通用格式校验工具

约定：
    - 校验类函数（is_xxx）：合法返回原值（str），非法返回 None
    - 判断类函数（如 is_mobile）：返回 bool
    - 正则全部预编译，避免重复编译开销
"""

import re


# ============================================================
# 预编译正则
# ============================================================
_PATTERN_DATE    = re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$")
_PATTERN_CALL    = re.compile(r'^1[3-9]\d{9}$')
_PATTERN_UUID    = re.compile(
    r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$'
)
_PATTERN_MD5     = re.compile(r'^[0-9a-fA-F]{32}$')
_PATTERN_CODE_6  = re.compile(r'^\d{6}$')
_PATTERN_CODE_64 = re.compile(r'^[0-9a-fA-F]{64}$')

# 移动端 UA 特征
_LONG_MOBILE_REGEX = re.compile(
    r'googlebot-mobile|android|avantgo|blackberry|blazer|elaine|hiptop|ip(hone|od)|kindle|midp|mmp'
    r'|mobile|o2|opera mini|palm( os)?|pda|plucker|pocket|psp|smartphone|symbian|treo|up\.(browser|link)'
    r'|vodafone|wap|windows ce; (iemobile|ppc)|xiino|maemo|fennec',
    re.IGNORECASE,
)
_SHORT_MOBILE_REGEX = re.compile(
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
    re.IGNORECASE,
)


# ============================================================
# 校验类：合法返回原值，非法返回 None
# ============================================================

def is_date(code):
    """校验 YYYY-MM-DD HH:MM:SS 格式（如 2025-01-01 00:00:00）"""
    if not isinstance(code, str):
        return None
    return code if _PATTERN_DATE.match(code) else None


def is_call(code):
    """校验中国大陆手机号（1[3-9] 开头 11 位）"""
    if not isinstance(code, str):
        return None
    return code if _PATTERN_CALL.match(code) else None


def is_uuid(code):
    """校验 UUID（8-4-4-4-12）"""
    if not isinstance(code, str):
        return None
    return code if _PATTERN_UUID.match(code) else None


def is_md5(code):
    """校验 32 位十六进制（MD5 / 32 位 token）"""
    if not isinstance(code, str):
        return None
    return code if _PATTERN_MD5.match(code) else None


def is_code(code):
    """校验 6 位纯数字（短信验证码）"""
    if not isinstance(code, str):
        return None
    return code if _PATTERN_CODE_6.match(code) else None


def is_token_64(code):
    """校验 64 位十六进制（微信 wx.login 凭证）"""
    if not isinstance(code, str):
        return None
    return code if _PATTERN_CODE_64.match(code) else None


# 向后兼容（旧代码用的是 is_code_wx）
is_code_wx = is_token_64


# ============================================================
# 判断类：返回 bool
# ============================================================

def is_mobile(ua):
    """
    判断 User-Agent 是否来自移动端

    :param ua: HTTP_USER_AGENT 字符串，可为 None
    :return: True 移动端 / False PC 或无法判断
    """
    if not ua or not isinstance(ua, str):
        return False
    if _LONG_MOBILE_REGEX.search(ua):
        return True
    return bool(_SHORT_MOBILE_REGEX.search(ua[:4]))