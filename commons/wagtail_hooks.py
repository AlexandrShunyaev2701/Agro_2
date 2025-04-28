from django.templatetags.static import static
from django.utils.html import format_html
from wagtail import hooks
from wagtail.admin.site_summary import SummaryItem


@hooks.register("construct_homepage_summary_items")
def remove_summary(request, items) -> None:
    """Remove summary of pages, documents and images from admin index."""
    items[:] = [i for i in items if not isinstance(i, SummaryItem)]


@hooks.register("construct_main_menu")
def remove_default_menu_items(request, items) -> None:
    """Remove default menu items."""
    exclude = ("explorer", "images", "reports", "help")
    items[:] = [i for i in items if i.name not in exclude]


@hooks.register("construct_settings_menu")
def remove_default_settings_items(request, items) -> None:
    """Remove default settings items."""
    exclude = ("collections", "workflows", "workflow-tasks")
    items[:] = [i for i in items if i.name not in exclude]


@hooks.register("construct_main_menu")
def hide_documents_menu_item(request, menu_items) -> None:
    """Delete item document from admin menu"""
    menu_items[:] = [item for item in menu_items if item.name != "documents"]


@hooks.register("insert_global_admin_css")
def global_admin_css():
    """Add custom CSS to admin site."""
    return format_html(
        '<link rel="stylesheet" href="{}">', static("admin/css/custom_admin.css")
    )
