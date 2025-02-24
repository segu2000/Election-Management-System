import random
from django.shortcuts import render, redirect
from .forms import CandidateOrVoterAccountOpenForm,ElectionAdminMemberAccountOpenForm, ElectionMemberAccountLoginForm, ElectionVoterDetailsForm, \
    CandicateDetailsForm
from .models import ElectionMember, CandidateInformation, VoterInformation, ElectionInformation, VotingInformation
from django.contrib import messages
from allauth.account.utils import perform_login, complete_signup
from allauth.account import app_settings as allauth_settings


def website_home_screen(request):
    return render(request, 'website_home.html')


def election_member_account_registration(request):
    url_path = request.get_full_path
    http_method_type = request.method
    if str(http_method_type).upper() == "POST":
        account_reg_form = ElectionAdminMemberAccountOpenForm(request.POST)
        if account_reg_form.is_valid():
            phone_number = account_reg_form.cleaned_data["phone_number"]
            email = account_reg_form.cleaned_data["email"]
            last_name = account_reg_form.cleaned_data["last_name"]
            first_name = account_reg_form.cleaned_data["first_name"]
            password = account_reg_form.cleaned_data["password"]
            if ElectionMember.objects.filter(username=email).exists():
                return render(request, 'ElectionMemberAccountOpening.html',
                              {'form': account_reg_form, 'get_full_path': url_path,
                               'error_msg': 'Email address is already exists ' + str(phone_number)})
            election_member = ElectionMember.objects.create(username=email, last_name=last_name, first_name=first_name,
                                                            email=email,
                                                            phone_number=phone_number)
            election_member.is_superuser = True
            election_member.is_staff = True
            election_member.member_type = "ADM"
            election_member.set_password(password)
            election_member.save()
            perform_login(request, election_member, allauth_settings.EMAIL_VERIFICATION, signup=False,
                          redirect_url=None, signal_kwargs=None)
            return redirect('admin_member_home')

    else:
        account_reg_form = ElectionAdminMemberAccountOpenForm()
        return render(request, 'ElectionMemberAccountOpening.html',
              {'form': account_reg_form})

def candidate_or_voter_registration(request):
    url_path = request.get_full_path
    http_method_type = request.method
    if str(http_method_type).upper() == "POST":
        account_reg_form = CandidateOrVoterAccountOpenForm(request.POST)
        if account_reg_form.is_valid():
            phone_number = account_reg_form.cleaned_data["phone_number"]
            email = account_reg_form.cleaned_data["email"]
            last_name = account_reg_form.cleaned_data["last_name"]
            first_name = account_reg_form.cleaned_data["first_name"]
            if ElectionMember.objects.filter(username=email).exists():
                return render(request, 'ElectionMemberAccountOpening.html',
                              {'form': account_reg_form, 'get_full_path': url_path,
                               'error_msg': 'Email address is already exists ' + str(phone_number)})
            election_member = ElectionMember.objects.create(username=email, last_name=last_name, first_name=first_name,
                                                            email=email,
                                                            phone_number=phone_number)

            if "cand" in request.path:
                election_member.member_type = "CAN"
                candObj = CandidateInformation.objects.create(member=election_member)
            else:
                voterObj = VoterInformation.objects.get_or_create(member=election_member)
                election_member.member_type = "VOT"
            election_member.save()
            perform_login(request, election_member, allauth_settings.EMAIL_VERIFICATION, signup=False,
                          redirect_url=None, signal_kwargs=None)
            if "cand" in request.path:
                return redirect('cand_member_home')
            else:
                return redirect('voter_home')

    else:
        account_reg_form = CandidateOrVoterAccountOpenForm()
        if "cand" in request.path:
            post_url = '/cand/registration/'
        else:
            post_url = '/voter/registration/'
        print(post_url)
        return render(request, 'CandidateorVoterAccountOpenForm.html',
              {'form': account_reg_form,'path':post_url})


def election_member_login(request):
    url_path = request.get_full_path
    if request.method == "POST":
        member_login_form = ElectionMemberAccountLoginForm(request.POST)
        if member_login_form.is_valid():
            email = member_login_form.cleaned_data["email"]
            password = member_login_form.cleaned_data["password"]
            if not ElectionMember.objects.filter(email=email).exists():
                member = ElectionMember.objects.filter(email=email).first()
                perform_login(request, member, allauth_settings.EMAIL_VERIFICATION, signup=False,
                              redirect_url=None, signal_kwargs=None)
                return redirect('admin_member_home')
    else:
        member_login_form = ElectionMemberAccountLoginForm()
    return render(request, 'ElectionMemberAccountLogin.html', {'form': member_login_form, 'get_full_path': url_path})

from .forms import CandidateLoginForm,VoterLoginForm
def candidate_login(request):
    url_path = request.get_full_path
    msg = ''
    if request.method == "POST":
        member_login_form = CandidateLoginForm(request.POST)
        if member_login_form.is_valid():
            candidate_id = member_login_form.cleaned_data["candidate_id"]
            password = member_login_form.cleaned_data["password"]
            cand = CandidateInformation.objects.filter(candidate_id=candidate_id).first()
            if cand:
                member = cand. member
                perform_login(request, member, allauth_settings.EMAIL_VERIFICATION, signup=False,
                                redirect_url=None, signal_kwargs=None)
                return redirect('cand_member_home')
            else:
                msg = "Invalid Candidate ID or Password"
                return render(request, 'CandidateAccountLogin.html',
                              {'msg':msg,'form': member_login_form, 'get_full_path': url_path})
    else:
        member_login_form = CandidateLoginForm()
    return render(request, 'CandidateAccountLogin.html', {'form': member_login_form, 'get_full_path': url_path})


def voter_login(request):
    url_path = request.get_full_path
    msg = ''
    if request.method == "POST":
        member_login_form = VoterLoginForm(request.POST)
        if member_login_form.is_valid():
            candidate_id = member_login_form.cleaned_data["candidate_id"]
            password = member_login_form.cleaned_data["password"]
            voter = VoterInformation.objects.filter(voter_id = candidate_id).first()
            if voter:
                member = voter.member
                perform_login(request, member, allauth_settings.EMAIL_VERIFICATION, signup=False,
                              redirect_url=None, signal_kwargs=None)
                return redirect('voter_home')
            else:
                msg = 'Invalid Voter ID or Password.'
                return render(request, 'CandidateAccountLogin.html',
                              {'msg': msg, 'form': member_login_form, 'get_full_path': url_path})
    else:
        member_login_form = VoterLoginForm()
        if "cand" in request.path:
            post_url = '/cand/login/'
        else:
            post_url = '/voter/login/'
    return render(request, 'CandidateAccountLogin.html', {'msg':msg,'form': member_login_form, 'get_full_path': url_path,'post_url':post_url})



def member_session_not_active(request):
    url_path = request.path
    if "admin" in str(url_path).lower():
        return redirect('superuser_login')
    elif "cand" or "candidate" in str(url_path).lower():
        return redirect('candidate_login')
    else:
        return redirect('voter_login')


def get_all_candidate_details(request):
    if not request.user.is_active:
        return member_session_not_active(request)
    candidates = CandidateInformation.objects.all()
    return render(request, 'Election_All_Candidates.html', {'candidates': candidates})


def get_candidate_details(request, id):
    if not request.user.is_active:
        return member_session_not_active(request)
    candidate = CandidateInformation.objects.filter(pk=id).first()
    return render(request, 'Election_Candidate.html', {'candidate': candidate})


def delete_candidate_details(request, id):
    if not request.user.is_active:
        return member_session_not_active(request)
    candidate = CandidateInformation.objects.filter(pk=id).first()
    candidate.is_fault_account = True
    candidate.is_account_verified = False
    candidate.description = "Candidate details not verified by admin."
    candidate.save()
    messages.add_message(request, messages.WARNING, "Candidate " + str(id) + " details not verified.")
    return redirect('all_candidate_details')


def verify_candidate_details(request, id):
    if not request.user.is_active:
        return member_session_not_active(request)
    candidate = CandidateInformation.objects.filter(pk=id).first()
    candidate.candidate_id = "CAND"+str(candidate.pk)
    # password = str(id) + str(candidate.user.phone_number)[:3] + str(candidate.user.last_name)[:3]
    password = "cand123"
    candidate.member.set_password(password)
    candidate.is_candidate_verified = True
    candidate.save()
    print("******************* CANDIDATE DETAILS VERIFIED ***************")
    print("\n")
    print("CANDIDATE ID: " + str(candidate.candidate_id))
    print("CANDIDATE Password : " + str("cand123"))
    print("\n\n")
    return redirect('all_candidate_details')


def get_all_voter_details(request):
    if not request.user.is_active:
        return member_session_not_active(request)
    voters = VoterInformation.objects.all()
    return render(request, 'Election_All_Voters.html', {'voters': voters})


def get_voter_details(request, voter_id):
    if not request.user.is_active:
        return member_session_not_active(request)
    voter = VoterInformation.objects.filter(pk=voter_id).first()
    return render(request, 'Election_Voter.html', {'voter': voter})


def delete_voter_details(request, voter_id):
    if not request.user.is_active:
        return member_session_not_active(request)
    voterObj = VoterInformation.objects.filter(pk=voter_id).first()
    voterObj.description = "Voter details not verified by admin."
    voterObj.is_active = False
    voterObj.save()
    messages.add_message(request, messages.WARNING, "Voter " + str(voter_id) + " details not verified.")
    return redirect('all_voter_details')


def verify_voter_details(request, voter_id):
    if not request.user.is_active:
        return member_session_not_active(request)
    voterObj = VoterInformation.objects.filter(pk=voter_id).first()
    voterObj.voter_id = "VOT"+str(voterObj.pk)
    # password = str(id) + str(voter.user.last_name)[:3] + str(voter.member.email[:4])
    password = "voter123"
    voterObj.member.set_password(password)
    voterObj.is_account_verified = True
    voterObj.save()
    print("******************* VOTER DETAILS VERIFIED ***************")
    print("\n")
    print("VOTER ID: " + str(voterObj.voter_id))
    print("VOTER Password : " + str("voter123"))
    print("\n\n")
    return redirect('all_voter_details')


from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile, File


def save_voter_member_information(request):
    member = request.user
    if not member.is_active:
        return member_session_not_active(request)
    voterObj, created_flag = VoterInformation.objects.get_or_create(member=member)
    if voterObj.ssn:
        messages.add_message(request, messages.INFO, 'Details already uploaded')
        return redirect('voter_home')
    if request.method == "POST":
        voter_details_form = ElectionVoterDetailsForm(request.POST, request.FILES)
        if voter_details_form.is_valid():
            voterObj.birth_date = voter_details_form.cleaned_data["birth_date"]
            voterObj.person_type = voter_details_form.cleaned_data["person_type"]
            voterObj.full_address = voter_details_form.cleaned_data["full_address"]
            voterObj.state = voter_details_form.cleaned_data["state"]
            voterObj.postal_code = voter_details_form.cleaned_data["postal_code"]
            voterObj.ssn = voter_details_form.cleaned_data["ssn"]
            driving_licence_filename = request.FILES['address_proof'].name
            file_content = ContentFile(request.FILES['address_proof'].read())
            voterObj.address_proof.save(driving_licence_filename, file_content)
            other_proof_filename = request.FILES['other_proof'].name
            other_doc_file_content = ContentFile(request.FILES['other_proof'].read())
            voterObj.other_proof.save(other_proof_filename, other_doc_file_content)
            voterObj.save()
            return redirect('voter_home')
    else:
        voter_details_form = ElectionVoterDetailsForm()
    return render(request, 'Upload_Election_Voter_Information.html', {'form': voter_details_form, 'voter': voterObj})


def save_candidate_member_information(request):
    member = request.user
    if not member.is_active:
        return member_session_not_active(request)
    candObj, candobj_flag = CandidateInformation.objects.get_or_create(member=member)
    if candObj.ssn:
        return redirect('cand_member_home')
    if request.method == "POST":
        candidate_form = CandicateDetailsForm(request.POST, request.FILES)
        print(candidate_form)
        if candidate_form.is_valid():
            candObj.birth_date = candidate_form.cleaned_data["birth_date"]
            candObj.person_type = candidate_form.cleaned_data["person_type"]
            candObj.full_address = candidate_form.cleaned_data["full_address"]
            candObj.state = candidate_form.cleaned_data["state"]
            candObj.postal_code = candidate_form.cleaned_data["postal_code"]
            candObj.ssn = candidate_form.cleaned_data["ssn"]
            candObj.candidate_party = candidate_form.cleaned_data["candidate_party"]
            driving_licence_filename = request.FILES['address_proof'].name
            file_content = ContentFile(request.FILES['address_proof'].read())
            candObj.address_proof.save(driving_licence_filename, file_content)
            try:
                other_proof_filename = request.FILES['other_proof'].name
                other_doc_file_content = ContentFile(request.FILES['other_proof'].read())
                candObj.other_proof.save(other_proof_filename, other_doc_file_content)
            except:
                pass
            candObj.save()
            return redirect('cand_member_home')
    else:
        candidate_form = CandicateDetailsForm()
    return render(request, 'Upload_Election_Candidate_Information.html', {'form': candidate_form, 'candidate': candObj})


def show_present_elections(request):
    member = request.user
    if not member.is_active:
        return member_session_not_active(request)
    print(request.user.pk)
    future_elections = ElectionInformation.objects.all()
    for e in future_elections:
        voterObj = VoterInformation.objects.filter(member=request.user).first()
        if VotingInformation.objects.filter(voter=voterObj,election=e).exists():
            print("exists")
            e.is_vote_utilized = True
        else:
            e.is_vote_utilized = False
    return render(request, 'Show_Elections.html', {'elections': future_elections})

def cast_vote(request, id):
    if not request.user.is_active:
        return member_session_not_active(request)
    election = ElectionInformation.objects.filter(pk=id).first()
    candidates = CandidateInformation.objects.filter(is_candidate_verified=True)
    member = request.user
    voterObj = VoterInformation.objects.filter(member=member).first()
    if not voterObj:
        messages.add_message(request, messages.WARNING, "You are not authroized to use this page.")
        return redirect('elections')
    if VotingInformation.objects.filter(election=election, voter=voterObj):
        messages.add_message(request, messages.INFO, "You are already used your vote for this " + str(election.election_name))
        return redirect('elections')
    if request.method == "POST":
        candidate_id = request.POST["candidate"]
        candidate = CandidateInformation.objects.filter(pk=candidate_id).first()
        voting, voting_flag = VotingInformation.objects.get_or_create(candidate=candidate, voter=voterObj,
                                                                      election=election)
        if not voting_flag:
            print("You are already used your vote for this " + str(election.election_name))
        else:
            print("You are successfully casted your vote in " + str(election.election_name))
        return redirect('elections')
    return render(request, 'Cast_Vote_For_Candidate.html',
                  {'election': election, 'candidates': candidates, 'voter': voterObj})


from django.db.models import Count, Sum


def election_results(request, id):
    if not request.user.is_active:
        return member_session_not_active(request)
    election = ElectionInformation.objects.filter(pk=id).first()
    total_votes = VotingInformation.objects.filter(election=election).count()
    results = VotingInformation.objects.filter(election=election).order_by(
        "candidate").values("candidate__member__first_name",
                            "candidate__pk",
                            "election__election_name", "election__election_date",
                            "candidate__political_party",
                            "candidate__member__last_name").annotate(
        the_count=Count("candidate"))
    print("results:", results)
    if not results:
        messages.add_message(request, messages.INFO, "Elections not yet completed")
        return redirect('admin_member_home')
    maximum_votes = max(r["the_count"] for r in results)
    winner_candidate_id = ''
    for result in results:
        result["voting_perc"] = float(result["the_count"]) / float(total_votes) * 100
        if maximum_votes == float(result["the_count"]):
            winner_candidate_id = result["candidate__pk"]
    election.is_election_completed = True
    if winner_candidate_id:
        winner = CandidateInformation.objects.filter(pk=winner_candidate_id).first()
        election.winning_candidate_id = winner_candidate_id
        msg = str(winner.member.first_name) + " " + str(winner.member.last_name) + " won the election " + str(
            election.election_name)
        messages.add_message(request, messages.SUCCESS, msg)
        election.description = msg
    election.save()
    return render(request, 'Show_Election_Results.html',
                  {'results': results, 'total_votes': total_votes, 'maximum_votes': maximum_votes})


def admin_member_home_screen(request):
    if not request.user.is_active:
        return member_session_not_active(request)
    member = request.user
    return render(request, 'Election_Admin_Member_Home.html')

def get_admin_profile_details(request):
    if not request.user.is_active:
        return member_session_not_active(request)
    return render(request,'Election_Admin_Member_Details.html')

def candidate_member_home_screen(request):
    if not request.user.is_active:
        return member_session_not_active(request)
    member = request.user
    print(member.pk)
    candidate = CandidateInformation.objects.filter(member=member).first()
    return render(request, 'Election_Candidate_Member_Home.html', {'candidate_id': candidate.id,'candidate':candidate})


def voter_member_home_screen(request):
    if not request.user.is_active:
        return member_session_not_active(request)
    member = request.user
    print(member.pk)
    voter = VoterInformation.objects.filter(member=member).first()
    print(voter.id)
    return render(request, 'Election_Voter_Member_Home.html', {'voter_id': voter.id,'voter':voter})
