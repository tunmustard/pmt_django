from django.contrib import admin
from django.utils.safestring import mark_safe
from django.urls import reverse

from .models import Pollset, Choice, Question


class EditLinkToInlineObject(object):
    def edit_link(self, instance):
        url = reverse('admin:%s_%s_change' % (
            instance._meta.app_label,  instance._meta.model_name),  args=[instance.pk] )
        if instance.pk:
            return mark_safe(u'<a href="{u}">edit</a>'.format(u=url))
        else:
            return ''

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3
    
class QuestionInline(EditLinkToInlineObject,admin.TabularInline):
    model = Question
    readonly_fields = ('edit_link',)
    #extra = 3
    #inlines = [ChoiceInline]


class PollsetAdmin(admin.ModelAdmin):
    list_display = ('poll_text', 'pub_date', 'was_published_recently','is_active','require_authorization')
    list_filter = ['pub_date']
    search_fields = ['poll_text']
    fieldsets = [
        (None,               {'fields': ['poll_text','is_active','require_authorization']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
        ('user_performed', {'fields': ['user_performed']}),
    ]
    inlines = [QuestionInline]


class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['question_text']
    fieldsets = [
        (None,               {'fields': ['question_text']}),
    ]
    inlines = [ChoiceInline]

admin.site.register(Pollset, PollsetAdmin)
admin.site.register(Question, QuestionAdmin)






