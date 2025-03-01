import os
import sys

path = os.path.expanduser('~/avazxoja1234/kitobxon_kids')  # your-username va your-project-name ni o'zgartiring
if path not in sys.path:
    sys.path.append(path)

from bot import main  # bot.py - bot faylingizning nomi