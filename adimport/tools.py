# -*- coding: utf-8 -*-
import re
import unidecode
from phpserialize import unserialize


# public symbols
__all__ = ["create_url", "convert_param"]


def create_url(value):
    return re.sub("[^0-9a-zA-Z_]", "", unidecode.unidecode(value.strip().replace(" ", "_")))


def convert_param(value):
    result = {}
    try:
        a = unserialize(value.encode('utf-8'))
    except ValueError:
        return False

    for key, value in a.items():
        if not key.startswith('Unit=') and _clean_text(key) and _clean_text(value):
            if not _clean_text(value.keys()[0]):
                continue
            result[_clean_text(key)] = _clean_text(value.keys()[0]) if len(value.keys()) == 1 else\
                [_clean_text(p) for p in value.keys()]
    return result


def _clean_text(value):
    _value = str(value).decode(encoding='utf-8')
    return re.sub(u"[^а-яА-ЯёЁйЙ\- ]+", "", _value.strip().replace("  ", " ").lower())


def clean_text(value):
    return value.strip().replace("  ", " ").lower()