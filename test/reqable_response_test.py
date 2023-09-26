import unittest

from reqable import CaptureHttpResponse

class HttpResponseTest(unittest.TestCase):
  def testHttpResponseConstructor(self):
    response = CaptureHttpResponse({
      'request': {
        'method': 'GET',
        'path': '/',
        'protocol': 'HTTP/1.1',
      },
      'code': 200,
      'message': 'OK',
      'protocol': 'HTTP/1.1',
    })
    self.assertEqual(response.code, 200)
    self.assertEqual(response.message, 'OK')
    self.assertEqual(response.protocol, 'HTTP/1.1')
    self.assertEqual(response.headers.entries, [])
    self.assertTrue(response.body.isNone)
    self.assertEqual(response.trailers.entries, [])

    response = CaptureHttpResponse({
      'request': {
        'method': 'GET',
        'path': '/',
        'protocol': 'HTTP/1.1',
      },
      'code': 200,
      'message': 'OK',
      'protocol': 'HTTP/1.1',
      'headers': [
        'foo: bar',
        'abc: 123',
        'hello: world'
      ],
      'body': {
        'type': 0,
        'payload': None
      },
      'trailers': [
        'foo: bar',
        'abc: 123',
        'hello: world'
      ],
    })
    self.assertEqual(response.code, 200)
    self.assertEqual(response.message, 'OK')
    self.assertEqual(response.protocol, 'HTTP/1.1')
    self.assertEqual(response.headers.entries, [
      'foo: bar',
      'abc: 123',
      'hello: world'
    ])
    self.assertEqual(response.body.type, 0)
    self.assertEqual(response.body.payload, None)
    self.assertEqual(response.trailers.entries, [
      'foo: bar',
      'abc: 123',
      'hello: world'
    ])


  def testHttpResponseCodeUpdate(self):
    response = CaptureHttpResponse({
      'request': {
        'method': 'GET',
        'path': '/',
        'protocol': 'HTTP/1.1',
      },
      'code': 200,
      'message': 'OK',
      'protocol': 'HTTP/1.1',
    })
    response.code = 404
    self.assertEqual(response.code, 404)

  def testHttpResponseHeadersUpdate(self):
    response = CaptureHttpResponse({
      'request': {
        'method': 'GET',
        'path': '/',
        'protocol': 'HTTP/1.1',
      },
      'code': 200,
      'message': 'OK',
      'protocol': 'HTTP/1.1',
    })
    response.headers['foo'] = 'bar'
    self.assertEqual(response.headers.entries, [
      'foo: bar'
    ])
    response.headers['name'] = 'megatron'
    self.assertEqual(response.headers.entries, [
      'foo: bar',
      'name: megatron'
    ])
    response.headers = [
      'foo: bar',
      'abc: 123'
    ]
    self.assertEqual(response.headers.entries, [
      'foo: bar',
      'abc: 123'
    ])
    response.headers = {
      'foo': 'bar',
      'abc': '123',
    }
    self.assertEqual(response.headers.entries, [
      'foo: bar',
      'abc: 123'
    ])
    response.headers = [
      ('foo', 'bar'),
      ('abc', '123'),
    ]
    self.assertEqual(response.headers.entries, [
      'foo: bar',
      'abc: 123'
    ])

  def testHttpResponseTrailersUpdate(self):
    response = CaptureHttpResponse({
      'request': {
        'method': 'GET',
        'path': '/',
        'protocol': 'HTTP/1.1',
      },
      'code': 200,
      'message': 'OK',
      'protocol': 'HTTP/1.1',
    })
    response.trailers['foo'] = 'bar'
    self.assertEqual(response.trailers.entries, [
      'foo: bar'
    ])
    response.trailers['name'] = 'megatron'
    self.assertEqual(response.trailers.entries, [
      'foo: bar',
      'name: megatron'
    ])
    response.trailers = [
      'foo: bar',
      'abc: 123'
    ]
    self.assertEqual(response.trailers.entries, [
      'foo: bar',
      'abc: 123'
    ])

  def testHttpResponseBodyUpdate(self):
    response = CaptureHttpResponse({
      'request': {
        'method': 'GET',
        'path': '/',
        'protocol': 'HTTP/1.1',
      },
      'code': 200,
      'message': 'OK',
      'protocol': 'HTTP/1.1',
    })
    response.body = 'Hello World'
    self.assertTrue(response.body.isText)
    self.assertEqual(response.body.payload, 'Hello World')

    response.body = {
      'foo': 'bar',
      'abc': 123
    }
    self.assertTrue(response.body.isText)
    self.assertEqual(response.body.payload, '{"foo": "bar", "abc": 123}')

    response.body = b'\x01\x02\x03\x04'
    self.assertTrue(response.body.isBinary)
    self.assertEqual(response.body.payload, b'\x01\x02\x03\x04')


  def testHttpResponseContentType(self):
    response = CaptureHttpResponse({
      'request': {
        'method': 'GET',
        'path': '/',
        'protocol': 'HTTP/1.1',
      },
      'code': 200,
      'message': 'OK',
      'protocol': 'HTTP/1.1',
      'headers': [
        'content-type: text/palin; charset=utf-8',
      ],
    })
    self.assertEqual(response.contentType, 'text/palin; charset=utf-8')
    self.assertEqual(response.mime, 'text/palin')

  def testHttpResponseSerialize(self):
    data = {
      'request': {
        'method': 'GET',
        'path': '/',
        'protocol': 'HTTP/1.1',
        'headers': [],
        'body': {
          'type': 0,
          'payload': None
        },
        'trailers': []
      },
      'code': 200,
      'message': 'OK',
      'protocol': 'HTTP/1.1',
      'headers': [
        'foo: bar',
        'abc: 123',
        'hello: world'
      ],
      'body': {
        'type': 1,
        'payload': 'Hello World'
      },
      'trailers': []
    }
    response = CaptureHttpResponse(data)
    self.assertEqual(response.serialize(), data)

    response.code = 404
    response.headers.remove('foo')
    response.body = 'Reqable'
    response.trailers['abc'] = '123'
    self.assertEqual(response.serialize(), {
      'request': {
        'method': 'GET',
        'path': '/',
        'protocol': 'HTTP/1.1',
        'headers': [],
        'body': {
          'type': 0,
          'payload': None
        },
        'trailers': []
      },
      'code': 404,
      'message': 'OK',
      'protocol': 'HTTP/1.1',
      'headers': [
        'abc: 123',
        'hello: world'
      ],
      'body': {
        'type': 1,
        'payload': 'Reqable'
      },
      'trailers': [
        'abc: 123',
      ]
    })

if __name__ == '__main__':
  unittest.main()