# shop views

import hashlib
import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.exceptions import ImproperlyConfigured
from django.core.mail import send_mail
from django.core.cache import cache
from django.core.paginator import Paginator  # For pagination
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, translate_url
from django.utils import timezone, translation
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView

from .forms import (
    ContactForm,
    CustomSignupForm,
    PrintForm,
    ReviewForm,
    AccountDeleteForm)

# Import all models
from .models import ContactSubmission, Print, Theme
from checkout.models import Cart

logger = logging.getLogger(__name__)

DELETE_ATTEMPT_LIMIT = 5
DELETE_ATTEMPT_WINDOW_SECONDS = 900  # 15 minutes

def _get_client_ip(request):
    forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "unknown")


# ==========================================
#               HOMEPAGE
# ==========================================
def homepage(request):
    # Get filters from query string
    print_type = request.GET.get("type")  # 'illustration' or 'photo'
    theme_slug = request.GET.get("theme")

    # Base queryset: active prints
    prints = Print.objects.filter(
        is_active=True,
        stock__gt=0,
    ).order_by("-date")

    # Filter by category type if provided
    if print_type in ["illustration", "photo"]:
        prints = prints.filter(type=print_type)

    # Filter by theme if provided
    theme = None
    if theme_slug:
        theme = Theme.objects.filter(slug=theme_slug).first()
        if theme:
            prints = prints.filter(themes=theme)

    # Paginate results
    paginator = Paginator(prints, 12)  # 12 prints per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "shop/homepage.html",
        {
            "page_obj": page_obj,
            "category": print_type,
            "theme": theme,
            "login_url": reverse("login"),
        },
    )


# ==========================================
#               UPLOAD PRINT
# ==========================================
@login_required
def upload_print(request):
    if request.method == "POST":
        form = PrintForm(request.POST, request.FILES)

        if form.is_valid():
            print_obj = form.save(commit=False)

            # Set today's date automatically
            print_obj.date = timezone.now().date()

            print_obj.save()
            form.save_m2m()

            # Redirect based on type
            if print_obj.type == "photo":
                return redirect("photography_gallery")

            elif print_obj.type == "illustration":
                return redirect("illustration_gallery")

    else:
        form = PrintForm()

    return render(request, "shop/upload.html", {"form": form})


# ==========================================
#          ILLUSTRATION GALLERY
# ==========================================
def illustration_gallery(request):
    prints = Print.objects.filter(
        type="illustration",
        stock__gt=0,
        is_active=True,
    ).order_by("-date")

    paginator = Paginator(prints, 20)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "shop/illustration_gallery.html",
        {
            "page_obj": page_obj,
            "category": "illustration",
            "theme": None,
        },
    )


# ==========================================
#         PHOTOGRAPHY GALLERY
# ==========================================
def photography_gallery(request):
    prints = Print.objects.filter(
        type="photo",
        stock__gt=0,
        is_active=True,
    ).order_by("-date")

    paginator = Paginator(prints, 20)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "shop/photography_gallery.html",
        {
            "page_obj": page_obj,
            "category": "photo",
            "theme": None,
        },
    )


# ==========================================
#          THEME FILTER
# ==========================================
# with optional print type
def theme_filter(request):
    slug = request.GET.get("theme")

    if not slug:
        return redirect("homepage")

    # 'illustration' or 'photo'
    print_type = request.GET.get("type")

    # If it's missing, redirect to the homepage
    theme = get_object_or_404(Theme, slug=slug)

    # Base queryset
    prints = Print.objects.filter(
        themes=theme,
        stock__gt=0,
        is_active=True,
    )

    # Decide which queryset to use based on print type
    if print_type == "illustration":
        prints = prints.filter(type="illustration")
        template = "shop/illustration_gallery.html"

    elif print_type == "photo":
        prints = prints.filter(type="photo")
        template = "shop/photography_gallery.html"

    else:
        # If no print type is specified, return all active prints
        # belonging to the selected theme (combine both)
        template = "shop/themed_gallery.html"

    prints = prints.order_by("-date")

    # Paginate results
    paginator = Paginator(prints, 20)  # 20 items per page

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        template,
        {
            "page_obj": page_obj,
            "theme": theme,
            "selected_theme": theme,
            "print_type": print_type,
            "category": print_type,
        },
    )

@login_required  # Ensures only logged-in users can leave reviews
def add_review(request, print_id):
    print_item = get_object_or_404(Print, id=print_id)

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            # Create the review object but don't save to DB yet
            review = form.save(commit=False)

            # Attach the print item and the currently logged-in user
            review.print_item = print_item
            review.user = request.user

            # Now save it permanently to the database
            review.save()

            # Redirect back to the print detail page or gallery
            return redirect(
                "homepage"
            )  # Replace with your actual detail or redirect URL
    else:
        form = ReviewForm()

    return render(
        request, "shop/add_review.html", {"form": form, "print_item": print_item}
    )


# ==========================================
#              SET LANGUAGE
# ==========================================
def custom_set_language(request):
    """
    Custom language switcher view that safely handles i18n URL prefixes
    and prevents redirect loops.
    """
    next_url = request.POST.get("next", request.GET.get("next", "/"))
    lang_code = request.POST.get("language", request.GET.get("language"))

    if lang_code and lang_code in [lang[0] for lang in settings.LANGUAGES]:
        # Activate language and set translation environment
        translation.activate(lang_code)

        # Strip current language prefix from next_url if present (e.g., '/de/
        # about/' -> '/about/')
        # FIX: Use .lower() to match lowercase URL prefixes like '/zh-hans/'
        for lang in [lang[0] for lang in settings.LANGUAGES]:
            prefix = f"/{lang}/".lower()
            if next_url.lower().startswith(prefix):
                next_url = next_url[len(prefix) - 1 :] # Keeps the leading slash
                break
            elif next_url.lower() == f"/{lang}".lower():
                next_url = "/"
                break

        # Translate the URL into the new language prefix pattern
        translated_url = translate_url(next_url, lang_code)

        # Create response and set the official Django language cookie
        response = HttpResponseRedirect(translated_url)
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code)
        return response

    return HttpResponseRedirect("/")


# ==========================================
#             CONTACT FORM
# ==========================================
def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            # Honeypot check
            if form.cleaned_data.get("website"):
                return redirect("thank_you")

            # Privacy checkbox server-side validation
            if not form.cleaned_data.get("privacy_agree"):
                form.add_error(
                    "privacy_agree", _("You must agree to the Privacy Notice")
                )
            else:
                # Metadata
                ip = request.META.get("REMOTE_ADDR", "")
                user_agent = request.META.get("HTTP_USER_AGENT", "")
                ip_hash = hashlib.sha256(ip.encode()).hexdigest()

                # Save to database
                ContactSubmission.objects.create(
                    name=form.cleaned_data["name"],
                    email=form.cleaned_data["email"],
                    message=form.cleaned_data["message"],
                    ip_hash=ip_hash,
                    user_agent=user_agent,
                    submitted_at=timezone.now(),
                    marketing_consent=form.cleaned_data.get("marketing_consent", False),
                )

                # Send email to admin
                send_mail(
                    subject=_("New Contact Form Submission from %(name)s")
                    % {"name": form.cleaned_data["name"]},
                    message=form.cleaned_data["message"],
                    from_email=form.cleaned_data["email"],
                    recipient_list=["1.space.channel.1@gmail.com"],
                )

                # Confirmation email to user
                subject = _("Thank you for contacting Hearth Design")
                message = _(
                    "Hi %(name)s,\n\n"
                    "Thank you for reaching out to us. "
                    "We've received your message and will get back to you shortly.\n\n"
                    "Best regards,\n"
                    "Hearth Design Team"
                ) % {"name": form.cleaned_data["name"]}
                send_mail(
                    subject=subject,
                    message=message,
                    from_email="noreply@hearth.design",
                    recipient_list=[form.cleaned_data["email"]],
                )

                return redirect("thank_you")
    else:
        form = ContactForm()
    return render(request, "shop/contact.html", {"form": form})


# ==========================================
#              SIGNUP
# ==========================================
def signup(request):
    if request.method == "POST":
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            send_mail(
                subject="Welcome to Hearth Shop!",
                message=f"Thank you for signing up, {user.username}.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
            return redirect("login")
    else:
        form = CustomSignupForm()
    return render(request, "registration/signup.html", {"form": form})


# ==========================================
#              DELETE ACCOUNT
# ==========================================
@login_required
@require_http_methods(["GET", "POST"])
def delete_account(request):
    if request.user.is_staff or request.user.is_superuser:
        messages.error(
            request,
            _(
                "Staff and administrator accounts cannot be deleted through this self-service form."
            ),
        )
        return redirect("homepage")

    cache_key = f"delete_account_attempts:user:{request.user.pk}"
    attempts = cache.get(cache_key, 0)

    if request.method == "POST":
        if attempts >= DELETE_ATTEMPT_LIMIT:
            messages.error(
                request,
                _(
                    "Too many account deletion attempts. Please wait a few minutes and try again."
                ),
            )
            return render(
                request,
                "shop/delete_account.html",
                {"form": AccountDeleteForm(user=request.user)},
            )

        form = AccountDeleteForm(request.POST, user=request.user)
        if form.is_valid():
            user = request.user
            deleted_user_id = user.pk
            client_ip = _get_client_ip(request)

            with transaction.atomic():
                Cart.objects.filter(user=user).delete()
                logout(request)
                user.delete()

            cache.delete(cache_key)
            logger.info(
                "Account deleted: user_id=%s ip=%s",
                deleted_user_id,
                client_ip,
            )
            messages.success(
                request,
                _("Your account has been permanently deleted."),
            )
            return redirect("homepage")

        cache.set(cache_key, attempts + 1, timeout=DELETE_ATTEMPT_WINDOW_SECONDS)
    else:
        form = AccountDeleteForm(user=request.user)

    return render(request, "registration/delete_account.html", {"form": form})


# ==========================================
#          CONTACT RESPONSE
# ==========================================
@login_required
def thank_you(request):
    return render(request, "shop/thank_you.html")


# ==========================================
#          FOOTER LINKS
# ==========================================
# Terms of Service
def terms_of_service(request):
    return render(request, "shop/terms.html")


# Private Policy
def privacy_policy(request):
    return render(request, "shop/privacy_policy.html")


# robots.txt
class RobotsTxtView(TemplateView):
    template_name = "robots.txt"
