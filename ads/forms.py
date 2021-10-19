from django import forms
from . models import Ads


class AdsForm(forms.ModelForm):
    class Meta:
        model = Ads
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(AdsForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
