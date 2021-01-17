#!/usr/bin/env python3

import gi
import sys
import yaml
import argparse
import os
import fnmatch


gi.require_version("Wnck", "3.0")
gi.require_version("Gtk", "3.0")

from gi.repository import Wnck
from gi.repository import Gtk


prev_active_window: Wnck.Window = None
prev_command: str = None


def printverbose(s: str):
	if (args.verbose):
		print(s)


def get_window_attributes(window: Wnck.Window):
	window_dir = dir(window)
	attributes = []
	if "get_application" in window_dir and "get_name" in dir(window.get_application()):
		attributes.append(("application", window.get_application().get_name()))
	if "get_name" in window_dir:
		attributes.append(("name", window.get_name()))
	if "get_class_group_name" in window_dir:
		attributes.append(("class_group", window.get_class_group_name()))
	if "get_class_instance_name" in window_dir:
		attributes.append(("class_instance", window.get_class_instance_name()))
	if "get_icon_name" in window_dir:
		attributes.append(("icon", window.get_icon_name()))
	return dict(attributes)


def print_window_attributes(attributes):
	if args.verbose:
		print("    match:")
		for k, v in attributes.items():
			print("      " + k + ": \"" + v + "\"")


def execute_rules(attributes):
	global prev_command

	rules_to_execute = find_matching_rules(attributes)
	for rule in rules_to_execute:
		command = rule["command"] if "command" in rule else None
		if not command is None:
			if command == prev_command and rule["skippable"]:
				print("  - skip: " + rule["name"])
				printverbose("    command: " + str(command))
			else:
				print("  - executing: " + rule["name"])
				print("    command: " + str(command))
				if rule["continue"]:
					print("    continue: true")
				if not rule["skippable"]:
					print("    skippable: false")
				os.system(command)
				prev_command = command
		else:
			print("  - no-cmd: " + rule["name"])


def find_matching_rules(attributes):
	printverbose("")
	rules_to_execute = []
	for rule in rules:
		if rule["match"] is None or all_match(rule, attributes):
			rules_to_execute.append(rule)
			printverbose("  - matched rule: " + str(rule))
			if not rule["continue"]:
				break
	printverbose("")
	return rules_to_execute


def all_match(rule, attributes):
	for k, v in rule["match"]:
		if not v is None and not fnmatch.fnmatch(attributes[k], v):
			return False
	return True


def do_active_window_changed(this_screen: Wnck.Screen, previously_active: Wnck.Window):
	global name_change_hook, prev_active_window, prev_attributes

	print ("\nactive-window-changed")
	active_window: Wnck.Window = this_screen.get_active_window()
	attributes = get_window_attributes(active_window)
	if (prev_active_window is not None):
		prev_active_window.disconnect(name_change_hook)
	prev_active_window = active_window
	prev_attributes = attributes
	if (active_window is not None):
		name_change_hook = active_window.connect("name-changed", do_window_name_changed)
		print_window_attributes(attributes)
		execute_rules(attributes)
	else:
		print("    window is None")


def do_window_name_changed(active_window: Wnck.Window):
	global prev_attributes

	print("\nwindow: name-changed")
	attributes = get_window_attributes(active_window)
	print_window_attributes(attributes)
	if (attributes != prev_attributes):
		print("  window changed")
		execute_rules(attributes)
	prev_attributes = attributes


def window_active_init():
	Gtk.init([])
	screen: Wnck.Screen = Wnck.Screen.get_default()
	screen.connect("active-window-changed", do_active_window_changed)
	Gtk.main()


def load_config():
	global rules
	rules = []
	try:
		ruleNum = 0
		full_path = os.path.expanduser(args.config)
		print("Loading config file: " + full_path)
		with open(full_path, "r") as file:
			configfile = yaml.load(file, Loader=yaml.FullLoader)
			for rule in configfile:
				ruleNum = ruleNum + 1
				name = rule["name"] if "name" in rule else "Rule " + str(ruleNum)
				printverbose("\n  - name: " + name)

				if ("match" in rule):
					match = []
					printverbose("    match:")
					for k in ["application", "name", "class_group", "class_instance", "icon"]:
						if k in rule["match"]:
							match.append((k, rule["match"][k]))
							printverbose("      " + k + ": " + rule["match"][k])
						else:
							match.append((k, None))
				else:
					match = None
				command = rule["command"] if "command" in rule else None
				printverbose("    command: " + str(command))
				cont = rule["continue"] if "continue" in rule else False
				printverbose("    continue: " + str(cont))
				skippable = rule["skippable"] if "skippable" in rule else True
				printverbose("    skippable: " + str(skippable))

				rules.append({"name":name, "match":match, "command":command, "continue":cont, "skippable":skippable})
		#print(str(rules))
		printverbose("\nConfig file parsed")
	except IOError:
		print("IOError: Unable to read " + args.config)
		sys.exit(1)


if __name__ == "__main__":
	try:
		parser = argparse.ArgumentParser()
		parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
		parser.add_argument("-c", "--config", help="location of a config file", default="~/.config/windowwatcher/config.yml")
		args = parser.parse_args()
		if args.verbose:
			print("Verbose")
		load_config()
		window_active_init()
	except KeyboardInterrupt:
		print("\nKeyboardInterrupt: Exit program")
		sys.exit(1)
