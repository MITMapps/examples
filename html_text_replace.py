"""
Credit to FernOfSigma https://mitmapps.ca/user/FernOfSigma for developing this
"""
from mitmproxy import http
from mitmproxy import ctx
from lxml import etree
from time import time


ALLOWED_TAGS = [
    "title",
    "div", "ol", "span", "ul",
    "blockquote", "figcaption", "figure", "p", "pre",
    "h1", "h2", "h3", "h4", "h5", "h6",
    "b", "em", "i","sub", "sup", "strong",
    "a", "abbr", "cite", "q", "s", "u"
]

MAPPINGS = [
    ["r", "w"],
    ["l", "w"],
    ["na", "nya"],
    ["ni", "nyi"],
    ["nu", "nyu"],
    ["ne", "nye"],
    ["no", "nyo"],
    ["ove", "uv"]
]

def _extend_mapping(attr: str) -> None:
    for old_mapping in MAPPINGS:
        new_mapping = [getattr(i, attr)() for i in old_mapping]
        if new_mapping not in MAPPINGS:
            MAPPINGS.append(new_mapping)

_extend_mapping("upper")
_extend_mapping("capitalize")

def owoify(text: str) -> str:
    root = etree.HTML(text)
    for elem in root.iter():
        if elem.tag in ALLOWED_TAGS:
            for src, dst in MAPPINGS:
                if elem.text is not None and src in elem.text:
                    elem.text = elem.text.replace(src, dst)
                if elem.tail is not None and src in elem.tail:
                    elem.tail = elem.tail.replace(src, dst)
    return etree.tostring(root, method='html', encoding='unicode')


class DataReplace:
    def response(self, flow: http.HTTPFlow):
        if "content-type" in flow.response.headers:
            content_type = flow.response.headers["content-type"]
            if "text/html" in content_type and len(flow.response.text):
                t0 = time()
                flow.response.text = owoify(flow.response.text)
                ctx.log.info(f"Processing took {time()-t0} seconds")


addons = [
    DataReplace()
]