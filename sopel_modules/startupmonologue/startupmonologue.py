# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

from sopel import module
from sopel.tools import stderr

import sopel_modules.osd

import time

try:
    from sopel_modules.botevents.botevents import *
    botevents_installed = True
except ImportError:
    botevents_installed = False

try:
    from sopel_modules.commandsquery.commandsquery import *
    commandsquery_installed = True
except ImportError:
    commandsquery_installed = False


def configure(config):
    pass


def setup(bot):
    pass


@module.event('001')
@module.rule('.*')
@module.thread(True)
def bot_startup_monologue(bot, trigger):

    if botevents_installed:
        while 'Sopel-BotEvents' not in bot.memory:
            pass
        while not check_bot_events(bot, ["connected"]):
            pass
    else:
        while not len(bot.channels.keys()) > 0:
            pass
        time.sleep(1)

    # Startup
    stderr("[Sopel-startupmonologue] " + bot.nick + " is now starting. Please wait while I load my configuration.")
    bot.osd(" is now starting. Please wait while I load my configuration.", bot.channels.keys(), 'ACTION')

    startupcomplete = [bot.nick + " startup complete"]
    if commandsquery_installed:
        if botevents_installed:
            while not check_bot_events(bot, ["Sopel-CommandsQuery"]):
                pass
        else:
            while 'Sopel-CommandsQuery' not in bot.memory:
                pass

        availablecomsnum, availablecomsfiles = 0, 0

        for commandstype in bot.memory['Sopel-CommandsQuery'].keys():
            if commandstype.endswith("_count"):
                availablecomsfiles += bot.memory['Sopel-CommandsQuery'][commandstype]
            else:
                availablecomsnum += len(bot.memory['Sopel-CommandsQuery'][commandstype].keys())

        startupcomplete.append("There are " + str(availablecomsnum) + " commands available in " + str(availablecomsfiles) + " files.")
        stderr("[Sopel-startupmonologue] " + "There are " + str(availablecomsnum) + " commands available in " + str(availablecomsfiles) + " files.")

    if botevents_installed:
        while not check_bot_events(bot, ["startup_complete"]):
            pass

    # Announce to chan, then handle some closing stuff
    bot.osd(startupcomplete, bot.channels.keys())

    if botevents_installed:
        startup_bot_event(bot, "Sopel-StartupMonologue")
    stderr("[Sopel-startupmonologue] " + bot.nick + " startup complete")
