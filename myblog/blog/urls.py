from django.conf.urls import url, include
from django.views.generic import RedirectView

from . import views

app_name = 'blog'
urlpatterns = [
    url(r'^$',
        views.IndexView.as_view(), name='index'),
    url(r'^article/(?P<title>\w+)/$',
        views.DetailView.as_view(), name='detail_post'),
    url(r'^article/new$',
        views.NewArticle.as_view(), name='new_post'),
    url(r'^article/(?P<title>\w+)/edit$',
        views.UpdateArticle.as_view(), name='edit_post'),
    url(r'^article/(?P<title>\w+)/delete',
        views.DeleteArticle.as_view(), name='delete_post'),
    url('^markdown/', include('django_markdown.urls')),
    url(r'^login/$',
        views.Login.as_view(), name='login'),
    url(r'^register/$',
        views.Register.as_view(), name='register'),
    url(r'^logout/$',
        views.Logout.as_view(), name='logout'),
    url(r'^feed/$',
        views.LatestEntriesFeed()),
    url(r'^.*$',
        RedirectView.as_view(url='/')),
]
