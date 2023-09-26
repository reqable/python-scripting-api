import json
import uuid
import os
from email.message import EmailMessage
from typing import Union, List, Tuple, Dict

class CaptureContext:
  def __init__(self, json: dict):
    self._url = json['url']
    self._scheme = json['scheme']
    self._host = json['host']
    self._port = json['port']
    self._cid = json['cid']
    self._ctime = json['ctime']
    self._sid = json['sid']
    self._stime = json['stime']
    self.shared = json.get('shared')

  def __str__(self):
    return self.toJson()

  def __add__(self, other) -> str:
    return str(self) + other

  def __radd__(self, other) -> str:
    return other + str(self)

  # Request full URL.
  @property
  def url(self) -> str:
    return self._url

  # URL scheme, http or https.
  @property
  def scheme(self) -> str:
    return self._scheme

  # URL host.
  @property
  def host(self) -> str:
    return self._host

  # URL port
  @property
  def port(self) -> int:
    return self._port

  # TCP connection id.
  @property
  def cid(self) -> int:
    return self._cid

  # TCP connection establised timestamp.
  @property
  def ctime(self) -> int:
    return self._ctime

  # HTTP session id.
  @property
  def sid(self) -> int:
    return self._sid

  # HTTP session timestamp.
  @property
  def stime(self) -> int:
    return self._stime

  # HTTP uniqued id.
  @property
  def uid(self) -> str:
    return f"{self.ctime}-{self.cid}-{self.sid}"

  def toJson(self) -> str:
    return json.dumps({
      'url': self._url,
      'scheme': self._scheme,
      'host': self._host,
      'port': self._port,
      'cid': self._cid,
      'ctime': self._ctime,
      'sid': self._sid,
      'stime': self._stime,
      'shared': self.shared,
    })

class CaptureHttpQueries:

  def __init__(self, entries = None):
    if entries is None:
      self._entries = []
    else:
      self._entries = entries

  @classmethod
  def parse(cls, query: str):
    if query is None:
      entries = []
    else:
      from urllib.parse import parse_qsl
      entries = parse_qsl(query, keep_blank_values = True)
    return cls(entries)

  @classmethod
  def of(cls, data):
    if isinstance(data, str):
      return cls.parse(data)
    elif isinstance(data, list) and all(isinstance(t, tuple) and isinstance(t[0], str) and
        isinstance(t[1], str) for t in data):
      return cls(data)
    elif isinstance(data, dict) and all(isinstance(key, str) and isinstance(value, str)
        for key, value in data.items()):
      entries = []
      for key, value in data.items():
        entries.append((key, value))
      return cls(entries)
    raise Exception('Unsupported query parameters data type')

  def __len__(self):
    return len(self._entries)

  def __iter__(self):
    return iter(self._entries)

  def __str__(self):
    return str(self._entries)

  def __add__(self, other):
    return str(self) + other

  def __radd__(self, other):
    return other + str(self)

  def __getitem__(self, name: Union[str, int]) -> Union[str, None]:
    if isinstance(name, int):
      return self._entries[name]
    index = self.index(name)
    if index >= 0:
      return self._entries[index][1]
    return None

  def __setitem__(self, name: str, value: str):
    if len(name) >= 1:
      index = self.index(name)
      if index >= 0:
        self._entries[index] = (name, value)
      else:
        self._entries.append((name, value))

  # Add a query paramater with name and value.
  def add(self, name: str, value: str):
    if not name:
      return
    self._entries.append((name, value))

  # Remove query paramaters by name, all the matched query paramaters will be removed.
  def remove(self, name: str):
    for index in reversed(self.indexes(name)):
      self._entries.pop(index)

  # Find the first query paramater index by name. If no matched, returns -1.
  def index(self, name: str) -> int:
    for i in range(len(self._entries)):
      if self._entries[i][0] == name:
        return i
    return -1

  # Find query paramater indexes by name.
  def indexes(self, name: str) -> List[int]:
    indexes = []
    for i in range(len(self._entries)):
      if self._entries[i][0] == name:
        indexes.append(i)
    return indexes

  # Remove all query paramaters.
  def clear(self):
    self._entries.clear()

  # Concat all the query paramaters to a query string.
  def concat(self, encode: bool = True) -> str:
    if encode:
      from urllib.parse import urlencode, quote
      # Keep asterish to be safe
      return urlencode(self._entries, safe='*', quote_via=quote)
    else:
      return '&'.join(['='.join(entry) for entry in self._entries])

  # Get all query paramaters.
  @property
  def entries(self) -> List[Tuple[str, str]]:
    return self._entries

  def serialize(self) -> str:
    return self.concat()

class CaptureHttpHeaders:

  def __init__(self, entries = None):
    self._entries = ([] if entries is None else entries)

  @classmethod
  def of(cls, data):
    if isinstance(data, list) and all(isinstance(e, str) for e in data):
      return cls(data)
    elif isinstance(data, list) and all(isinstance(t, tuple) and isinstance(t[0], str) and
        isinstance(t[1], str) for t in data):
      entries = []
      for t in data:
        entries.append(f'{t[0]}: {t[1]}')
      return cls(entries)
    elif isinstance(data, dict) and all(isinstance(key, str) and isinstance(value, str)
        for key, value in data.items()):
      entries = []
      for key, value in data.items():
        entries.append(f'{key}: {value}')
      return cls(entries)
    raise Exception('Unsupported headers data type')

  def __len__(self):
    return len(self._entries)

  def __iter__(self):
    return iter(self._entries)

  def __str__(self):
    return str(self._entries)

  def __add__(self, other):
    return str(self) + other

  def __radd__(self, other):
    return other + str(self)

  def __getitem__(self, name) -> Union[str, None]:
    if isinstance(name, int):
      return self._entries[name]
    index = self.index(name)
    if index >= 0:
      return self._entries[index][len(name) + 2:]
    return None

  def __setitem__(self, name: str, value: str):
    if len(name) >= 1:
      index = self.index(name)
      if index >= 0:
        self._entries[index] = name + ': ' + value
      else:
        self._entries.append(name + ': ' + value)

  # Add a header line with name and value.
  def add(self, name: str, value: str):
    if not name:
      return
    self._entries.append(name + ': ' + value)

  # Remove headers by name, all the matched headers will be removed.
  def remove(self, name: str):
    if isinstance(name, str):
      for index in reversed(self.indexes(name)):
        self._entries.pop(index)

  # Find the first header index by name. If no matched, returns -1.
  def index(self, name: str) -> int:
    for i in range(len(self._entries)):
      if self._entries[i].lower().startswith(name.lower() + ': '):
        return i
    return -1

  # Find header indexes by name.
  def indexes(self, name: str) -> List[int]:
    indexes = []
    for i in range(len(self._entries)):
      if self._entries[i].lower().startswith(name.lower() + ': '):
        indexes.append(i)
    return indexes

  # Remove all headers.
  def clear(self):
    self._entries.clear()

  # Get all header lines.
  @property
  def entries(self) -> List[str]:
    return self._entries

  def serialize(self) -> List[str]:
    return self._entries

class CaptureHttpBody:

  __type_none = 0
  __type_text = 1
  __type_binary = 2
  __type_multipart = 3

  def __init__(self, type: int = 0, payload = None):
    self._type = type
    self._payload = payload

  @classmethod
  def of(cls, data = None):
    if isinstance(data, str):
      type = cls.__type_text
      payload = data
    elif isinstance(data, dict):
      type = cls.__type_text
      payload = json.dumps(data)
    elif isinstance(data, bytes):
      type = cls.__type_binary
      payload = data
    elif isinstance(data, CaptureHttpBody):
      return data
    else:
      type = cls.__type_none
      payload = None
    return cls(type, payload)

  @classmethod
  def parse(cls, dict):
    if dict == None:
      return cls(cls.__type_none, None)
    type = dict['type']
    if type == cls.__type_none:
      payload = None
    elif type == cls.__type_text:
      payload = dict['payload']
    elif type == cls.__type_binary:
      payload = dict['payload']
      if isinstance(payload, str):
        with open(payload, mode = 'rb') as file:
          payload = file.read()
      elif isinstance(payload, bytes):
        payload = payload
      else:
        payload = bytes()
    elif type == cls.__type_multipart:
      payload = []
      for multipart in dict['payload']:
        payload.append(CaptureHttpMultipartBody(multipart))
    return cls(type, payload)

  def __repr__(self):
    if self.isMultipart:
      return f'Multipart {len(self._payload)} body'
    else:
      return str(self)

  def __add__(self, other):
    return str(self) + other

  def __radd__(self, other):
    return other + str(self)

  def __len__(self):
    return 0 if self.isNone else len(self._payload)

  def __iter__(self):
    return iter(self._payload)

  def __str__(self):
    if self.isNone:
      return ''
    elif self.isText:
      if isinstance(self._payload, str):
        return self._payload
      else:
        return json.dumps(self._payload)
    elif self.isBinary:
      return str(self._payload)
    else:
      raise Exception('Unsupported str for multipart body')

  # Deprecated! Use isNone/isText/isBinary/isMultipart instead.
  # Return the body type.
  @property
  def type(self) -> int:
    return self._type

  # The http body payload.
  @property
  def payload(self) -> Union[None, str, bytes, List]:
    return self._payload

  # Determine whether the body is None.
  @property
  def isNone(self) -> bool:
    return self._type is CaptureHttpBody.__type_none

  # Determine whether the body is a text string.
  @property
  def isText(self) -> bool:
    return self._type is CaptureHttpBody.__type_text

  # Determine whether the body is a binary bytes.
  @property
  def isBinary(self) -> bool:
    return self._type is CaptureHttpBody.__type_binary

  # Determine whether the body is a multipart type.
  @property
  def isMultipart(self) -> bool:
    return self._type is CaptureHttpBody.__type_multipart

  # Set the body to None.
  def none(self):
    self._type = CaptureHttpBody.__type_none
    self._payload = None

  # Set the body to a text string.
  def text(self, value: str):
    self._type = CaptureHttpBody.__type_text
    self._payload = value

  # Set the body to a specified file content, the file content must be a text string.
  def textFromFile(self, value: str):
    with open(value, mode = 'r', encoding='UTF-8') as file:
      self._payload = file.read()
    self._type = CaptureHttpBody.__type_text

  # Set the body to the specified file content, the file content must be a binary bytes.
  def file(self, value: str):
    if isinstance(value, str):
      self.binary(value)

  # Set the body to binary bytes.
  def binary(self, value: Union[str, bytes]):
    if isinstance(value, str):
      self._type = CaptureHttpBody.__type_binary
      with open(value, mode = 'rb') as file:
        self._payload = file.read()
    if isinstance(value, bytes):
      self._type = CaptureHttpBody.__type_binary
      self._payload = value

  # Set the body to binary bytes.
  def multiparts(self, value: list):
    if not isinstance(value, list):
      return
    payload = []
    for multipart in value:
      if isinstance(multipart, CaptureHttpMultipartBody):
        payload.append(multipart)
    if len(payload) == 0:
      return
    self._type = CaptureHttpBody.__type_multipart
    self._payload = payload

  # Convert the body content to a json dict.
  def jsonify(self):
    if self.isText:
      self._payload = json.loads(self._payload)

  # Replace old string to a new one. The body type must be a text.
  def replace(self, old: str, new: str, count: int = -1):
    if self.isText and isinstance(self._payload, str):
      self._payload = self._payload.replace(old, new, count)

  # If the body type is a json dict, returns the value. Note: you must call jsonify() before this.
  # If the body type is binary, returns the value at the index.
  # If the body type is multipart, returns the part at the index.
  def __getitem__(self, name: Union[str, int]):
    if self.isText:
      if not isinstance(self._payload, dict):
        raise Exception('Did you forget to call `jsonify()` before operating json dict?')
      return self._payload[name]
    if self.isBinary and isinstance(name, int):
      return self._payload[name]
    if self.isMultipart and isinstance(name, int):
      return self._payload[name]
    return None

  # Set the json dict value by name. Note: you must call jsonify() before this.
  def __setitem__(self, name: str, value):
    if self.isText:
      if not isinstance(self._payload, dict):
        raise Exception('Did you forget to call `jsonify()` before operating json dict?')
      self._payload[name] = value

  # Write the body content to a file.
  def writeFile(self, path: str):
    if self.isText:
      with open(path, "w", encoding='UTF-8') as file:
        if isinstance(self._payload, str):
          file.write(self._payload)
        else:
          file.write(json.dumps(self._payload))
    elif self.isBinary:
      with open(path, "wb") as file:
        file.write(self._payload)
    elif self.isMultipart:
      raise Exception('Write a multipart body to file is supported!')

  def serialize(self):
    type = self._type
    if self.isNone:
      payload = None
    elif self.isText:
      if isinstance(self._payload, str):
        if len(self._payload) == 0:
          payload = None
          type = CaptureHttpBody.__type_none
        else:
          payload = self._payload
      else:
        payload = json.dumps(self._payload)
    elif self.isBinary:
      if len(self._payload) == 0:
        type = CaptureHttpBody.__type_none
        payload = None
      else:
        payload = os.path.join(os.getcwd(), 'tmp-' + str(uuid.uuid4()))
        with open(payload, 'wb') as file:
          file.write(self._payload)
    elif self.isMultipart:
      if len(self._payload) == 0:
        type = CaptureHttpBody.__type_none
        payload = None
      else:
        payload = []
        for multipart in self._payload:
          payload.append(multipart.serialize())
    return {
      'type': type,
      'payload': payload,
    }

class CaptureHttpMultipartBody(CaptureHttpBody):

  def __init__(self, json: dict):
    self._headers = CaptureHttpHeaders(json['headers'])
    body = CaptureHttpBody.parse(json['body'])
    super().__init__(body.type, body.payload)

  def _concatDisposition(name: str, filename: str, type: str):
    if name != '' and filename != '':
      return f'{type}; name="{name}"; filename="{filename}"'
    elif name != '':
      return f'{type}; name="{name}"'
    elif filename != '':
      return f'{type}; filename="{filename}"'
    return None

  @classmethod
  def text(cls, text: str, name: str = '', filename: str = '', headers = None, type = 'form-data'):
    if headers is None:
      headers = []
    headers.append(f'content-length: {len(text)}')
    disposition = CaptureHttpMultipartBody._concatDisposition(name, filename, type)
    if disposition is not None:
      headers.append(f'content-disposition: {disposition}')
    return cls({
      'headers': headers,
      'body': {
        'type': 1,
        'payload': text
      }
    })

  @classmethod
  def file(cls, file: str, name: str = '', filename: str = '', headers = None, type = 'form-data'):
    if headers is None:
      headers = []
    headers.append(f'content-length: {os.stat(file).st_size}')
    disposition = CaptureHttpMultipartBody._concatDisposition(name, filename, type)
    if disposition is not None:
      headers.append(f'content-disposition: {disposition}')
    return cls({
      'headers': headers,
      'body': {
        'type': 2,
        'payload': file
      }
    })

  # Get the part headers.
  @property
  def headers(self) -> CaptureHttpHeaders:
    return self._headers

  # Set the part headers.
  @headers.setter
  def headers(self, data: Union[List[str], List[Tuple[str, str]], Dict[str, str]]):
    self._headers = CaptureHttpHeaders.of(data)

  # Get the part name.
  @property
  def name(self) -> Union[str, None]:
    return self._getDispositionParamValue('name')

  # Set the part name.
  @name.setter
  def name(self, data: str):
    self._setDispositionParamValue('name', data)

  # Get the part filename.
  @property
  def filename(self) -> Union[str, None]:
    return self._getDispositionParamValue('filename')

  # Set the part filename.
  @filename.setter
  def filename(self,  data: str):
    self._setDispositionParamValue('filename', data)

  def serialize(self) -> dict:
    return {
      'headers': self._headers.serialize(),
      'body': super().serialize()
    }

  def _getDispositionParamValue(self, param):
    disposition = self._headers['content-disposition']
    if disposition is None:
      return None
    message = EmailMessage()
    message.add_header('content-disposition', disposition)
    return message.get_param(param, header='content-disposition')

  def _setDispositionParamValue(self, param, value):
    disposition = self._headers['content-disposition']
    if disposition is None:
      return
    message = EmailMessage()
    message.add_header('content-disposition', disposition)
    message.set_param(param, value, header='content-disposition')
    self._headers['content-disposition'] = message.get('content-disposition')

class CaptureHttpRequest:
  def __init__(self, json):
    self._method = json['method']
    self._protocol = json['protocol']
    self._headers = CaptureHttpHeaders(json.get('headers'))
    self._body = CaptureHttpBody.parse(json.get('body'))
    self._trailers = CaptureHttpHeaders(json.get('trailers'))
    from urllib.parse import urlparse
    url = urlparse(json['path'])
    self._path = url.path
    self._queries = CaptureHttpQueries.parse(url.query)

  def __str__(self):
    return self.toJson()

  def __add__(self, other):
    return str(self) + other

  def __radd__(self, other):
    return other + str(self)

  # Get the request http protocol, such as HTTP/1.1, h2.
  @property
  def protocol(self) -> str:
    return self._protocol

  # Get the request http method, such as GET, POST.
  @property
  def method(self) -> str:
    return self._method

  # Set the request http method.
  @method.setter
  def method(self, data) -> str:
    if isinstance(data, str) and data != '':
      self._method = data
    else:
      raise Exception('Request method must be a non-empty string.')

  # Get the request path.
  @property
  def path(self) -> str:
    return self._path

  # Set the request path.
  @path.setter
  def path(self, data: str):
    if isinstance(data, str) and data != '':
      self._path = data
    else:
      raise Exception('Request path must be a non-empty string.')

  # Get the request query paramaters.
  @property
  def queries(self) -> CaptureHttpQueries:
    return self._queries

  # Set the request query paramaters.
  @queries.setter
  def queries(self, data: Union[str, List[Tuple[str, str]], Dict[str, str]]):
    self._queries = CaptureHttpQueries.of(data)

  # Get the request headers.
  @property
  def headers(self) -> CaptureHttpHeaders:
    return self._headers

  # Set the request headers.
  @headers.setter
  def headers(self, data: Union[List[str], List[Tuple[str, str]], Dict[str, str]]):
    self._headers = CaptureHttpHeaders.of(data)

  # Get the request trailers. Note that the implementation of this function is incomplete, please do not use it.
  @property
  def trailers(self) -> CaptureHttpHeaders:
    return self._trailers

  # Set the request trailers. Note that the implementation of this function is incomplete, please do not use it.
  @trailers.setter
  def trailers(self, data: Union[List[str], List[Tuple[str, str]], Dict[str, str]]):
    self._trailers = CaptureHttpHeaders.of(data)

  # Get the request body.
  @property
  def body(self) -> CaptureHttpBody:
    return self._body

  # Set the request body.
  @body.setter
  def body(self, data: Union[str, bytes, dict, CaptureHttpBody]):
    self._body = CaptureHttpBody.of(data)

  # Get the request content type from headers.
  @property
  def contentType(self) -> Union[str, None]:
    return self._headers['content-type']

  # Get the request mime type from headers.
  @property
  def mime(self) -> Union[str, None]:
    contentType = self._headers['content-type']
    if contentType == None:
      return None
    message = EmailMessage()
    message.add_header('content-type', contentType)
    return message.get_content_type()

  # Serialize the request fields to a dict.
  def serialize(self) -> dict:
    if len(self.queries) == 0:
      path = self.path
    else:
      path = self.path + '?' + self.queries.serialize()
    return {
      'method': self.method,
      'path': path,
      'protocol': self._protocol,
      'headers': self._headers.serialize(),
      'body': self._body.serialize(),
      'trailers': self._trailers.serialize(),
    }

  def toJson(self) -> str:
    return json.dumps(self.serialize())

class CaptureHttpResponse:
  def __init__(self, json):
    self._request = CaptureHttpRequest(json['request'])
    self._code = json['code']
    self._message = json['message']
    self._protocol = json['protocol']
    self._headers = CaptureHttpHeaders(json.get('headers'))
    self._body = CaptureHttpBody.parse(json.get('body'))
    self._trailers = CaptureHttpHeaders(json.get('trailers'))

  def __str__(self):
    return self.toJson()

  def __add__(self, other):
    return str(self) + other

  def __radd__(self, other):
    return other + str(self)

  # Get the request informations.
  @property
  def request(self) -> CaptureHttpRequest:
    return self._request

  # Get the response status code.
  @property
  def code(self) -> int:
    return self._code

  # Set the response status code.
  @code.setter
  def code(self, data: int):
    if isinstance(data, int) and data >= 100 and data <= 600:
      self._code = data
    else:
      raise Exception('Response code must be a int (100 - 600).')

  # Get the response status message, maybe None.
  @property
  def message(self) -> Union[str, None]:
    return self._message

  # Get the response http protocol, such as HTTP/1.1, h2.
  @property
  def protocol(self) -> str:
    return self._protocol

  # Get the response headers.
  @property
  def headers(self) -> CaptureHttpHeaders:
    return self._headers

  # Set the response headers.
  @headers.setter
  def headers(self, data: Union[List[str], List[Tuple[str, str]], Dict[str, str]]):
    self._headers = CaptureHttpHeaders.of(data)

  # Set the response trailers. Note that the implementation of this function is incomplete, please do not use it.
  @property
  def trailers(self) -> CaptureHttpHeaders:
    return self._trailers

  # Get the response trailers. Note that the implementation of this function is incomplete, please do not use it.
  @trailers.setter
  def trailers(self, data: Union[List[str], List[Tuple[str, str]], Dict[str, str]]):
    self._trailers = CaptureHttpHeaders.of(data)

  # Get the response body.
  @property
  def body(self) -> CaptureHttpBody:
    return self._body

  # Set the response body.
  @body.setter
  def body(self, data: Union[str, bytes, dict, CaptureHttpBody]):
    self._body = CaptureHttpBody.of(data)

  # Get the response content type from headers.
  @property
  def contentType(self) -> Union[str, None]:
    return self._headers['content-type']

  # Get the response mime type from headers.
  @property
  def mime(self) -> Union[str, None]:
    contentType = self._headers['content-type']
    if contentType == None:
      return None
    message = EmailMessage()
    message.add_header('content-type', contentType)
    return message.get_content_type()

  # Serialize the response fields to a dict.
  def serialize(self) -> dict:
    return {
      'request': self._request.serialize(),
      'code': self.code,
      'message': self._message,
      'protocol': self._protocol,
      'headers': self._headers.serialize(),
      'body': self._body.serialize(),
      'trailers': self._trailers.serialize(),
    }

  def toJson(self) -> str:
    return json.dumps(self.serialize())