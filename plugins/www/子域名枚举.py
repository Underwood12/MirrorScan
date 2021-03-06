import socket

def assign(service, arg):
    if service == 'dns':
        return True, arg

def audit(arg):
    if not _G['subdomain']:
        return
    socket.setdefaulttimeout(5)
    domain = util.get_domain_root(arg)
    tlds = [pro + '.' + domain for pro in util.list_from_file('database/sub_domain.txt')]
    try:
        socket.gethostbyname('stackoverflowsb.' + domain)
    except Exception:
        for hostname in tlds:
            try:
                ip = socket.gethostbyname(hostname)
                if not hostname.startswith('www.'):
                    security_info('subdomain discover: %s' % hostname)
                    task_push('www', 'http://%s/' % hostname, target=hostname)
                    task_push('ip', ip, target=hostname)
            except Exception:
                pass