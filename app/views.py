from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from .forms import ProductForm, CustomUserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from .models import Producto,Cart,CartItem,Purchase
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import render

def currency(request):
    return render(request, 'currency.html')

def clients(request):
    users = User.objects.all()
    return render(request, 'clients.html', {'users': users})

def editar_cliente(request,id):
    if request.method == 'GET':
        Persona = get_object_or_404(Persona, pk=id)
        form = CustomUserCreationForm(instance=Persona)
        return render(request, 'client_detail.html', {'Persona': Persona, 'form': form})
    else:
        try:
            print(request.POST)
            Persona = get_object_or_404(Persona, pk=id)
            form = CustomUserCreationForm(request.POST, instance=Persona)
            form.save()
            return redirect('clients')
        except ValueError:
            return render(request, 'editar_cliente.html', {'client': Persona, 'form': form, 'error': "Error al Actualizar al Cliente"})

def login_inicial(request):
    if request.method == 'POST':
        username = request.POST.get('nombrelogin')
        password = request.POST.get('passwordlogin')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Cambia 'nombre-de-tu-vista' por el nombre de la vista a la que deseas redirigir después del inicio de sesión exitoso
        else:
            error_message = "Credenciales inválidas. Inténtalo de nuevo."
            return render(request, 'registration/login_inicial.html', {'error_message': error_message})
    else:
        return render(request, 'registration/login_inicial.html')

def home(request):
    productos = Producto.objects.all()
    data={
        'productos': productos 
    }
    return render(request,'app/home.html',data)


def agregar_producto(request):
    data = {
        'form': ProductForm()
    }
    if request.method == 'POST':
        formulario = ProductForm(data=request.POST,files=request.FILES)
        if formulario.is_valid():
            formulario.save()


    return render(request, 'app/producto/agregar.html', data)


def listar_prod(request):
    productos = Producto.objects.all()
    data={
        'productos' : productos
    }
    return render(request,'app/producto/listar.html',data)

def modificar_prod(request,id):
    producto = get_object_or_404(Producto, id=id)
    
    data = {
        'form' : ProductForm(instance=producto)
    }
    if request.method == 'POST':
        formulario = ProductForm(data=request.POST,files=request.FILES, instance=producto)
        if formulario.is_valid():
            formulario.save()
            return redirect(to="listar_prod")
    return render(request,'app/producto/modificar.html',data)


def eliminar_prod(request,id):
    producto = get_object_or_404(Producto,id=id)
    producto.delete()
    return redirect(to="listar_prod")

def registro(request):
    data = {
        'form': CustomUserCreationForm
    }

    if request.method == 'POST':
        formulario = CustomUserCreationForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            user = authenticate(username=formulario.cleaned_data["username"],password=formulario.cleaned_data["password1"])
            
            content_type = ContentType.objects.get(app_label='app', model='producto')
            permission = Permission.objects.get(content_type=content_type, codename='view_producto')

            # Agregar el permiso al usuario
            user.user_permissions.add(permission)

            # Redirigir al home 
            return redirect(to="home")
            
        data["form"] = formulario
        
    return render(request, 'registration/registro.html', data)


def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    return render(request, 'prod.html', {'product': producto})

def admin_login_view(request):
    # Tu lógica de inicio de sesión del administrador aquí
    return render(request, 'registration/admin_login_view.html')
def agregar_al_carrito(request,producto_id):
    cart , created =Cart.objects.get_or_create(user=request.user)
    producto=get_object_or_404(Producto, id=producto_id)
    
    cart_item,created=CartItem.objects.get_or_create(cart=cart, producto=producto)
    if not created:
            cart_item.quantity  +=1
            cart_item.save()
            
    return redirect('carrito')
def carrito(request):
    cart = Cart.objects.filter(user=request.user).first()
    total = cart.total_ca if cart else 0
    cart_items = cart.cartitem_set.select_related('producto') if cart else []
    
    context = { 
        'cart': cart_items,
        'total': total
    }
    return render(request, 'carrito.html', context)

@login_required
def aumentar(request,cart_item_id):
    cart_item=get_object_or_404(CartItem,id=cart_item_id)
    if cart_item.quantity < 15:
        cart_item.quantity +=1
        cart_item.save()
    return redirect('carrito')
@login_required
def disminuir(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    elif cart_item.quantity == 1:
        cart_item.delete()
    
    return redirect('carrito')

@login_required
def Hacer_compra(request):
    user = request.user
    cart = get_object_or_404(Cart, user=user)

    total_ca = cart.total_ca

    with transaction.atomic():
        for item in cart.cartitem_set.all():
            product = item.producto
            product.stock -= item.quantity
            product.save()
        purchase = Purchase.objects.create(user=user, cart=cart, total=total_ca)

        cart.producto.clear()

    return redirect('home')
@login_required


def ver_ordeness(request):
    user = request.user
    pedidos = Purchase.objects.filter(user=user)
    context = {
        'pedidos': pedidos
    }
    return render(request, 'ordenes.html', context)
def shop_view(request):
    productos = Producto.objects.all()
    data={
        'productos': productos 
    }
    return render(request, 'shop.html',data)

def dash_admin(request):
    user = request.user
    pedidos = Purchase.objects.all()
    context = {
        'pedidos': pedidos
    }
    return render(request, 'dash_admin.html', context)
def acercade (request):
    return render(request,'Acercade.html')