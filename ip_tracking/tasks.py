from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import RequestLog, SuspiciousIP
from django.db.models import Count

@shared_task
def detect_suspicious_ips():
    # Définir la période d'analyse (dernière heure)
    one_hour_ago = timezone.now() - timedelta(hours=1)
    
    # Chemins sensibles à surveiller
    sensitive_paths = ['/admin', '/login', '/api']
    
    # Détecter les IPs avec plus de 100 requêtes par heure
    high_frequency_ips = RequestLog.objects.filter(
        timestamp__gte=one_hour_ago
    ).values('ip_address').annotate(
        request_count=Count('ip_address')
    ).filter(request_count__gt=100)
    
    # Détecter les IPs accédant aux chemins sensibles fréquemment
    sensitive_path_ips = RequestLog.objects.filter(
        timestamp__gte=one_hour_ago,
        path__in=sensitive_paths
    ).values('ip_address').annotate(
        request_count=Count('ip_address')
    ).filter(request_count__gt=10)
    
    # Traiter les IPs suspectes
    for ip_data in high_frequency_ips:
        SuspiciousIP.objects.get_or_create(
            ip_address=ip_data['ip_address'],
            defaults={
                'reason': f"High frequency: {ip_data['request_count']} requests/hour",
                'request_count': ip_data['request_count']
            }
        )
    
    for ip_data in sensitive_path_ips:
        SuspiciousIP.objects.get_or_create(
            ip_address=ip_data['ip_address'],
            defaults={
                'reason': f"Sensitive paths accessed: {ip_data['request_count']} times/hour",
                'request_count': ip_data['request_count']
            }
        )
    
    return f"Analyzed {len(high_frequency_ips) + len(sensitive_path_ips)} suspicious IPs"