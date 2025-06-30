from django.contrib import admin
from .models import (UsuarioNormal, UsuarioEmpresa, CategoriaProducto, CategoriaRepuesto, Producto, Repuesto, Carrito)


class ProductoAdmin(admin.ModelAdmin):
    exclude = ('creado_por', 'modificado_por')

    def save_model(self, request, obj, form, change):
        if not change:  # Si es creación
            obj.creado_por = request.user
        obj.modificado_por = request.user
        super().save_model(request, obj, form, change)

class RepuestoAdmin(admin.ModelAdmin):
    exclude = ('creado_por', 'modificado_por')

    def save_model(self, request, obj, form, change):
        if not change:  # Si es creación
            obj.creado_por = request.user
        obj.modificado_por = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Producto, ProductoAdmin)
admin.site.register(Repuesto, RepuestoAdmin)
admin.site.register(CategoriaProducto)
admin.site.register(CategoriaRepuesto)
admin.site.register(UsuarioNormal)
admin.site.register(UsuarioEmpresa)
admin.site.register(Carrito)
# Register your models here.
