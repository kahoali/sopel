# coding=utf8
"""
lookup.py - LDAP inteface module by EAS at RedHat
Licensed under the Eiffel Forum License 2.

This module relies on LDAP, python-ldap
"""
from __future__ import unicode_literals

import sopel.module
import ldap
import sys


def configure(config):
    pass


def setup(bot):
    pass

# ldap search command
@sopel.module.commands('search', 'lookup')
def search(bot, trigger):
    bot.reply('Why do you want to know about ' + trigger.group(2) + "?")
