import requests


def get_html(url):
    req = requests.get(url)
    return req.json()


images_list = get_html('https://api.jfbapp.cn/facemesh/billboard')
path = '/Users/yingdai/workspace/hupu2/{}.jpg'
for images in images_list['faces']:
    with open(path.format(images['id']), 'wb') as f:
        r = requests.get(images['image'])
        print(images['image'])
        f.write(r.content)
    f.close()
