# [Kubeseal](//packagecontrol.io/packages/Kubeseal)

This plugin will convert a Kubernetes Secret manifest to a [Bitnami SealedSecret](https://github.com/bitnami-labs/sealed-secrets) manifest.

There's a command palette entry called `Kubeseal: Seal this secret` to run it.

## Options

Users can override the options in `Packages/User/Kubeseal.sublime-settings`.

This file can be opened either through the menus (_Preferences_ > _Package Settings_ > _Kubeseal_ > _Settings_) or through the command palette (<kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd>) and enter `Preferences: Kubeseal settings`.

## Installation

##### Using the package manager

1. Install the [Sublime Text Package Control](//packagecontrol.io/installation) plugin if you haven't already.
    - _Preferences_ > _Package Control_
2. Open up the command palette (<kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd>) and enter `Package Control: Install Package`
3. Search for `Kubeseal` and hit <kbd>Enter</kbd> to install.

##### Manual installation with Git

1. Click the `Preferences > Browse Packages` menu.
2. Open up a terminal and execute the following:
    - `git clone https://github.com/p3lim/sublime-kubeseal Kubeseal`
3. Restart Sublime Text.
