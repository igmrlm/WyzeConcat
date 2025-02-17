A simple script that opens a gui window for concatening wyze camera videos without re-encoding them. 

Usage: 

1. python concat.py
2. Browse to the sdcard root folder
3. Browse to the destination folder and type an output name
4. Click start

Dependancies: natsort, tkinter, threading, subprocess.

FFMPEG Must be in your shell path. 


TODO:

1. Update the script to indentify videos with 0 filesize and omit them as they currently must be manually deleted otherwise they will cause ffmpeg to crash
2. Modify the progress bar code to show the actual progress instead of indeterminate. 
