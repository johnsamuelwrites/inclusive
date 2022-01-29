import locale
import gettext

def get_default_locale_encoding():
    default, encoding = locale.getdefaultlocale()
    return default, encoding

def get_default_locale_message_handler():
    default, encoding = get_default_locale_encoding()
    lang = gettext.translation('inclusivewriting', localedir='locales', languages=[default])
    lang.install()
    return lang.gettext
