import requests
from django.conf import settings


class StripeService:
    @staticmethod
    def create_product(name, description):
        """Создаем продукт в Stripe"""
        url = "https://api.stripe.com/v1/products"
        headers = {
            "Authorization": f"Bearer {settings.STRIPE_SECRET_KEY}",
        }
        data = {
            "name": name,
            "description": description,
        }
        response = requests.post(url, headers=headers, data=data)
        return response.json()

    @staticmethod
    def create_price(product_id, amount):
        """Создаем цену в Stripe"""
        url = "https://api.stripe.com/v1/prices"
        headers = {
            "Authorization": f"Bearer {settings.STRIPE_SECRET_KEY}",
        }
        # Умножаем на 100 (gthtdjlbv bp rjgttr d he,kb)
        amount_in_cents = int(amount * 100)

        data = {
            "product": product_id,
            "unit_amount": amount_in_cents,
            "currency": "rub",
        }
        response = requests.post(url, headers=headers, data=data)
        return response.json()

    @staticmethod
    def create_checkout_session(price_id):
        """Создаем сессию оплаты и получаем ссылку"""
        url = "https://api.stripe.com/v1/checkout/sessions"
        headers = {
            "Authorization": f"Bearer {settings.STRIPE_SECRET_KEY}",
        }
        data = {
            "line_items[0][price]": price_id,
            "line_items[0][quantity]": "1",
            "mode": "payment",
            "success_url": "https://example.com/success",
            "cancel_url": "https://example.com/cancel",
        }
        response = requests.post(url, headers=headers, data=data)
        return response.json()
