# coding=utf8
"""
lookup.py - LDAP inteface module by EAS at RedHat
Licensed under the Eiffel Forum License 2.

This module relies on LDAP, python-ldap
"""
from __future__ import unicode_literals

import ldap
import sys
import os.path
import sopel.module
from sopel.config.types import StaticSection, ValidatedAttribute

class LDAPSection(StaticSection):
    base_dn = ValidatedAttribute('base_dn', str)

def configure(config):
    config.define_section('ldap',LDAPSection, valude=False)
    config.ldap.configure_setting('base_dn',"What is your base dn?")


def setup(bot):
    bot.config.define_section('ldap',LDAPSection)

# ldap search command
@sopel.module.commands('search', 'lookup')
def search(bot, trigger):
    bot.say("I am configured to use:" + bot.config.ldap.base_dn)
    bot.reply('Why do you want to know about ' + trigger.group(2) + "?")
