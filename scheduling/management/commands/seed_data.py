from django.core.management.base import BaseCommand
from scheduling.models import Professional, Service, DateSlot, TimeSlot
from datetime import date, timedelta


class Command(BaseCommand):
    help = 'Popular banco com dados iniciais'

    def handle(self, *args, **kwargs):
        self.stdout.write('Criando profissionais...')
        
        # Criar profissionais
        prof1, _ = Professional.objects.get_or_create(
            name='Ana Silva',
            defaults={'specialty': 'Manicure', 'is_active': True}
        )
        
        prof2, _ = Professional.objects.get_or_create(
            name='Carla Santos',
            defaults={'specialty': 'Pedicure', 'is_active': True}
        )
        
        self.stdout.write(self.style.SUCCESS(f'Profissionais: {Professional.objects.count()}'))
        
        # Criar serviços
        self.stdout.write('Criando serviços...')
        
        Service.objects.get_or_create(
            name='Manicure Completa',
            defaults={
                'description': 'Corte, lixa e esmaltação',
                'duration_minutes': 60,
                'price': 50.00,
                'is_active': True
            }
        )
        
        Service.objects.get_or_create(
            name='Pedicure Completa',
            defaults={
                'description': 'Corte, lixa e esmaltação dos pés',
                'duration_minutes': 45,
                'price': 40.00,
                'is_active': True
            }
        )
        
        Service.objects.get_or_create(
            name='Manicure e Pedicure',
            defaults={
                'description': 'Serviço completo',
                'duration_minutes': 120,
                'price': 80.00,
                'is_active': True
            }
        )
        
        self.stdout.write(self.style.SUCCESS(f'Serviços: {Service.objects.count()}'))
        
        # Criar datas para os próximos 30 dias
        self.stdout.write('Criando datas disponíveis...')
        hoje = date.today()
        total_datas = 0
        
        for i in range(30):
            data = hoje + timedelta(days=i)
            # Pula fins de semana
            if data.weekday() < 6:
                for prof in [prof1, prof2]:
                    date_slot, created = DateSlot.objects.get_or_create(
                        date=data,
                        professional=prof,
                        defaults={'is_available': True}
                    )
                    
                    if created:
                        # Criar horários das 9h às 18h
                        for hora in range(9, 18):
                            TimeSlot.objects.get_or_create(
                                date_slot=date_slot,
                                start_time=f'{hora:02d}:00',
                                defaults={
                                    'end_time': f'{hora:02d}:30',
                                    'status': 'available'
                                }
                            )
                        total_datas += 1
        
        self.stdout.write(self.style.SUCCESS(f'Datas criadas: {total_datas}'))
        self.stdout.write(self.style.SUCCESS('Dados iniciais criados com sucesso!'))
