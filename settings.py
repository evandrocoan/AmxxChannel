#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# These lines allow to use UTF-8 encoding and run this file with `./update.py`, instead of `python update.py`
# https://stackoverflow.com/questions/7670303/purpose-of-usr-bin-python3
# https://stackoverflow.com/questions/728891/correct-way-to-define-python-source-code-encoding
#
#

#
# Licensing
#
# Amxx Channel Settings, all the settings required by this channel
# Copyright (C) 2017 Evandro Coan <https://github.com/evandrocoan>
#
#  This program is free software; you can redistribute it and/or modify it
#  under the terms of the GNU General Public License as published by the
#  Free Software Foundation; either version 3 of the License, or ( at
#  your option ) any later version.
#
#  This program is distributed in the hope that it will be useful, but
#  WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#  General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import os
import sublime

from channel_manager.channel_utilities import clean_urljoin
from channel_manager.channel_utilities import run_channel_setup

CURRENT_PACKAGE_ROOT_DIRECTORY = os.path.dirname( os.path.realpath( __file__ ) ).replace( ".sublime-package", "" )
CURRENT_PACKAGE_NAME           = os.path.basename( CURRENT_PACKAGE_ROOT_DIRECTORY )

def plugin_loaded():
    global g_channel_settings
    CHANNEL_RAW_URL = "https://raw.githubusercontent.com/evandrocoan/StudioChannel/master/"

    g_channel_settings = {}
    g_channel_settings['CHANNEL_ROOT_URL']    = "https://github.com/evandrocoan/SublimeTextAmxxSimpleIDE"
    g_channel_settings['DEFAULT_CHANNEL_URL'] = "https://packagecontrol.io/channel_v3.json"

    g_channel_settings['CHANNEL_FILE_URL']  = clean_urljoin( CHANNEL_RAW_URL, "channel.json" )
    g_channel_settings['CHANNEL_FILE_PATH'] = os.path.join( CURRENT_PACKAGE_ROOT_DIRECTORY, "channel.json" )

    g_channel_settings['CHANNEL_REPOSITORY_URL']  = clean_urljoin( CHANNEL_RAW_URL, "repository.json" )
    g_channel_settings['CHANNEL_REPOSITORY_FILE'] = os.path.join( CURRENT_PACKAGE_ROOT_DIRECTORY, "repository.json" )

    g_channel_settings['PACKAGES_TO_INSTALL_FIRST'] = \
    [
        "Notepad++ Color Scheme",
    ]

    g_channel_settings['PACKAGES_TO_INSTALL_LAST'] = \
    [
        "Default",
        "PackagesManager",
    ]

    g_channel_settings['FORBIDDEN_PACKAGES'] = \
    [
        "0_settings_loader",
        "PackagesManager",
        "ChannelManager",
        "Notepad++ Color Scheme",
        "OverrideUnpackedPackages",
        "amxmodx",
        "AmxxPawn",
    ]

    g_channel_settings['DEFAULT_PACKAGE_FILES'] = \
    [
        ".gitignore",
        ".no-sublime-package",
        "Context.sublime-menu",
        "Distraction Free.sublime-settings",
        "Find Results.hidden-tmLanguage",
        "Main.sublime-menu",
        "README.md",
        "Sublime Text Settings.sublime-settings",
        "Tab Context.sublime-menu",
        "install_package_control.py",
        "platform_edit_settings.py",
        "synced_side_bar_watcher.py",
        "transpose.py",
    ]

    g_channel_settings['PACKAGES_TO_NOT_INSTALL_STABLE'] = \
    [
        "User",
        "PackagesManager",
    ]

    g_channel_settings['PACKAGES_TO_NOT_INSTALL_DEVELOPMENT'] = \
    [
    ]

    g_channel_settings['PACKAGES_TO_INSTALL_EXCLUSIVELY'] = \
    [
        "ActiveViewJumpBack",
        "amxmodx",
        "AmxxChannel",
        "AmxxPawn",
        "ChannelManager",
        "ClearCursorsCarets",
        "Default",
        "DefaultSyntax",
        "Diff",
        "FixedSelectionsClear",
        "FixProjectSwitchRestartBug",
        "MoveText",
        "Notepad++ Color Scheme",
        "OverrideUnpackedPackages",
        "OverwriteCommitCompletion",
        "PackagesManager",
        "PowerCursors",
        "Side-by-Side Settings",
    ]

    g_channel_settings['PACKAGES_TO_IGNORE_ON_DEVELOPMENT'] = \
    [
    ]

    run_channel_setup( g_channel_settings, CURRENT_PACKAGE_NAME, CURRENT_PACKAGE_ROOT_DIRECTORY )

    # from channel_manager.channel_utilities import print_all_variables_for_debugging
    # print_all_variables_for_debugging
    # import sublime_plugin
    # sublime_plugin.reload_plugin( "channel_manager.channel_utilities" )

