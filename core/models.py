# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from .utils import duration_string


class Baby(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    birth_date = models.DateField(blank=False, null=False)

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')
        ordering = ['last_name', 'first_name']
        verbose_name_plural = 'Babies'

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)


class DiaperChange(models.Model):
    baby = models.ForeignKey('Baby', related_name='diaper_change')
    time = models.DateTimeField(blank=False, null=False)
    wet = models.BooleanField()
    solid = models.BooleanField()
    color = models.CharField(max_length=255, blank=True, choices=[
        ('black', 'Black'),
        ('brown', 'Brown'),
        ('green', 'Green'),
        ('yellow', 'Yellow'),
    ])

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')
        ordering = ['-time']

    def __str__(self):
        return 'Diaper change for {} on {}'.format(self.baby, self.time.date())


class Feeding(models.Model):
    baby = models.ForeignKey('Baby', related_name='feeding')
    start = models.DateTimeField(blank=False, null=False)
    end = models.DateTimeField(blank=False, null=False)
    type = models.CharField(max_length=255, choices=[
        ('breast milk', 'Breast milk'),
        ('formula', 'Formula'),
    ])
    method = models.CharField(max_length=255, choices=[
        ('bottle', 'Bottle'),
        ('left breast', 'Left breast'),
        ('right breast', 'Right breast'),
    ])

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')
        ordering = ['-start']

    def __str__(self):
        return 'Feeding for {} on {} ({})'.format(
            self.baby, self.end.date(), self.duration())

    def duration(self):
        return duration_string(self.start, self.end)


class Note(models.Model):
    baby = models.ForeignKey('Baby', related_name='note')
    note = models.TextField()
    time = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')
        ordering = ['-time']

    def __str__(self):
        return 'Note about {} on {}'.format(self.baby, self.time.date())


class Sleep(models.Model):
    baby = models.ForeignKey('Baby', related_name='sleep')
    start = models.DateTimeField(blank=False, null=False)
    end = models.DateTimeField(blank=False, null=False)

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')
        ordering = ['-start']
        verbose_name_plural = 'Sleep'

    def __str__(self):
        return 'Sleep for {} on {} ({})'.format(
            self.baby, self.end.date(), self.duration())

    def duration(self):
        return duration_string(self.start, self.end)


class TummyTime(models.Model):
    baby = models.ForeignKey('Baby', related_name='tummy_time')
    start = models.DateTimeField(blank=False, null=False)
    end = models.DateTimeField(blank=False, null=False)
    milestone = models.CharField(max_length=255, blank=True)

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')
        ordering = ['-start']

    def __str__(self):
        return 'Tummy time for {} on {} ({})'.format(
            self.baby, self.end.date(), self.duration())

    def duration(self):
        return duration_string(self.start, self.end)