from django import forms
from django.db.models import fields
from . models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name','description','price','image1','image2','image3','image4','stock','brand']

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
