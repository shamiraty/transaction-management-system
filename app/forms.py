from django import forms
from django.core.validators import RegexValidator
from .models import Transaction
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, Div
from crispy_forms.layout import Submit

# form  for  insertion and updation
class TransactionForm(forms.ModelForm):
    amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Amount'}),
        validators=[
            RegexValidator(
                regex=r'^\d+(\.\d{1,2})?$',
                message="Enter a valid amount with up to two decimal places."
            )
        ]
    )
    phonenumber = forms.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                regex=r'^\d{10}$',
                message="Phone number must be exactly 10 digits."
            )
        ],
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter 10-digit phone number'}),
    )

    class Meta:
        model = Transaction
        fields = ['network', 'action', 'customer', 'amount', 'phonenumber']
        widgets = {
            'network': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select Network'}),
            'action': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select Action'}),
            'customer': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Customer Name'}),
        }

    def __init__(self, *args, **kwargs):
        super(TransactionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Div(
                Field('network', css_class="form-group col-md-4"),
                Field('action', css_class="form-group col-md-4"),
                Field('customer', css_class="form-group col-md-4"),
                css_class='row'
            ),
            Div(
                Field('amount', css_class="form-group col-md-4"),
                Field('phonenumber', css_class="form-group col-md-4"),
                css_class='row'
            ),
            Submit('submit', 'Submit', css_class="btn btn-primary btn-block mt-1")
        )


