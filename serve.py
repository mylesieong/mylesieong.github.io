#!/usr/bin/env python3
"""Local preview server. `python3 serve.py [port]` then open http://localhost:8123"""
import functools, os, sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.abspath(__file__))
port = int(sys.argv[1]) if len(sys.argv) > 1 else 8123
handler = functools.partial(SimpleHTTPRequestHandler, directory=ROOT)
print("serving %s at http://localhost:%d" % (ROOT, port))
ThreadingHTTPServer(("127.0.0.1", port), handler).serve_forever()
