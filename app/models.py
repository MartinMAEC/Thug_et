from django.conf import settings
from django.db import models
from django.conf import settings
from django.db import models

class Producto(models.Model):
    artista = models.CharField(max_length=50, default='Desconocido')
    nombreprod = models.CharField(max_length=50)
    precio = models.IntegerField()
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to="productos", null=True)
    stock = models.PositiveIntegerField(default=1000)

    def __str__(self):
        return self.nombreprod
    

class Persona(models.Model):       
    rut = models.CharField(max_length=10, primary_key=True)
    nombre = models.CharField(max_length=50, null=False)
    apellido = models.CharField(max_length=50, null=False)
    edad = models.IntegerField(null=False)
    
    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    producto = models.ManyToManyField(Producto, through='CartItem')
    
    @property
    def total_ca(self):
        cart_items = self.cartitem_set.all()
        total_ca = sum(item.subtotal() for item in cart_items)
        return total_ca
        
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    def subtotal(self):
        return self.quantity * self.producto.precio
    
class Purchase(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)  # Puedes ajustar los parámetros según tus necesidades

    def __str__(self):
        return f"Purchase #{self.id}"