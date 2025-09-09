from celery import shared_task
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from .models import Order


@shared_task
def send_invoice_to_admin(order_id):
    """
    Send order invoice to admin email.
    """
    try:
        order = Order.objects.select_related(
            'shipping_address'
        ).prefetch_related(
            'items__supplier_product__product',
            'items__supplier_product__supplier'
        ).get(id=order_id)


        context = {
            'order': order,
            'items': order.items.all(),
            'shipping_address': order.shipping_address
        }

        subject = f'Накладная заказа #{order.order_number}'
        message = render_to_string('emails/invoice_admin.txt', context)
        html_message = render_to_string('emails/invoice_admin.html', context)


        email = EmailMessage(
            subject=subject,
            body=html_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.ADMIN_EMAIL],
        )
        email.content_subtype = 'html'
        email.send()

    except Order.DoesNotExist:
        print(f"Order with id {order_id} does not exist")


@shared_task
def send_order_confirmation_email(order_id):
    """
    Send order confirmation email to customer.
    """
    try:
        order = Order.objects.select_related(
            'user', 'shipping_address'
        ).prefetch_related(
            'items__supplier_product__product'
        ).get(id=order_id)

        context = {
            'order': order,
            'items': order.items.all(),
            'shipping_address': order.shipping_address
        }

        subject = f'Подтверждение заказа #{order.order_number}'
        message = render_to_string('emails/order_confirmation.txt', context)
        html_message = render_to_string('emails/order_confirmation.html', context)

        email = EmailMessage(
            subject=subject,
            body=html_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[order.user.email],
        )
        email.content_subtype = 'html'
        email.send()

        send_invoice_to_admin.delay(order_id)

    except Order.DoesNotExist:
        print(f"Order with id {order_id} does not exist")