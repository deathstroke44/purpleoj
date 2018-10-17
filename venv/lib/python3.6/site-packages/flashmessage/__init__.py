"""\
Flash message service
"""

import logging
import urllib
from bn import AttributeDict
from pipestack.pipe import Pipe, Marble
from httpkit.helper.cookie import set_cookie, get_cookie, unset_cookie, delete_cookie

log = logging.getLogger(__name__)

class FlashMessageError(Exception):
    pass

def encode_flash(message, message_type, allowed_message_types):
    """
    'message_type:good&message:asd%3D%2B%C3%A7'
    """
    if message_type not in allowed_message_types:
        raise FlashMessageError(
            "Expected message_type to be one of %s, not %r"%(
                str(allowed_message_types)[1:-1], 
                message_type
            )
        )
    result = urllib.urlencode(
        {
            'message_type': message_type, 
            'message': message.encode('utf8')
        }
    ).replace('=',':')
    if len(result) >= 4096:
        raise FlashMessageError(
            'The encoded flash message is too long to store in the cookie'
        )
    return result

def decode_flash(cookie_value):
    parts = cookie_value.split('&')
    result = {}
    for part in parts:
        k, v = part.split(':')
        result[k] = urllib.unquote(v.replace(':', '=').replace('+', ' ')).decode('utf8')
    return result


class FlashMessagePipe(Pipe):
    def __init__(self, *k, **p):
        self.cookie_name='flash'
        self.allowed_message_types=['good', 'normal', 'error']

        if not len(self.allowed_message_types):
            raise FlashMessageError(
                'You must have at least one allowed message type'
            )    
        Pipe.__init__(self, *k, **p)

    def enter(self, service):
        _set_cookie = []
        _remove_cookie = []

        def remove():
            _remove_cookie.append(True)

        def set(message, message_type=None):
            while(_set_cookie):
                _set_cookie.pop()
            if message_type is None: 
                message_type = self.allowed_message_types[0]
            elif message_type not in self.allowed_message_types:
                raise FlashMessageError(
                    'No such message type %r', message_type
                )    
            _set_cookie.append((message_type, message))

        def set_now(message, message_type=None):
            service[self.name]['message'] = message
            service[self.name]['message_type'] = message_type

        service[self.name] = AttributeDict(
            message=None,
            message_type=None,
            remove=remove,
            set=set,
            set_now=set_now,
            _set_cookie=_set_cookie,
            _remove_cookie=_remove_cookie,
        )

        # Populate service.flash
        cookie = get_cookie(service.environ.get('HTTP_COOKIE', ''), name=self.cookie_name)
        if cookie:
            result = decode_flash(cookie)
            service[self.name]['message'] = result['message']
            service[self.name]['message_type'] = result['message_type']

    def leave(self, service, error=False):
        #raise Exception("Remove...", service[name]['_remove_cookie'], service[name]['_set_cookie'])
        if service[self.name]['_set_cookie']:
            message_type, message = service[self.name]['_set_cookie'][0]
            # Remove any other cookie with the same name
            unset_cookie(self.cookie_name, header_list=service.http_response.header_list, path='/', domain=None)
            # Set the new one
            cookie = set_cookie(
                key=self.cookie_name, 
                value=encode_flash(
                    message,
                    message_type,
                    self.allowed_message_types
                ), 
            )
            service.http_response.header_list.append(dict(name='Set-Cookie', value=cookie))
            log.debug('Set flash message response cookie: %r', cookie)
        elif service[self.name]['_remove_cookie']:
            cookie = delete_cookie(self.cookie_name, path='/', domain=None)
            service.http_response.header_list.append(dict(name='Set-Cookie', value=cookie))
            log.debug('Removing flash response cookie: %r', cookie)
        else:
            log.debug('No flash message set')
