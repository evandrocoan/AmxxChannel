

import sublime
import sublime_plugin

import os

try:
    from OverrideUnpackedPackages.override_unpacked_packages import add_folder_to_processing_queue

except ImportError as error:
    print( "Error: Could not import the package `OverrideUnpackedPackages`, please install the package." + str( error ) )

"""

# Fix Main Menus

Delete the default main menu for the `amxmodx` package, because when it updates
we would get duplicated menu entries as the default menu for that package is set
on the `User/Main.sublime-menu` file.


# Diff Configurations

This folder has the purpose to disable the default Diff package Context Menus.
As they were moved into the Custom Settings package.

"""

CURRENT_DIRECTORY = os.path.dirname( os.path.realpath( __file__ ) )


def plugin_loaded():
    add_files_to_copy_list()


def add_files_to_copy_list():
    add_folder_to_processing_queue( CURRENT_DIRECTORY, "Default", 100 )


