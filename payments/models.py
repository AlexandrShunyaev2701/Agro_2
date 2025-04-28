import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Invoice(models.Model):
    """Model representing an invoice"""

    class InvoiceStatus(models.TextChoices):
        """Model choices for invoice status"""

        PENDING = "PENDING"
        PAID = "PAID"
        EXPIRED = "EXPIRED"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    amount = models.DecimalField("Invoice sum", max_digits=10, decimal_places=2)
    created_at = models.DateTimeField("Creating date", auto_now_add=True)
    status = models.CharField(
        "Invoices status", choices=InvoiceStatus.choices, default=InvoiceStatus.PENDING
    )
    expires_at = models.DateTimeField("Expiring date", null=True, blank=True)

    class Meta:
        verbose_name = "Invoice"
        verbose_name_plural = "Invoices"

    def clean(self) -> None:
        """Validate field expires_at for creating Invoice objects"""
        if self.expires_at <= timezone.now():
            raise ValidationError("Invoice has expired failed value")

    def __str__(self):
        return f"Invoice: {self.id} - status: {self.status}"


class PaymentAttempt(models.Model):
    """Model representing a payment attempt"""

    class PaymentStatus(models.TextChoices):
        """Model choices for payment status"""

        SUCCESS = "SUCCESS"
        INSUFFICIENT_FUNDS = "INSUFFICIENT_FUNDS"
        REFUSAL = "REFUSAL"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    invoice = models.ForeignKey(
        Invoice, on_delete=models.PROTECT, related_name="payment_attempts"
    )
    deposit_amount = models.DecimalField(
        "Deposit amount", max_digits=10, decimal_places=2
    )
    attempted_at = models.DateTimeField("Attempted date", auto_now_add=True)
    payment_status = models.CharField(
        "Payment status", choices=PaymentStatus.choices, editable=False
    )

    class Meta:
        verbose_name = "Payment attempt"
        verbose_name_plural = "Payment attempts"

    def clean(self) -> None:
        """Validate PaymentAttempt"""
        if self.invoice.status in ["PAID", "EXPIRED"]:
            raise ValidationError(
                "You cannot create a payment attempt for a paid or overdue invoice."
            )

    def __str__(self):
        return f"Payment attempt: {self.id} - status: {self.payment_status}"
