from pyngrok import ngrok

def re_url():
    public_url = ngrok.connect(80)
    return public_url.public_url