"""
checklist URL Configuration
"""
from django.conf.urls import url
from checklist import views

urlpatterns = [
    url(r'^$', views.Index.as_view()),
    url(r'^checklists/$', views.CheckListsView.as_view(), name='checklists'),
    url(r'^checklist/(?P<id>[0-9]+)$', views.CheckListView.as_view(), name='checklist'),
    url(r'^checklist_items/$', views.CheckListItemsView.as_view(), name='checklist_items'),
    url(r'^checklist_item/(?P<id>[0-9]+)$', views.CheckListItemView.as_view(), name='checklist_item'),
    url(r'^search/$', views.SearchView.as_view(), name='search'),
]
