from .extensions import db
from datetime import datetime


class Aluno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), unique=True, nullable=False)
    matricula = db.Column(db.Integer, unique=True, nullable=False)
    curso = db.Column(db.String(255), nullable=False)
    data_ingresso = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    telefone = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    permissao = db.Column(db.String(255), nullable=False, default='Aluno')
    projetos = db.relationship('AlunoProjeto', back_populates='aluno')


class Professor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    matricula = db.Column(db.Integer, unique=True, nullable=False)
    curso = db.Column(db.String(255), nullable=False)
    telefone = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    aprovado = db.Column(db.Boolean, nullable=False, default=False)
    permissao = db.Column(db.String(255), nullable=False, default='Professor')
    projetos_propostos = db.relationship('Projeto', back_populates='proponente')


class Projeto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.String(255), nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    professor_id = db.Column(db.Integer, db.ForeignKey('professor.id'), nullable=False)
    aprovado = db.Column(db.Boolean, default=False, nullable=False)
    alunos_cadastrados = db.relationship('AlunoProjeto', back_populates='projeto')
    proponente = db.relationship('Professor', back_populates='projetos_propostos')
    edital_pdf = db.Column(db.String(255), nullable=True)  # Adicionando campo para armazenar o nome do arquivo PDF



class AlunoProjeto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey('aluno.id'), nullable=False)
    projeto_id = db.Column(db.Integer, db.ForeignKey('projeto.id'), nullable=False)
    aprovado = db.Column(db.Boolean, default=False, nullable=False)
    aluno = db.relationship('Aluno', back_populates='projetos')
    projeto = db.relationship('Projeto', back_populates='alunos_cadastrados')


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    permissao = db.Column(db.String(255), nullable=False, default='Admin')
