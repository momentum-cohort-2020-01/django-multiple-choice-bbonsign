from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from users.models import User
from .models import Snippet, Tag
from .forms import SnippetForm


@login_required
def user_home(request):
    user = request.user
    snippets = user.snippets.all()
    context = {'snippets': snippets}
    return render(request, 'snippets/user_home.html', context=context)


@login_required
def add_snippet(request):
    if request.method == 'POST':
        form = SnippetForm(request.POST)
        if form.is_valid():
            snippet = form.save(commit=False)
            snippet.owner = request.user
            snippet.save()
            return redirect('user_home')
    else:
        form = SnippetForm()
        context = {'form': form}
        return render(request, 'snippets/form.html', context=context)
