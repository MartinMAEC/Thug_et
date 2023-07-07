from django.urls import path
from django.contrib import admin
from .views import *
urlpatterns =[
    path('', home, name="home"),
    path('agregarprod/',agregar_producto,name="agregar_producto"),
    path('listarprod/',listar_prod,name="listar_prod"),
    path('modificarprod/<id>/',modificar_prod,name="modificar_prod"),
    path('eliminarprod/<id>/',eliminar_prod,name="eliminar_prod"),
    path('registro/',registro,name="registro"),
    path('producto/<int:producto_id>/', detalle_producto, name='detalle_producto'),
    path('admin-login/', admin_login_view, name='admin_login_view'),
    path('admin/', admin.site.urls),
    path('agregar-al-carrito/<int:producto_id>/',agregar_al_carrito,name='agregar_al_carrito'),
    path('carrito',carrito,name='carrito'),
    path('disminuir/<int:cart_item_id>/', disminuir, name='disminuir'),
    path('aumentar/<int:cart_item_id>/', aumentar, name='aumentar'),
    path('Hacer_compra', Hacer_compra, name='Hacer_compra'),
    path('eventos',eventos, name='eventos'),
    path('verordenes', ver_ordeness, name='verordenes'),
    path('shop', shop_view, name='shop'),
    path('dash_admin', dash_admin, name='dash_admin'),
    path('acercade', acercade, name='acercade'),
    path('login_inicial', login_inicial, name='login_inicial'),
    path('clients', clients, name='clients'),
    path('currency', currency, name='currency'),
    
    
    
    
    ]