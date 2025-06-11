from django.shortcuts import render, redirect
from .models import Farmer, Product, Order, OrderItem
from django.contrib.auth.decorators import login_required
from .forms import SimpleRegisterForm

def index(request):
    return render(request, 'index.html')

def farmers(request):
    farmers = Farmer.objects.all()
    return render(request, 'farmers.html', {'farmers': farmers})

def products(request):
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products})

def contact(request):
    return render(request, 'contact.html')

def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart
    return redirect('products')

def view_cart(request):
    cart = request.session.get('cart', {})
    items = []
    total = 0

    for product_id, qty in cart.items():
        product = Product.objects.get(id=product_id)
        subtotal = product.price * qty
        items.append({
            'product': product,
            'quantity': qty,
            'subtotal': subtotal,
        })
        total += subtotal

    return render(request, 'cart.html', {'items': items, 'total': total})

def increase_quantity(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        cart[str(product_id)] += 1
    request.session['cart'] = cart
    return redirect('view_cart')

def decrease_quantity(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        cart[str(product_id)] -= 1
        if cart[str(product_id)] <= 0:
            del cart[str(product_id)]
    request.session['cart'] = cart
    return redirect('view_cart')

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
    request.session['cart'] = cart
    return redirect('view_cart')

def clear_cart(request):
    request.session['cart'] = {}
    return redirect('view_cart')

def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('view_cart')

    total = 0
    items = []

    for product_id, qty in cart.items():
        product = Product.objects.get(id=product_id)
        subtotal = product.price * qty
        total += subtotal
        items.append((product, qty, subtotal))

    order = Order.objects.create(
        user=request.user if request.user.is_authenticated else None,
        total=total
    )

    for product, qty, subtotal in items:
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=qty,
            subtotal=subtotal
        )

    request.session['cart'] = {}

    return render(request, 'checkout.html', {'order': order})

@login_required
def account(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'account.html', {'orders': orders})

def register_view(request):
    if request.method == 'POST':
        form = SimpleRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # хешируем
            user.save()
            return redirect('login')  # после регистрации — на логин
    else:
        form = SimpleRegisterForm()
    return render(request, 'register.html', {'form': form})


