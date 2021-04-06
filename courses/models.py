from django.db import models
from django.http import HttpResponseRedirect
from django.urls import reverse
from ckeditor.fields import RichTextField
from .fields import OrderField
from ckeditor_uploader.fields import RichTextUploadingField


class Subject(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class Course(models.Model):

    subject = models.ForeignKey(Subject,
                                related_name='courses',
                                on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    overview = models.TextField()
    intro = RichTextUploadingField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return HttpResponseRedirect(reverse('course_detail', kwargs={'slug': self.slug}))


class Module(models.Model):
    course = models.ForeignKey(Course,
                               related_name='modules',
                               on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    # description = RichTextField(blank=True)
    description = RichTextUploadingField(blank=True)
    order = OrderField(blank=True, for_fields=['course'])

    def __str__(self):
        return f'{self.order}. {self.title}'

    class Meta:
        ordering = ['order']

    def get_absolute_url(self):
        return HttpResponseRedirect(reverse('course_detail', kwargs={'slug': self.slug}))


class PracticeQuestions(models.Model):
    course = models.ForeignKey(Course,
                               related_name='questions',
                               on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=False)
    question = RichTextField(blank=False)
    answer = RichTextField(blank=True)
    hint = models.TextField(blank=True)
    Test = models.TextField(blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return HttpResponseRedirect(reverse('practice', kwargs={'slug': self.title}))