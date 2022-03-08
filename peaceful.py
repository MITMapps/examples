from mitmproxy import http
from mitmproxy import ctx
import json


class Peace:
    def __init__(self):
        self.num = 0

    def response(self, flow: http.HTTPFlow):
        ctx.log.info("Received Response")
        if 'wikipedia.org' in flow.request.url:
            ctx.log.info(f'Received Response url {flow.request.url}')
            ctx.log.info(f'Received Response headers {json.dumps(list(flow.response.headers.keys()))}')
            if 'content-type' in flow.response.headers:
                contenttype = flow.response.headers['content-type']
                ctx.log.info(f'Received Response content-type {contenttype}')
                if 'text/html' in contenttype:
                    flow.response.text = flow.response.text.replace('war', 'peace')

addons = [
    Peace()
]