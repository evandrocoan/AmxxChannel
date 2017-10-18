

import sublime
import sublime_plugin

import os

"""

# Fix Main Menus

Delete the default main menu for the `amxmodx` package, because when it updates
we would get duplicated menu entries as the default menu for that package is set
on the `User/Main.sublime-menu` file.


# Diff Configurations

This folder has the purpose to disable the default Diff package Context Menus.
As they were moved into the Custom Settings package.

"""

def plugin_loaded() :
    install_setting_file( "amxmodx", "Main.sublime-menu" )
    install_setting_file( "Diff", "Context.sublime-menu" )

def install_setting_file( package_name, target_file_name ):
    target_directory = sublime.packages_path()
    target_file      = os.path.join( target_directory, package_name, target_file_name )

    attempt_to_install_file( target_directory, target_file, "\n[\n\n]\n" )

def attempt_to_install_file( target_directory, target_file, input_file_string ):

    if not os.path.exists( target_directory ):
        os.makedirs( target_directory )

    text_file = open( target_file, "w" )
    text_file.write( input_file_string )
    text_file.close()


