from faker import Faker
from faker.providers import BaseProvider
from faker import providers

fake = Faker()

fake_jp = Faker('jp_JP')

fake_ru = Faker('ru_RU')

fake_de = Faker('de_DE')

print(fake.name())
print(fake_jp.name())
print(fake_ru.address())

print(fake_de.address())
print(fake_ru.job())
print(fake_ru.currency())
print(fake_ru.credit_card_full())



# свой собственный класс

class MyProvider(BaseProvider):

    def foo(self):
        return 'bar'

fake.add_provider(MyProvider)
n = fake.foo()
print(n)
