from django import forms
from django.core.validators import RegexValidator
from .models import Transaction
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, Div
from crispy_forms.layout import Layout, Row, Column, Submit
from .models import *

# form  for  insertion and updation of transaction
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
                Field('network', css_class=""),
                Field('action', css_class=""),
                Field('customer', css_class=""),
                css_class='row'
            ),
            Div(
                Field('amount', css_class=""),
                Field('phonenumber', css_class=""),
                css_class='row'
            ),
            Submit('submit', 'Submit', css_class="btn btn-primary btn-block mt-1")
        )


# form  for  insertion and updation of product
class ProductBatchForm(forms.Form):
    product_name = forms.CharField(
        max_length=200,
        label="Product Name",
        validators=[RegexValidator(regex=r'^[a-zA-Z0-9 ]+$', message="Only alphanumeric characters and spaces are allowed.")],
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    product_description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        required=False,
        label="Product Description"
    )
    total_quantity = forms.IntegerField(
        min_value=1,
        label="Total Quantity",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    total_purchasing_price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        label="Total Purchasing Price",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    selling_price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        label="Selling Price",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    tax_collection = forms.ModelChoiceField(
        queryset=Tax.objects.all(),
        label="Tax Collection",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    expiry_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label="Expiry Date"
    )
    category = forms.ModelChoiceField(
        queryset=ProductCategory.objects.all(),
        label="Category",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('product_name', css_class='col-md-6'),
                Column('category', css_class='col-md-6')
               
            ),
            Row(
                Column('total_quantity', css_class='col-md-6'),
                Column('total_purchasing_price', css_class='col-md-6')
            ),
            Row(
                Column('selling_price', css_class='col-md-6'),
                Column('tax_collection', css_class='col-md-6')
            ),
            Row(
                Column('expiry_date', css_class='col-md-6'),
                 Column('product_description', css_class='col-md-6')
            ),
            Submit('submit', 'Add Products', css_class='btn btn-primary w-25')
        )

# form  for  sold product
class SoldProductForm(forms.ModelForm):
    class Meta:
        model = SoldProduct
        fields = [
            'product_name', 
            'product_description', 
            'purchasing_price', 
            'selling_price', 
            'tax_collection', 
            'barcode', 
            'expiry_date', 
            'category', 
        ]
        widgets = {
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
        }


#forms  for editing product
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'product_name', 
            'product_description', 
            'purchasing_price', 
            'selling_price', 
            'tax_collection', 
            'barcode', 
            'expiry_date', 
            'category'
        ]
