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
# Amxxx Channel settings and commands
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
import sublime_plugin

from channel_manager.channel_utilities import clean_urljoin
from channel_manager.channel_utilities import load_data_file
from channel_manager.channel_utilities import get_main_directory
from channel_manager.channel_utilities import get_dictionary_key

from channel_manager import channel_installer
from channel_manager import channel_uninstaller

try:
    from package_control.package_manager import clear_cache

except ImportError:
    pass

from channel_manager.channel_manager import main as manager_main
from channel_manager.submodules_manager import main as submodules_main
from channel_manager.copy_default_package import main as copy_default_main


# Infer the correct package name and current directory absolute path
CURRENT_DIRECTORY    = os.path.dirname( os.path.realpath( __file__ ) )
CURRENT_PACKAGE_NAME = os.path.basename( CURRENT_DIRECTORY ).rsplit('.', 1)[0]

# Hold all the information for this channel, which will be used by the `ChannelManager` to install
# this channel
g_channel_settings = {}


def plugin_loaded():
    """
        We can only load the information when the Sublime Text API is available due the use of the
        get_main_directory() which requires it.
    """
    global g_channel_settings

    # The folder where the directory where the Sublime Text `Packages` (loose packages) folder is on
    CHANNEL_MAIN_DIRECTORY = get_main_directory( CURRENT_DIRECTORY )

    # The folder where the User settings are on
    USER_FOLDER_PATH = os.path.join( CHANNEL_MAIN_DIRECTORY, "Packages", "User" )

    # The temporary folder to download the main repository when installing the development version
    g_channel_settings['TEMPORARY_FOLDER_TO_USE'] = "__channel_temporary_directory"
    g_channel_settings['CHANNEL_PACKAGE_NAME']    = CURRENT_PACKAGE_NAME

    # Where to save the settings for channel after it is installed on the user's machine
    g_channel_settings['USER_FOLDER_PATH']              = USER_FOLDER_PATH
    g_channel_settings['CHANNEL_INSTALLATION_SETTINGS'] = \
            os.path.join( USER_FOLDER_PATH,CURRENT_PACKAGE_NAME + ".sublime-settings" )


    # The local path to the files, used to save the generated channels. Valid URLs to the files, to use
    # when installing the stable version of the channel See also:
    # https://packagecontrol.io/docs/channels_and_repositories

    # The default Package Control channel
    g_channel_settings['DEFAULT_CHANNEL_URL'] = "https://packagecontrol.io/channel_v3.json"

    # The URL of the directory where the files `channel.json` and `repository.json` are hosted
    CHANNEL_RAW_URL = "https://raw.githubusercontent.com/evandrocoan/SublimeStudioChannel/master/"

    # The URL to the main A direct URL/Path to the repository where there is the `.gitmodules` file
    # listing all the channel packages to use when generating Studio Channel files.
    g_channel_settings['CHANNEL_ROOT_URL']       = "https://github.com/evandrocoan/SublimeTextAmxxSimpleIDE"
    g_channel_settings['CHANNEL_ROOT_DIRECTORY'] = CHANNEL_MAIN_DIRECTORY

    # The file path to the Channel File `channel.json` to use when installing the development version
    g_channel_settings['CHANNEL_FILE_URL']  = clean_urljoin( CHANNEL_RAW_URL, "channel.json" )
    g_channel_settings['CHANNEL_FILE_PATH'] = os.path.join( CURRENT_DIRECTORY, "channel.json" )

    # A direct URL/Path to the Repository File `repository.json` to use when installing the
    # stable/development version
    g_channel_settings['CHANNEL_REPOSITORY_URL']  = clean_urljoin( CHANNEL_RAW_URL, "repository.json" )
    g_channel_settings['CHANNEL_REPOSITORY_FILE'] = os.path.join( CURRENT_DIRECTORY, "repository.json" )

    # A direct URL/Path to the `settings.json` to use when installing the stable/development version
    g_channel_settings['CHANNEL_SETTINGS_URL']  = clean_urljoin( CHANNEL_RAW_URL, "settings.json" )
    g_channel_settings['CHANNEL_SETTINGS_PATH'] = os.path.join( CURRENT_DIRECTORY, "settings.json" )


    # You can specify for some packages to be popped out from the list and being installed by
    # last/first in the following order presented.
    g_channel_settings['PACKAGES_TO_INSTALL_FIRST'] = \
    [
        "Notepad++ Color Scheme",
    ]

    g_channel_settings['PACKAGES_TO_INSTALL_LAST'] = \
    [
        "Default",
        "PackagesManager",
    ]

    # Packages which are not allowed to be selected by the user while choosing the packages to not
    # be installed. Useful for packages which are required for the channel maintainability.
    g_channel_settings['FORBIDDEN_PACKAGES'] = \
    [
        "PackagesManager",
        "ChannelManager",
        "Notepad++ Color Scheme",
        "OverrideUnpackedPackages",
        "amxmodx",
        "AmxxPawn",
    ]

    # The default user preferences file
    g_channel_settings['USER_SETTINGS_FILE'] = "Preferences.sublime-settings"

    # Packages which you do want to install on the Stable or Development version, when reading
    # the `.gitmodules` packages list.
    g_channel_settings['PACKAGES_TO_NOT_INSTALL_STABLE'] = \
    [
        "User",
        "PackagesManager",
    ]

    g_channel_settings['PACKAGES_TO_NOT_INSTALL_DEVELOPMENT'] = \
    [
    ]

    # The files of the `Default.sublime-package` you are installing
    g_channel_settings['DEFAULT_PACKAGES_FILES'] = \
    [
        ".gitignore",
        ".no-sublime-package",
        "Context.sublime-menu",
        "Default (Linux).sublime-keymap",
        "Default (Linux).sublime-mousemap",
        "Default (OSX).sublime-keymap",
        "Default (OSX).sublime-mousemap",
        "Default (Windows).sublime-keymap",
        "Default (Windows).sublime-mousemap",
        "Distraction Free.sublime-settings",
        "Find Results.hidden-tmLanguage",
        "install_package_control.py",
        "package-metadata.json",
        "Preferences (Linux).sublime-settings",
        "Preferences (OSX).sublime-settings",
        "Preferences (Windows).sublime-settings",
        "Preferences.sublime-settings",
        "README.md",
        "Sublime Text Settings.sublime-settings",
        "Tab Context.sublime-menu",
        "transpose.py",
    ]


def is_channel_installed():
    """
        Returns True if the channel is installed, i.e., there are packages added to the
        `packages_to_uninstall` list.
    """

    # Only attempt to check it, if the settings are loaded
    if len( g_channel_settings ) > 0:
        channelSettingsPath = g_channel_settings['CHANNEL_INSTALLATION_SETTINGS']

        if os.path.exists( channelSettingsPath ):
            settings = load_data_file( channelSettingsPath )
            return len( get_dictionary_key( settings, "packages_to_uninstall", [] ) ) > 0

    return False


def add_channel():
    """
        Add your channel URL to the Package Control channel list and cleans the cached channels.
    """
    package_control = "Package Control.sublime-settings"
    channel_url     = g_channel_settings['CHANNEL_FILE_URL']

    package_control_settings = sublime.load_settings( package_control )
    channels                 = package_control_settings.get( "channels", [] )

    if channel_url in channels:
        channels.remove( channel_url )

    channels.append( channel_url )
    package_control_settings.set( "channels", channels )

    print( "Adding %s channel to %s: %s" % ( CURRENT_PACKAGE_NAME, package_control, str( channels ) ) )
    sublime.save_settings( package_control )

    clear_cache()


class AmxxChannelRunUninstallation( sublime_plugin.ApplicationCommand ):

    def run(self):
        sublime.active_window().run_command( "show_panel", {"panel": "console", "toggle": False} )
        channel_uninstaller.main( g_channel_settings )


class AmxxChannelRunInstallation( sublime_plugin.ApplicationCommand ):

    def run(self, version="stable"):
        """
            Call the ChannelManager installer to install all the channel packages.

            @param version   Either the value "stable" or "development" to install the
                             Development or Stable Version of the channel.
        """
        add_channel()
        g_channel_settings['INSTALLATION_TYPE'] = version

        sublime.active_window().run_command( "show_panel", {"panel": "console", "toggle": False} )
        channel_installer.main( g_channel_settings )

    def is_enabled(self):
        return not is_channel_installed()


class AmxxChannelGenerateChannelFile( sublime_plugin.ApplicationCommand ):

    def run(self, create_tags, command="all"):
        sublime.active_window().run_command( "show_panel", {"panel": "console", "toggle": False} )
        manager_main( g_channel_settings, create_tags, command )

    def is_enabled(self):
        return is_channel_installed()


class AmxxChannelRun( sublime_plugin.ApplicationCommand ):

    def run(self, run):
        sublime.active_window().run_command( "show_panel", {"panel": "console", "toggle": False} )
        submodules_main( run )

    def is_enabled(self):
        return is_channel_installed()


class AmxxChannelUpdateDefaultPackages( sublime_plugin.ApplicationCommand ):

    def run(self):
        sublime.active_window().run_command( "show_panel", {"panel": "console", "toggle": False} )
        copy_default_main( g_channel_settings['DEFAULT_PACKAGES_FILES'], True )

    def is_enabled(self):
        return is_channel_installed()


