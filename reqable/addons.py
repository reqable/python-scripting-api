# API Docs: https://reqable.com/docs/capture/addons

from reqable import *

def onRequest(context, request):
  # Print url to console
  # print('request url ' + context.url)

  # Update or add a query parameter
  # request.queries['foo'] = 'bar'

  # Update or add a http header
  # request.headers['foo'] = 'bar'

  # Replace http body with a text
  # request.body = 'Hello World'

  # Map with a local file
  # request.body.file('~/Desktop/body.json')

  # Convert to dict if the body is a JSON
  # request.body.jsonify()
  # Update the JSON content
  # request.body['foo'] = 'bar'

  # Done
  return request

def onResponse(context, response):
  # Update status code
  # response.code = 404

  # APIs are same as `onRequest`

  # Done
  return response
