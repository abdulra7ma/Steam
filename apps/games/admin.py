from django.contrib import admin

from games.models import Category, Game, Raiting, Platform



class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'desc', 'price', 'category', 'raiting')
    list_filter = ('created_at', 'title', 'platforma')
    search_fields = ('title', 'price')
    date_hierarchy = 'created_at'
    ordering = ['created_at']

admin.site.register(Category)
admin.site.register(Game,PostAdmin)
admin.site.register(Raiting)
admin.site.register(Platform)