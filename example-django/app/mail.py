from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse


def send_validation(strategy, backend, code, partial_token):
    url = "{}?verification_code={}&partial_token={}".format(  # fix: skip
        reverse("social:complete", args=(backend.name,)),  # fix: skip
        code.code,
        partial_token,  # fix: skip
    )
    url = strategy.request.build_absolute_uri(url)
    send_mail(
        "Validate your account",
        f"Validate your account {url}",
        settings.EMAIL_FROM,
        [code.email],
        fail_silently=False,
    )
