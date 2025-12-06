"""
checklist URL Configuration
"""

from django.urls import path

from checklist import views

urlpatterns = [
    path("", views.Index.as_view()),
    path("checklists/", views.CheckListsView.as_view(), name="checklists"),
    path("checklist/<int:id>", views.CheckListView.as_view(), name="checklist"),
    path(
        "checklist_items/",
        views.CheckListItemsView.as_view(),
        name="checklist_items",
    ),
    path(
        "checklist_item/<int:id>",
        views.CheckListItemView.as_view(),
        name="checklist_item",
    ),
    path("search/", views.SearchView.as_view(), name="search"),
]
