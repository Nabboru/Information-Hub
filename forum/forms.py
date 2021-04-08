from django import forms 
from .models import ForumPost 
from .models import Comment
from .models import AnnouncementPost
  
  
# creating a form 
class ForumPostForm(forms.ModelForm): 
    # create meta class 
    class Meta: 
        # specify model to be used 
        model = ForumPost 
  
        # specify fields to be used 
        fields = [ 
         "subject", 
         "content", 
         "for_patient",
         "for_family",
        ]

        labels = {
            'for_patient': ('Visible for other patients users'),
            'for_family': ('Visible for other family users'),
        }

 
class CommentForm(forms.ModelForm): 
    class Meta: 
        model = Comment
        fields = [ 
            "content", 
        ] 

class AnnouncementForm(forms.ModelForm): 
    # create meta class 
    class Meta: 
        # specify model to be used 
        model =  AnnouncementPost
  
        # specify fields to be used 
        fields = [ 
         "subject", 
         "content", 
        ]