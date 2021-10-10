from django import forms
from django.db.models import fields
from .models import Order, OrderProduct
from .forms import OrderProduct



class OrderForm1(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone', 'email', 'address_line_1', 'address_line_2', 'country', 'state', 'city', 'pincode', 'order_note']


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

        self.fields['user'].widget.attrs['readonly'] = True
        self.fields['payment'].widget.attrs['readonly'] = True
        self.fields['order_number'].widget.attrs['readonly'] = True


class OrderProductForm(forms.ModelForm):
    class Meta:
        model = OrderProduct
        fields = ['status']

    def __init__(self, *args, **kwargs):
        super(OrderProductForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

        self.fields['status'].widget.attrs['value'] = 'Select'