from django.contrib import admin
from django.urls import path
from django.utils.translation import gettext_lazy as _
from django.contrib.admin.sites import NotRegistered
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from common.djangoapps.student.admin import (
    UserProfileInline,
    AccountRecoveryInline,
    UserChangeForm,
    LanguageAutocomplete,
    CountryAutocomplete,
)
from .models import *


class ExtendedUserProfileInline(admin.StackedInline):
    """Inline admin interface for UserProfile model."""

    model = ExtendedUserProfile
    can_delete = False
    verbose_name_plural = _("Extended User profile")


class UserAdmin(BaseUserAdmin):
    """Admin interface for the User model."""

    inlines = (UserProfileInline, ExtendedUserProfileInline, AccountRecoveryInline)
    form = UserChangeForm

    def get_urls(self):
        """
        Re-register the language and country autocomplete URL patterns.

        The platform's original UserAdmin (student/admin.py) registers these
        two URL patterns inside its own get_urls(). When this plugin replaces
        the User model's admin registration, those URLs are lost because our
        UserAdmin does not inherit get_urls() from the platform's UserAdmin —
        it inherits from BaseUserAdmin (django.contrib.auth.admin.UserAdmin),
        which has no knowledge of these autocomplete views.

        Without this override, the ListSelect2 widget in UserProfileInlineForm
        calls reverse('admin:language-autocomplete') at render time and raises
        a NoReverseMatch, crashing the entire User change view with HTTP 500.
        """
        urls = super().get_urls()
        custom_urls = [
            path(
                "language-autocomplete/",
                LanguageAutocomplete.as_view(),
                name="language-autocomplete",
            ),
            path(
                "country-autocomplete/",
                CountryAutocomplete.as_view(),
                name="country-autocomplete",
            ),
        ]
        return custom_urls + urls

    def get_readonly_fields(self, request, obj=None):
        """
        Allows editing the users while skipping the username check, so we can have Unicode username with no problems.
        The username is marked read-only when editing existing users regardless of `ENABLE_UNICODE_USERNAME`, to simplify the bokchoy tests.  # lint-amnesty, pylint: disable=line-too-long
        """
        django_readonly = super().get_readonly_fields(request, obj)
        if obj:
            return django_readonly + ("username",)
        return django_readonly


# We must first un-register the User model since it may also be registered by the auth app.
try:
    admin.site.unregister(User)
except NotRegistered:
    pass

admin.site.register(User, UserAdmin)
