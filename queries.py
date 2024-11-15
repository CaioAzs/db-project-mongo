from pymongo import MongoClient

client = MongoClient('localhost', 27017) #inserir informações de conexão
db = client['BANCO_MONGO'] #nome do banco

alunos_collection = db['alunos']
departamentos_collection = db['departamentos']
grupos_tcc_collection = db['grupos_tcc']

def historico_escolar_aluno(aluno_id):
    historico = alunos_collection.find_one(
        {"_id": aluno_id},
        {"cursos.disciplinas": 1, "_id": 0}
    )
    if historico is None:
        print(f"Nenhum aluno encontrado com o ID: {aluno_id}")
        return

    for curso in historico['cursos']:
        for disciplina in curso['disciplinas']:
            print({
                "codigo_disciplina": disciplina["disciplina"]["_id"],
                "nome_disciplina": disciplina["disciplina"]["nome_disciplina"],
                "semestre": disciplina["semestre"],
                "ano": disciplina["ano"],
                "nota_final": disciplina["nota_final"]
            })

def historico_disciplinas_professor(professor_id):
    result = alunos_collection.aggregate([
        {"$unwind": "$cursos"},
        {"$unwind": "$cursos.disciplinas"},
        {"$match": {"cursos.disciplinas.professor.id_professor": professor_id}},
        {"$project": {
            "disciplina": "$cursos.disciplinas.disciplina.nome_disciplina",
            "semestre": "$cursos.disciplinas.semestre",
            "ano": "$cursos.disciplinas.ano"
        }}
    ])
    for entrada in result:
        print(entrada)

def listar_alunos_formados(ano, semestre):
    result = alunos_collection.aggregate([
        {"$unwind": "$cursos"},
        {"$unwind": "$cursos.disciplinas"},
        {"$match": {
            "cursos.disciplinas.ano": ano,
            "cursos.disciplinas.semestre": semestre,
            "cursos.disciplinas.nota_final": {"$gte": 5.0}  # Considerando nota >= 5 como aprovação
        }},
        {"$group": {
            "_id": "$_id",
            "nome_aluno": {"$first": "$nome_aluno"},
            "total_disciplinas": {"$sum": 1},
            "disciplinas_aprovadas": {"$sum": {"$cond": [{"$gte": ["$cursos.disciplinas.nota_final", 5]}, 1, 0]}}
        }},
        {"$match": {
            "$expr": {"$eq": ["$total_disciplinas", "$disciplinas_aprovadas"]}
        }}
    ])
    for entrada in result:
        print(entrada)

def listar_professores_chefes():
    result = departamentos_collection.find({}, {"chefe": 1, "nome_departamento": 1, "_id": 0})
    for entrada in result:
        print({
            "nome_departamento": entrada["nome_departamento"],
            "chefe_nome": entrada["chefe"]["nome_professor"],
            "chefe_email": entrada["chefe"]["email_professor"]
        })

def listar_grupos_tcc():
    result = grupos_tcc_collection.find({}, {"descricao_grupo": 1, "orientador": 1, "membros": 1, "_id": 0})
    for entrada in result:
        print({
            "orientador_nome": entrada["orientador"]["nome_professor"],
            "membros": [{"nome_aluno": membro["nome_aluno"]} for membro in entrada["membros"]]
        })


print("\n\nQUERY 1 - HISTÓRICO ESCOLAR DE UM ALUNO ESPECÍFICO")
aluno_id = '0ca7246a-87da-4cf0-8443-3e309e77d16f' # Substitua com o ID desejado
historico_escolar_aluno(aluno_id)

print("\n\nQUERY 2 - HISTÓRICO DE DISCIPLINAS DE UM PROFESSOR ESPECÍFICO")
professor_id = '8c5ec654-07c1-4b1b-a8e7-e687806fb9f7'  # Substitua com o ID desejado
historico_disciplinas_professor(professor_id)

print("\n\nQUERY 3 - ALUNOS FORMADOS")
ano = 2023
semestre = 2
listar_alunos_formados(ano, semestre)

print("\n\nQUERY 4 - PROFESSORES CHEFES DE DEPARTAMENTO")
listar_professores_chefes()

print("\n\nQUERY 5 - GRUPOS DE TCC")
listar_grupos_tcc() 
