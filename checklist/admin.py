# -*- coding: utf-8 -*-

"""
Admin module for checklist
"""

from __future__ import unicode_literals

from django.contrib import admin
from checklist.models import CheckList, CheckListItem

admin.site.register(CheckList)
admin.site.register(CheckListItem)
