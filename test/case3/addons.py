# API Docs: https://reqable.com/docs/capture/addons

from reqable import *

def onRequest(context, request):
  context.shared = 1
  # Done
  return request

def onResponse(context, response):
  context.shared = 2
  # Done
  return response
