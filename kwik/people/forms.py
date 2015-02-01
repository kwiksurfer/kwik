from django import forms
from django.contrib.auth.models import User
from people.models import UserProfile, Message

class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = {'sex',}
        # exclude = ('status','friends','joined_at',)
        widgets = {


            # 'picture': ProfilePictureField(),   # create profile picture field.
            #                                     # a selector showing all current user's pictures
            #                                     # along with a current picture view and
            #                                     # a picture uploader
            #                                     # actually, I'll just add a profile picture page jare
        }

class UserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {
        'duplicate_username': ("A user with that username already exists."),
        'password_mismatch': ("The two password fields didn't match."),
        'duplicate_email': ("A user with that email address already exists."),
    }
    username = forms.RegexField(label=("Username"), max_length=30,
        regex=r'^[\w.@+-]+$',
        help_text = ("Required. 30 characters or fewer. Letters, digits and "
                      "@/./+/-/_ only."),
        error_messages = {
            'invalid': ("This value may contain only letters, numbers and "
                         "@/./+/-/_ characters.")})
    email = forms.EmailField(label=("Email Address"))
    password1 = forms.CharField(label=("Password"),
        widget=forms.PasswordInput)
    password2 = forms.CharField(label=("Password confirmation"),
        widget=forms.PasswordInput,
        help_text = ("Enter the same password as above, for verification."))

    class Meta:
        model = User
        fields = ("username","email",)

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])

    def clean_email(self):
        # Since User.email is not unique, this check is IMPORTant,
        # what ORM error?
        email = self.cleaned_data["email"]
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(self.error_messages['duplicate_email'])

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'])
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class AuthenticationForm(forms.Form):
    """
    Base class for authenticating users. Extend this to get a form that accepts
    username/password logins.
    """
    username = forms.CharField(label=("Username"), max_length=30)
    password = forms.CharField(label=("Password"), widget=forms.PasswordInput)

    error_messages = {
        'invalid_login': ("Please enter a correct username and password. "
                           "Note that both fields are case-sensitive."),
        'no_cookies': ("Your Web browser doesn't appear to have cookies "
                        "enabled. Cookies are required for logging in."),
        'inactive': ("This account is inactive."),
    }

    def __init__(self, request=None, *args, **kwargs):
        """
        If request is passed in, the form will validate that cookies are
        enabled. Note that the request (a HttpRequest object) must have set a
        cookie with the key TEST_COOKIE_NAME and value TEST_COOKIE_VALUE before
        running this validation.
        """
        self.request = request
        self.user_cache = None
        super(AuthenticationForm, self).__init__(*args, **kwargs)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            #self.user_cache = authenticate(username=username,
            #                               password=password)
            self.user_cache = authenticate(email=username,
                                                          password=password)
            #if self.user_cache is None:
            #    self.user_cache = self.email_verified_user_cache

            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'])
            elif not self.user_cache.is_active:
                raise forms.ValidationError(self.error_messages['inactive'])
        self.check_for_test_cookie()
        return self.cleaned_data

    def check_for_test_cookie(self):
        if self.request and not self.request.session.test_cookie_worked():
            raise forms.ValidationError(self.error_messages['no_cookies'])

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache


class MessageForm(forms.ModelForm):


    class Meta:
        model = Message

        widgets = {
            'message': forms.Textarea(attrs={'cols': 40, 'rows': 2,})
        }
        # exclude = {'conversation',}

class RequestDeleteForm(forms.Form):
    request_id = forms.HiddenInput()

class UserChangeForm(forms.ModelForm):

    def clean_password(self):
        return self.initial["password"]

    class Meta:
        model = User
        fields = ('first_name','last_name',)

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')
