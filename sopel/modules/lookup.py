# coding=utf8
"""
lookup.py - LDAP inteface module by EAS at RedHat IT
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
    ldap_host = ValidatedAttribute('host', str)
    ldap_search_attrs = ValidatedAttribute('search_attrs', str)
    dict_path = ValidatedAttribute('dict_path',str)
    commands  = {}

def configure(config):
    config.define_section('ldap',LDAPSection, valude=False)
    config.ldap.configure_setting('base_dn',"What is your base dn?")
    config.ldap.configure_setting('ldap_host',"Which LDAP host should I communicate with?")
    config.ldap.configure_setting('search_attrs',"What LDAP attributes should I use to search?")
    config.ldap.configure_setting('dict_path', "Where is the attribute dictionary for LDAP translation?")

def setup(bot):
    bot.config.define_section('ldap',LDAPSection)
    bot.config.ldap.commands = {}
    # Load in possible commands from configuration file
    with open( bot.config.ldap.dict_path, "r" ) as f:
        content = f.readlines()

        for line in content:
            parts = line.strip("\n").split("=")
            keys = parts[1].split(",")
            value = parts[0]

            for k in keys:
                bot.config.ldap.commands[k] = value

# ldap search command
@sopel.module.require_privmsg
@sopel.module.commands('search', 'lookup')
def search(bot, trigger):
    bot.say("I am configured to use:" + bot.config.ldap.base_dn)
    bot.reply('Why do you want to know about ' + trigger.group(2) + "?")

    _ldap_get_all_attrs(bot,trigger.group(2))

# helper method
def _ldap_get_all_attrs(bot,query_string,specific_attr=None):
    #filter = '(uid=%s)' % str(sys.argv[1])
    attrs = bot.config.ldap.ldap_search_attrs.split(',')
    filter = '(|' + ''.join(map( lambda x : ( "(" + str(x) + "=%s" + ")"), attrs )) + ")"
    filter = filter % tuple([query_string] * len(attrs))
    l = ldap.initialize(bot.config.ldap.ldap_host)
    result = l.search_s(bot.config.ldap.base_dn,ldap.SCOPE_SUBTREE,filter,specific_attr)
    for val in result[0][1].keys():
        bot.say(val)

