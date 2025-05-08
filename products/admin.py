from django.contrib import admin
from django import forms
from .models import Brand, Category, Product

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "description", "created_at", "updated_at")
    search_fields = ("name",)
    list_filter = ("is_active",)
    

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "description", "created_at", "updated_at")
    search_fields = ("name",)
    list_filter = ("is_active",)
    
class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()
        self.fields['category'].label_from_instance = lambda obj: obj.name

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = ("title", "brand", "category", "price", "is_active", "created_at", "updated_at")
    search_fields = ("title", "brand__name", "category__name", "description")
    list_filter = ("is_active", "brand", "category")
    list_editable = ("price", "is_active")
    list_per_page = 25
    ordering = ("title",)