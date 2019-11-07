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

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to  = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class' : 'stext-111 cl2 plh3 size-116 p-lr-18','placeholder':'Name *'})
        self.fields['email'].widget.attrs.update({'class': 'stext-111 cl2 plh3 size-116 p-lr-18','placeholder':'Email *'})
        self.fields['to'].widget.attrs.update({'class' : 'stext-111 cl2 plh3 size-116 p-lr-18','placeholder':'To....'})
        self.fields['comments'].widget.attrs.update({'class' : 'stext-111 cl2 plh3 size-124 p-lr-18 p-tb-15','placeholder':'Comment....'})

class SearchForm(forms.Form):
    query = forms.CharField(max_length=30)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['query'].widget.attrs.update({'placeholder':'Search'})

