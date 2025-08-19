[app]
# App metadata
title = Mutoon
package.name = mutoon
package.domain = org.mcy
version = 0.1

# Source
source.dir = .
source.main = main.py

# App branding
icon.filename = mtoon_logo.png
presplash.filename = mtoon_presplash.png
fullscreen = 1
orientation = portrait

# External dependencies (remove python-bidi from requirements)
requirements = python3,kivy==2.3.0,kivymd==1.2.0,cython==0.29.36,arabic_reshaper,Pillow

# Architecture
android.archs = arm64-v8a

# Include all needed assets recursively
source.include_exts = py,kv,png,jpg,jpeg,ttf,otf,atlas,json
source.include_patterns = Images/**/*,UI/**/*,fonts/**/*,PDF_Images/**/*,bidi/**/*
source.include_dirs = fonts,Images,UI,PDF_Images,bidi

# Add assets for packaging
android.add_assets = fonts:fonts,Images:Images,UI:UI,PDF_Images:PDF_Images

# Android SDK/NDK settings
android.ndk = 25b
android.minapi = 21
android.api = 33
p4a.bootstrap = sdl2
p4a.ignore_setup_py = 1

# Permissions
android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

# Exclude unnecessary files
exclude_patterns = \
    *.pyc,*.pyo,*.pyd,__pycache__,\
    .git,.github,.gitignore,\
    *.md,*.txt,\
    *.sh,*.bat,\
    venv,env,.venv,\
    tests,*.test,\
    android-ndk*,\
    commandlinetools*,\
    gradle*

# Build/Logging
log_level = 2
consolelog = 0
android.release = 0
android.allow_backup = 1
android.strip = 1

[buildozer]
log_level = 2
