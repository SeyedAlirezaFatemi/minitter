from datetime import timedelta

from django.contrib.sessions.models import Session
from django.http import HttpResponse

from twitter.information_gathering import get_client_ip, get_request_time
from .models import Request, UnAuthorizedRequests


class OneSessionPerUser:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            old_session_key = request.user.logged_in_user.session_key
            # Find the current session key
            current_session_key = request.session.session_key
            if old_session_key and old_session_key != current_session_key:
                # Delete the old session key if it exists
                try:
                    old_session = Session.objects.get(session_key=old_session_key)
                except Session.DoesNotExist:
                    pass
                else:
                    old_session.delete()

            request.user.logged_in_user.session_key = current_session_key
            request.user.logged_in_user.save()

        response = self.get_response(request)
        return response


class ManyRequests:
    def __init__(self, get_response, h, n):
        self.h = h
        self.n = n
        self.get_response = get_response

    def __call__(self, request):
        ip_address = get_client_ip(request)
        touch_time = get_request_time(request)
        req = Request.objects.filter(ip_address=ip_address)
        if req and not req.black_list:
            duration = touch_time - req.last_request_time
            if duration > timedelta(self.h):
                req.num_of_requests += 1
            else:
                req.num_of_requests = 1
            req.last_request_time = touch_time
        if not req:
            req = Request(ip_address=ip_address, last_request_time=touch_time)
        if req and req.num_of_requests >= self.n:
            req.black_list = True
        if req and req.black_list:
            return HttpResponse("Hell NO! Too many requests!")
        req.save()

        response = self.get_response(request)
        return response


class HandleUnAuthorizedRequests:
    def __init__(self, get_response, n):
        self.n = n
        self.get_response = get_response

    def __call__(self, request):
        ip_address = get_client_ip(request)
        req = UnAuthorizedRequests.objects.filter(ip_address=ip_address)
        if req and not req.black_list and not request.user.is_authenticated:
            req.num_of_requests += 1
        if not req and not request.user.is_authenticated:
            req = Request(ip_address=ip_address, user=request.user)
        if req and req.num_of_requests >= self.n:
            req.black_list = True
        if req and req.black_list:
            return HttpResponse("Hell NO! Too many unauthorized requests!")
        req.save()
        response = self.get_response(request)
        return response
