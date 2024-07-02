from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.http import JsonResponse
import requests
import logging
import base64

logger = logging.getLogger(__name__)

from .models import MyProfile, CustomerInfo
from .forms import RegisterForm, LoginForm, UpdateUserForm, UpdateProfileForm, InvoiceForm, MyProfileForm, CustomerInfoForm

from .utils import send_invoice_peppol

import base64

def profile_and_customers(request):
    try:
        profile = MyProfile.objects.get(pk=1)  # Assuming there is only one profile
    except MyProfile.DoesNotExist:
        profile = MyProfile.objects.create()  # This will use the default values

    if request.method == 'POST' and 'profile-submit' in request.POST:
        profile_form = MyProfileForm(request.POST, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('profile_and_customers')
    else:
        profile_form = MyProfileForm(instance=profile)
    
    customers = CustomerInfo.objects.all()
    
    if request.method == 'POST' and 'customer-submit' in request.POST:
        customer_form = CustomerInfoForm(request.POST)
        if customer_form.is_valid():
            customer_form.save()
            return redirect('profile_and_customers')
    else:
        customer_form = CustomerInfoForm()

    context = {
        'profile_form': profile_form,
        'customers': customers,
        'customer_form': customer_form,
    }
    return render(request, 'users/profile_and_customers.html', context)  # Ensure the path is correct

def edit_customer(request, pk):
    customer = get_object_or_404(CustomerInfo, pk=pk)
    if request.method == 'POST':
        form = CustomerInfoForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('profile_and_customers')
    else:
        form = CustomerInfoForm(instance=customer)
    return render(request, 'users/edit_customer.html', {'form': form})

def delete_customer(request, pk):
    customer = get_object_or_404(CustomerInfo, pk=pk)
    customer.delete()
    return redirect('profile_and_customers')

def send_invoice(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST, request.FILES)
        if form.is_valid():
            sender = form.cleaned_data.get('sender')
            print('Sender:', sender)
            pdf_file = request.FILES.get('pdf_file')
            if pdf_file:
                pdf_content = pdf_file.read()
                pdf_base64 = base64.b64encode(pdf_content).decode('utf-8')
                print('pdf_base64', pdf_base64)
                # Do something with the base64 encoded PDF file (send to API, save to storage, etc.)
                # send_invoice_peppol(pdf_base64)
            invoice_data = {
                "legalEntityId": 288230,
                "routing": {
                    "emails": [
                    "d662b5d59a93d52f36891302c0eba14d@example.com"
                    ],
                    "eIdentifiers": [
                    {
                        "scheme": "NL:KVK",
                        "id": "012345677"
                    },
                    {
                        "scheme": "NL:VAT",
                        "id": "NL000000000B45"
                    }
                    ]
                },
                "attachments": [
                    {
                    "filename": "myname.pdf",
                    "document": pdf_base64,
                    "mimeType": "application/pdf",
                    "primaryImage": False,
                    "documentId": "myId",
                    "description": "A Description"
                    }
                ],
                "document": {
                    "documentType": "invoice",
                    "invoice": {
                    "invoiceNumber": "202112007",
                    "issueDate": "2021-12-07",
                    "documentCurrencyCode": "EUR",
                    "taxSystem": "tax_line_percentages",
                    "accountingCustomerParty": {
                        "party": {
                        "companyName": "KC Nederland BV",
                        "address": {
                            "street1": "Minervum 7040",
                            "zip": "4817 ZL",
                            "city": "Breda",
                            "country": "NL"
                        }
                        },
                        "publicIdentifiers": [
                        {
                            "scheme": "NL:KVK",
                            "id": "012345677"
                        },
                        {
                            "scheme": "NL:VAT",
                            "id": "NL000000000B45"
                        }
                        ]
                    },
                    "invoiceLines": [
                        {
                        "description": "The things you purchased",
                        "amountExcludingVat": form.cleaned_data.get('vat_amount_per_line'),
                        "tax": {
                            "percentage": 0,
                            "category": "reverse_charge",
                            "country": "NL"
                        }
                        }
                    ],
                    "taxSubtotals": [
                        {
                        "percentage": 0,
                        "category": "reverse_charge",
                        "country": "NL",
                        "taxableAmount": 10,
                        "taxAmount": 0
                        }
                    ],
                    "paymentMeansArray": [
                        {
                        "account": "NL50ABNA0552321249",
                        "holder": "Storecove",
                        "code": "credit_transfer"
                        }
                    ],
                    "amountIncludingVat": 10
                    }
                }
            }    
            #return redirect('invoice_success')
            try:
                response = send_invoice_peppol(invoice_data)
                return JsonResponse(response, status=200)
            except requests.exceptions.RequestException as e:
                logger.error(f"RequestException: {e}")
                return JsonResponse({'error': str(e)}, status=500)
            except Exception as e:
                logger.error(f"Exception: {e}")
                return JsonResponse({'error': str(e)}, status=500)
        else:
            logger.error(f"Form is invalid: {form.errors}")
            return JsonResponse({'error': 'Invalid form data', 'details': form.errors}, status=400)
    else:
        form = InvoiceForm()
    return render(request, 'users/send_invoice.html', {'form': form})

def home(request):
    return render(request, 'users/home.html')

# def send_invoice(request):
#   return render(request, 'users/send_invoice.html')


class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'users/register.html'

    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect(to='/')

        # else process dispatch as it otherwise normally would
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect(to='login')

        return render(request, self.template_name, {'form': form})


# Class based view that extends from the built in login view to add a remember me functionality
class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True

        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('users-home')


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('users-home')


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='users-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'users/profile.html', {'user_form': user_form, 'profile_form': profile_form})
