from django import forms


class DateRangeForm(forms.Form):
    start_date = forms.DateTimeField(
        input_formats=['%d.%m.%Y'],
        widget=forms.DateInput(
            format='%d.%m.%Y', attrs={'class': 'form-control'}
        ),
    )
    end_date = forms.DateTimeField(
        input_formats=['%d.%m.%Y'],
        widget=forms.DateInput(
            format='%d.%m.%Y', attrs={'class': 'form-control'}
        ),
    )

