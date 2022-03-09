from mitmproxy import http
from mitmproxy import ctx
from lxml import etree
from time import time


REPLACEMENTS = [('russian', 'clowns'), ('russia', 'clown land'), ('putin', 'butt head')]


def _extend_mapping(attr: str) -> None:
    # from https://github.com/FernOfSigma/owoifier/blob/main/owoifier/owoifier.py
    for old in REPLACEMENTS:
        new = [getattr(i, attr)() for i in old]
        if new not in REPLACEMENTS:
            REPLACEMENTS.append(new)


_extend_mapping("upper")
_extend_mapping("capitalize")

def remove_war(text):
    root = etree.HTML(text)
    for element in root.iter():
        if element.tag != 'script':
            for token, sub in REPLACEMENTS:
                if element.text is not None and token in element.text:
                    element.text = element.text.replace(token, sub)
                if element.tail is not None and token in element.tail:
                    element.tail = element.tail.replace(token, sub)
    return etree.tostring(root, method='html', encoding='unicode')


class TextReplace:
    def response(self, flow: http.HTTPFlow):
        if 'content-type' in flow.response.headers:
            contenttype = flow.response.headers['content-type']
            if 'text/html' in contenttype and len(flow.response.text):
                t0 = time()
                flow.response.text = remove_war(flow.response.text)
                ctx.log.info(f'processing took {time()-t0} seconds')
addons = [
    TextReplace()
]