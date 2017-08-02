from django.contrib.auth.models import User


def run():
    if not User.objects.filter(username="michaelg").exists():
        User.objects.create_superuser(
            "michaelg",
            "michaelg@represently.com",
            '90pSnCR@EGG>KZvjee"H7Ka4{D/(NAi%yV=Bi7f*Z9wpy8HTYWSN4+cX9sw9GuxT'
            )
