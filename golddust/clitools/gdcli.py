#  Copyright 2015-2016 John "LuaMilkshake" Marion
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""GoldDust CLI Utility Module

This module contains helper functions for the GoldDust CLI tools."""


import sys


def ask_confirm(question, default_yes):
    """Ask the user a yes/no question.

    This only looks at the first character of the response, and
    is case-insensitive.

    Takes:
        question (str): The question to ask the user. Include a
                        question mark.
        default_yes (bool): If the user just hits enter, should
                            we assume 'yes'?

    Returns a bool of True for a 'yes' response, False for 'no'.
    """
    while True:
        sys.stdout.write("{} [{}] ".format(question,
                                           "Y/n" if default_yes else "y/N"))
        sys.stdout.flush()
        response = sys.stdin.readline()
        if response[0].lower() == 'y':
            return True
        elif response[0].lower() == 'n':
            return False
        elif len(response) == 1:
            return default_yes


def ask_string(question, default):
    """Ask the user for a string.

    Takes:
        question (str): The question to ask the user. Include a
                        question mark.
        default (str): If the user just hits enter, this is returned.

    Returns what the user responded with as a str. If the user enters
    nothing, will return the default.
    """
    sys.stdout.write("{} [{}] ".format(question, default))
    sys.stdout.flush()

    response = sys.stdin.readline()[:-1]

    if len(response) == 0:
        return default

    return response
