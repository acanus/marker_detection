#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import threading
import webcam.views as views
import cv2
def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marker_detection.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

import socket
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

if __name__ == '__main__':   
    # IPAddr = get_ip()
    # print(IPAddr)
    # if __debug__:
    #     sys.argv.append('runserver')
    # sys.argv.append(str(IPAddr)+':5000')
    sys.argv.append('--noreload')
    #sys.argv.append('--nothreading')
    thread_camera=threading.Thread(target = main,args=[])
    thread_camera.start()
    views.mainloop()
    
