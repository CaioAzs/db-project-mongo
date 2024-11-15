from faker import Faker
import random
from pymongo import MongoClient

client = MongoClient('localhost', 27017) #inserir informações de conexão
db = client['BANCO_MONGO'] #nome do banco
fake = Faker('pt_BR')

departamentos_collection = db['departamentos']
alunos_collection = db['alunos']
grupos_tcc_collection = db['grupos_tcc']

cursos = [
    "Ciência da Computação", "Engenharia Elétrica", "Engenharia de Robôs",
    "Engenharia Química", "Engenharia Mecânica", "Administração"
]
disciplinas = [
    "Cálculo Diferencial e Integral", "Física para Engenharia", "Álgebra Linear",
    "Mecânica dos Sólidos", "Banco de Dados", "Termodinâmica",
    "Cálculo Numérico", "Resistência dos Materiais", "Fundamentos de Programação"
]
departamentos = [
    "Ciência da Computação", "Matemática", "Elétrica",
    "Química", "Mecânica", "Física", "Administração de Empresas"
]

for i, departamento in enumerate(departamentos):
    cursos_embutidos = []
    for curso in random.sample(cursos, random.randint(2, 4)):
        disciplinas_embutidas = []
        for disciplina in random.sample(disciplinas, random.randint(2, 5)):
            professor = {
                "_id": fake.uuid4(),
                "nome_professor": fake.name(),
                "email_professor": fake.email()
            }
            disciplinas_embutidas.append({
                "_id": fake.uuid4(),
                "nome_disciplina": disciplina,
                "professor": professor
            })
        cursos_embutidos.append({
            "_id": fake.uuid4(),
            "nome_curso": curso,
            "disciplinas": disciplinas_embutidas
        })

    chefe = {
        "_id": fake.uuid4(),
        "nome_professor": fake.name(),
        "email_professor": fake.email()
    }
    professores_embutidos = [
        {"_id": fake.uuid4(), "nome_professor": fake.name(), "email_professor": fake.email()}
        for _ in range(random.randint(3, 6))
    ]

    departamentos_collection.insert_one({
        "_id": i + 1,
        "nome_departamento": departamento,
        "chefe": chefe,
        "professores": professores_embutidos,
        "cursos": cursos_embutidos
    })

for i in range(80):
    curso = random.choice(list(departamentos_collection.aggregate([{"$unwind": "$cursos"}, {"$sample": {"size": 1}}])))['cursos']
    
    num_disciplinas = random.randint(2, min(4, len(curso['disciplinas'])))
    disciplinas_embutidas = []
    for disciplina in random.sample(curso['disciplinas'], num_disciplinas):
        disciplinas_embutidas.append({
            "disciplina": {
                "_id": disciplina['_id'],
                "nome_disciplina": disciplina['nome_disciplina']
            },
            "professor": {
                "id_professor": disciplina['professor']['_id'],
                "nome_professor": disciplina['professor']['nome_professor']
            },
            "ano": random.randint(2010, 2024),
            "semestre": random.randint(1, 2),
            "nota_final": round(random.uniform(0, 10), 2)
        })

    alunos_collection.insert_one({
        "_id": fake.uuid4(),
        "nome_aluno": fake.name(),
        "ano_inicio": random.randint(2010, 2024),
        "email_aluno": fake.email(),
        "cursos": [
            {
                "_id": curso['_id'],
                "nome_curso": curso['nome_curso'],
                "disciplinas": disciplinas_embutidas
            }
        ]
    })

for i in range(5):
    orientador = random.choice(list(departamentos_collection.aggregate([{"$unwind": "$professores"}, {"$sample": {"size": 1}}])))['professores']
    membros = random.sample(list(alunos_collection.find()), random.randint(2, 4))

    grupos_tcc_collection.insert_one({
        "_id": fake.uuid4(),
        "descricao_grupo": fake.bs(),
        "orientador": {
            "_id": orientador['_id'],
            "nome_professor": orientador['nome_professor'],
            "email_professor": orientador['email_professor']
        },
        "membros": [{"_id": membro['_id'], "nome_aluno": membro['nome_aluno']} for membro in membros ]
        })