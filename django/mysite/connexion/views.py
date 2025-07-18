from django.shortcuts import render
from django.shortcuts import redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User

class login_page(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("dashboard_page_url")

        return render(request, 'connexion/login.html')

    def post(self, request):
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")
            
            if not (username and password):
                messages.error(request, "Please enter your username and password.")
                return redirect("login_page_url")

            if "@" in username:
                user_email = User.objects.filter(email=username).first()
                if user_email is None:
                    messages.error(request, "Please enter a valid email.")
                    return redirect("login_page_url")
                username = user_email.username

            user_email = User.objects.filter(username=username).first()
            if user_email is None:
                messages.error(request, "Please enter a valid username.")
                return redirect("login_page_url")

            authenticated_user = authenticate(request, username=username, password=password)
            if authenticated_user is not None:
                if not authenticated_user.profile.mfa_enabled:
                    # Login the user if authentication is successful
                    loginss = login(request, authenticated_user)
                    # Redirect to the page the user was trying to access before logging in
                    if "next" in request.POST:
                        return redirect(request.POST["next"])
                    else:
                        # Redirect to the home page or another appropriate page
                        return redirect("dashboard_page_url")
                else:
                    context = self.get_context_data()
                    context.update({"user_id": authenticated_user.profile.id})
                    return render(request, "connexion/verify_mfa.html", context)
            else:
                messages.error(request, "Please enter a valid username.")
                return redirect("login_page_url")

        return render(request, "connexion/login.html")

def logout_page(request):
    logout(request)
    return redirect("login_page_url")
# class LoginVerifyMfaView(AuthView):
#     def get(self, request):
#         if request.user.is_authenticated:
#             # If the user is already logged in, redirect them to the home page or another appropriate page.
#             return redirect("index")  # Replace 'index' with the actual URL name for the home page

#         # Render the login page for users who are not logged in.
#         return super().get(request)

#     def post(self, request, *args, **kwargs):
#         otp = request.POST.get('otp_code')
#         user_id = request.POST.get('user_id')
#         context = self.get_context_data()
#         context.update({"user_id": user_id})
#         if not user_id:
#             messages.error(request, "Invalid request")
#             return  render(request, "auth/verify_mfa.html", context)
#         user = Profile.objects.get(id=user_id)
#         if self.verify_2fa_otp(user, otp):
#             user = User.objects.get(id=user.user_id)
#             if self.login_user(request, user):
#                 return redirect("index")
#             else:
#                 messages.error(request, "Can't login user")
#                 return  render(request, "auth/verify_mfa.html", context)
#         else:
#             messages.error(request, "Invalid Code")
#             return  render(request, "auth/verify_mfa.html", context)

#     def verify_2fa_otp(self, user, otp):
#         totp = pyotp.TOTP(user.mfa_secret)
#         if totp.verify(otp):
#             user.mfa_enabled = True
#             user.save()
#             return True
#         return False

#     def login_user(self, request, user):
#         login(request, user)
#         return True

# class LoginResetMfaCodeView(AuthView):
#     def get(self, request):
#         if request.user.is_authenticated:
#             return redirect("index")
#         context = self.get_context_data()
#         user_id = request.GET.get('user_id')
#         context.update({
#             "user_id": user_id,
#             "qr_code_data_uri": self.get_qr_code(user_id)
#         })
#         return render(request, "auth/reset_mfa_code.html", context)

#     def get_qr_code(self, user_id):
#         user = Profile.objects.get(id=user_id)
#         if not user.mfa_secret:
#             user.mfa_secret = pyotp.random_base32()
#             user.save()

#         otp_uri = pyotp.totp.TOTP(user.mfa_secret).provisioning_uri(name=user.email, issuer_name='assetmanagement')

#         qr = qrcode.make(otp_uri)
#         buffer = io.BytesIO()
#         qr.save(buffer, format("PNG"))

#         buffer.seek(0)
#         qr_code = base64.b64encode(buffer.getvalue()).decode("utf-8")

#         qr_code_data_uri = f"data:image/png;base64,{qr_code}"
#         return qr_code_data_uri

#     def post(self, request, *args, **kwargs):
#         otp = request.POST.get('otp_code')
#         user_id = request.POST.get('user_id')
#         context = self.get_context_data()
#         context.update({
#             "user_id": user_id,
#         })
#         if not user_id:
#             messages.error(request, "Invalid request")
#             return render(request, "auth/verify_mfa.html", context)
#         user = Profile.objects.get(id=user_id)
#         if self.verify_2fa_otp(user, otp):
#             messages.success(request, "MFA reset successfully")
#             return redirect('login')
#         else:
#             messages.error(request, "Invalid OTP code from image, please try reset again")
#             return render(request, "auth/verify_mfa.html", context)

#     def verify_2fa_otp(self, user, otp):
#         totp = pyotp.TOTP(user.mfa_secret)
#         if totp.verify(otp):
#             user.mfa_enabled = True
#             user.save()
#             return True
#         return False