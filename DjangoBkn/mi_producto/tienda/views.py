from .models import Repuesto, Producto, CategoriaProducto, CategoriaRepuesto, Carrito, UsuarioNormal, UsuarioEmpresa
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ProductoSerializer
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import requests
import json
from django.core.mail import send_mail
import os
from django.conf import settings

#api chileexpress

import requests

import urllib.request
import json
from django.http import JsonResponse



# Vista para seleccionar tipo de cuenta
def seleccion_cuenta(request):
    return render(request, 'seleccion_cuenta.html')

def tipo_producto(request):
    return render(request, 'tipoProducto.html') 

# Página principal con imágenes en carrusel
def index(request):
    carrousel_dir = os.path.join(settings.MEDIA_ROOT, 'Carrousel')
    imagenes = []
    if os.path.exists(carrousel_dir):
        for nombre in os.listdir(carrousel_dir):
            if nombre.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
                imagenes.append(f'Carrousel/{nombre}')
    productos_destacados = Producto.objects.filter(destacado=True)
    repuestos_destacados = Repuesto.objects.filter(destacado=True)
    return render(request, 'index.html', {
        'imagenes': imagenes,
        'productos_destacados': productos_destacados,
        'repuestos_destacados': repuestos_destacados,
    })

def contacto(request):
    return render(request, 'contacto.html')

def usuario(request):
    return render(request, 'usuario.html')

def carrito(request):
    return render(request, 'carrito.html')

def pagar(request):
    if request.method == 'POST':
        # Aquí va la lógica para procesar el pago
        # Por ahora solo redirigimos a la página principal después del pago

        # Ejemplo: limpiar el carrito, registrar la compra, etc.
        # carrito = obtener_carrito_del_usuario(request.user)
        # procesar_pago(carrito)
        # limpiar_carrito(carrito)

        return redirect('index')  # Cambia 'index' por la url que quieras
    else:
        # Si intentan acceder por GET o otro método, redirigimos al carrito
        return redirect('carrito')
    
def eliminar_del_carrito(request, producto_id):
    if request.method == 'POST':
        item = get_object_or_404(Carrito, id=producto_id)
        item.delete()
    return redirect('carrito')

def register_us(request):
    if request.method == "POST":
        nombre = request.POST.get('nombre', '').strip()
        apellido = request.POST.get('apellido', '').strip()
        rut = request.POST.get('rut', '').strip()
        correo = request.POST.get('correo', '').strip()
        password = request.POST.get('contrasena', '')
        confirm_password = request.POST.get('verifica_contrasena', '')

        if password != confirm_password:
            messages.error(request, "Las contraseñas no coinciden.")
            return render(request, 'register_us.html')

        if UsuarioNormal.objects.filter(rut=rut).exists():
            messages.error(request, "El RUT ya está registrado.")
            return render(request, 'register_us.html')
        if UsuarioNormal.objects.filter(correo=correo).exists():
            messages.error(request, "El correo ya está registrado.")
            return render(request, 'register_us.html')

        nuevo_usuario = UsuarioNormal(
            nombre=nombre,
            apellido=apellido,
            rut=rut,
            correo=correo,
            password=make_password(password)
        )
        nuevo_usuario.save()

        messages.success(request, "Cuenta creada exitosamente.")
        return redirect('index')

    return render(request, 'register_us.html')

def register_em(request):
    if request.method == "POST":
        nombre = request.POST.get('nombre', '').strip()
        apellido = request.POST.get('apellido', '').strip()
        nombre_empresa = request.POST.get('nombre_empresa', '').strip()
        rut_empresa = request.POST.get('rut_empresa', '').strip()
        correo = request.POST.get('correo', '').strip()
        password = request.POST.get('contrasena', '')
        confirm_password = request.POST.get('verifica_contrasena', '')

        if password != confirm_password:
            messages.error(request, "Las contraseñas no coinciden.")
            return render(request, 'register_em.html')

        if UsuarioEmpresa.objects.filter(rut_empresa=rut_empresa).exists():
            messages.error(request, "El RUT de empresa ya está registrado.")
            return render(request, 'register_em.html')
        if UsuarioEmpresa.objects.filter(correo=correo).exists():
            messages.error(request, "El correo ya está registrado.")
            return render(request, 'register_em.html')

        nuevo_usuario = UsuarioEmpresa(
            nombre=nombre,
            apellido=apellido,
            nombre_empresa=nombre_empresa,
            rut_empresa=rut_empresa,
            correo=correo,
            password=make_password(password)
        )
        nuevo_usuario.save()

        messages.success(request, "Cuenta de empresa creada exitosamente.")
        return redirect('index')

    return render(request, 'register_em.html')

def login_usuario(request):
    if request.method == "POST":
        correo = request.POST.get('correo', '').strip()
        contrasena = request.POST.get('contrasena', '')
        tipo_usuario = request.POST.get('tipo_usuario', '')

        if tipo_usuario == "normal":
            usuario = UsuarioNormal.objects.filter(correo=correo).first()
            if usuario and check_password(contrasena, usuario.password):
                # Login exitoso, redirige a index
                request.session['usuario_nombre'] = usuario.nombre
                return redirect('index')    
            else:
                error = "Usuario o contraseña incorrectos para Usuario Normal."
                return render(request, 'usuario.html', {'error': error})

        elif tipo_usuario == "empresa":
            usuario = UsuarioEmpresa.objects.filter(correo=correo).first()
            if usuario and check_password(contrasena, usuario.password):
                # Login exitoso, redirige a index
                request.session['usuario_nombre'] = usuario.nombre
                return redirect('index')
            else:
                error = "Usuario o contraseña incorrectos para Usuario Empresa."
                return render(request, 'usuario.html', {'error': error})

        else:
            error = "Seleccione un tipo de usuario válido."
            return render(request, 'usuario.html', {'error': error})

    return render(request, 'usuario.html')

def cerrar_sesion(request):
    if 'usuario_nombre' in request.session:
        del request.session['usuario_nombre']
    return redirect('index')

# Vista para listar productos, con filtros por categoría y búsqueda
def lista_productos(request):
    categoria_id = request.GET.get('categoria')
    q = request.GET.get('q')
    categorias = CategoriaProducto.objects.all()
    productos = Producto.objects.filter(es_publico=True)
    categoria_seleccionada = None

    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)
        try:
            categoria_seleccionada = CategoriaProducto.objects.get(id=categoria_id)
        except CategoriaProducto.DoesNotExist:
            categoria_seleccionada = None

    if q:
        productos = productos.filter(nombre__icontains=q)

    return render(request, 'productos.html', {
        'productos': productos,
        'categorias': categorias,
        'categoria_seleccionada': categoria_seleccionada,
    })

def lista_repuestos(request):
    categoria_id = request.GET.get('categoria')
    q = request.GET.get('q')
    categorias = CategoriaRepuesto.objects.all()
    repuestos = Repuesto.objects.filter(es_publico=True)
    categoria_seleccionada = None

    if categoria_id:
        repuestos = repuestos.filter(categoria_id=categoria_id)
        try:
            categoria_seleccionada = CategoriaRepuesto.objects.get(id=categoria_id)
        except CategoriaRepuesto.DoesNotExist:
            categoria_seleccionada = None

    if q:
        repuestos = repuestos.filter(nombre__icontains=q)

    return render(request, 'repuestos.html', {
        'repuestos': repuestos,
        'categorias': categorias,
        'categoria_seleccionada': categoria_seleccionada,
    })

# Detalle del producto y sus repuestos públicos
def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    repuestos = Repuesto.objects.filter(producto=producto, es_publico=True)
    return render(request, 'detalle.html', {
        'producto': producto,
        'repuestos': repuestos
    })

def detalle_repuesto(request, repuesto_id):
    repuesto = get_object_or_404(Repuesto, pk=repuesto_id, es_publico=True)
    return render(request, 'detalleRepuestos.html', {  # Cambiado a detalleRepuestos.html
        'repuesto': repuesto
    })

# Agregar productos al carrito (requiere sesión iniciada)
@login_required
def agregar_al_carrito(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        cantidad = int(request.POST.get('cantidad', 1))
        precio = int(request.POST.get('precio', 0))

        Carrito.objects.create(
            usuario=request.user,
            nombre=nombre,
            cantidad=cantidad,
            precio_unitario=precio
        )
        return redirect('lista_productos')
    return redirect('lista_productos')

# Mostrar el carrito del usuario autenticado
@login_required
def mostrar_carrito(request):
    productos_carrito = Carrito.objects.filter(usuario=request.user)
    total_carrito = sum(item.total for item in productos_carrito)
    return render(request, 'carrito.html', {
        'productos_carrito': productos_carrito,
        'total_carrito': total_carrito,
    })

# API REST para consultar productos en formato JSON
class ProductoAPIView(APIView):
    def get(self, request):
        productos = Producto.objects.all()
        serializer = ProductoSerializer(productos, many=True)
        return Response(serializer.data)

def listar_ciudades_origen(request):
    try:
        url = "https://restservices-qa.starken.cl/apiqa/starkenservices/rest/listarCiudadesOrigen"
        headers = {
            'Content-Type': 'application/json',
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            return JsonResponse(data, safe=False)
        else:
            return JsonResponse({'error': 'Error en la solicitud a la API'}, status=response.status_code)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
def listar_ciudades_destino(request):
    try:
        url = "https://restservices-qa.starken.cl/apiqa/starkenservices/rest/listarCiudadesDestino"
        headers = {
            'Content-Type': 'application/json',
            'Rut': '76211240',  # Valor proporcionado en la imagen
            'Clave': 'key',     # Valor proporcionado en la imagen
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            return JsonResponse(data, safe=False)
        else:
            return JsonResponse({'error': 'Error en la solicitud a la API'}, status=response.status_code)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def consultar_tarifas(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            codigoCiudadDestino = body.get('codigoCiudadDestino')
            print(f"Código de ciudad destino recibido: {codigoCiudadDestino}")  # Verificar el código

            # URL y headers de la API
            url = "https://restservices-qa.starken.cl/apiqa/starkenservices/rest/consultarTarifas"
            headers = {
                'Content-Type': 'application/json',
                'Rut': '76211240',  # Valor proporcionado en la imagen
                'Clave': 'key',     # Valor proporcionado en la imagen
            }

            # Cuerpo de la solicitud
            payload = {
                "codigoCiudadOrigen": 1,
                "codigoCiudadDestino": int(codigoCiudadDestino),
                "codigoAgenciaDestino": 0,
                "codigoAgenciaOrigen": 0,
                "alto": 4,
                "ancho": 4,
                "largo": 4,
                "kilos": 4,
                "cuentaCorriente": "19154",  # Cuenta corriente válida
                "cuentaCorrienteDV": "K",   # Dígito verificador válido
                "rutCliente": "",
            }

            # Realizar la solicitud
            response = requests.post(url, json=payload, headers=headers)

            if response.status_code == 200:
                data = response.json()
                if data.get('codigoRespuesta') == 0:
                    print("No se encontraron tarifas disponibles.")
                    return JsonResponse({'error': 'No se encontraron tarifas disponibles.'}, status=404)
                return JsonResponse(data, safe=False)
            else:
                print(f"Error en la solicitud a la API: {response.status_code}, {response.text}")
                return JsonResponse({'error': 'Error en la solicitud a la API'}, status=response.status_code)
        except Exception as e:
            print(f"Excepción ocurrida: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)

def calcular_envio(request):
    return render(request, 'calcular_envio.html')

def enviar_correo_confirmacion(usuario_email, productos, total):
    try:
        asunto = "Confirmación de Compra - AutoParts"
        mensaje = "Gracias por tu compra. Aquí están los detalles:\n\n"
        for producto in productos:
            mensaje += f"Producto: {producto['nombre']}\nCantidad: {producto['cantidad']}\nSubtotal: ${producto['subtotal']}\n\n"
        mensaje += f"Total pagado: ${total}\n\nGracias por confiar en nosotros."
        
        send_mail(
            asunto,
            mensaje,
            'tu_correo@gmail.com',  # Cambia esto por tu correo configurado
            [usuario_email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error al enviar el correo: {str(e)}")
        return False

@csrf_exempt
def confirmar_pago(request):
    if request.method == 'POST':
        try:
            # Simula la recepción de datos del pago
            datos_pago = json.loads(request.body)
            usuario_email = datos_pago.get('email')  # Email del usuario
            productos = datos_pago.get('productos')  # Lista de productos comprados
            total = datos_pago.get('total')  # Total pagado

            # Enviar correo de confirmación
            correo_enviado = enviar_correo_confirmacion(usuario_email, productos, total)
            if correo_enviado:
                return JsonResponse({'mensaje': 'Pago confirmado y correo enviado.'}, status=200)
            else:
                return JsonResponse({'error': 'Pago confirmado, pero no se pudo enviar el correo.'}, status=500)
        except Exception as e:
            print(f"Error en la confirmación del pago: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)

# Create your views here.
