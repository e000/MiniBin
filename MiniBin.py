"""
    MiniBin
    ~~~~~~~

    A minimal pastebin.

    This program is free software. It comes without any warranty, to
    the extent permitted by applicable law. You can redistribute it
    and/or modify it under the terms of the Do What The Fuck You Want
    To Public License, Version 2, as published by Sam Hocevar. See
    http://sam.zoy.org/wtfpl/COPYING for more details.

"""

from flask import Flask, render_template, request, send_file, abort, url_for, redirect
import string, random, os
from datetime import datetime

app = Flask(__name__)
file_path = '/tmp/minibin'

domain = string.ascii_letters + string.digits + "_-"
random_filename = lambda len = 15: ''.join(random.choice(domain) for i in xrange(len))
domain2 = string.ascii_letters + string.digits
random_prefix = lambda len = 1: ''.join(random.choice(domain2) for i in xrange(len))

if not os.path.exists(file_path):
    os.makedirs(file_path)

if not os.path.isdir(file_path):
    raise RuntimeError("%r is not a directory." % file_path)

if not os.access(file_path, os.W_OK | os.X_OK | os.R_OK):
    raise RuntimeError("%r is not writable" % file_path)

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/up", methods=['POST'])
def up():
    code = request.form['code']
    prefix_1 = random_prefix()
    prefix_2 = random_prefix(2)
    file_name = random_filename(12)
    date_str = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    _file_path = os.path.join(file_path, prefix_1, prefix_2)

    if not os.path.exists(_file_path):
        os.makedirs(_file_path)

    with open(os.path.join(_file_path, file_name), 'w') as fp:
        fp.write(render_template("paste.html", date_str = date_str, code = code))

    return redirect(url_for('paste', file = prefix_1 + prefix_2 + file_name))

@app.route("/<file>")
def paste(file):
    prefix_1 = file[0]
    prefix_2 = file[1:3]
    file_name = file[3:]
    file_name = os.path.join(file_path, prefix_1, prefix_2, file_name)

    if os.path.exists(file_name):
        return send_file(file_name, mimetype="text/html; charset=utf8")

    abort(404)


if __name__ == '__main__':
    app.run(debug = True)