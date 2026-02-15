#
# SPDX-FileCopyrightText: 2022 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

"""Functions to handle locales"""

import locale
import gettext
import pkg_resources


def _get_locale_encoding() -> str:
    """
    Return locale encoding in a Python-version-compatible way.
    """
    if hasattr(locale, "getencoding"):
        return locale.getencoding()
    return locale.getpreferredencoding(False)


def get_default_locale_encoding():
    """
    Get default locale information
    """
    default_locale, _ = locale.getlocale()
    encoding = _get_locale_encoding()

    if default_locale is None or default_locale == "":
        default_locale = "en_US"
    if encoding is None or encoding == "":
        encoding = "utf-8"
    return default_locale, encoding


def get_default_locale_message_handler():
    """
    Get default locale information and the locale handler
    """
    default, _ = get_default_locale_encoding()
    localesdir = pkg_resources.resource_filename("inclusivewriting", "locales")
    lang = gettext.translation(
        "inclusivewriting", localedir=localesdir, languages=[default], fallback=True
    )
    lang.install()
    return lang.gettext
