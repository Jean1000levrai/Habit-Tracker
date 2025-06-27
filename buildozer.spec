[app]
version = 1.0
title = HabitTracker
package.name = habittracker
package.domain = org.jeansalomon
source.dir = ./src
source.include_exts = py,png,jpg,kv,atlas,otf,ttf,json
source.exclude_dirs = tests, bin, .git, __pycache__, .venv, .venv311

# (list all the entry point files, main.py is your launcher)
entrypoint = main.py

# (list of all the requirements, separated by a comma)
requirements = python3,kivy,kivymd,plyer

# (include any additional source files or folders)
# assets/fonts and data folders are included by default due to source.include_exts

# (icon of the application)
icon.filename = assets/screenshots/screenshot3.png

# (presplash of the application)
# presplash.filename = %(source.dir)s/assets/screenshots/screenshot4.png

# (android permissions)
android.permissions = INTERNET, VIBRATE

# (android api)
android.api = 33
android.minapi = 21
android.ndk = 25b
android.gradle_dependencies = com.android.tools.build:gradle:7.2.2
android.gradle_version = 7.5

# (orientation)
orientation = portrait

# (fullscreen)
fullscreen = 1

# (android logcat filters)
logcat_filters = *:S python:D

# (include all .kv files in ui and ui_scripts)
include_patterns = assets/*, data/*, src/ui/**/*.kv, src/ui_scripts/**/*.kv

# (fonts)
# FontAwesome is in assets/fonts/fa-solid.otf, included by source.include_exts

# (copy .json config and db files)
# Already included by source.include_exts

# (other settings)
android.arch = armeabi-v7a, arm64-v8a, x86, x86_64

# (python version)
# python3 is default, but you can specify:
# android.python_version = 3

# (if you use webbrowser, add this to requirements)
# webbrowser is stdlib, no need to add

# (if you use sqlite3, it's included in python3)

# (if you use notification, plyer is already in requirements)

# (if you use OpenGL, Kivy handles it)

# (if you use KivyMD, it's in requirements)

# (if you use hashlib, it's stdlib)

# (if you use json, it's stdlib)
