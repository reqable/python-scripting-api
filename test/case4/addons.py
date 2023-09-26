# API Docs: https://reqable.com/docs/capture/addons

from reqable import *
import hashlib

def onRequest(context, request):
  queries = sorted(request.queries)
  text = '&'.join(['='.join(query) for query in queries])
  algorithm = hashlib.md5()
  algorithm.update(text.encode(encoding='UTF-8'))
  signature = algorithm.hexdigest()
  request.headers['signature'] = signature
  # Done
  return request

def onResponse(context, response):
  # Done
  return response
