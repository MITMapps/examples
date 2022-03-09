from mitmproxy import http
from mitmproxy import ctx
import json
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


def tree_iter(tree, func, key=None):
    if isinstance(tree, dict):
        rtn = {}
        for k, value in tree.items():
            rtn[k] = tree_iter(value, func, k)
        return rtn
    elif isinstance(tree, list):
        rtn = []
        for value in tree:
            rtn.append(tree_iter(value, func, key))
        return rtn
    else:
        return func(tree, key)


def replace_fun(text, key):
    if key in ['content', 'text', 'title'] and isinstance(text, str):
        for token, sub in REPLACEMENTS:
            text = text.replace(token, sub)
    return text


def remove_war(text):
    root = json.loads(text)
    root = tree_iter(root, replace_fun, 'root')
    return json.dumps(root)


class DataReplace:
    def response(self, flow: http.HTTPFlow):
        if 'content-type' in flow.response.headers:
            contenttype = flow.response.headers['content-type']
            if 'application/json' in contenttype and len(flow.response.text):
                t0 = time()
                flow.response.text = remove_war(flow.response.text)
                ctx.log.info(f'processing took {time()-t0} seconds')


addons = [
    DataReplace()
]