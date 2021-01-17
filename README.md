Window Watcher
================================================================

Small script that can detect when the active window changes

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
---
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

  - name: Default
    command: "g815-led -a a4a4a4"
```

For more samples see config.sample.yml
