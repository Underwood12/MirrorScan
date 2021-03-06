from re import findall,search,I

def plus(msg):
    security_info(msg)

def secure(cookie):
    if not search(r'secure;',cookie,I):
        plus('Cookie without Secure flag set')

def httponly(cookie):
    if not search(r'httponly;',cookie,I):
        plus('Cookie without HttpOnly flag set')

def domain(cookie):
    if search(r'domain\=\S*',cookie,I):
        domain = findall(r'domain\=(.+?);',cookie,I)
        if domain:
            plus('Session Cookie are valid only at Sub/Domain: %s'%domain[0])

def path(cookie):
    if search(r'path\=\S*',cookie,I):
        path = findall(r'path\=(.+?);',cookie,I)
        if path:
            plus('Session Cookie are valid only on that Path: %s'%path[0])

def multiple(cookie):
    if search(r'(.+?)\=\S*;',cookie,I):
        cookie_sessions = findall(r'(.+?)\=\S*;',cookie,I)
        for cs in cookie_sessions:
            if cs not in ['domain','path','expires']:
                plus('Cookie Header contains multiple cookies')
                break

def x_xss(headers):
    if 'x-xss-protection' not in headers:
        plus('X-XSS-Protection header missing')

def x_frame(headers):
    if 'x-frame-options' not in headers:
        plus('Clickjacking: X-Frame-Options header missing')

def content_type(headers):
    if 'content-type' not in headers:
        plus('Content-Type header missing')

def sts(headers):
    if 'strict-transport-security' not in headers:
        plus('Strict-Transport-Security header missing')

def x_content(headers):
    if 'x-content-type-options' not in headers:
        plus('X-Content-Type-Options header missing')

def assign(service, arg):
    if service == "www":
        return True, arg

def audit(arg):
    code, head, res, err, _ = curl.curl2(arg)
    secure(head)
    httponly(head)
    domain(head)
    path(head)
    multiple(head)
    x_xss(head)
    x_frame(head)
    content_type(head)
    sts(head)
    x_content(head)
