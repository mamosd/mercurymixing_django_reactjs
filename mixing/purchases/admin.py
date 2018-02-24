from __future__ import unicode_literals

from django.contrib import admin

from .models import Purchase


@admin.register(Purchase)
class PurchasAdmin(admin.ModelAdmin):
    fields = ["created", "user", "credits", "amount", "charge_details"]
    readonly_fields = ["created"]
    list_display = ["user", "amount", "credits", "created"]
    date_hierarchy = "created"
    list_filter = ["user"]
    search_fields = ["user__username", "user__email"]
