# -*- coding: utf-8 -*-
"""
Checklist Views
"""

from __future__ import unicode_literals

from django.shortcuts import redirect, render
from django.http import HttpResponseBadRequest, HttpResponseNotFound, JsonResponse, QueryDict
from django.views import View
from checklist.models import CheckList, CheckListItem

class CheckListsView(View):
    """
    All Checklists
    """
    def get(self, request):
        """ get all checklists """
        all_checklists = CheckList.objects.all()
        return render(request, 'checklists.html', {'checklists':all_checklists})

    def post(self, request):
        """ post a new checklist """
        name = request.POST.get('name')
        if not name:
            return HttpResponseBadRequest()
        checklist = CheckList(name=name)
        checklist.save()

        return redirect('checklist', id=checklist.id)


class CheckListView(View):
    """
    Checklist
    """
    def get(self, request, id):
        """ get a checklist """
        try:
            checklist = CheckList.objects.get(pk=id)
        except Exception:
            return HttpResponseNotFound()
        items = CheckListItem.objects.filter(checklist=checklist)
        return render(request, 'checklist.html', {
            'checklist': checklist,
            'items': items
            })

    def put(self, request, id):
        """ edit a checklist """
        try:
            checklist = CheckList.objects.get(pk=id)
        except Exception:
            return HttpResponseNotFound()

        put_params = QueryDict(request.body)
        name = put_params.get('name')
        is_starred = put_params.get('is_starred')
        if name:
            checklist.name = name
        if is_starred is not None:
            checklist.is_starred = is_starred
        checklist.save()
        return JsonResponse({'success': True})

    def delete(self, request, id):
        """ delete a checklist """
        try:
            checklist = CheckList.objects.get(pk=id)
        except Exception:
            return HttpResponseBadRequest()

        checklist.delete()
        return JsonResponse({'success': True})


class CheckListItemsView(View):
    """
    All Checklist Items
    """
    def post(self, request):
        """ post a new checklist item """
        item = request.POST.get('item')
        checklist_id = request.POST.get('checklist_id')
        if not item or not checklist_id:
            return HttpResponseBadRequest()

        try:
            checklist = CheckList.objects.get(pk=checklist_id)
        except Exception:
            return HttpResponseNotFound()

        checklist_item = CheckListItem(checklist=checklist, item=item)
        checklist_item.save()
        return redirect('checklist', id=checklist_id)


class CheckListItemView(View):
    """
    Checklist Item
    """
    def put(self, request, id):
        """ edit a checklist item """
        try:
            checklist_item = CheckListItem.objects.get(pk=id)
        except Exception:
            return HttpResponseNotFound()

        put_params = QueryDict(request.body)
        item = put_params.get('item')
        position = put_params.get('position')
        is_checked = put_params.get('is_checked')
        if item:
            checklist_item.item = item
        if position:
            checklist_item.position = position
        if is_checked is not None:
            checklist_item.is_checked = is_checked
        checklist_item.save()
        return JsonResponse({'success': True})

    def delete(self, request, id):
        """ delete a checklist item """
        try:
            checklist_item = CheckListItem.objects.get(pk=id)
        except Exception:
            return HttpResponseBadRequest()

        checklist_item.delete()
        return JsonResponse({'success': True})
