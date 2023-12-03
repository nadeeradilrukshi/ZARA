from django.shortcuts import render,get_object_or_404, redirect
from django.http import HttpResponse
from . import models
from django.contrib.auth.decorators import login_required

def hello_function(request):
    return HttpResponse("Hello, this is your app!")

def home(request):
     products = models.Product.objects.all()
     return render(request, 'products.html',{'products': products})
 

@login_required(login_url='/admin/login')
def add_to_cart(request, product_id):
    
    product = get_object_or_404(models.Product, id=product_id)
   
    # Check if the user already has the product in the cart
    cart_item, created = models.CartItem.objects.get_or_create(
         user=request.user,
         product=product
    )
    #print(cart_item.product)
    # print(cart_item)
    if not created:
        # If the item already exists, increment the quantity
        cart_item.quantity += 1
        cart_item.save()

    return redirect('/viewcart')

@login_required(login_url='/admin/login/')
def remove_from_cart(request, product_id):
    
    product = get_object_or_404(models.Product, id=product_id)
   
    # Check if the user already has the product in the cart
    cart_item, created = models.CartItem.objects.get_or_create(
         user=request.user,
         product=product
    )
        
    if not created and cart_item.quantity>0:
        # If the item already exists, increment the quantity
        cart_item.quantity -= 1
        cart_item.save()
        
    if not cart_item.quantity > 0 :
        cart_item.delete()

    return redirect('/viewcart')

@login_required(login_url='/admin/login/')
def view_cart(request):
    cart_items = models.CartItem.objects.filter(user=request.user)
      # Calculate subtotal for each cart item and total for all items
    cart_info = []
    full_total = 0

    for item in cart_items:
        subtotal = item.product.price * item.quantity
        full_total += subtotal

        cart_info.append({
            'product': item.product,
            'quantity':item.quantity,
            'subtotal': subtotal,
        })
     
    return render(request, 'cartItems.html', {'cart_items': cart_info})