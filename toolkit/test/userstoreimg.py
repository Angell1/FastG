import requests
import random
import hashlib
import os

path = os.path.abspath(__file__)
def store_userimg(userid):
    size=256
    styles = ['identicon', 'monsterid', 'wavatar']
    random_str = ''.join([chr(random.randint(0x0000, 0x9fbf)) for i in range(random.randint(1, 25))])
    m1 = hashlib.md5("{}".format(random_str).encode("utf-8")).hexdigest()
    url = 'http://www.gravatar.com/avatar/{}?s={}&d={}'.format(m1, size, random.choice(styles))
    res = requests.get(url)
    print(type(res.content))
    with open(path + 'image%s.jpg' % str(userid), 'wb')as f:
        f.write(res.content)


def get_userimg(userid):
    with open(path + 'image%s.jpg' % str(userid), 'rb')as f:
        return f.read()

