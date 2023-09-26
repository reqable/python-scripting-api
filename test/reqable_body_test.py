import unittest

from reqable import CaptureHttpBody, CaptureHttpMultipartBody

class HttpBodyTest(unittest.TestCase):
  def testHttpBodyConstructor(self):
    body = CaptureHttpBody(0, None)
    self.assertEqual(body.type, 0)
    self.assertEqual(body.payload, None)

    body = CaptureHttpBody.of(None)
    self.assertEqual(body.type, 0)
    self.assertEqual(body.payload, None)

    body = CaptureHttpBody.of()
    self.assertEqual(body.type, 0)
    self.assertEqual(body.payload, None)

    body = CaptureHttpBody.parse({
      'type': 0,
      'payload': None
    })
    self.assertEqual(body.type, 0)
    self.assertEqual(body.payload, None)

    body = CaptureHttpBody(1, 'Hello World')
    self.assertEqual(body.type, 1)
    self.assertEqual(body.payload, 'Hello World')

    body = CaptureHttpBody.of('Hello World')
    self.assertEqual(body.type, 1)
    self.assertEqual(body.payload, 'Hello World')

    body = CaptureHttpBody.parse({
      'type': 1,
      'payload': 'Hello World'
    })
    self.assertEqual(body.type, 1)
    self.assertEqual(body.payload, 'Hello World')

    body = CaptureHttpBody(2, b'\x01\x02\x03\x04')
    self.assertEqual(body.type, 2)
    self.assertEqual(body.payload, b'\x01\x02\x03\x04')

    body = CaptureHttpBody.of(b'\x01\x02\x03\x04')
    self.assertEqual(body.type, 2)
    self.assertEqual(body.payload, b'\x01\x02\x03\x04')

    body = CaptureHttpBody.parse({
      'type': 2,
      'payload': 'data/body_binary.bin'
    })
    self.assertEqual(body.type, 2)
    self.assertEqual(body.payload, b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A')

    body = CaptureHttpBody.parse({
      'type': 3,
      'payload': [
        {
          'headers': [
            'foo: bar',
            'abc: 123',
            'hello: world'
          ],
          'body': {
            'type': 1,
            'payload': 'Hello World'
          }
        }
      ]
    })
    self.assertEqual(body.type, 3)
    self.assertEqual(len(body.payload), 1)
    self.assertTrue(type(body.payload[0]) is CaptureHttpMultipartBody)

    body = CaptureHttpBody.of({
      'foo': 'bar',
      'abc': 123,
      'hello': 'world'
    })
    self.assertEqual(body.type, 1)
    self.assertEqual(body.payload, '{"foo": "bar", "abc": 123, "hello": "world"}')


  def testHttpBodyNone(self):
    body = CaptureHttpBody()
    self.assertEqual(len(body), 0)
    self.assertEqual(str(body), '')
    self.assertTrue(body.isNone)
    self.assertFalse(body.isText)
    self.assertFalse(body.isBinary)
    self.assertFalse(body.isMultipart)

    self.assertEqual(body.serialize(), {
      'type': 0,
      'payload': None
    })


  def testHttpBodyText(self):
    body = CaptureHttpBody.of('Hello World')
    self.assertEqual(len(body), len('Hello World'))
    self.assertEqual(str(body), 'Hello World')
    self.assertFalse(body.isNone)
    self.assertTrue(body.isText)
    self.assertFalse(body.isBinary)
    self.assertFalse(body.isMultipart)

    body.replace('Hello', 'Hi')
    self.assertEqual(body.payload, 'Hi World')
    self.assertEqual(body.serialize(), {
      'type': 1,
      'payload': 'Hi World'
    })


  def testHttpBodyJson(self):
    body = CaptureHttpBody.of({"foo":"bar","abc":123,"hello":"world"})
    body.jsonify()
    self.assertEqual(body['foo'], 'bar')
    self.assertEqual(body['abc'], 123)
    self.assertEqual(body['hello'], 'world')
    body['foo'] = 'good'
    self.assertEqual(body['foo'], 'good')
    body['python'] = {
      'hi': 'reqable',
    }
    self.assertEqual(body['python'], {
      'hi': 'reqable',
    })
    body['python']['hi'] = 'megatron'
    self.assertEqual(body['python'], {
      'hi': 'megatron',
    })
    self.assertEqual(str(body), '{"foo": "good", "abc": 123, "hello": "world", "python": {"hi": "megatron"}}')
    self.assertEqual(body.serialize(), {
      'type': 1,
      'payload': '{"foo": "good", "abc": 123, "hello": "world", "python": {"hi": "megatron"}}'
    })


  def testHttpBodyBinary(self):
    body = CaptureHttpBody.parse({
      'type': 2,
      'payload': 'data/body_binary.bin'
    })
    self.assertFalse(body.isNone)
    self.assertFalse(body.isText)
    self.assertTrue(body.isBinary)
    self.assertFalse(body.isMultipart)
    self.assertEqual(len(body), 8)
    self.assertEqual(body[0], 0x89)
    self.assertEqual(body[1], 0x50)
    # TODO test serialize


  def testHttpBodyMultipart(self):
    data = {
      'type': 3,
      'payload': [
        {
          'headers': [
            'foo: bar',
            'abc: 123',
            'hello: world'
          ],
          'body': {
            'type': 1,
            'payload': 'Hello World'
          }
        }
      ]
    }
    body = CaptureHttpBody.parse({
      'type': 3,
      'payload': [
        {
          'headers': [
            'foo: bar',
            'abc: 123',
            'hello: world'
          ],
          'body': {
            'type': 1,
            'payload': 'Hello World'
          }
        }
      ]
    })
    self.assertFalse(body.isNone)
    self.assertFalse(body.isText)
    self.assertFalse(body.isBinary)
    self.assertTrue(body.isMultipart)
    self.assertEqual(len(body), 1)
    self.assertTrue(isinstance(body[0], CaptureHttpMultipartBody))
    self.assertEqual(body[0].headers.entries, [
      'foo: bar',
      'abc: 123',
      'hello: world'
    ])
    self.assertEqual(body[0].type, 1)
    self.assertEqual(body[0].payload, 'Hello World')
    self.assertRaises(Exception, str, body)
    for part in body:
      self.assertEqual(body[0], part)
    self.assertEqual(body.serialize(), data)

  def testHttpBodyUpdate(self):
    body = CaptureHttpBody()
    body.text('Hello World')
    self.assertEqual(body.type, 1)
    self.assertEqual(body.payload, 'Hello World')

    body.textFromFile('data/body_text.json')
    self.assertEqual(body.type, 1)
    self.assertEqual(body.payload, '{\n  "foo": "bar",\n  "abc": 123,\n  "hello": "world"\n}')

    body.file('data/body_binary.bin')
    self.assertEqual(body.type, 2)
    self.assertEqual(body.payload, b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A')

    body.binary('data/body_binary.bin')
    self.assertEqual(body.type, 2)
    self.assertEqual(body.payload, b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A')
    body.binary(b'\x01\x02\x03\x04')
    self.assertEqual(body.type, 2)
    self.assertEqual(body.payload, b'\x01\x02\x03\x04')

    body.multiparts([
      CaptureHttpMultipartBody.text('Hi World'),
      CaptureHttpMultipartBody.file('data/body_binary.bin')
    ])
    self.assertEqual(body.type, 3)
    self.assertTrue(body.payload[0].isText)
    self.assertEqual(body.payload[0].payload, 'Hi World')
    self.assertTrue(body.payload[1].isBinary)
    self.assertEqual(body.payload[1].payload, b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A')

    body.none()
    self.assertEqual(body.type, 0)
    self.assertEqual(body.payload, None)

if __name__ == '__main__':
  unittest.main()