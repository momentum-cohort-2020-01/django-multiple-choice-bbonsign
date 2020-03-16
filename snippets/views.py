from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector

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
def snippet_detail(request, snip_id):
    snippet = Snippet.objects.get(id=snip_id)
    context = {'snippet': snippet}
    return render(request, 'snippets/snippet_detail.html', context=context)


@login_required
def search(request):
    param = request.GET.get('q')
    public_snippets = Snippet.objects.filter(public=True)
    query = SearchQuery(param, search_type='plain')
    vector = SearchVector('language__name', weight='A')+SearchVector('title', weight='C')+SearchVector(
        'code',  weight='B')+SearchVector('description',  weight='D')+SearchVector('tags__name', weight='D')
    rank = SearchRank(vector, query)
    results = public_snippets.annotate(
        rank=rank).filter(rank__gte=0.05).order_by('-rank')
    return JsonResponse({
        "status": "ok",
        "snippets": prepare_snippets(results)
    })


@login_required
@csrf_exempt
@require_http_methods(['DELETE'])
def snippet_delete(request, snip_id):
    snippet = Snippet.objects.get(id=snip_id)
    if snippet.owner == request.user:
        snippet.delete()
        return JsonResponse({
            "status": "ok",
            "data": "Successfully deleted"
        })
    else:
        return JsonResponse({
            "status": "ok",
            "data": "You do not have permission to delete this snippet"
        })


@login_required
def snippet_edit(request, snip_id):
    snippet = Snippet.objects.get(id=snip_id)
    if snippet.owner != request.user:
        return redirect('/')
    if request.method == 'POST':
        form = SnippetForm(request.POST, instance=snippet)
        if form.is_valid():
            # snippet = form.save(commit=False)
            # snippet.owner = request.user
            snippet.save()
            return redirect(f'/snippet/{snip_id}')
    else:
        form = SnippetForm(instance=snippet)
        context = {'form': form}
        return render(request, 'snippets/form.html', context=context)


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


@login_required
def fork(request, snip_id):
    user = request.user
    snippet = Snippet.objects.get(id=snip_id)
    new_snippet = snippet
    new_snippet.pk = None
    new_snippet.owner = user
    new_snippet.parent = Snippet.objects.get(id=snip_id)
    new_snippet.save()
    snippet.copies += 1
    snippet.save()
    # context = {'snippet': new_snippet, 'message': "You're cloned snippet:"}
    # return render(request, 'snippets/snippet_detail.html', context=context)
    return redirect('snippet_detail', new_snippet.id)


@login_required
# @csrf_exempt
@require_GET
def all_public(request):
    snippets = Snippet.objects.filter(public=True)
    return JsonResponse({
        "status": "ok",
        "snippets": prepare_snippets(snippets)
    })


def prepare_snippets(snippet_set):
    snippets = {}
    for snippet in snippet_set:
        snippets[snippet.id] = prepare_snippet(snippet)
    return snippets


def prepare_snippet(snippet):
    return {
        'id': snippet.id,
        'title': snippet.title,
        'owner': snippet.owner.username,
        'code': snippet.code,
        'preview': snippet.preview,
        'description': snippet.description,
        'language': snippet.language.name,
        'copies': snippet.copies,
        'public': snippet.public,
        # 'parentId': snippet.parent.id
    }


@login_required
def tree(request, snip_id):
    snippet = Snippet.objects.get(id=snip_id)
    root = find_root(snippet)
    tree = descendent_tree(root)
    tree_string = family_tree(tree)
    print(tree_string)
    return JsonResponse({
        'status': 'ok',
        'tree': tree_string
    })


def find_root(snippet):
    current = snippet
    parent = snippet.parent
    while parent is not None:
        current = parent
        parent = parent.parent
    return current


def descendent_tree(snippet):
    if snippet is None:
        return None
    child_list = [descendent_tree(child) for child in snippet.children.all()]
    return {'snippet': prepare_snippet(snippet), 'children': child_list}


def print_tree(tree, n):
    if tree is None:
        return
    print('--'*n+str(tree['snippet']))
    for child in tree['children']:
        print_tree(child, n+1)


def show(tree, n):
    result = '   |'*n
    if n > 0:
        result = result + "--->"
    result = f"{result}{tree['snippet']['owner']}'s Snippet: {tree['snippet']['id']}\n"
    if len(tree['children']) > 0:
        for child in tree['children']:
            result += show(child, n+1)
    return result


def family_tree(tree):
    """
    Returns the string representation.
    """
    if tree['snippet'] is None:
        return ''
    else:
        result = show(tree, 0)
        return result