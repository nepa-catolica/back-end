from marshmallow import Schema, fields, validate
from marshmallow import post_dump

from src.utils.extensions import ma
from src.utils.models import Professor, Aluno

class ProjetoSchema(Schema):
    vagas = fields.Integer(required=True, validate=validate.Range(min=1, error="O número de vagas deve ser ao menos 1"))
    titulacao = fields.String(required=True, validate=validate.Length(min=1, error="Titulação é obrigatória"))
    curso = fields.String(required=True, validate=validate.Length(min=1, error="Curso é obrigatório"))
    titulo = fields.String(required=True, validate=validate.Length(min=1, error="Título é obrigatório"))
    linhaDePesquisa = fields.String(required=True, validate=validate.Length(min=1, error="Linha de pesquisa é obrigatória"))
    situacao = fields.String(required=True, validate=validate.Length(min=1, error="Situação é obrigatória"))
    descricao = fields.String(required=True, validate=validate.Length(min=1, error="Descrição é obrigatória"))
    palavrasChave = fields.String(required=True, validate=validate.Length(min=1, error="Palavras-chave são obrigatórias"))
    localizacao = fields.String(required=True, validate=validate.Length(min=1, error="Localização é obrigatória"))
    populacao = fields.String(required=True, validate=validate.Length(min=1, error="População é obrigatória"))
    justificativa = fields.String(required=True, validate=validate.Length(min=1, error="Justificativa é obrigatória"))
    objetivoGeral = fields.String(required=True, validate=validate.Length(min=1, error="Objetivo geral é obrigatório"))
    objetivoEspecifico = fields.String(required=True, validate=validate.Length(min=1, error="Objetivo específico é obrigatório"))
    metodologia = fields.String(required=True, validate=validate.Length(min=1, error="Metodologia é obrigatória"))
    cronogramaDeAtividade = fields.String(required=True, validate=validate.Length(min=1, error="Cronograma de atividades é obrigatório"))
    referencias = fields.String(required=True, validate=validate.Length(min=1, error="Referências são obrigatórias"))
    termos = fields.Boolean(required=True, error_messages={"required": "É necessário aceitar os termos"})

class AlunoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Aluno
        load_instance = True

class ProfessorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Professor
        load_instance = True


class AlunoProjetoFullSchema(Schema):
    id = fields.UUID(attribute='aluno.id')
    nome = fields.String(attribute='aluno.nome')
    email = fields.Email(attribute='aluno.email')
    curso = fields.String(attribute='aluno.curso')
    aprovado = fields.Boolean()
    reprovado = fields.Boolean()

aluno_schema: Schema = AlunoSchema()
professor_schema: Schema = ProfessorSchema()