#!/bin/bash
python manage.py collectstatic --noinput
python manage.py migrate
python manage.py shell -c "
from scheduling.models import Professional, Service, DateSlot, TimeSlot
from datetime import date, timedelta

# Criar profissionais se não existirem
if Professional.objects.count() == 0:
    prof1 = Professional.objects.create(name='Ana Silva', specialty='Manicure', is_active=True)
    prof2 = Professional.objects.create(name='Carla Santos', specialty='Pedicure', is_active=True)
else:
    prof1 = Professional.objects.first()

# Criar serviços se não existirem
if Service.objects.count() == 0:
    Service.objects.create(name='Manicure Completa', description='Corte, lixa e esmaltação', duration_minutes=60, price=50.00, is_active=True)
    Service.objects.create(name='Pedicure Completa', description='Corte, lixa e esmaltação dos pés', duration_minutes=45, price=40.00, is_active=True)
    Service.objects.create(name='Manicure e Pedicure', description='Serviço completo', duration_minutes=120, price=80.00, is_active=True)

# Criar datas para os próximos 30 dias
hoje = date.today()
for i in range(30):
    data = hoje + timedelta(days=i)
    if data.weekday() < 6:  # Seg-Sex
        date_slot, created = DateSlot.objects.get_or_create(
            date=data,
            professional=prof1,
            defaults={'is_available': True}
        )
        if created and TimeSlot.objects.filter(date_slot=date_slot).count() == 0:
            for hora in range(9, 18):
                TimeSlot.objects.create(
                    date_slot=date_slot,
                    start_time=f'{hora:02d}:00',
                    end_time=f'{hora:02d}:30',
                    status='available'
                )
"
