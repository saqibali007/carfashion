from django.contrib import admin
from django.utils.html import format_html
from .models import (Category, Product, CustomerProfile, Order,
                     OrderItem, HomeServiceBooking, Review, Cart, CartItem)

admin.site.site_header = "CarFashion Admin"
admin.site.site_title = "CarFashion"
admin.site.index_title = "Welcome to CarFashion Admin Panel"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product_name', 'price', 'quantity', 'subtotal']

    def subtotal(self, obj):
        return f'₹{obj.subtotal}'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'stock_status', 'is_available', 'is_featured']
    list_editable = ['price', 'stock', 'is_available', 'is_featured']
    list_filter = ['category', 'is_available', 'is_featured']
    search_fields = ['name', 'brand']
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 25

    def stock_status(self, obj):
        if obj.stock == 0:
            return format_html('<span style="color:red;font-weight:bold;">Out of Stock</span>')
        elif obj.stock < 5:
            return format_html('<span style="color:orange;font-weight:bold;">Low ({})</span>', obj.stock)
        return format_html('<span style="color:green;font-weight:bold;">In Stock ({})</span>', obj.stock)
    stock_status.short_description = 'Stock Status'


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'city', 'state']
    search_fields = ['user__username', 'user__email', 'phone']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user', 'total_amount', 'status', 'created_at']
    list_editable = ['status']
    list_filter = ['status', 'created_at']
    search_fields = ['order_number', 'user__username', 'user__email']
    inlines = [OrderItemInline]
    readonly_fields = ['order_number', 'total_amount', 'created_at']
    ordering = ['-created_at']

    def total_amount(self, obj):
        return f'₹{obj.total_amount}'


@admin.register(HomeServiceBooking)
class HomeServiceBookingAdmin(admin.ModelAdmin):
    list_display = ['booking_number', 'user', 'service_type', 'preferred_date',
                    'preferred_time', 'status', 'created_at']
    list_editable = ['status']
    list_filter = ['service_type', 'status', 'preferred_date']
    search_fields = ['booking_number', 'user__username', 'user__email']
    readonly_fields = ['booking_number', 'user', 'created_at']
    ordering = ['-created_at']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'rating', 'created_at']
    list_filter = ['rating']
    search_fields = ['user__username', 'product__name']
