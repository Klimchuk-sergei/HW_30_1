import django_filters
from .models import Payment


class PaymentFilter(django_filters.FilterSet):
    paid_course = django_filters.NumberFilter(
        field_name="course",
        label="Paid course",
    )

    paid_lesson = django_filters.NumberFilter(
        field_name="lesson",
        label="Paid lesson",
    )

    ordering = django_filters.OrderingFilter(
        fields=(
            ("payment_date", "date"),
            ("-payment_date", "-date"),
        ),
        filed_labels={
            "date": "дата опалты (по возрастанию)",
            "-date": "дата оплаты (по убыванию)",
        },
    )

    class Meta:
        model = Payment
        fields = ["paid_course", "paid_lesson", "payment_method"]
