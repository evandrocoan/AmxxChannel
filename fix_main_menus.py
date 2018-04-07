

import sublime
import sublime_plugin

import os

try:
    from OverrideUnpackedPackages.override_unpacked_packages import add_folder_to_processing_queue

except ImportError as error:
    print( "Error: Could not import the package `OverrideUnpackedPackages`, please install the package. " + str( error ) )

    def add_folder_to_processing_queue(*args):
        print( "fix_main_menus, add_folder_to_processing_queue could not add the following arguments..." )

        for arg in args:
            print( str( arg ) )

"""

# Fix Main Menus

Delete the default main menu for the `Amxmodx` package, because when it updates
we would get duplicated menu entries as the default menu for that package is set
on the `User/Main.sublime-menu` file.


# Diff Configurations

This folder has the purpose to disable the default Diff package Context Menus.
As they were moved into the Custom Settings package.

"""

PACKAGE_ROOT_DIRECTORY = os.path.dirname( os.path.realpath( __file__ ) )


def plugin_loaded():
    sublime.set_timeout( add_files_to_copy_list, 2000 )


def add_files_to_copy_list():
    from .commands import is_channel_installed
    from .commands import get_channel_file_setting

    if is_channel_installed() \
            and get_channel_file_setting( "is_channel_installed", True ):

        add_folder_to_processing_queue( PACKAGE_ROOT_DIRECTORY, os.path.join( "User", "Amxx" ), 100 )

