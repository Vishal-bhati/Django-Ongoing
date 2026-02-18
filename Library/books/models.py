from django.db import models
from django.conf import settings


class Book(models.Model):
    google_book_id = models.CharField(max_length=200, unique=True, null=True, blank=True)
    title = models.CharField(max_length=100)
    total_pages = models.IntegerField()

class UserBook(models.Model):
    STATUS_CHOICES = [
        ("reading", "Reading"),
        ("finished", "Finished"),
        ("paused", "Paused"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE    
    )

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE
    )

    current_page = models.IntegerField(default=0)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="reading"
    )
    last_updated = models.DateTimeField(auto_now=True)

    def update_progress(self, page):
        self.current_page = page
        self.status = "finished" if page >0 else "reading"
        self.save()

    def __str__(self):
        return f"{self.user.username} - {self.book.title} ({self.status})"