#!/usr/bin/env python3

import gi
import sys

gi.require_version("Wnck", "3.0")
gi.require_version("Gtk", "3.0")

from gi.repository import Wnck
from gi.repository import Gtk


prev_active_window: Wnck.Window = None

def get_app_name(window: Wnck.Window):
	if (window is None):
		return "-None-"
	elif (not "get_application" in dir(window)):
		return "-NoApp"
	elif (not "get_name" in dir(window.get_application())):
		return "-NoName"
	else:
		return window.get_application().get_name()

def get_window_name(window: Wnck.Window):
	if (window is None):
		return "-None-"
	elif (not "get_name" in dir(window)):
		return "-NoName"
	else:
		return window.get_name()

def get_window_class_group_name(window: Wnck.Window):
	if (window is None):
		return "-None-"
	elif (not "get_class_group_name" in dir(window)):
		return "-NoClassGroupName"
	else:
		return window.get_class_group_name()

def get_window_class_instance_name(window: Wnck.Window):
	if (window is None):
		return "-None-"
	elif (not "get_class_instance_name" in dir(window)):
		return "-NoClassInstanceName"
	else:
		return window.get_class_instance_name()

def get_window_icon_name(window: Wnck.Window):
	if (window is None):
		return "-None-"
	elif (not "get_icon_name" in dir(window)):
		return "-NoIconName"
	else:
		return window.get_icon_name()

def print_window(name: str, window: Wnck.Window):
	if (window is not None):
		print("  " + name)
		print("    app: " + get_app_name(window))
		print("    name: " + get_window_name(window))
		print("    class group: " + get_window_class_group_name(window))
		print("    class instance: " + get_window_class_instance_name(window))
		print("    icon: " + get_window_icon_name(window))
	else:
		print("  " + name + " is None")

def do_active_window_changed(this_screen: Wnck.Screen, previously_active: Wnck.Window):
	global name_change_hook, prev_active_window

	print ("\nactive-window-changed")
	active_window: Wnck.Window = this_screen.get_active_window()
	print_window("active", active_window)
	if (prev_active_window is not None):
		prev_active_window.disconnect(name_change_hook)
	prev_active_window = active_window
	if (active_window is not None):
		name_change_hook = active_window.connect("name-changed", do_window_name_changed)

def do_window_name_changed(active_window: Wnck.Window):
	print ("\nwindow: name-changed")
	print_window("active", active_window)

def window_active_init():
	Gtk.init([])
	screen: Wnck.Screen = Wnck.Screen.get_default()
	screen.connect("active-window-changed", do_active_window_changed)
	Gtk.main()

if __name__ == "__main__":
	try:
		window_active_init()
	except KeyboardInterrupt:
		print("\nKeyboardInterrupt: Exit program")
		sys.exit(1)
