# -*- coding: utf-8 -*-

"""
Models for Checklist
"""
from __future__ import unicode_literals
from django.db import models
from positions import PositionField

class CheckList(models.Model):
    """ Checklist model """
    name = models.TextField(max_length=100)
    is_starred = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

IMPORTANCE_CHOICES = (
    (0, 'Default'),
    (1, 'High'),
    (2, 'Very Important'),
)

class CheckListItem(models.Model):
    """ Checklist Item model """
    checklist = models.ForeignKey('CheckList', on_delete=models.CASCADE, related_name='items')
    item = models.TextField(max_length=1000)
    is_checked = models.BooleanField(default=False)
    position = PositionField(collection='checklist')
    importance = models.IntegerField(default=0)

    def __unicode__(self):
        if self.is_checked:
            return "(done) %s" % self.item
        return self.item
