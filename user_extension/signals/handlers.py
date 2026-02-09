"""
    Manage signal handlers here
"""

import logging

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from lms.djangoapps.verify_student.models import ManualVerification
from lms.djangoapps.verify_student.utils import earliest_allowed_verification_date
from xmodule.modulestore.django import SignalHandler

from ..models import ExtendedUserProfile

log = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def sync_extended_profile(sender, instance, created, **kwargs):
    """
    On new user creation create object for ExtendedUserProfile
    """
    if created:
        ExtendedUserProfile.objects.create(user=instance)


def set_id_verification_status(user):
    """
    Bypass id_verification for all users.
    Creates an approved ManualVerification if one doesn't exist.
    """
    try:
        # Get previous valid, non-expired verification attempts for this user
        verifications = ManualVerification.objects.filter(
            user=user,
            status="approved",
            created_at__gte=earliest_allowed_verification_date(),
        )

        # If there is none, create a new approved verification for the user
        if not verifications:
            ManualVerification.objects.create(
                user=user,
                status="approved",
            )
            log.info("ManualVerification approved for: %s", user.username)
    except Exception as e:  # pylint: disable=broad-except
        log.error("Error setting ID verification status for user %s: %s", user.username, str(e))


@receiver(post_save, sender=User)
def auto_approve_id_verification_on_registration(sender, instance, created, **kwargs):
    """
    Automatically approve ID verification when a new user is created (registration).
    """
    if created:
        set_id_verification_status(instance)
