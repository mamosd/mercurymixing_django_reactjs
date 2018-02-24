from __future__ import unicode_literals

import stripe

from django import forms
from django.contrib.messages import success
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views import generic

from mezzanine.conf import settings

from utils import notify_exception

from .models import Purchase


class PurchaseForm(forms.ModelForm):
    """
    Collect Stripe data and create a new Purchase.
    """
    stripe_token = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = Purchase
        fields = ["stripe_token", "credits", "amount"]
        widgets = {
            # The amount will be populated by JS
            "amount": forms.HiddenInput(),
        }

    def clean(self):
        """
        Validate Stripe and amount data.
        """
        data = super(PurchaseForm, self).clean()

        if not data.get("stripe_token"):
            raise forms.ValidationError("Missing Stripe token")

        real_amount = data.get("credits", 0) * settings.PURCHASE_CREDIT_PRICE
        if not data.get("amount") == real_amount:
            raise forms.ValidationError("Amount mismatch")


class PurchaseDashboard(generic.edit.FormMixin, generic.TemplateView):
    """
    Allows users to view and purchase credits for mixing Tracks.
    """
    form_class = PurchaseForm
    template_name = "purchases/dashboard.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        """
        Requrired to apply login_required.
        Can be swapped by proper mixin in Django 1.9.
        https://docs.djangoproject.com/en/1.9/topics/auth/default/#the-loginrequired-mixin
        """
        return super(PurchaseDashboard, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Add previous Purchases and PurchaseForm to the context.
        """
        kwargs.setdefault("form", self.get_form())
        kwargs.update({
            "purchases": Purchase.objects.filter(user=self.request.user),
        })
        return super(PurchaseDashboard, self).get_context_data(**kwargs)

    def create_charge(self, data):
        """
        Connect to the Stripe API and create the charge.
        """
        stripe.api_key = settings.STRIPE_SK

        try:
            charge = stripe.Charge.create(
                currency="usd",
                amount=data.get("amount", 0) * 100,  # Convert to cents
                source=data.get("stripe_token"),
            )

        except stripe.error.CardError as e:
            error = e.json_body["error"]
            raise forms.ValidationError(error.get("message", "Your card was declined"))

        except stripe.error.StripeError as e:
            notify_exception(self.request, e)
            raise forms.ValidationError("An error occurred during payment")

        return charge

    def post(self, request, *args, **kwargs):
        """
        Validate the form and create the charge.
        """
        form = self.get_form()

        if not form.is_valid():
            return self.form_invalid(form)

        try:
            charge = self.create_charge(form.cleaned_data)
        except forms.ValidationError as stripe_error:
            form.add_error(field=None, error=stripe_error)
            return self.form_invalid(form)

        purchase = form.save(commit=False)
        purchase.charge_details = str(charge)
        purchase.user = request.user
        purchase.save()
        success(request, "Purchase completed successfully", fail_silently=True)
        return HttpResponseRedirect(request.path)
