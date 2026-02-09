"""
Management command to approve ID verification for existing users.
"""

import logging

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from lms.djangoapps.verify_student.models import ManualVerification
from lms.djangoapps.verify_student.utils import earliest_allowed_verification_date

log = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Management command to approve ID verification for existing users.

    Usage:
        ./manage.py lms approve_id_verification
        ./manage.py lms approve_id_verification --all
        ./manage.py lms approve_id_verification --username john_doe
        ./manage.py lms approve_id_verification --batch-size 100
    """

    help = "Approve ID verification for existing users who don't have valid verification"

    def add_arguments(self, parser):
        parser.add_argument(
            "--all",
            action="store_true",
            help="Process all users without valid ID verification",
        )
        parser.add_argument(
            "--username",
            type=str,
            help="Approve ID verification for a specific user",
        )
        parser.add_argument(
            "--batch-size",
            type=int,
            default=100,
            help="Number of users to process in each batch (default: 100)",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be done without making any changes",
        )

    def handle(self, *args, **options):
        all_users = options["all"]
        username = options["username"]
        batch_size = options["batch_size"]
        dry_run = options["dry_run"]

        if not all_users and not username:
            self.stdout.write(
                self.style.ERROR("You must specify either --all or --username <username>")
            )
            return

        if username:
            try:
                user = User.objects.get(username=username)
                self._approve_user_verification(user, dry_run)
            except User.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'User "{username}" does not exist'))
        else:
            self._approve_all_users(batch_size, dry_run)

    def _approve_user_verification(self, user, dry_run=False):
        """
        Approve ID verification for a single user.
        """
        earliest_date = earliest_allowed_verification_date()

        # Check if user already has valid verification
        existing_verification = ManualVerification.objects.filter(
            user=user,
            status="approved",
            created_at__gte=earliest_date,
        ).exists()

        if existing_verification:
            self.stdout.write(
                self.style.WARNING(f'User "{user.username}" already has valid ID verification')
            )
            return

        if dry_run:
            self.stdout.write(
                self.style.SUCCESS(f"[DRY RUN] Would approve ID verification for: {user.username}")
            )
        else:
            ManualVerification.objects.create(
                user=user,
                status="approved",
            )
            self.stdout.write(self.style.SUCCESS(f"Approved ID verification for: {user.username}"))
            log.info("ManualVerification approved for: %s", user.username)

    def _approve_all_users(self, batch_size, dry_run=False):
        """
        Approve ID verification for all users who don't have valid verification.
        """
        earliest_date = earliest_allowed_verification_date()

        # Get all users who don't have valid verification
        users_with_verification = ManualVerification.objects.filter(
            status="approved",
            created_at__gte=earliest_date,
        ).values_list("user_id", flat=True)

        users_to_approve = User.objects.exclude(id__in=users_with_verification).order_by("id")

        total_users = users_to_approve.count()

        if total_users == 0:
            self.stdout.write(self.style.SUCCESS("No users need ID verification approval"))
            return

        self.stdout.write(
            self.style.WARNING(f"Found {total_users} users without valid ID verification")
        )

        if dry_run:
            self.stdout.write(
                self.style.SUCCESS(
                    f"[DRY RUN] Would approve ID verification for {total_users} users"
                )
            )
            # Show first 10 users as examples
            for user in users_to_approve[:10]:
                self.stdout.write(f"  - {user.username}")
            if total_users > 10:
                self.stdout.write(f"  ... and {total_users - 10} more")
            return

        approved_count = 0
        error_count = 0

        # Process users in batches
        user_ids = list(users_to_approve.values_list("id", flat=True))

        for i in range(0, len(user_ids), batch_size):
            batch_ids = user_ids[i : i + batch_size]
            batch_users = User.objects.filter(id__in=batch_ids)

            for user in batch_users:
                try:
                    ManualVerification.objects.create(
                        user=user,
                        status="approved",
                    )
                    approved_count += 1

                    if approved_count % 50 == 0:
                        self.stdout.write(
                            f"Progress: {approved_count}/{total_users} users processed"
                        )
                except Exception as e:  # pylint: disable=broad-except
                    error_count += 1
                    log.error("Error approving verification for %s: %s", user.username, str(e))

        # Print final progress if not already printed
        if approved_count % 50 != 0:
            self.stdout.write(
                f"Progress: {approved_count}/{total_users} users processed"
            )

        self.stdout.write(
            self.style.SUCCESS(f"\nCompleted! Approved: {approved_count}, Errors: {error_count}")
        )
