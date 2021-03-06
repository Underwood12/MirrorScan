# -*- coding:utf-8 -*-

import leancloud

def authentication(controller):
    def warpper(cls, *args, **kwargs):
        user = cls.get_secure_cookie('user')
        uhash = cls.get_secure_cookie('hash')
        if user and uhash:
            return controller(cls, *args, **kwargs)
        else:
            cls.redirect('/login')
    return warpper

def protect(controller):
    def warpper(cls, *args, **kwargs):
        if cls.request.headers.get('User-Agent') == 'Python-urllib/2.7':
            return controller(cls, *args, **kwargs)
        else:
            userQuery = leancloud.Query('mUser')
            userQuery.equal_to('uhash', args[0])
            if userQuery.find():
                userInfo = userQuery.first()
                userInfo.set('block', True)
                userInfo.set('group', '黑名单用户')
                userInfo.save()
                cls.write('您已经被封禁')
            else:
                cls.write('拒绝访问')
    return warpper