from django.conf.urls import patterns, include, url



from posts import views

urlpatterns = patterns('',
    url(r'^$', views.index),
    url(r'^auth/$', views.auth_view),
    url(r'^logout/$', views.logout),
    url(r'^login/$',views.login),
    url(r'^signup/$',views.signup),
    url(r'^newPost/$',views.newPost),
    url(r'^comment/(?P<post_id>\d+)',views.comment,name="PostComment"),
    url(r'^post/(?P<post_id>\d+)',views.viewPost,name='viewPost'),
    url(r'^delete/(?P<post_id>\d+)',views.delete,name='deletePost'),
    url(r'^edit/(?P<post_id>\d+)',views.edit,name='EditPost'),
    url(r'^update_post/$', views.update_post, name='updatePost'),
    url(r'^comment_cmnt/(?P<cmnt_id>\d+)',views.cmntCmnt,name = "CommentComment"),

)