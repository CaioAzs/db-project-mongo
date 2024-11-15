# Projeto 1 de Banco de Dados - MongoDB
---
Caio de Souza Conceição - RA: 22.122.033-8
Lucas Dias Batista - RA: 22.122.065-0
---
## Estrutura do Banco de Dados

O banco de dados contém as seguintes coleções:

- **departamentos**: Armazena informações sobre departamentos acadêmicos, incluindo cursos e professores.
- **alunos**: Contém dados sobre os alunos, incluindo cursos, disciplinas e notas.
- **grupos_tcc**: Registra os grupos de TCC, com os membros e orientadores.

## Funcionalidades

**Consultas**:
   - **Histórico Escolar de um Aluno**: Retorna as disciplinas e notas de um aluno específico.
   - **Histórico de Disciplinas de um Professor**: Retorna as disciplinas lecionadas por um professor, incluindo o ano e semestre.
   - **Alunos Formados**: Lista os alunos que concluíram todas as disciplinas e possuem nota final maior ou igual a 5.
   - **Professores Chefes de Departamento**: Exibe os professores que são chefes de cada departamento.
   - **Grupos de TCC**: Lista os grupos de TCC com seus membros e orientador.

## Dependências

- **Faker**: Biblioteca para geração de dados falsos.
- **pymongo**: Cliente Python para interação com o MongoDB.

2. Configure a conexão com o MongoDB no script `mongo_client` com suas credenciais.

## Exemplo de Execução

Após configurar o MongoDB, execute o arquivo `main.py` ajustando as informações de conexäo com o banco no começo do arquivo.
Após a geração das coleções, execute o arquivo `queries.py`. Exemplo de saída:

```bash
QUERY 1 - HISTÓRICO ESCOLAR DE UM ALUNO ESPECÍFICO
{
  "codigo_disciplina": "12345",
  "nome_disciplina": "Cálculo Diferencial e Integral",
  "semestre": 1,
  "ano": 2021,
  "nota_final": 7.5
}

QUERY 2 - HISTÓRICO DE DISCIPLINAS DE UM PROFESSOR ESPECÍFICO
{
  "disciplina": "Física para Engenharia",
  "semestre": 2,
  "ano": 2022
}

QUERY 3 - ALUNOS FORMADOS
{
  "_id": "123456789",
  "nome_aluno": "nome",
  "total_disciplinas": 10,
  "disciplinas_aprovadas": 10
}

QUERY 4 - PROFESSORES CHEFES DE DEPARTAMENTO
{
  "nome_departamento": "Ciência da Computação",
  "chefe_nome": "Prof. 2",
  "chefe_email": "a@email.com"
}

QUERY 5 - GRUPOS DE TCC
{
  "orientador_nome": "Prof. 1",
  "membros": [{"nome_aluno": "nome"}, {"nome_aluno": "nome"}]
}
```
