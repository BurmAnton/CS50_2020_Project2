from django.contrib import admin
from .models import Listing, Comment, Bid, User

# Register your models here.

class ListingAdmin(admin.ModelAdmin):
    list_display = ("title", "id", "category", "creator")
    filter_horizontal = ("subscribers",)
    list_filter = ['date']
    search_fields = ['title']

class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "text", "listing", "date")
    fields = ["text", "date"]
   

admin.site.register(Listing, ListingAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Bid)
admin.site.register(User)