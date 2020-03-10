from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from users.models import User
from .models import Snippet, Tag
# from .forms import


@login_required
def user_home(request):
    user = request.user
    snippets = user.snippets.all()
    context = {'snippets': snippets}
    return render(request, 'snippets/user_home.html', context=context)
