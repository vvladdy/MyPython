from sqlalchemy import create_engine, MetaData, Text, Column, Integer, String
from sqlalchemy.schema import Table
from faker import Faker

engine = create_engine('sqlite:///sample.db', echo=True)

metadata = MetaData()

workers = Table(
    'workers', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('f_name', String(50), unique=True, nullable=False),
    Column('s_name', String(100), unique=True),
    Column('position', Text),
)
# workers.create(engine)

connection = engine.connect()

insert = workers.insert().values(
    f_name='Ivan',
    s_name='Borisov',
    position='supply manager',
)
# connection.execute(insert)

update = workers.update().values(
    position='supply chain manager',
)
# connection.execute(update)

# или оновление именно по имеющейся инф-ции в базе
smth = workers.update().where(
    workers.c.position == 'supply chain manager').values(
    position='supply chain'
)
# connection.execute(update)

# удаление элемента определенного из таблицы
# del_el = workers.delete().where(workers.c.f_name == 'Ivan')
# connection.execute(del_el)

faker = Faker()
fake_ru = Faker('ru_RU')

# добавление нескольких строк
# connection.execute(workers.insert(), [
#     {'f_name': 'Sergey', 's_name': 'TuniK', 'position': 'Programmer'},
#     {'f_name': f'{fake_ru.name()}', 's_name': f'{fake_ru.last_name()}',
#      'position': f'{fake_ru.job()}'},
#     {'f_name': f'{fake_ru.name()}', 's_name': f'{fake_ru.last_name()}',
#      'position': f'{fake_ru.job()}'}
# ])

# for i in range(10):
#     connection.execute(workers.insert(), [
#     {'f_name': f'{fake_ru.name()}', 's_name': f'{fake_ru.last_name()}',
#         'position': f'{fake_ru.job()}'}
#     ])

wk = workers.select().where(workers.c.position == 'supply chain manager')
print(connection.execute(wk).fetchmany(2))

newreq = workers.select()
print(connection.execute(newreq).fetchall())

# или так вывод на экран элементов
# result = connection.execute(wk)
# for i in result:
#     print(i)
