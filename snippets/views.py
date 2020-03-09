from django.shortcuts import render, redirect, get_object_or_404

from users.models import User
from .models import Snippet, Tag
# from .forms import


def test(request):
    return render(request, 'base.html', context={})
