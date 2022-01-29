import locale
import pkg_resources
import gettext

def get_default_locale_encoding():
    default, encoding = locale.getdefaultlocale()
    return default, encoding

def get_default_locale_message_handler():
    default, encoding = get_default_locale_encoding()
    localesdir = pkg_resources.resource_filename('inclusivewriting', 'locales')
    lang = gettext.translation('inclusivewriting', localedir=localesdir, languages=[default])
    lang.install()
    return lang.gettext
