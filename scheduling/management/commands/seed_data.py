from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta, time
from scheduling.models import Professional, Service, DateSlot, TimeSlot


class Command(BaseCommand):
    help = 'Popula o banco de dados com dados iniciais para teste'

    def handle(self, *args, **options):
        self.stdout.write('Criando dados iniciais...')

        # Criar profissionais
        professionals_data = [
            {'name': 'Mariana', 'specialty': 'Manicure e Pedicure'},
            {'name': 'Carla', 'specialty': 'Nail Art e Unhas Gel'},
            {'name': 'Juliana', 'specialty': 'Spa e Tratamentos'},
        ]

        professionals = []
        for prof_data in professionals_data:
            prof, created = Professional.objects.get_or_create(
                name=prof_data['name'],
                defaults={
                    'specialty': prof_data['specialty'],
                    'is_active': True
                }
            )
            professionals.append(prof)
            if created:
                self.stdout.write(f'  Criado profissional: {prof.name}')

        # Criar serviços
        services_data = [
            {'name': 'Manicure', 'description': 'Corte, lixamento e pintura de unhas', 'duration_minutes': 30, 'price': 35.00},
            {'name': 'Pedicure', 'description': 'Tratamento completo dos pés', 'duration_minutes': 45, 'price': 45.00},
            {'name': 'Unhas Gel', 'description': 'Aplicação de unhas em gel', 'duration_minutes': 90, 'price': 120.00},
            {'name': 'Nail Art', 'description': 'Decoração artística nas unhas', 'duration_minutes': 60, 'price': 80.00},
            {'name': 'Spa das Mãos', 'description': 'Tratamento spa completo para mãos', 'duration_minutes': 60, 'price': 70.00},
            {'name': 'Spa dos Pés', 'description': 'Tratamento spa completo para pés', 'duration_minutes': 60, 'price': 75.00},
            {'name': 'Esmaltação em Gel', 'description': 'Esmaltação semipermanente', 'duration_minutes': 45, 'price': 55.00},
            {'name': 'Manicure + Pedicure', 'description': 'Combo manicure e pedicure', 'duration_minutes': 75, 'price': 70.00},
        ]

        services = []
        for serv_data in services_data:
            serv, created = Service.objects.get_or_create(
                name=serv_data['name'],
                defaults={
                    'description': serv_data['description'],
                    'duration_minutes': serv_data['duration_minutes'],
                    'price': serv_data['price'],
                    'is_active': True
                }
            )
            services.append(serv)
            if created:
                self.stdout.write(f'  Criado serviço: {serv.name}')

        # Criar DateSlots para os próximos 30 dias
        today = timezone.now().date()
        time_slots_config = [
            time(9, 0), time(9, 30), time(10, 0), time(10, 30),
            time(11, 0), time(11, 30), time(13, 0), time(13, 30),
            time(14, 0), time(14, 30), time(15, 0), time(15, 30),
            time(16, 0), time(16, 30), time(17, 0), time(17, 30),
        ]

        slots_created = 0
        for day_offset in range(1, 31):  # Próximos 30 dias
            date = today + timedelta(days=day_offset)

            # Não criar horários aos domingos
            if date.weekday() == 6:
                continue

            for professional in professionals[:2]:  # Apenas 2 profissionais por dia
                date_slot, created = DateSlot.objects.get_or_create(
                    date=date,
                    professional=professional,
                    defaults={'is_available': True}
                )

                if created:
                    for i, start_time in enumerate(time_slots_config[:12]):  # 12 horários por dia
                        end_hour = start_time.hour
                        end_min = start_time.minute + 30
                        if end_min >= 60:
                            end_hour += 1
                            end_min -= 60
                        end_time = time(end_hour, end_min)

                        TimeSlot.objects.create(
                            date_slot=date_slot,
                            start_time=start_time,
                            end_time=end_time,
                            status='available'
                        )
                        slots_created += 1

        self.stdout.write(self.style.SUCCESS(
            f'\nDados criados com sucesso!\n'
            f'  - {len(professionals)} profissionais\n'
            f'  - {len(services)} serviços\n'
            f'  - {slots_created} horários disponíveis\n\n'
            f'Agora você pode:\n'
            f'  1. Acessar /gestao/login/ para fazer login como admin\n'
            f'  2. Criar usuário admin com: python manage.py createsuperuser\n'
            f'  3. Verificar os dados em: /gestao/\n'
        ))