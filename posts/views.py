from django.shortcuts import render , render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.context_processors import csrf
from django.contrib import auth
from django.contrib.auth.models import User
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import Http404
from forms import *
from models import *
from django.core import serializers
import json

import pdb

def login(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('login.html',c)

def auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')

    user = auth.authenticate(username=username, password=password)
    if user is not None:
        auth.login(request, user)
        
        return HttpResponseRedirect('/')
    else:
        c = {}
        c.update(csrf(request))
        c['errors'] = True
        c['request'] = request
        return render_to_response('login.html',c,context_instance=RequestContext(request))

def logout(request):
    auth.logout(request)
    request.session = {}
    return HttpResponseRedirect('/login/')

def signup(request):
    if request.method == 'POST':
        form = MyRegistrationForm(request.POST)
        if form.is_valid():
            signu= form.save(commit=False)
            signu.save()
            return HttpResponseRedirect('/')
        else: 
            return render_to_response('signup.html', {'form': form}, context_instance=RequestContext(request))
    args = {}
    args.update(csrf(request))
    args['request'] = request
    args['form'] = MyRegistrationForm()
    return render_to_response('signup.html', args,context_instance=RequestContext(request))

def index(request):
    posts = Post.objects.all()
    c = {}
    c.update(csrf(request))
    c['request'] = request
    c['posts']= posts
    return render_to_response('index.html',c,context_instance=RequestContext(request))

def newPost(request):
    #pdb.set_trace()
    if request.method == 'POST':
        form = NewPostForm(request.POST)
        if form.is_valid():
            post = Post(title= request.POST['title'],content=request.POST['content'],author = request.user)

            post.save()
            return HttpResponseRedirect('/')
        else:
            return render_to_response('newPost.html', {'form': form}, context_instance=RequestContext(request))

    args = {}
    args.update(csrf(request))
    args['request'] = request
    args['form'] = NewPostForm()
    return render_to_response('newPost.html', args,context_instance=RequestContext(request))

def viewPost(request,post_id):
    post = Post.objects.get(id = post_id)
    args = {}
    args.update(csrf(request))
    args['request'] = request
    args['post'] = post
    #pdb.set_trace()
    post_type = ContentType.objects.get_for_model(post.__class__)
    comments = Comments.objects.filter(content_type = post_type, object_id = post_id).order_by('-conmmentTime')
    args['comments'] = comments
    args['cmnt_cmnt'] = Comments.objects.all()

    """data = serializers.serialize("json", Comments.objects.all())
    allField = json.loads(data)
    args['data'] = allField"""
    args['result'] = postCmnt(post_id)
    #print postCmnt(post_id)
    return render_to_response('viewPost.html', args,context_instance=RequestContext(request))
    

def edit(request,post_id):
    post = Post.objects.get(id=post_id)
    if post.author == request.user:
        args = {}
        args.update(csrf(request))
        args['request'] = request
        args['form'] = NewPostForm(instance = post)
        args['id'] = post_id
        return render_to_response('editPost.html', args,context_instance=RequestContext(request))
    else:
        raise Http404

def update_post(request):

    if request.method == 'POST':
        id = request.GET.get('id')
        post = Post.objects.get(pk=id)

        form = NewPostForm(request.POST, instance = post)

        if form.is_valid():
            form.save()

        return HttpResponseRedirect('/')
def delete(request,post_id):
    post = Post.objects.get(id=post_id)
    if post.author == request.user:

        Post.objects.filter(id=post_id).delete()
        return HttpResponseRedirect('/')
    else:
        raise Http404
@login_required(login_url='/login/')
def comment(request,post_id):
    post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        cmnt = Comments(content_object = post, user = request.user, comment = request.POST['comment'])
        cmnt.save()
        args = {}
        args.update(csrf(request))
        args['request'] = request
        args['post'] = post
        post_type = ContentType.objects.get_for_model(post.__class__)
        args['comments'] = Comments.objects.filter(content_type = post_type, object_id = post_id)
        args['cmnt_cmnt'] = Comments.objects.all()
        return render_to_response('viewPost.html', args,context_instance=RequestContext(request))

@login_required(login_url='/login/')
def comment_cmnt(request,cmnt_id):
    #pdb.set_trace()
    cmnt = Comments.objects.get(id=cmnt_id)
    if request.method == 'POST':
        cmnt = Comments(content_object = cmnt, user = request.user, comment = request.POST['comment_text'])
        cmnt.save()
        post = Post.objects.get(id=request.POST['post_id'])
        args = {}
        args.update(csrf(request))

        args['request'] = request
        args['post'] = post
        post_type = ContentType.objects.get_for_model(post.__class__)
        args['comments'] = Comments.objects.filter(content_type = post_type, object_id = request.POST['post_id'])
        args['cmnt_cmnt'] = Comments.objects.all()
        return render_to_response('ajaxviewPost.html', args,context_instance=RequestContext(request))

    return HttpResponse("hello")

def postCmnt(post_id):
    r = {}
    post = Post.objects.get(id=post_id)
    post_type = ContentType.objects.get_for_model(post.__class__)
    q = Comments.objects.filter(content_type = post_type, object_id = post_id)


    for c in q:
        r[c] = cmntCmnt(c)

    return r



def cmntCmnt(c):
    #pdb.set_trace()
    
    cmnt_type = ContentType.objects.get_for_model(c.__class__)
    z = Comments.objects.filter(content_type = cmnt_type, object_id = c.id)

    p ={}
    q =[]
    for l in  z:
        p[l] = cmntCmnt(l)
    q.append(p)
    return q


