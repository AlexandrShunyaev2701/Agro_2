from django.forms import ModelForm
from wagtail.admin.panels import FieldPanel
from wagtail_modeladmin.helpers import PermissionHelper
from wagtail_modeladmin.options import ModelAdmin, modeladmin_register
from wagtail_modeladmin.views import CreateView

from payments.models import Invoice, PaymentAttempt

from .tasks import expire_invoice


class AdminPermissionHelper(PermissionHelper):
    """Custom permission helper for PaymentAttempt model"""

    def user_can_delete_obj(self, user, obj):
        """Method for checking delete permission for PaymentAttempt model"""
        return False

    def user_can_edit_obj(self, user, obj):
        """Method for checking edit permission for PaymentAttempt model"""
        return False


class InvoiceCreateView(CreateView):
    """Create View for Invoice Model"""

    model = Invoice

    def form_valid(self, form: ModelForm) -> ModelForm:
        """Form validation for Invoice Model"""
        obj = form.save(commit=False)
        obj.save()
        expire_invoice.apply_async(
            args=[str(obj.id)],
            eta=obj.expires_at,
        )
        return super().form_valid(form)


class InvoiceWagtailModelAdmin(ModelAdmin):
    """ModelAdmin for Invoice"""

    model = Invoice
    menu_label = "Invoice"
    menu_icon = "doc-full"
    list_display = ("id", "amount", "status", "created_at", "expires_at")
    panels = [
        FieldPanel("amount"),
        FieldPanel("expires_at"),
    ]
    permission_helper_class = AdminPermissionHelper
    list_filter = [
        "status",
    ]
    create_view_class = InvoiceCreateView


class PaymentAttemptCreateView(CreateView):
    """CreateView for PaymentAttempt model"""

    model = PaymentAttempt

    def form_valid(self, form: ModelForm) -> ModelForm:
        """Form validation for PaymentAttempt model"""
        obj = form.save(commit=False)
        if (
            obj.invoice.status == Invoice.InvoiceStatus.PENDING
            and obj.deposit_amount < obj.invoice.amount
        ):
            obj.payment_status = PaymentAttempt.PaymentStatus.INSUFFICIENT_FUNDS
        elif obj.invoice.status == Invoice.InvoiceStatus.EXPIRED:
            obj.payment_status = PaymentAttempt.PaymentStatus.REFUSAL
        else:
            obj.payment_status = PaymentAttempt.PaymentStatus.SUCCESS
            obj.invoice.status = Invoice.InvoiceStatus.PAID
            obj.invoice.save(update_fields=["status"])

        obj.save()
        return super().form_valid(form)


class PaymentAttemptWagtailModelAdmin(ModelAdmin):
    """ModelAdmin for PaymentAttempt"""

    model = PaymentAttempt
    menu_label = "Payment Attempt"
    menu_icon = "doc-full"
    list_display = ("id", "invoice", "deposit_amount", "attempted_at", "payment_status")
    permission_helper_class = AdminPermissionHelper
    create_view_class = PaymentAttemptCreateView
    list_filter = [
        "payment_status",
    ]


modeladmin_register(InvoiceWagtailModelAdmin)
modeladmin_register(PaymentAttemptWagtailModelAdmin)
