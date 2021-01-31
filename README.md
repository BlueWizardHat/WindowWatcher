Window Watcher
================================================================

Small script that can detect when the active window changes and run a command when it happens.


## Configuration

By default the script will use "\~/.config/windowwatcher/config.yml" as it's config file, this can be overridden with the -c argument.

Configuration is in yaml format and consists of a number of window rules. A sample rule could look like this

```yaml
  - name: Sublime Text
    match:
      application: "Sublime Text"
      name: "untitled"
      class_group: "Sublime_text"
      class_instance: "sublime_text"
      icon: "untitles"
    command: "g815-led -a a4a4a4"
    continue: false
    skippable: true
```

Each rule has up to 5 elements "name", "match", "command", "continue" and "skippable"

	* name - optional name, if not given the rule will be given a name based on it's position in the config file.
	* match - optional match specification, an empty or missing "match" element means the rule matches everything.
	* command - optional command to execute
	* continue - true or false. indicates if rules after this rule should be processed if this rule is a match, defaults to false
	* skippable - true or false, indicates if the command should be skipped if it is the same as the previously executed command, defaults to true.


#### Matching windows

It is possible to match 5 window attributes

	* application - application name
	* name - window title
	* class_group - window class group name
	* class_instance - window class instance name
	* icon - window icon

Use the -v flag to have the script print out these attributes when changing window.
Every match element is optional and only elements present will be required to match, but every element present in a rule must match for the rule to match.

It is possible to use glob matching so you can use "\*" in the elements to match. For example

```yaml
      application: "*HTTPS*Chromium"
```


#### Default match

To create a default match just create a rule with no "match" element. This will match every window.

```yaml
  - name: Default
    command: "g815-led -a a4a4a4"
```


### Example configuration

```yaml
#
# Rules for window changed
#

window-changed:
  - name: Sublime Text
    match:
      application: "Sublime Text"
      class_group: "Sublime_text"
      class_instance: "sublime_text"
    command: "g815-led -a a4a4a4"

  - name: Chromium
    match:
      class_group: "Chromium"
      class_instance: "chromium"
    command: "g815-led -a a4a4a4"

  - name: Guake in ~/Projects
    match:
      application: "guake"
      name: "*: ~/Projects"
    command: "g815-led -a a4a4a4"

  - name: Guake in HOME
    match:
      application: "guake"
      name: "*: ~"
    command: "g815-led -a a4a4a4"

  - name: Default
    command: "g815-led -a a4a4a4"


#
# Rules for window opened
#

window-opened:

  - name: Default
```

For more examples see [config.sample.yml](https://github.com/BlueWizardHat/WindowWatcher/blob/master/config.sample.yml)


## FAQ

**Q: Why?**

**A:** Because I have a fancy RGB keyboard and [g810-led](https://github.com/MatMoul/g810-led) only lets you change the colors, but does not contain a daemon to monitor window changes and I want to change the colors depending on which program has focus.

**Q: Is this useful?**

**A:** Probably not, but it was fun to do.


## Screensavers

No window event seems to be emitted when the screensaver is activated or when it is deactivated. However it is possible to watch
for screensaver activation using an external script that listens on dbus-events. On screensaver activation run whatever command you want in that script and on deactivation you can run windowwatcher.py --once.

The following example listens on the xfce screensaver, on activation it stops spotify playing and makes a g810 keyboard lights use
the breathe effect. On screensaver deactivation it runs "windowwatcher.py --once" to restore the command for the activated window.

```bash
#!/usr/bin/env bash

spotify_stop="dbus-send --session --dest=org.mpris.MediaPlayer2.spotify --type=method_call --print-reply --reply-timeout=1000 /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Stop"

while read line; do
	if [[ "$line" == "boolean true" ]]; then
		echo "screensaver activated"
		$spotify_stop > /dev/null 2>&1
		g810-led -fx breathing all f4f4f4 10 > /dev/null 2>&1
	elif [[ "$line" == "boolean false" ]]; then
		echo "screensaver deactivated"
		windowwatcher.py --once > /dev/null 2>&1
	fi
done < <(dbus-monitor --session "type='signal',interface='org.xfce.ScreenSaver',member='ActiveChanged'")
```

If you are using another window manager than Xfce you will just have to use dbus-monitor to figure out what interface to listen to,
or ask Google.
