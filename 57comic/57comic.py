#!-*-coding:utf-8-*-
# https://stackoverflow.com/questions/25707558/json-valueerror-expecting-property-name-line-1-column-2-char-1
# https://stackoverflow.com/questions/2753878/how-to-evaluate-javascript-code-in-python
import re
import string
import requests
import ast
digs = string.digits + string.ascii_letters

header = {
    "User-Agent": "Mozilla / 5.0 (Macintosh; Intel Mac OS X 10_13_0) \
    AppleWebKit / 537.36 (KHTML, like Gecko) Chrome / 65.0.3325.181 Safari / 537.36"}
fail_list = []
base_url = 'http://images.720rs.com/{}'


def int2base(x, base):
    if x < 0:
        sign = -1
    elif x == 0:
        return digs[0]
    else:
        sign = 1

    x *= sign
    digits = []

    while x:
        digits.append(digs[int(x % base)])
        x = int(x / base)

    if sign < 0:
        digits.append('-')

    digits.reverse()

    return ''.join(digits)


def unpack(p, a, c, k, e=None, d=None):
    for i in xrange(c - 1, -1, -1):
        if k[i]:
            p = re.sub('\\b' + int2base(i, a) + '\\b', k[i], p)
    return p


def get_content(url, header=None):
    r = requests.get(url, headers=header)
    if r.status_code == 200:
        return r.content
    else:
        global fail_list
        fail_list.append(url)
        print "error code {}".format(r.status_code)
        print "error download {}".format(url)


def get_html_js(content):
    i = content.find('eval(')
    j = content.find('$((function(core)')
    return r'''{}'''.format(content[i:j].strip())


def eval_js(s):
    js = eval("unpack" + s[s.find('}(') + 1:-1])
    content = js[js.find('={') + 1:-1]
    return ast.literal_eval(content)


def get_pic_urls(fs):
    urls = map(lambda x: base_url.format(x), fs)
    return urls


def download_pic(urls, s):
    for index, url in enumerate(urls, 1):
        filename = 'comic/all/{}_{}.jpg'.format(
            s['cid'].split('/')[2], index)
        c = get_content(url, header)
        print "downloading {}".format(url)
        with open(filename, 'wb') as f:
            f.write(c)
        f.close()


for i in range(266, 703):
    c = get_content('http://www.57mh.com/28028/0{}.html'.format(i), header)
    c = get_html_js(c)
    d = eval_js(c)
    urls = get_pic_urls(d['fs'])
    download_pic(urls, d)
