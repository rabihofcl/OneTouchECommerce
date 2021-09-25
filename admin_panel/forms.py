from django import forms
from brand.models import Brand

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = '__all__'

    def save(self):
        photo = super(BrandForm, self).save()
        return photo
