from django.db.models import Count

from ..models import Invoice, PaymentAttempt


def dashboard_callback(request, context):
    """Return context for dashboard."""
    inv_qs = Invoice.objects.values("status").annotate(count=Count("id"))
    att_qs = PaymentAttempt.objects.values("payment_status").annotate(count=Count("id"))

    status_colors = {
        Invoice.InvoiceStatus.PENDING: "yellow",
        Invoice.InvoiceStatus.PAID: "green",
        Invoice.InvoiceStatus.EXPIRED: "red",
        PaymentAttempt.PaymentStatus.SUCCESS: "green",
        PaymentAttempt.PaymentStatus.INSUFFICIENT_FUNDS: "orange",
        PaymentAttempt.PaymentStatus.REFUSAL: "red",
    }

    invoice_cards = [
        {
            "status": item["status"],
            "count": item["count"],
            "color": status_colors.get(item["status"], "gray"),
        }
        for item in inv_qs
    ]
    attempt_cards = [
        {
            "status": item["payment_status"],
            "count": item["count"],
            "color": status_colors.get(item["payment_status"], "gray"),
        }
        for item in att_qs
    ]

    context.update(
        {
            "invoice_cards": invoice_cards,
            "attempt_cards": attempt_cards,
        }
    )
    return context
