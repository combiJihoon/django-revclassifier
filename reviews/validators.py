from django.core.exceptions import ValidationError


def validate_address1(value):
    if "시" not in value:
        raise ValidationError("~'시'로 입력하세요", code='invalid')


def validate_address2(value):
    if "구" not in value:
        raise ValidationError("~'구'로 입력하세요", code='invalid')


def validate_address3(value):
    if "동" not in value:
        raise ValidationError("~'동'으로 입력하세요", code='invalid')


def validate_symbols(value):
    if ("@" in value) or ("#" in value):
        raise ValidationError("@와 #은 포함될 수 없습니다.", code='symbol-err')
