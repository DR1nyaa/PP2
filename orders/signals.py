from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Order
from .tasks import send_order_status_update_email

@receiver(pre_save, sender=Order)
def track_order_status_change(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_instance = Order.objects.get(pk=instance.pk)
            if old_instance.status != instance.status:
                # Send email notification for status change
                send_order_status_update_email.delay(instance.id, old_instance.status, instance.status)
        except Order.DoesNotExist:
            pass