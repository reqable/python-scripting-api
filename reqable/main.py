import sys
import json
from reqable import CaptureContext, CaptureHttpRequest, CaptureHttpResponse
import addons

def main():
  argv = sys.argv[1:]
  if len(argv) != 2:
    raise Exception('Invalid reqable script arguments')
  type = argv[0]
  if type == 'request':
    onRequest(argv[1])
  elif type == 'response':
    onResponse(argv[1])
  else:
    raise Exception('Unexpected type ' + type)

def onRequest(request):
  with open(request, 'r', encoding='UTF-8') as content:
    data = json.load(content)
    context = CaptureContext(data['context'])
    result = addons.onRequest(context, CaptureHttpRequest(data['request']))
    if result is not None:
      with open(request + '.cb', 'w', encoding='UTF-8') as callback:
        callback.write(json.dumps({
          'request': result.serialize(),
          'shared': context.shared,
        }))

def onResponse(response):
  with open(response, 'r', encoding='UTF-8') as content:
    data = json.load(content)
    context = CaptureContext(data['context'])
    result = addons.onResponse(context, CaptureHttpResponse(data['response']))
    if result is not None:
      with open(response + '.cb', 'w', encoding='UTF-8') as callback:
        callback.write(json.dumps({
          'response': result.serialize(),
          'shared': context.shared,
        }))

if __name__== '__main__':
  main()