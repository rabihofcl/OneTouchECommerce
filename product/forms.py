from django import forms
from . models import Product


class ProductForm(forms.ModelForm):
    image1 = forms.ImageField(required=False, error_messages = {'invalid':("Image files only")}, widget=forms.FileInput)
    image2 = forms.ImageField(required=False, error_messages = {'invalid':("Image files only")}, widget=forms.FileInput)
    image3 = forms.ImageField(required=False, error_messages = {'invalid':("Image files only")}, widget=forms.FileInput)
    image4 = forms.ImageField(required=False, error_messages = {'invalid':("Image files only")}, widget=forms.FileInput)
    class Meta:
        model = Product
        fields = ['product_name','description','price','image1','image2','image3','image4','stock','brand']

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

            self.fields['image1'].widget.attrs['data-toggle'] = 'modal'
            self.fields['image1'].widget.attrs['data-target'] = '#exampleModal'

            self.fields['image2'].widget.attrs['data-toggle'] = 'modal'
            self.fields['image2'].widget.attrs['data-target'] = '#exampleModal'

            self.fields['image3'].widget.attrs['data-toggle'] = 'modal'
            self.fields['image3'].widget.attrs['data-target'] = '#exampleModal'

            self.fields['image4'].widget.attrs['data-toggle'] = 'modal'
            self.fields['image4'].widget.attrs['data-target'] = '#exampleModal'
