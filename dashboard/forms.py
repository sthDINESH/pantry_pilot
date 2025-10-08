from allauth.account.forms import LoginForm, SignupForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Div, HTML
from crispy_bootstrap5.bootstrap5 import FloatingField


class CustomLoginForm(LoginForm):
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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(FloatingField('username'), css_class='w-100 mb-3'),
            Div(FloatingField('email'), css_class='w-100 mb-3'),
            Div(
                FloatingField('password1'),
                # HTML("""
                #     <div class="form-text text-muted small">
                #         <ul class="mb-0">
                #             <li>Your password can't be too similar to your other personal information.</li>
                #             <li>Your password must contain at least 8 characters.</li>
                #             <li>Your password can't be a commonly used password.</li>
                #             <li>Your password can't be entirely numeric.</li>
                #         </ul>
                #     </div>
                # """),
                css_class='w-100 mb-3'
            ),
            Div(FloatingField('password2'), css_class='w-100 mb-3'),
        )

