from django.core.exceptions import ValidationError


def validate_address(value):
    if ("동" not in value) or ("읍" not in value) or ("면" not in value):
        raise ValidationError("주소의 동/읍/면 중 하나가 꼭 포함되어야 합니다.", code='invalid')


def validate_symbols(value):
    if ("@" in value) or ("#" in value):
        raise ValidationError("@와 #은 포함될 수 없습니다.", code='symbol-err')
