from django.shortcuts import redirect
from requests import session

def auth_middleware(get_response):
    def middleware(request, *args, **kwargs):
        if not request.session.get('admin_id'):
            return redirect('/lms-admin/sign-in/')
            
        response = get_response(request, *args, **kwargs)     

        return response

    return middleware