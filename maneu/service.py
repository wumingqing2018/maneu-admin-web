from maneu.models import ManeuAdmin
from maneu.models import ManeuGuess
from maneu.models import ManeuOrderV2
from maneu.models import ManeuStore
from maneu.models import ManeuSubjectiveRefraction
from maneu.models import ManeuVisionSolutions


def find_user_username(username=''):
    """
    通过username查找用户
    """
    return ManeuAdmin.objects.filter(username=username).first()


def find_order_phone(phone=''):
    try:
        return ManeuOrderV2.objects.filter(phone=phone).order_by('-time').first()
    except BaseException as msg:
        print(msg)
        return msg


def find_users_id(id=''):
    try:
        return ManeuAdmin.objects.filter(id=id).first()
    except BaseException as msg:
        print(msg)
        return None


def find_guess_id(id=''):
    try:
        return ManeuGuess.objects.filter(id=id).first()
    except BaseException as msg:
        print(msg)
        return None


def find_guess_phone(phone=''):
    try:
        return ManeuGuess.objects.filter(phone=phone).first()
    except BaseException as msg:
        print(msg)
        return None


def find_store_id(id=''):
    try:
        return ManeuStore.objects.filter(id=id).first()
    except BaseException as msg:
        print(msg)
        return None


def find_ManeuVisionSolutions_id(id=''):
    try:
        return ManeuVisionSolutions.objects.filter(id=id).first()
    except BaseException as msg:
        print(msg)
        return None


def find_subjectiverefraction_id(id=''):
    try:
        return ManeuSubjectiveRefraction.objects.filter(id=id).first()
    except BaseException as msg:
        print(msg)
        return None
