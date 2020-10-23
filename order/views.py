from datetime import datetime
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from django.db.models import Sum
from .models import Order, OrderItem
from .forms import DateRangeForm



class HomeView(TemplateView):
    template_name = 'index.html'


class OrderListView(ListView):

    model = Order
    template_name = 'orders.html'
    form_class = DateRangeForm
    default_date_range = [
        datetime(2018, 1, 1, 0, 0, 0),
        datetime(2018, 1, 31, 23, 59, 59, 999)
    ]

    def get_form(self):
        if 'start_date' in self.request.GET and 'end_date' in self.request.GET:
            return self.form_class(data=self.request.GET)
        return self.form_class(
            initial={
                'start_date': self.default_date_range[0],
                'end_date': self.default_date_range[1],
            }
        )

    def get_date_range(self):
        form = self.get_form()
        if form.is_valid():
            start_date = form.cleaned_data.get('start_date')
            end_date = form.cleaned_data.get('end_date').replace(
                hour=23, minute=59, second=59, microsecond=999
            )
            return [start_date, end_date]
        return self.default_date_range

    def get_queryset(self):
        date_range = self.get_date_range()
        order_items = OrderItem.objects.filter(
            order__create_date__range=date_range)
        orders = order_items.values(
            'order__number', 'order__create_date').annotate(
            price=Sum('product_price'))
        order_items = order_items.values(
            'product_name', 'amount', 'order__number')
        queryset = [
            {
                'number': order.get('order__number'),
                'create_date': order.get('order__create_date'),
                'price': order.get('price'),
                'items': order_items.filter(
                    order__number=order.get('order__number'))
            }
            for order in orders
        ]
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context


class TopProductsView(ListView):

    model = OrderItem
    template_name = 'top_products.html'
    form_class = DateRangeForm
    default_date_range = [
        datetime(2018, 1, 1, 0, 0, 0),
        datetime(2018, 1, 31, 23, 59, 59, 999)
    ]

    def get_form(self):
        if 'start_date' in self.request.GET and 'end_date' in self.request.GET:
            return self.form_class(data=self.request.GET)
        return self.form_class(
            initial={
                'start_date': self.default_date_range[0],
                'end_date': self.default_date_range[1],
            }
        )

    def get_date_range(self):
        form = self.get_form()
        if form.is_valid():
            start_date = form.cleaned_data.get('start_date')
            end_date = form.cleaned_data.get('end_date').replace(
                hour=23, minute=59, second=59, microsecond=999
            )
            return [start_date, end_date]
        return self.default_date_range

    def get_queryset(self):
        date_range = self.get_date_range()
        order_items = self.model.objects.filter(
            order__create_date__range=date_range)

        products = order_items.values('product_name').annotate(
            total=Sum('amount')).order_by('-total')[:20]

        order_items = order_items.values(
            'product_name', 'product_price', 'order__number',
            'order__create_date',
        )
        top_products = [
            {
                'product_name': product.get('product_name'),
                'items': order_items.filter(
                    product_name=product.get('product_name')
                ),
            }
            for product in products
        ]
        return top_products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context
