from django import forms
from brand.models import Brand


class BrandForm(forms.ModelForm):
    logo = forms.ImageField(required=False, error_messages={
                            'invalid': ("Image files only")}, widget=forms.FileInput)

    class Meta:
        model = Brand
        fields = ['brand_name', 'description', 'logo']

    def save(self):
        photo = super(BrandForm, self).save()
        return photo

    def __init__(self, *args, **kwargs):
        super(BrandForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

            self.fields['logo'].widget.attrs['data-toggle'] = 'modal'
            self.fields['logo'].widget.attrs['data-target'] = '#exampleModal'

        # data-toggle="modal" data-target="#exampleModal"
