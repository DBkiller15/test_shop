import random
import pytz
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from order.models import Order, OrderItem


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('num_orders', type=int)

    def handle(self, *args, **options):
        num_orders = options.get('num_orders', 5)
        start_date = datetime(2018, 1, 1, 9, 0, tzinfo=pytz.UTC)

        for num in range(num_orders):
            date = start_date + timedelta(hours=num)
            order = Order.objects.create(number=num, create_date=date)
            num_items = random.randint(1, 5)
            for n in range(num_items):
                OrderItem.objects.create(
                    order=order,
                    product_name=f'Товар-{random.randint(1, 100)}',
                    product_price=random.randint(100, 9999),
                    amount=random.randint(1, 10),
                )
