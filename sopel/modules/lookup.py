# coding=utf8
"""
lookup.py - LDAP inteface module by EAS at RedHat IT
Licensed under the Eiffel Forum License 2.

This module relies on LDAP, python-ldap
"""
from __future__ import unicode_literals

import ldap
import ldif
import sys
import os.path
import sopel.module
from sopel.config.types import StaticSection, ValidatedAttribute

class LDAPSection(StaticSection):
    base_dn = ValidatedAttribute('base_dn', str)
    ldap_host = ValidatedAttribute('host', str)
    ldap_search_attrs = ValidatedAttribute('search_attrs', str)
    dict_path = ValidatedAttribute('dict_path',str)
    dict  = {}

def configure(config):
    config.define_section('ldap',LDAPSection, valude=False)
    config.ldap.configure_setting('base_dn',"What is your base dn?")
    config.ldap.configure_setting('ldap_host',"Which LDAP host should I communicate with?")
    config.ldap.configure_setting('search_attrs',"What LDAP attributes should I use to search?")
    config.ldap.configure_setting('dict_path', "Where is the attribute dictionary for LDAP translation?")

def setup(bot):
    bot.config.define_section('ldap',LDAPSection)
    bot.config.ldap.dict = {}
    # open( bot.config.ldap.dict_path, "r" )

# ldap search command
@sopel.module.require_privmsg
@sopel.module.commands('search', 'lookup')
def search(bot, trigger):
    bot.say("I am configured to use:" + bot.config.ldap.base_dn)
    bot.reply('Why do you want to know about ' + trigger.group(2) + "?")
    command_args = trigger.group(2).split(" ")
    ldif_writer = ldif.LDIFWriter(sys.stdout)
    if len(command_args) > 1:
        if str(command_args[1]) == u'*':
            result = _ldap_do_search(bot,command_args[0])
            for dn,entry in result:
                bot.say("In dn: " + str(dn))
                for key in entry.keys():
                    bot.say(str(key) + ": " + str(entry.get(key,"Not set.")) )
        else:
            result = _ldap_do_search(bot,command_args[0],[str(command_args[1])])
            for dn,entry in result:
                bot.say(str(entry[str(command_args[1])][0]))
    else:
        result = _ldap_do_search(bot,command_args[0])
        for val in result[0][1].keys():
            bot.say(val)

# helper method
def _ldap_do_search(bot,query_string,specific_attr=None):
    #filter = '(uid=%s)' % str(sys.argv[1])
    attrs = bot.config.ldap.ldap_search_attrs.split(',')
    filter = '(|' + ''.join(map( lambda x : ( "(" + str(x) + "=%s" + ")"), attrs )) + ")"
    filter = filter % tuple([query_string] * len(attrs))
    l = ldap.initialize(bot.config.ldap.ldap_host)
    result = l.search_s(bot.config.ldap.base_dn,ldap.SCOPE_SUBTREE,filter,specific_attr)
    return result
