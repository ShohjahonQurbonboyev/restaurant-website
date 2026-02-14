from django.contrib import admin
from .models import Category, MenuItem, Order, OrderItem, Recipe
from .models import Feedback


# ===================== CATEGORIES (TYPES) =====================

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug", "order")
    list_editable = ("order",)
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("order", "name")


# ===================== MENU ITEMS =====================

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category", "price")
    list_filter = ("category",)
    search_fields = ("name", "description")
    ordering = ("-id",)
    autocomplete_fields = ("category",)  # category ko'p bo'lsa qidirish oson bo'ladi


# ===================== ORDERS + ORDER ITEMS INLINE =====================

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    min_num = 0
    can_delete = True

    # Jazzmin tab ichida ko‘rsatish
    classes = ("order-items-tab",)

    fields = ("menu_item", "quantity", "item_price", "line_total")
    readonly_fields = ("item_price", "line_total")
    autocomplete_fields = ("menu_item",)

    def item_price(self, obj):
        if obj and obj.menu_item_id:
            return obj.menu_item.price
        return "-"
    item_price.short_description = "Narx"

    def line_total(self, obj):
        if obj and obj.menu_item_id:
            return obj.menu_item.price * (obj.quantity or 0)
        return "-"
    line_total.short_description = "Jami"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "phone", "location", "payment_method", "total", "created_at")
    list_filter = ("payment_method", "created_at")
    search_fields = ("phone", "location")
    ordering = ("-id",)

    fieldsets = (
        ("General", {
            "fields": ("phone", "location", "payment_method", "total"),
            "classes": ("tab-general",),
        }),
    )

    inlines = [OrderItemInline]


# ===================== RECIPES =====================

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "category", "is_featured", "created_at")
    list_filter = ("category", "is_featured")
    search_fields = ("title",)
    ordering = ("-id",)




@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "created_at")
    search_fields = ("name", "phone", "message")
