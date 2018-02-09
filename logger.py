from __future__ import print_function
import sys
import traceback

class Logger:
    def __init__(self):
        traceback.print_exc(file=sys.stdout)

    def console(self, text):
        text = str(text)
        print(text, file=sys.stderr)

    def info(self, text):
        text = str(text)
        print(text, file=sys.stderr)

    def warning(self, text):
        text = str(text)
        print(text, file=sys.stderr)
    
    def error(self):
        exc_type, exc_value, exc_tb = sys.exc_info()
        print(exc_type, exc_value, exc_tb, file=sys.stderr)
        traceback.print_exception(exc_type, exc_value, exc_tb)

    
    def critical(self, text=''):
        exc_type, exc_value, exc_tb = sys.exc_info()
        print('error code=H:',exc_type, exc_value, exc_tb, file=sys.stderr)
        traceback.print_exception(exc_type, exc_value, exc_tb)
