from django.db.models import Count

from ..models import Invoice, PaymentAttempt


def dashboard_callback(request, context):
    """Return context for dashboard with correctly mapped status colors."""

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

    invoice_cards = []
    for item in inv_qs:
        status_enum = Invoice.InvoiceStatus(item["status"])
        invoice_cards.append(
            {
                "status": status_enum,
                "count": item["count"],
                "color": status_colors.get(status_enum, "gray"),
            }
        )

    attempt_cards = []
    for item in att_qs:
        status_enum = PaymentAttempt.PaymentStatus(item["payment_status"])
        attempt_cards.append(
            {
                "status": status_enum,
                "count": item["count"],
                "color": status_colors.get(status_enum, "gray"),
            }
        )

    context.update(
        {
            "invoice_cards": invoice_cards,
            "attempt_cards": attempt_cards,
        }
    )
    return context
