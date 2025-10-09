from allauth.account.forms import LoginForm, SignupForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Div
from crispy_bootstrap5.bootstrap5 import FloatingField


class CustomLoginForm(LoginForm):
    """
    Custom login form to render fields using BS5 floating fields
    Inherits the fields from allAuth LoginForm
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column(FloatingField('login'), css_class="col-12"),
                Column(FloatingField('password'), css_class="col-12"),
            )
        )


class CustomSignupForm(SignupForm):
    """
    Custom signup form to render fields using BS5 floating fields
    Inherits the fields from allAuth SignupForm
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(FloatingField('username'), css_class='w-100 mb-3'),
            Div(FloatingField('email'), css_class='w-100 mb-3'),
            Div(
                FloatingField('password1'),
                css_class='w-100 mb-3'
            ),
            Div(FloatingField('password2'), css_class='w-100 mb-3'),
        )
