from django.core.validators import RegexValidator


class SlugValidator(RegexValidator):
    regex = r'^[-a-zA-Z0-9_]+$'
