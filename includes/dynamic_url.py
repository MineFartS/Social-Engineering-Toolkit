"""
Original Author : https://github.com/karthi-the-hacker
Fork Author     : https://github.com/minefarts
"""
from pyngrok import ngrok

def re_url():
    return ngrok.connect(80).public_url