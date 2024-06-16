# API Docs: https://reqable.com/docs/capture/addons

from reqable.reqable import CaptureContext, CaptureHttpRequest, CaptureHttpResponse

def onRequest(context: CaptureContext, request: CaptureHttpRequest) -> CaptureHttpRequest:
  return request

def onResponse(context: CaptureContext, response: CaptureHttpResponse) -> CaptureHttpResponse:
  return response