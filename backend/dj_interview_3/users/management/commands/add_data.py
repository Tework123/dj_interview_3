from django.core.management import BaseCommand
from django.utils import timezone
from faker import Faker
from users.models import CustomUser
from dateutil.relativedelta import relativedelta


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        fake = Faker()

        # добавляем админа
        CustomUser.objects.create_superuser(email='admin@mail.ru',
                                            password='admin@mail.ru')

        # добавляем пользователей
        for i in range(1, 10):
            name = fake.name()
            name_join = name.replace(' ', '')
            city = fake.city()
            job = fake.job()
            if i == 1:
                name_join = 'user'

            CustomUser.objects.create_user(email=name_join + '@mail.ru',
                                           password=name_join + '@mail.ru',
                                           first_name=name.split(' ')[0],
                                           last_name=name.split(' ')[1],
                                           city=city,
                                           about_me=job,
                                           date_of_birth=timezone.now() - relativedelta(years=35))

        self.stdout.write(self.style.SUCCESS('Пользователи успешно созданы!'))
