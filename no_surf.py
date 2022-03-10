from mitmproxy import http
from mitmproxy import ctx
import json
from time import time


def trim_tree(tree, key=None):
    if isinstance(tree, dict):
        for k, value in tree.items():
            tree[k] = trim_tree(value, k)

    elif isinstance(tree, list):
        if key in ['continuationItems', 'postIds', 'edges', 'itemList']:
            tree = []
        else:
            rtn = []
            for value in tree:
                rtn.append(trim_tree(value, key))
            tree = rtn
    return tree


def remove_continuation(text):
    root = json.loads(text)
    root = trim_tree(root, 'root')
    return json.dumps(root)


class StopContinuation:
    def response(self, flow: http.HTTPFlow):
        if 'content-type' in flow.response.headers:
            contenttype = flow.response.headers['content-type']
            if 'application/json' in contenttype and len(flow.response.text):
                t0 = time()
                flow.response.text = remove_continuation(flow.response.text)
                ctx.log.info(f'processing took {time()-t0} seconds')


addons = [
    StopContinuation()
]