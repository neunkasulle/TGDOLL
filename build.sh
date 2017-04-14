#!bin/bash
rm -rf __pycache__ build/ dist/ main.spec
pyinstaller -n ChooseYourPlayer -w -F -i "Icon-CYP-16x16.ico" main.py
cp -r res dist/res




