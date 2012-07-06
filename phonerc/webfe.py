from flask import Flask, session, redirect, url_for, escape, request, make_response, render_template, send_file

from StringIO import StringIO
from xml.etree.ElementTree import ElementTree, fromstring

import pycisco.cmpush as cmpush
import pycisco.cmxml as cmxml

app = Flask(__name__)

from collections import namedtuple

Navigation = namedtuple('Navigation', 'href caption')

BUTTONS = [
    ('Key:Settings', 'Settings'),
    ('Key:KeyPad0', '0'),
    ('Key:KeyPad1', '1'),
    ('Key:KeyPad2', '2'),
    ('Key:KeyPad3', '3'),
    ('Key:KeyPad4', '4'),
    ('Key:KeyPad5', '5'),
    ('Key:KeyPad6', '6'),
    ('Key:KeyPad7', '7'),
    ('Key:KeyPad8', '8'),
    ('Key:KeyPad9', '9'),
    ('Key:Soft1', 'softkey 1'),
    ('Key:Soft2', 'softkey 2'),
    ('Key:Soft3', 'softkey 3'),
    ('Key:Soft4', 'softkey 4'),
    ('Key:NavUp', 'up'),
    ('Key:NavDwn', 'down'),
    ]

def make_xml_response(*args, **kw):
    response = make_response(*args, **kw)
    response.headers['content-type'] = 'text/xml'
    return response

start = [False]

@app.route('/screenshot/<ip>', methods=['GET', 'POST'])
def screenshot(ip):
    import pycisco.cipimage as cipimage
    cip_data = cmpush.screenshot(ip, 'user', 'password')
    tree = fromstring(cip_data)
    im = cipimage.load_cip(tree)

    img_io = StringIO()
    im.save(img_io, 'GIF')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/gif')

@app.route('/phones', methods=['GET', 'POST'])
def phones():
    ips = ['10.19.0.%d' % i for i in range(2, 255)]#[:16]
    # ips = ['10.19.0.77', '10.19.0.77']
    return render_template('phones.html', ips=ips)

@app.route('/click/<ip>/<button>', methods=['GET', 'POST'])
def click(ip, button):
    cmpush.execute(ip, cmxml.create_execute_url(button), 'user', 'password')
    return 'clicking'

@app.route('/ctl/<ip>', methods=['GET', 'POST'])
def ctl(ip):
    navigation = [Navigation(url_for('.click', ip=ip, button=button), caption) for button, caption in BUTTONS]
    return render_template('ctl.html', screenshot_url=url_for('.screenshot', ip=ip), navigation=navigation)

