from django.contrib import admin
from .models import ElectionMember, VoterInformation, CandidateInformation, ElectionInformation, VotingInformation
from django.contrib.auth.models import Group

admin.site.register(ElectionMember)
admin.site.register(VoterInformation)
admin.site.register(CandidateInformation)
admin.site.register(ElectionInformation)
admin.site.register(VotingInformation)
admin.site.unregister(Group)
