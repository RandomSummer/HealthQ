# Django Backend (views.py)
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def health_data(request):
    sample_data = {"heart_rate": 72, "blood_pressure": "120/80", "temperature": 98.6}
    return JsonResponse(sample_data)