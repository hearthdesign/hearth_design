# ==========================================
#             SHOP APP URL ROUTES
# ==========================================
from django.urls import path
from . import views

# ==========================================
#        GALLERIES, CATALOG & REVIEWS
# ==========================================
urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("theme-filter/", views.theme_filter, name="theme_filter"),
    path(
        "gallery/illustrations/",
        views.illustration_gallery,
        name="illustration_gallery",
    ),
    path(
        "gallery/photography/",
        views.photography_gallery,
        name="photography_gallery",
    ),
    path("upload/", views.upload_print, name="upload_print"),
    # Requires print_id so reviews attach to a specific Print item
    path(
        "review/add/<int:print_id>/",
        views.add_review,
        name="add_review",
    ),
    # ==========================================
    #       ACCOUNT, CONTACT & LEGAL PAGES
    # ==========================================
    path("signup/", views.signup, name="signup"),
    path("account/delete/", views.delete_account, name="delete_account"),
    path("thank-you/", views.thank_you, name="thank_you"),
    path("contact/", views.contact_view, name="contact"),
    path("terms/", views.terms_of_service, name="terms_of_service"),
    path("privacy-policy/", views.privacy_policy, name="privacy_policy"),
    # ==========================================
    #         LANGUAGE SWITCHER & ROBOTS
    # ==========================================
    path("set-language/", views.custom_set_language, name="custom_set_language"),
    path("robots.txt", views.RobotsTxtView.as_view(), name="robots_txt"),
]