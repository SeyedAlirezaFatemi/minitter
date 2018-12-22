from django.contrib.sessions.models import Session
from django.http import HttpResponse

from .models import LoggedInUser, Request, UnAuthorizedRequests
from datetime import datetime, timedelta


class OneSessionPerUser:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            current_session_key = request.user.logged_in_user.session_key
            if current_session_key and current_session_key != request.session.session_key:
                Session.objects.get(session_key=current_session_key).delete()

            request.user.logged_in_user.session_key = request.session.session_key
            request.user.logged_in_user.save()

        response = self.get_response(request)
        return response


class ManyRequests:
    def __init__(self, get_response, h, n, m):
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
        if req.num_of_requests >= self.n:
            req.black_list = True
        if req and req.black_list:
            return HttpResponse("oops! too many responses!")
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
        if req.num_of_requests >= self.n:
            req.black_list = True
        if req and req.black_list:
            return HttpResponse("oops! too many unauthorized responses!")
        req.save()
        response = self.get_response(request)
        return response


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_client_browser(request):
    return request.META['HTTP_USER_AGENT']


def get_request_time(request):
    return request.session['last_touch']
