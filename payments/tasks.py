from celery import shared_task

from .models import Invoice


@shared_task
def expire_invoice(invoice_id: str) -> None:
    """Task for change Invoice status to expired."""
    Invoice.objects.filter(pk=invoice_id, status=Invoice.InvoiceStatus.PENDING).update(
        status=Invoice.InvoiceStatus.EXPIRED
    )
