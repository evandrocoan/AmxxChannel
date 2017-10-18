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

from ChannelManager.channel_utilities import clean_urljoin
from ChannelManager.channel_utilities import get_main_directory

from ChannelManager import channel_uninstaller
from ChannelManager import channel_installer

try:
    from package_control.package_manager import clear_cache

except ImportError:
    pass

from ChannelManager.channel_manager import main as manager_main
from ChannelManager.submodules_manager import main as submodules_main
from ChannelManager.copy_default_package import main as default_main


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
    STUDIO_MAIN_DIRECTORY = get_main_directory( CURRENT_DIRECTORY )

    # The folder where the User settings are on
    USER_FOLDER_PATH = os.path.join( STUDIO_MAIN_DIRECTORY, "Packages", "User" )

    # The temporary folder to download the main repository when installing the development version
    g_channel_settings['TEMPORARY_FOLDER_TO_USE'] = "__channel_studio_temp"
    g_channel_settings['STUDIO_PACKAGE_NAME']     = CURRENT_PACKAGE_NAME

    # Where to save the settings for channel after it is installed on the user's machine
    g_channel_settings['USER_FOLDER_PATH']             = USER_FOLDER_PATH
    g_channel_settings['STUDIO_INSTALLATION_SETTINGS'] = \
            os.path.join( USER_FOLDER_PATH,CURRENT_PACKAGE_NAME + ".sublime-settings" )


    # The local path to the files, used to save the generated channels. Valid URLs to the files, to use
    # when installing the stable version of the channel See also:
    # https://packagecontrol.io/docs/channels_and_repositories

    # The default Package Control channel
    g_channel_settings['DEFAULT_CHANNEL_URL'] = "https://packagecontrol.io/channel_v3.json"

    # The URL of the folder where the channel files are hosted
    STUDIO_RAW_URL = "https://raw.githubusercontent.com/your_user_name/MyBrandNewChannel/master/"

    # The URL to the main A direct URL/Path to the repository where there is the `.gitmodules` file
    # listing all the channel packages to use when generating Studio Channel files.
    g_channel_settings['STUDIO_MAIN_URL']       = "https://github.com/your_user_name/MyParentRepository"
    g_channel_settings['STUDIO_MAIN_DIRECTORY'] = STUDIO_MAIN_DIRECTORY

    # The file path to the Channel File `channel.json` to use when installing the development version
    g_channel_settings['STUDIO_CHANNEL_URL']  = clean_urljoin( STUDIO_RAW_URL, "channel.json" )
    g_channel_settings['STUDIO_CHANNEL_FILE'] = os.path.join( CURRENT_DIRECTORY, "channel.json" )

    # A direct URL/Path to the Repository File `repository.json` to use when installing the
    # stable/development version
    g_channel_settings['STUDIO_REPOSITORY_URL']  = clean_urljoin( STUDIO_RAW_URL, "repository.json" )
    g_channel_settings['STUDIO_REPOSITORY_FILE'] = os.path.join( CURRENT_DIRECTORY, "repository.json" )

    # A direct URL/Path to the `settings.json` to use when installing the stable/development version
    g_channel_settings['STUDIO_SETTINGS_URL']  = clean_urljoin( STUDIO_RAW_URL, "settings.json" )
    g_channel_settings['STUDIO_SETTINGS_PATH'] = os.path.join( CURRENT_DIRECTORY, "settings.json" )


    # You can specify for some packages to be popped out from the list and being installed by
    # last in the following order presented.
    g_channel_settings['PACKAGES_TO_INSTALL_LAST'] = \
    [
        "My Package Penultimate Package",
        "My Package Penult Package",
        "My Package Last Package",
    ]

    # The default user preferences file
    g_channel_settings['USER_SETTINGS_FILE'] = "Preferences.sublime-settings"

    # Do not try to install this own package and the Package Control, as they are currently running
    g_channel_settings['PACKAGES_TO_NOT_INSTALL'] = [ "Package Control", CURRENT_PACKAGE_NAME ]

    # The files of the `Default.sublime-package` you are installed
    g_channel_settings['DEFAULT_PACKAGES_FILES'] = \
    [
        "Tab Context.sublime-menu",
        "Context.sublime-menu",
    ]


def add_studio_channel():
    """
        Add your channel URL to the Package Control channel list and cleans the cached channels.
    """
    package_control    = "Package Control.sublime-settings"
    studio_channel_url = g_channel_settings['STUDIO_CHANNEL_URL']

    package_control_settings = sublime.load_settings( package_control )
    channels                 = package_control_settings.get( "channels", [] )

    if studio_channel_url in channels:
        channels.remove( studio_channel_url )

    channels.insert( 0, studio_channel_url )
    package_control_settings.set( "channels", channels )

    print( "Adding %s channel to %s: %s" % ( CURRENT_PACKAGE_NAME, package_control, str( channels ) ) )
    sublime.save_settings( package_control )

    clear_cache()


class MyBrandNewChannelRunInstallation( sublime_plugin.ApplicationCommand ):

    def run(self, version="stable"):
        """
            Call the ChannelManager installer to install all the channel packages.

            @param version   Either the value "stable" or "development" to install the
                             Development or Stable Version of the channel.
        """
        add_studio_channel()
        g_channel_settings['INSTALLATION_TYPE'] = version

        sublime.active_window().run_command( "show_panel", {"panel": "console", "toggle": False} )
        channel_installer.main( g_channel_settings )


class MyBrandNewChannelRunUninstallation( sublime_plugin.ApplicationCommand ):

    def run(self):
        sublime.active_window().run_command( "show_panel", {"panel": "console", "toggle": False} )
        channel_uninstaller.main( g_channel_settings )


class MyBrandNewChannelGenerateChannelFile( sublime_plugin.ApplicationCommand ):

    def run(self):
        sublime.active_window().run_command( "show_panel", {"panel": "console", "toggle": False} )
        manager_main( g_channel_settings )


class MyBrandNewChannelRun( sublime_plugin.ApplicationCommand ):

    def run(self, run):
        sublime.active_window().run_command( "show_panel", {"panel": "console", "toggle": False} )
        submodules_main( run )


class MyBrandNewChannelUpdateDefaultPackages( sublime_plugin.ApplicationCommand ):

    def run(self):
        sublime.active_window().run_command( "show_panel", {"panel": "console", "toggle": False} )
        default_main( g_channel_settings['DEFAULT_PACKAGES_FILES'], True )


