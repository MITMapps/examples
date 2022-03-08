from mitmproxy import http
from mitmproxy import ctx
from lxml import etree
from time import time


def remove_war(text):
    root = etree.HTML(text)
    for element in root.iter():
        for token, sub in [('war', 'peace'), ('War', 'Peace'), ('WAR', 'PEACE')]:
            if element.text is not None and token in element.text:
                element.text = element.text.replace(token, sub)
            if element.tail is not None and token in element.tail:
                element.tail = element.tail.replace(token, sub)
    return etree.tostring(root, method='html', encoding='unicode')


class PEACE:
    def __init__(self):
        self.num = 0

    def response(self, flow: http.HTTPFlow):
        if 'wikipedia.org' in flow.request.url:
            if 'content-type' in flow.response.headers:
                contenttype = flow.response.headers['content-type']
                if 'text/html' in contenttype:
                    t0 = time()
                    flow.response.text = remove_war(flow.response.text)
                    ctx.log.info(f'processing took {time()-t0} seconds')
addons = [
    PEACE()
]