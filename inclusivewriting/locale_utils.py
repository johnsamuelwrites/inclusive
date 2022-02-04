#
# SPDX-FileCopyrightText: 2022 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

"""Functions to handle locales"""

import locale
import gettext
import pkg_resources


def get_default_locale_encoding():
    """
    Get default locale information
    """
    default, encoding = locale.getdefaultlocale()
    return default, encoding


def get_default_locale_message_handler():
    """
    Get default locale information and the locale handler
    """
    default, _ = get_default_locale_encoding()
    localesdir = pkg_resources.resource_filename("inclusivewriting", "locales")
    lang = gettext.translation(
        "inclusivewriting", localedir=localesdir, languages=[default]
    )
    lang.install()
    return lang.gettext
