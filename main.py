from peewee import *

db = SqliteDatabase('academia.db')

class Profesores(Model):
    maestro_id = AutoField()
    nombre = CharField()
    apellido = CharField()
    telefono = CharField()
    email = CharField(unique=True)

    class Meta:
        database = db

class Clases(Model):
    clase_id = AutoField()
    cod_curso = CharField()
    fecha_inicio_curso = DateField()
    fecha_fin_curso = DateField()
    horario = CharField()
    maestro_id = ForeignKeyField(Profesores)

    class Meta:
        database = db

db.connect()
db.create_tables([Profesores, Clases])

## INSERT
chamo = Profesores( nombre='Chamo',
                    apellido='Linares',
                    telefono='640568923',
                    email='alinares@paradigmadigital.com')
chamo.save()

# curso_python = Clases( cod_curso='python_101',
#                     fecha_inicio_curso='2020-03-09',
#                     fecha_fin_curso='2020-03-20',
#                     horario='Matutino',
#                     maestro_id = 1)
# curso_python.save()

data = [
    {'cod_curso': 'python_202', 'fecha_inicio_curso': '2020-04-06', 'fecha_fin_curso': '2020-04-10', 'horario': 'Nocturno', 'maestro_id': 1},
    {'cod_curso': 'go_101', 'fecha_inicio_curso': '2020-04-13', 'fecha_fin_curso': '2020-04-17', 'horario': 'Matutitno', 'maestro_id': 1},
    {'cod_curso': 'linux_101', 'fecha_inicio_curso': '2020-04-20', 'fecha_fin_curso': '2020-04-24', 'horario': 'Vespertino', 'maestro_id': 1},
]

with db.atomic():
    query = Clases.insert_many(data)
    query.execute()


## UPDATE
# chamo_update = Profesores.update(nombre='Alvaro').where(Profesores.maestro_id == 1).execute()


## DELETE
# go_delete = Clases.delete().where(Clases.cod_curso == 'go_101').execute()


## SELECT
# for profesor in Profesores.select():
#     print('Nombre: {} - Apellido: {} - Teléfono: {} - Email: {}'
#     .format(profesor.nombre, profesor.apellido, profesor.telefono, profesor.email))

## SELECT JOIN
query = (Profesores
         .select(Profesores, Clases)
         .join(Clases)
         .group_by(Clases.cod_curso)
         .where(Profesores.maestro_id == Clases.maestro_id))

for curso in query:
    print('El curso {} esta comienza el {} y termina el {}, y va ser impartido por {} {}'
    .format(curso.clases.cod_curso, curso.clases.fecha_inicio_curso, curso.clases.fecha_fin_curso, curso.nombre, curso.apellido))
