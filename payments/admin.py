from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Invoice, PaymentAttempt
from .tasks import expire_invoice
from .unfold.sites import payments_admin_site


class PermissionHelper:
    """Permission helper class"""

    def get_actions(self, request):
        actions = super().get_actions(request)
        actions.pop("delete_selected", None)
        return actions

    def has_change_permission(self, request, obj=None) -> bool:
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        return False


@admin.register(Invoice, site=payments_admin_site)
class InvoiceUnfoldAdmin(PermissionHelper, ModelAdmin):
    list_display = ("id", "amount", "status", "expires_at")
    list_filter = ("status",)
    readonly_fields = ("status",)

    def save_model(self, request, obj, form, change):
        """Save method for Invoice"""
        super().save_model(request, obj, form, change)
        expire_invoice.apply_async(
            args=[str(obj.id)],
            eta=obj.expires_at,
        )


@admin.register(PaymentAttempt, site=payments_admin_site)
class PaymentAttemptUnfoldAdmin(PermissionHelper, ModelAdmin):
    list_display = ("id", "invoice", "deposit_amount", "payment_status", "attempted_at")
    list_filter = ("payment_status",)
    readonly_fields = ("payment_status",)

    def save_model(self, request, obj, form, change):
        """Save method for PaymentAttempt"""
        if not change:
            invoice = obj.invoice

            if invoice.status == Invoice.InvoiceStatus.EXPIRED:
                obj.payment_status = PaymentAttempt.PaymentStatus.REFUSAL

            elif (
                invoice.status == Invoice.InvoiceStatus.PENDING
                and obj.deposit_amount < invoice.amount
            ):
                obj.payment_status = PaymentAttempt.PaymentStatus.INSUFFICIENT_FUNDS

            else:
                obj.payment_status = PaymentAttempt.PaymentStatus.SUCCESS
                invoice.status = Invoice.InvoiceStatus.PAID
                invoice.save(update_fields=["status"])

        super().save_model(request, obj, form, change)
