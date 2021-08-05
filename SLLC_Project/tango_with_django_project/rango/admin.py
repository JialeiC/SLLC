from django.contrib import admin
from rango.models import Category, Page,Question
from rango.models import UserProfile

class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url')

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'likes','views')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Question,QuestionAdmin)
admin.site.register(UserProfile)