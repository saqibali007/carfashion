from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


def send_order_confirmation_email(order):
    """Send order confirmation email with receipt to customer."""
    subject = f'Order Confirmed! #{order.order_number} - CarFashion'
    
    items_text = '\n'.join([
        f'  - {item.product_name} x{item.quantity} = ₹{item.subtotal}'
        for item in order.items.all()
    ])
    
    message = f"""
Dear {order.user.first_name or order.user.username},

Thank you for shopping with CarFashion! Your order has been confirmed.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
         ORDER RECEIPT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Order Number : #{order.order_number}
Order Date   : {order.created_at.strftime('%d %B %Y, %I:%M %p')}
Status       : {order.get_status_display()}

ITEMS ORDERED:
{items_text}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL AMOUNT : ₹{order.total_amount}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DELIVERY ADDRESS:
{order.shipping_address}

Contact: {order.phone}

Your order will be processed and shipped within 2-3 business days.
You will receive a tracking update via email once shipped.

For any queries, reply to this email or contact us.

Thank you for choosing CarFashion!
🚗 Drive in Style.

— Team CarFashion
"""
    
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[order.user.email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f'Email sending failed: {e}')
        return False


def send_service_booking_email(booking):
    """Send home service booking confirmation to customer."""
    subject = f'Home Service Booked! #{booking.booking_number} - CarFashion'
    
    message = f"""
Dear {booking.user.first_name or booking.user.username},

Your home service booking has been received!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
     SERVICE BOOKING RECEIPT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Booking Number : #{booking.booking_number}
Service        : {booking.get_service_type_display()}
Date           : {booking.preferred_date.strftime('%d %B %Y')}
Time           : {booking.preferred_time.strftime('%I:%M %p')}
Status         : {booking.get_status_display()}

SERVICE ADDRESS:
{booking.address}

Contact: {booking.phone}

DESCRIPTION:
{booking.description}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Our technician will arrive at your location on the scheduled date and time.
We will confirm your booking within 2 hours.

For any queries, reply to this email or contact us.

Thank you for choosing CarFashion Home Service!
🔧 We come to you.

— Team CarFashion
"""
    
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[booking.user.email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f'Email sending failed: {e}')
        return False


def send_welcome_email(user):
    """Send welcome email to newly registered user."""
    subject = 'Welcome to CarFashion! 🚗'
    message = f"""
Dear {user.first_name or user.username},

Welcome to CarFashion — Your one-stop destination for premium car accessories!

Your account has been created successfully.

Username: {user.username}
Email: {user.email}

Start exploring our collection of:
✅ LED Headlights & DRLs
✅ Car Body Kits & Wraps  
✅ Interior Accessories
✅ Performance Parts
✅ And much more!

We also offer HOME SERVICE — our technicians come to you!

Visit us: http://localhost:8000

Drive in Style with CarFashion!

— Team CarFashion
"""
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=True,
        )
    except Exception as e:
        print(f'Welcome email failed: {e}')
