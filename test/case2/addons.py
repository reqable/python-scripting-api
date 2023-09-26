# API Docs: https://reqable.com/docs/capture/addons

from reqable import *

def onRequest(context, request):
  # Print url to console
  # print('request url ' + context.url)

  request.method = 'HEAD'
  request.path = '/abc'
  request.queries['foo'] = 'bar'
  request.headers['foo'] = 'bar'
  request.trailers['foo'] = 'bar'
  request.body = 'foobar'

  # Done
  return request

def onResponse(context, response):
  # Update status code
  # response.code = 404

  # APIs are same as `onRequest`
  response.code = 404
  response.headers['foo'] = 'bar'
  response.trailers['foo'] = 'bar'
  response.body = 'foobar'


  # Done
  return response
