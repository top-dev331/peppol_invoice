from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import Profile, MyProfile, CustomerInfo

class InvoiceForm(forms.Form):
    sender = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter sender details'}))
    receiver = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter receiver details'}))
    document_type = forms.ChoiceField(choices=[('invoice', 'Invoice')], widget=forms.Select(attrs={'class': 'form-control'}))
    invoice_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    due_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}), required=False)
    purchase_order_reference = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    gross_sales_amount = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    high_vat = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'High VAT'}), required=False)
    low_vat = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Low VAT'}), required=False)
    zero_vat = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Zero VAT'}), required=False)
    reverse_charge_vat = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Reverse Charge VAT'}), required=False)
    payment_method = forms.ChoiceField(choices=[('bank', 'Bank'), ('paypal', 'PayPal'), ('credit_card', 'Credit Card')], widget=forms.Select(attrs={'class': 'form-control'}))
    article_code = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Enter article code'}))
    description = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Enter description'}))
    quantity = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Enter quantity'}))
    price_per_unit = forms.DecimalField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Enter price per unit'}))
    total_amount_per_line = forms.DecimalField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Enter total amount per line'}))
    vat_amount_per_line = forms.DecimalField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Enter VAT amount per line'}))
    vat_type = forms.ChoiceField(choices=[('high', 'High VAT'), ('low', 'Low VAT'), ('zero', 'Zero VAT'), ('reverse_charge', 'Reverse Charge VAT')], required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    sum_of_lines = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control', 'readonly': True}), required=False)
    sum_of_vat_types = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control', 'readonly': True}), required=False)
    pdf_file = forms.FileField(label='Upload PDF File', required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))


class RegisterForm(UserCreationForm):
    # fields we want to include and customize in our form
    first_name = forms.CharField(max_length=100,
                                 required=True,
                                 widget=forms.TextInput(attrs={'placeholder': 'First Name',
                                                               'class': 'form-control',
                                                               }))
    last_name = forms.CharField(max_length=100,
                                required=True,
                                widget=forms.TextInput(attrs={'placeholder': 'Last Name',
                                                              'class': 'form-control',
                                                              }))
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Username',
                                                             'class': 'form-control',
                                                             }))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'placeholder': 'Email',
                                                           'class': 'form-control',
                                                           }))
    password1 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))
    password2 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password',
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Username',
                                                             'class': 'form-control',
                                                             }))
    password = forms.CharField(max_length=50,
                               required=True,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                 'class': 'form-control',
                                                                 'data-toggle': 'password',
                                                                 'id': 'password',
                                                                 'name': 'password',
                                                                 }))
    remember_me = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'remember_me']


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email']


class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))

    class Meta:
        model = Profile
        fields = ['avatar', 'bio']

class MyProfileForm(forms.ModelForm):
    class Meta:
        model = MyProfile
        fields = '__all__'

class CustomerInfoForm(forms.ModelForm):
    class Meta:
        model = CustomerInfo
        fields = '__all__'