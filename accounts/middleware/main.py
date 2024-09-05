from django.utils.deprecation import MiddlewareMixin

class AuthenticationPopupMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.show_registration_popup = not request.user.is_authenticated
        print(f"Popup Flag: {request.show_registration_popup}")  # For debugging
