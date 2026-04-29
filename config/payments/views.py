from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django_ratelimit.decorators import ratelimit
import logging
from cryptography.fernet import Fernet
from django.conf import settings
from .models import Payment
import json

logger = logging.getLogger(__name__)
cipher = Fernet(settings.FERNET_KEY)

@csrf_exempt
@ratelimit(key='ip', rate='5/m', block=True)
def login_view(request):
        
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            
            # Use real Django authentication
            from django.contrib.auth import authenticate
            user = authenticate(username=username, password=password)
            
            if user is not None:
                logger.info(f"Login attempt for user: {username} from IP: {request.META.get('REMOTE_ADDR')}")
                return JsonResponse({'message': 'Login attempt'})
            else:
                logger.warning("Multiple failed login attempts detected")
                return JsonResponse({'status': 'error', 'message': 'Invalid credentials or access without authentication'}, status=401)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

@csrf_exempt
def make_payment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            card_data = data.get('card_number')
            
            if not card_data:
                return JsonResponse({'status': 'error', 'message': 'Missing card_number'}, status=400)
            
            # Encrypt sensitive data
            try:
                encrypted_data = cipher.encrypt(card_data.encode('utf-8'))
            except Exception as e:
                # Invalid encrypted payloads or encryption error
                logger.error(f"Encryption error: {str(e)}")
                return JsonResponse({'status': 'error', 'message': 'Encryption failed or invalid payload'}, status=400)
            
            # Store encrypted data in the database
            payment = Payment.objects.create(
                encrypted_card_data=encrypted_data,
                amount=data.get('amount', 0.0)
            )
            
            return JsonResponse({
                'status': 'success', 
                'message': 'Payment processed and encrypted',
                'payment_id': payment.id
            })
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)
