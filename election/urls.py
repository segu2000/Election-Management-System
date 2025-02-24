
from django.contrib import admin
from django.urls import path

from application.views import candidate_login, voter_login, candidate_or_voter_registration, voter_member_home_screen, \
    candidate_member_home_screen, admin_member_home_screen, save_voter_member_information, \
    save_candidate_member_information, get_voter_details, delete_voter_details, \
    verify_voter_details, verify_candidate_details, election_member_account_registration, election_member_login, \
    website_home_screen, get_all_candidate_details, \
    get_candidate_details, delete_candidate_details, get_all_voter_details, show_present_elections, cast_vote, \
    election_results,get_admin_profile_details

urlpatterns = [
    # tested all urls
    path('election/commission/admin/', admin.site.urls),
    path('',website_home_screen,name='election_home'),
    path('admin/registration/', election_member_account_registration, name='admin_signup'),
    path('admin/login/', election_member_login, name='superuser_login'),
    path('admin/home/',admin_member_home_screen,name='admin_member_home'),
    path('cand/registration/', candidate_or_voter_registration, name='candicate_signup'),
    path('voter/registration/', candidate_or_voter_registration, name='voter_signup'),
    path('cand/login/', candidate_login, name='candidate_login'),
    path('voter/login/', voter_login, name='voter_login'),
    path('candidates/', get_all_candidate_details, name='all_candidate_details'),
    path('cand/<int:id>/', get_candidate_details, name='get_candidate'),
    path('cand/del/<int:id>/', delete_candidate_details, name='del_candidate'),
    path('cand/verify/<int:id>/', verify_candidate_details, name='verify_candidate'),
    path('cand/home/',candidate_member_home_screen,name='cand_member_home'),
    path('voter/home/',voter_member_home_screen,name='voter_home'),
    path('cand/upload/details/', save_candidate_member_information, name='save_candidate_details'),
    path('voters/', get_all_voter_details, name='all_voter_details'),
    path('voter/<int:voter_id>/', get_voter_details, name='get_voter'),
    path('voter/del/<int:voter_id>/', delete_voter_details, name='del_voter'),
    path('voter/verify/<int:voter_id>/', verify_voter_details, name='verify_voter'),
    path('voter/upload/details/', save_voter_member_information, name='upload_voter_details'),
    path('present/elections/', show_present_elections, name='elections'),
    path('cast/vote/<int:id>/',cast_vote,name='cast_vote'),
    path('election/results/<int:id>/',election_results,name='election_results'),
    path('admin/profile/details/',get_admin_profile_details,name='admin_profile_details'),
]
