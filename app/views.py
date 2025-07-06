"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
from rest_framework.decorators import api_view
from rest_framework.response import Response

# API 的實際操作的地方

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )
