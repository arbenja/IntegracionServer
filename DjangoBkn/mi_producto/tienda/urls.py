from django.urls import path
from . import views
from .views import index, lista_productos, ProductoAPIView, contacto, usuario, mostrar_carrito, agregar_al_carrito


urlpatterns = [
    path('', index, name='index'),  # Página principal con el carrusel
    path('tipo-producto/', views.tipo_producto, name='tipo_producto'),
    path('productos/', lista_productos, name='lista_productos'),  # Página con productos
    path('api/productos/', ProductoAPIView.as_view(), name='producto_api'),  # API REST
    path('repuestos/', views.lista_repuestos, name='lista_repuestos'),
    path('repuestos/detalle/<int:repuesto_id>/', views.detalle_repuesto, name='detalle_repuesto'),
    path('contacto/', contacto, name='contacto'),
    path('usuario/', views.usuario, name='usuario'),
    path('producto/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),
    path('agregar-al-carrito/', agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/', mostrar_carrito, name='carrito'),
    path('seleccion-cuenta/', views.seleccion_cuenta, name='seleccion_cuenta'),
    path('registrar-usuario/', views.register_us, name='register_us'),
    path('registrar-empresa/', views.register_em, name='register_em'),
    path('login/', views.login_usuario, name='login_usuario'),
    path('pagar/', views.pagar, name='pagar'),
    path('eliminar-del-carrito/<int:producto_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('cerrar_sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    path('listar-ciudades-origen/', views.listar_ciudades_origen, name='listar_ciudades_origen'),
    path('listar-ciudades-destino/', views.listar_ciudades_destino, name='listar_ciudades_destino'),
    path('consultar-tarifas/', views.consultar_tarifas, name='consultar_tarifas'),
    path('calcular-envio/', views.calcular_envio, name='calcular_envio'),
]

