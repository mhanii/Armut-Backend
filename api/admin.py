from django.contrib import admin
from .models import Category, Store, Product, Banner, ProductImage, Color
from django import forms

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "date_added", "link")
    inlines = [ProductImageInline]
    filter_horizontal = ("colors",)
    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if "link" in fields:
            fields.remove("link")
        return fields

class ColorAdminForm(forms.ModelForm):
    class Meta:
        model = Color
        fields = "__all__"
        widgets = {
            'hex_code': forms.TextInput(attrs={'type': 'color'}),
        }

class ColorAdmin(admin.ModelAdmin):
    form = ColorAdminForm

admin.site.register(Category)
admin.site.register(Store)
admin.site.register(Product, ProductAdmin)
admin.site.register(Banner)
admin.site.register(Color, ColorAdmin)




