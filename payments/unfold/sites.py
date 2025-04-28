from unfold.sites import UnfoldAdminSite


class PaymentsUnfoldAdminSite(UnfoldAdminSite):
    """Class for Unfold Payments Admin"""

    site_title = "Unfold Payments Admin"


payments_admin_site = PaymentsUnfoldAdminSite(name="payments_unfold")
