from django.views.generic.edit import FormMixin
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django import forms
class PasswordChangeFormEdit(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'class' : 'stext-111 cl2 plh3 size-116 p-lr-18','placeholder':'Old password'})
        self.fields['new_password1'].widget.attrs.update({'class' : 'stext-111 cl2 plh3 size-116 p-lr-18','placeholder':'New password'})
        self.fields['new_password2'].widget.attrs.update({'class' : 'stext-111 cl2 plh3 size-116 p-lr-18','placeholder':'New password confirmation'})


class PasswordResetFormEdit(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class' : 'stext-111 cl2 plh3 size-116 p-lr-18','placeholder':'Old password'})


class PasswordResetConfirmFormEdit(SetPasswordForm):
    def __init__(self, *args, **kwargs):
       super().__init__(self, *args, **kwargs)
       self.fields['old_password'].widget.attrs.update({'class' : 'stext-111 cl2 plh3 size-116 p-lr-18','placeholder':'Old password'})
       self.fields['new_password1'].widget.attrs.update({'class' : 'stext-111 cl2 plh3 size-116 p-lr-18','placeholder':'New password'})
       self.fields['new_password2'].widget.attrs.update({'class' : 'stext-111 cl2 plh3 size-116 p-lr-18','placeholder':'New password confirmation'})
