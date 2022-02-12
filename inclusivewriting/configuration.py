#
# SPDX-FileCopyrightText: 2022 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

"""
Functions to handle suggestions for different languages
"""

import json

import pkg_resources

from inclusivewriting.file_utils import read_file


def get_all_language_resource_config_file(config_file: str = None):
    """
    Get the resource files for all languages
    """
    # File containing links to resources
    if config_file is None or config_file == "":
        all_language_resource_file = pkg_resources.resource_filename(
            "inclusivewriting", "configuration.json"
        )
        return all_language_resource_file
    return config_file


def get_all_language_resources(config_file: str = None):
    """
     This method can be used to obtain all the language resources configured in the configuration
     file. If the configuration file is not specified, the default configuration file is used

    Parameters
    ----------
      config_file : str
        This parameter contains the file path of a congiguration file

    Returns
    -------
      resources
        language resources

    """
    config_file = get_all_language_resource_config_file(config_file)
    resources = {}
    resource_file_string = read_file(config_file)
    resources_parsed_data = json.loads(resource_file_string)
    for key, value in resources_parsed_data.items():
        resources[key] = value
    return resources
