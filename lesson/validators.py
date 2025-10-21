from django.core.exceptions import ValidationError


def validate_youtube_only(value):
    """
    Валидация ссылок на ютуб
    """
    if value:
        """проверяем содержимое ссылок, только youtube.com или youtube.be"""

        if "youtube.com" not in value and "youtu.be" not in value:
            raise ValidationError("Допустимы только ссылки на YouTube.")

        """ Проверка на действительность ссылки """
        if not value.startswith(("https://www.youtube.com")):
            raise ValueError("Ссылка должна начинаться с http:// или https://")


class YouTubeValidator:
    """Класс для проверки ссылок на ютуб"""

    def __init__(self, field):
        self.field = field

    def __call__(self, attrs):
        field_value = attrs.get(self.field)
        if field_value:
            validate_youtube_only(field_value)
