import csv
from django.http import HttpResponse
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
    
    def export_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="products.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['tItulo', 'marca', 'Categoria', 'preço', 'descrição', 'criado em', 'atualizado em'])
        
        for product in queryset:
            writer.writerow([product.title, product.brand.name, product.category.name, product.price, product.is_active, product.description, product.created_at, product.updated_at])
        
        return response
    export_to_csv.short_description = 'exportar como CSV'
    actions = [export_to_csv]