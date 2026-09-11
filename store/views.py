from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Cart, Address, Order, OrderItem
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def home(request):
    return render(request, 'store/home.html')


def product(request):

    products = Product.objects.all()

    category = request.GET.get('category')
    sort = request.GET.get('sort')
    search = request.GET.get('search')

    # SEARCH PRODUCTS
    if search:
        products = products.filter(
            name__icontains=search
        )

    # FILTER BY CATEGORY
    if category:
        products = products.filter(
            category=category
        )

    # SORT PRODUCTS
    if sort == 'newest':
        products = products.order_by('-id')

    elif sort == 'low-high':
        products = products.order_by('price')

    elif sort == 'high-low':
        products = products.order_by('-price')

    context = {
        'products': products,
        'selected_category': category,
        'selected_sort': sort,
        'search': search,
    }

    return render(request, 'store/product.html', context)

def sale(request):

    products = Product.objects.filter(
        sale_price__isnull=False
    )

    return render(
        request,
        'store/sale.html',
        {'products': products}
    )

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    related_products = Product.objects.filter(
        category=product.category
    ).exclude(
        id=product.id
    )[:4]

    context = {
        'product': product,
        'related_products': related_products,
    }

    return render(request, 'store/product_detail.html', context)

def add_to_cart(request, product_id):

    product = get_object_or_404(Product, id=product_id)

    if not request.user.is_authenticated:
        return redirect('login')

    quantity = int(request.POST.get('quantity', 1))

    # Check if product is out of stock
    if product.stock == 0:

        messages.error(
            request,
            "This product is currently out of stock."
        )

        return redirect(
            'product_detail',
            product_id=product.id
        )

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product
    )
    # Calculate total quantity requested
    if created:
        new_quantity = quantity
    else:
        new_quantity = cart_item.quantity + quantity

    # Prevent adding more than available stock
    if new_quantity > product.stock:
        return redirect(
            'product_detail',
            product_id=product.id
        )

    cart_item.quantity = new_quantity
    cart_item.save()

    return redirect(
        'product_detail',
        product_id=product.id
    )
def cart(request):

    if not request.user.is_authenticated:
        return redirect('login')

    cart_items = Cart.objects.filter(user=request.user)

    total = 0

    for item in cart_items:
        item.total_price = item.product.price * item.quantity
        total += item.total_price

    context = {
        'cart_items': cart_items,
        'total': total,
    }

    return render(request, 'store/cart.html', context)
def update_cart_quantity(request, item_id):

    if not request.user.is_authenticated:
        return redirect('login')

    cart_item = get_object_or_404(
        Cart,
        id=item_id,
        user=request.user
    )

    if request.method == 'POST':

        action = request.POST.get('action')

        # INCREASE QUANTITY
        if action == 'increase':

            if cart_item.quantity < cart_item.product.stock:
                cart_item.quantity += 1
            else:
                messages.error(
                    request,
                    f"Only {cart_item.product.stock} items are available in stock."
                )

        # DECREASE QUANTITY
        elif action == 'decrease':

            if cart_item.quantity > 1:
                cart_item.quantity -= 1

        cart_item.save()

    return redirect('cart')
def remove_from_cart(request, item_id):

    if not request.user.is_authenticated:
        return redirect('login')

    cart_item = get_object_or_404(
        Cart,
        id=item_id,
        user=request.user
    )

    if request.method == 'POST':
        cart_item.delete()

    return redirect('cart')
def checkout(request):

    if not request.user.is_authenticated:
        return redirect('login')

    # GET LOGGED-IN USER'S ADDRESSES
    addresses = Address.objects.filter(user=request.user)

    # SAVE NEW ADDRESS
    if request.method == 'POST':

        Address.objects.create(
            user=request.user,
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            phone=request.POST.get('phone'),
            address=request.POST.get('address'),
            city=request.POST.get('city'),
            state=request.POST.get('state'),
            pincode=request.POST.get('pincode')
        )

        return redirect('checkout')


    # GET LOGGED-IN USER'S CART
    cart_items = Cart.objects.filter(user=request.user)

    total = 0

    for item in cart_items:
        item.total_price = item.product.price * item.quantity
        total += item.total_price


    # GET DETAILS FROM FIRST SAVED ADDRESS
    user_address = addresses.first()


    context = {
        'cart_items': cart_items,
        'addresses': addresses,
        'user_address': user_address,
        'total': total,
    }

    return render(request, 'store/checkout.html', context)
# =========================
# SIGNUP
# =========================

def signup(request):
    if request.method == 'POST':

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('signup')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(request, "Account created successfully. Please log in.")
        return redirect('login')

    return render(request, 'store/signup.html')


# =========================
# LOGIN
# =========================

def login_view(request):
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('home')

        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'store/login.html')


# =========================
# LOGOUT
# =========================

def logout_view(request):
    logout(request)
    return redirect('home')

def place_order(request):

    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':

        selected_address_id = request.POST.get('selected_address')

        if not selected_address_id:
            return redirect('checkout')

        address = get_object_or_404(
            Address,
            id=selected_address_id,
            user=request.user
        )

        cart_items = Cart.objects.filter(user=request.user)

        if not cart_items.exists():
            return redirect('cart')

        total = 0

        # CHECK STOCK AND CALCULATE TOTAL
        for item in cart_items:

            # Make sure enough stock is available
            if item.quantity > item.product.stock:

                messages.error(
                    request,
                    f"{item.product.name} does not have enough stock available."
                )

                return redirect('cart')

            total += item.product.price * item.quantity


        # CREATE ORDER
        order = Order.objects.create(
            user=request.user,
            address=address,
            total_amount=total
        )


        # CREATE ORDER ITEMS AND REDUCE STOCK
        for item in cart_items:

            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

            # Reduce product stock
            item.product.stock -= item.quantity
            item.product.save()


        # CLEAR USER'S CART
        cart_items.delete()


        # GO TO ORDER CONFIRMATION PAGE
        return redirect(
            'order_confirmation',
            order_id=order.id
        )

    return redirect('checkout')

def order_confirmation(request, order_id):

    if not request.user.is_authenticated:
        return redirect('login')

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    context = {
        'order': order,
    }

    return render(
        request,
        'store/order_confirmation.html',
        context
    )

def my_orders(request):

    if not request.user.is_authenticated:
        return redirect('login')

    orders = Order.objects.filter(
        user=request.user
    ).order_by('-created_at')

    context = {
        'orders': orders,
    }

    return render(
        request,
        'store/my_orders.html',
        context
    )

def order_detail(request, order_id):

    if not request.user.is_authenticated:
        return redirect('login')

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    context = {
        'order': order,
    }

    return render(
        request,
        'store/order_detail.html',
        context
    )

def contact(request):
    return render(request, 'store/contact.html')

def profile(request):
    if not request.user.is_authenticated:
        return redirect('login')

    return render(request, 'store/profile.html')