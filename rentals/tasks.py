from celery import shared_task

from .models import Notification, RentalRequest


@shared_task
def notify_rental_status_change(rental_id: int, new_status: str) -> dict:
    """Create lightweight in-app notifications after a rental status update."""

    rental = RentalRequest.objects.select_related('game', 'game__owner', 'borrower').get(pk=rental_id)

    recipients = {rental.borrower}
    if rental.game.owner_id != rental.borrower_id:
        recipients.add(rental.game.owner)

    notifications_created = 0
    for user in recipients:
        Notification.objects.create(
            user=user,
            rental_request=rental,
            title=f'Rental request {new_status}',
            message=(
                f'"{rental.game.title}" is now marked as {new_status}. '
                f'Borrower: {rental.borrower.username}. Owner: {rental.game.owner.username}.'
            ),
        )
        notifications_created += 1

    return {
        'rental_id': rental_id,
        'status': new_status,
        'notifications_created': notifications_created,
    }
