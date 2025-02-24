from .models import POLITICAL_PARTY_CHOICES
from django import forms

class ElectionAdminMemberAccountOpenForm(forms.Form):
    last_name = forms.CharField(required=True,max_length=30,label="Admin Last Name")
    first_name = forms.CharField(required=True,max_length=60,label="Admin First Name")
    phone_number = forms.CharField(required=True,max_length=10,label="Admin Phone Number")
    email = forms.EmailField(required=True,label="Email Address")
    password = forms.CharField(required=True,widget=forms.PasswordInput(),label="Password")

class CandidateOrVoterAccountOpenForm(forms.Form):
    last_name = forms.CharField(required=True,max_length=30,label="Last Name")
    first_name = forms.CharField(required=True,max_length=60,label="First Name")
    phone_number = forms.CharField(required=True,max_length=10,label="Phone Number")
    email = forms.EmailField(required=True,label="Email Address")


class ElectionMemberAccountLoginForm(forms.Form):
    email = forms.EmailField(required=True,label="Admin Email Address")
    password = forms.CharField(required=True,widget=forms.PasswordInput(),label="Password")

class CandidateLoginForm(forms.Form):
    candidate_id = forms.CharField(required=True,label="Candidate ID")
    password = forms.CharField(required=True,widget=forms.PasswordInput(),label="Password")

class VoterLoginForm(forms.Form):
    candidate_id = forms.CharField(required=True,label="Voter ID")
    password = forms.CharField(required=True,widget=forms.PasswordInput(),label="Password")

class ElectionVoterDetailsForm(forms.Form):
    birth_date = forms.DateField(required=True,label="Date of birth")
    person_type = forms.ChoiceField(choices=(('Male','Male'),('Female','Female')), required=True)
    full_address = forms.CharField(max_length=180)
    state = forms.ChoiceField(choices=(('KS','Kansas'),), required=True)
    postal_code = forms.CharField(max_length=5, required=True)
    ssn = forms.CharField(max_length=9, required=True,label="Social Security Number")
    address_proof = forms.FileField(required=True,label="Upload Address Proof")
    other_proof = forms.FileField(required=False,label="Upload other proof")


class CandicateDetailsForm(forms.Form):
    birth_date = forms.DateField(required=True,label="Date of birth")
    person_type = forms.ChoiceField(choices=(('Male','Male'),('Female','Female')), required=True)
    full_address = forms.CharField(max_length=180)
    state = forms.ChoiceField(choices=(('KS','Kansas'),), required=True)
    postal_code = forms.CharField(max_length=5, required=True)
    ssn = forms.CharField(max_length=9, required=True,label="Social Secuirty Number")
    candidate_party = forms.ChoiceField(choices=POLITICAL_PARTY_CHOICES, required=True)
    address_proof = forms.FileField(required=True,label="Upload Address Proof")
    other_proof = forms.FileField(required=False,label="Upload previous milestone Documents")
