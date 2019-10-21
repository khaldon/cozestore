from . models import Comment
from django import forms 
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body' )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class' : 'stext-111 cl2 plh3 size-116 p-lr-18','placeholder':'Name *'})
        self.fields['email'].widget.attrs.update({'class': 'stext-111 cl2 plh3 size-116 p-lr-18','placeholder':'Email *'})
        self.fields['body'].widget.attrs.update({'class' : 'stext-111 cl2 plh3 size-124 p-lr-18 p-tb-15','placeholder':'Comment....'})