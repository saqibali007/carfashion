import random
import string
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.db.models import Q, Avg
from .models import (Product, Category, Cart, CartItem, Order, OrderItem,
                     HomeServiceBooking, Review, CustomerProfile)
from .forms import (RegisterForm, CheckoutForm, ReviewForm,
                    HomeServiceForm, ProfileUpdateForm)
from .email_utils import (send_order_confirmation_email,
                           send_service_booking_email, send_welcome_email)


def generate_order_number():
    return 'CF' + ''.join(random.choices(string.digits, k=8))


def generate_booking_number():
    return 'HS' + ''.join(random.choices(string.digits, k=8))


# ──────────────── HOME ────────────────
def home(request):
    featured_products = Product.objects.filter(is_featured=True, is_available=True)[:8]
    categories = Category.objects.all()[:6]
    latest_products = Product.objects.filter(is_available=True).order_by('-created_at')[:8]
    context = {
        'featured_products': featured_products,
        'categories': categories,
        'latest_products': latest_products,
    }
    return render(request, 'store/home.html', context)


# ──────────────── AUTH ────────────────
def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            send_welcome_email(user)
            login(request, user)
            messages.success(request, f'Welcome to CarFashion, {user.first_name}! Your account is ready.')
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'store/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'store/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')


# ──────────────── PRODUCTS ────────────────
def product_list(request):
    products = Product.objects.filter(is_available=True)
    categories = Category.objects.all()
    
    category_slug = request.GET.get('category')
    search_query = request.GET.get('q')
    sort_by = request.GET.get('sort', 'newest')
    
    if category_slug:
        products = products.filter(category__slug=category_slug)
    
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(brand__icontains=search_query)
        )
    
    if sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')
    else:
        products = products.order_by('-created_at')
    
    context = {
        'products': products,
        'categories': categories,
        'selected_category': category_slug,
        'search_query': search_query,
        'sort_by': sort_by,
    }
    return render(request, 'store/product_list.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_available=True)
    reviews = product.reviews.all().order_by('-created_at')
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    related_products = Product.objects.filter(
        category=product.category, is_available=True
    ).exclude(id=product.id)[:4]
    
    review_form = ReviewForm()
    user_reviewed = False
    
    if request.user.is_authenticated:
        user_reviewed = Review.objects.filter(product=product, user=request.user).exists()
        
        if request.method == 'POST' and not user_reviewed:
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.product = product
                review.user = request.user
                review.save()
                messages.success(request, 'Your review has been submitted!')
                return redirect('product_detail', slug=slug)
    
    context = {
        'product': product,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'related_products': related_products,
        'review_form': review_form,
        'user_reviewed': user_reviewed,
    }
    return render(request, 'store/product_detail.html', context)


# ──────────────── CART ────────────────
@login_required
def cart_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    return render(request, 'store/cart.html', {'cart': cart})


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if not product.in_stock:
        messages.error(request, f'Sorry, {product.name} is out of stock.')
        return redirect('product_detail', slug=product.slug)
    
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not created:
        if cart_item.quantity < product.stock:
            cart_item.quantity += 1
            cart_item.save()
            messages.success(request, f'Updated quantity for {product.name}.')
        else:
            messages.warning(request, f'Only {product.stock} units available.')
    else:
        messages.success(request, f'{product.name} added to cart!')
    
    return redirect('cart')


@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    messages.info(request, 'Item removed from cart.')
    return redirect('cart')


@login_required
def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    quantity = int(request.POST.get('quantity', 1))
    if quantity > 0 and quantity <= cart_item.product.stock:
        cart_item.quantity = quantity
        cart_item.save()
    elif quantity <= 0:
        cart_item.delete()
    return redirect('cart')


# ──────────────── CHECKOUT & ORDERS ────────────────
@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    if not cart.items.exists():
        messages.warning(request, 'Your cart is empty.')
        return redirect('cart')
    
    profile, _ = CustomerProfile.objects.get_or_create(user=request.user)
    
    initial_data = {
        'full_name': f'{request.user.first_name} {request.user.last_name}'.strip() or request.user.username,
        'email': request.user.email,
        'phone': profile.phone,
        'address': profile.address,
        'city': profile.city,
        'state': profile.state,
        'pincode': profile.pincode,
    }
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            d = form.cleaned_data
            shipping = f"{d['address']}, {d['city']}, {d['state']} - {d['pincode']}"
            
            # Check stock availability
            for item in cart.items.all():
                if item.quantity > item.product.stock:
                    messages.error(request, f'Only {item.product.stock} units of {item.product.name} available.')
                    return redirect('cart')
            
            # Create order
            order = Order.objects.create(
                user=request.user,
                order_number=generate_order_number(),
                total_amount=cart.total,
                shipping_address=shipping,
                phone=d['phone'],
                notes=d.get('notes', ''),
            )
            
            # Create order items & reduce stock
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    product_name=item.product.name,
                    price=item.product.price,
                    quantity=item.quantity,
                )
                item.product.stock -= item.quantity
                item.product.save()
            
            # Clear cart
            cart.items.all().delete()
            
            # Send confirmation email
            email_sent = send_order_confirmation_email(order)
            
            msg = f'Order #{order.order_number} placed successfully!'
            if email_sent:
                msg += ' A confirmation receipt has been sent to your email.'
            messages.success(request, msg)
            return redirect('order_detail', order_number=order.order_number)
    else:
        form = CheckoutForm(initial=initial_data)
    
    return render(request, 'store/checkout.html', {'form': form, 'cart': cart})


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/order_list.html', {'orders': orders})


@login_required
def order_detail(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    return render(request, 'store/order_detail.html', {'order': order})


# ──────────────── HOME SERVICE ────────────────
@login_required
def home_service(request):
    bookings = HomeServiceBooking.objects.filter(user=request.user).order_by('-created_at')
    
    if request.method == 'POST':
        form = HomeServiceForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.booking_number = generate_booking_number()
            booking.save()
            
            email_sent = send_service_booking_email(booking)
            
            msg = f'Home service booked! Booking #{booking.booking_number}'
            if email_sent:
                msg += ' — Confirmation sent to your email.'
            messages.success(request, msg)
            return redirect('home_service')
    else:
        profile, _ = CustomerProfile.objects.get_or_create(user=request.user)
        form = HomeServiceForm(initial={'phone': profile.phone, 'address': profile.address})
    
    return render(request, 'store/home_service.html', {'form': form, 'bookings': bookings})


# ──────────────── PROFILE ────────────────
@login_required
def profile(request):
    profile, _ = CustomerProfile.objects.get_or_create(user=request.user)
    orders = Order.objects.filter(user=request.user).order_by('-created_at')[:5]
    bookings = HomeServiceBooking.objects.filter(user=request.user).order_by('-created_at')[:3]
    
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.email = form.cleaned_data['email']
            request.user.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=profile, user=request.user)
    
    return render(request, 'store/profile.html', {
        'form': form, 'orders': orders, 'bookings': bookings
    })
