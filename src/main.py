import os
import webbrowser
from time import strftime
import subprocess
import requests
import pyperclip

import gi
gi.require_version('Notify', '0.7')
from gi.repository import Notify

'''
This script needs pygobject, requests, pyperclip, maim, slop
'''

file = "teknik-" + strftime("%Y_%m_%d-%H:%M:%S") + ".png"
screenshot_folder = os.getenv('HOME') + '/Pictures/Screenshot/'
filepath = screenshot_folder + file

subprocess.run(["maim --hidecursor --format=png -m 8 --select " + filepath],
               shell=True, check=True)


def upload():
    url = "https://api.teknik.io/v1/Upload"

    data = {'file': (filepath, open(filepath, 'rb'))}
    headers = {'encrypt': True,
               'GenDeletionKey': True,
               'savekey': True,
               'contentType': 'image/png'}

    r = requests.post(url, files=data, data=headers)
    r.raise_for_status()

    r_dict = r.json()
    global url_img
    global url_del
    url_img = r_dict.get('result').get('url')
    url_del = url_img + '/' + r_dict.get('result').get('deletionKey')


def logs():
    log_file = open(screenshot_folder + "log.txt", "a")
    log_file.write(url_del + '\n')
    log_file.close()


def notify():
    Notify.init("teknik-screenshot")
    notification = Notify.Notification.new("Upload finished")
    notification.show()
    Notify.uninit()


if os.path.isfile(filepath):
    upload()
    webbrowser.open_new_tab(url_img)
    pyperclip.copy(url_img)
    notify()
    logs()
