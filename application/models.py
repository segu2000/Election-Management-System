from django.contrib.auth.models import AbstractUser
from django.db import models

POLITICAL_PARTY_CHOICES = (('DEM','Democratic'),('REP','Republican'),
)


class ElectionMember(AbstractUser):
    election_member_id = models.AutoField(primary_key=True)
    phone_number = models.CharField(max_length=10, null=True, blank=True)
    # Election commission actor types - Voter, Admin (handle all voters & candidates), Candidate
    member_type = models.CharField(max_length=3,
                                   choices=(('CAN', 'Candidate'), ('VOT', 'Voter'), ('ADM', 'Election Admin')), null=True)

    def __str__(self):
        """
        Returning the primary key of object
        """
        return str(self.election_member_id)



class VoterInformation(models.Model):
    """
    Saving the all Voters information in this table.
    """
    id = models.AutoField(primary_key=True)
    member = models.ForeignKey(ElectionMember, on_delete=models.CASCADE)
    voter_id = models.CharField(max_length=20,null=True,blank=True)
    birth_date = models.DateField(null=True)
    person_type = models.CharField(max_length=6, choices=(('Male','Male'),('Female','Female')), null=True, blank=True)
    full_address = models.CharField(max_length=180,null=True)
    state = models.CharField(choices=(('KS','Kansas'),), max_length=2,null=True)
    postal_code = models.CharField(max_length=5,null=True)
    ssn = models.CharField(max_length=9,null=True)
    address_proof = models.FileField(upload_to='voter_documents/',null=True)
    other_proof = models.FileField(upload_to='voter_documents/',null=True,blank=True)
    is_account_verified = models.BooleanField(default=False)
    description = models.CharField(max_length=100,null=True,blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.id)


class CandidateInformation(models.Model):
    """
    Saving all candidate information in this table.
    """
    id = models.AutoField(primary_key=True) # primary key of the table.
    member = models.ForeignKey(ElectionMember, on_delete=models.CASCADE)
    candidate_id = models.CharField(max_length=20,null=True,blank=True) # candidate id ( will create by admin once details verified)
    birth_date = models.DateField(null=True) # date of birth of candidate
    person_type = models.CharField(max_length=6, choices=(('Male','Male'),('Female','Female')),null=True)
    full_address = models.CharField(max_length=180,null=True)
    state = models.CharField(choices=(('KS','Kansas'),), max_length=2,null=True)
    postal_code = models.CharField(max_length=5,null=True)
    ssn = models.CharField(max_length=9,null=True)
    political_party = models.CharField(max_length=3, choices=POLITICAL_PARTY_CHOICES,null=True)
    address_proof = models.FileField(upload_to='candidate_documents/',null=True)
    is_candidate_verified = models.BooleanField(default=False)
    is_fault_account = models.BooleanField(default=False)
    description = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        """
        Returning the primary key of table.
        """
        return str(self.id)


class ElectionInformation(models.Model):
    """
    Saving all elections information - admin will enter the details of each election.
    """
    election_id = models.AutoField(primary_key=True)
    election_name = models.CharField(max_length=200)
    election_date = models.DateField(null=True, blank=True)
    election_result_date = models.DateField(null=True, blank=True)
    election_description = models.CharField(max_length=100, null=True, blank=True)
    is_election_completed = models.BooleanField(default=False)
    winning_candidate_id = models.CharField(max_length=20,null=True,blank=True)


    def __str__(self):
        return str(self.election_id)


class VotingInformation(models.Model):
    """
    Saving elections votes in this table.
    """
    id = models.AutoField(primary_key=True)
    election = models.ForeignKey(ElectionInformation, on_delete=models.CASCADE)
    candidate = models.ForeignKey(CandidateInformation, on_delete=models.CASCADE)
    voter = models.ForeignKey(VoterInformation, on_delete=models.CASCADE)
    created = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.id)
