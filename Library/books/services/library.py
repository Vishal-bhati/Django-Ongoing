from books.models import UserBook

def currently_reading(user):
    return UserBook.objects.filter(
        user=user,
        status="reading"
    )

def recently_finished(user, limit = 5):
    return UserBook.objects.filter(
        user=user,
        status="finished"
    ).order_by("-last_updated")[:limit]