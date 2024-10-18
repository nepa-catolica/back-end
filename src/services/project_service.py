from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from src.utils.models import Projeto, Professor, Aluno, AlunoProjeto
from src.utils.extensions import db

class ProjetoService:

    @staticmethod
    def register_aluno_projeto(matricula, projeto_id):
        # Busca o aluno pela matrícula
        aluno = Aluno.query.filter_by(matricula=matricula).first()

        if not aluno:
            return {'msg': 'Aluno não encontrado'}, 404

        # Busca o projeto pelo ID
        projeto = Projeto.query.filter_by(id=projeto_id).first()

        if not projeto:
            return {'msg': 'Projeto não encontrado'}, 404

        # Verifica se o aluno já está cadastrado no projeto
        aluno_projeto = AlunoProjeto.query.filter_by(aluno_id=aluno.id, projeto_id=projeto.id).first()

        if aluno_projeto:
            return {'msg': 'Aluno já está cadastrado neste projeto'}, 400

        # Cadastrar o aluno no projeto
        cadastro_aluno_projeto = AlunoProjeto(aluno_id=aluno.id, projeto_id=projeto.id)

        db.session.add(cadastro_aluno_projeto)
        db.session.commit()

        return {'msg': 'Aluno cadastrado com sucesso no projeto', 'aluno_projeto': {
            'aluno_id': cadastro_aluno_projeto.aluno_id,
            'projeto_id': cadastro_aluno_projeto.projeto_id
        }}, 201

    @staticmethod
    def register_projeto(professor_id, vagas, titulacao, curso, titulo, linhaDePesquisa, situacao, descricao, palavrasChave,
                         localizacao, populacao, justificativa, objetivoGeral, objetivoEspecifico, metodologia,
                         cronogramaDeAtividade, referencias, termos):
        try:
            projeto = Projeto(
                professor_id=professor_id,
                vagas = vagas,
                titulacao=titulacao,
                curso=curso,
                titulo=titulo,
                linhaDePesquisa=linhaDePesquisa,
                situacao=situacao,
                descricao=descricao,
                palavrasChave=palavrasChave,
                localizacao=localizacao,
                populacao=populacao,
                justificativa=justificativa,
                objetivoGeral=objetivoGeral,
                objetivoEspecifico=objetivoEspecifico,
                metodologia=metodologia,
                cronogramaDeAtividade=cronogramaDeAtividade,
                referencias=referencias,
                termos=termos
            )

            projeto.set_data_limite_edicao()

            db.session.add(projeto)
            db.session.commit()

            return {'msg': 'Projeto registrado com sucesso', 'status': 201, 'projeto': projeto}

        except SQLAlchemyError as e:
            db.session.rollback()
            return {'msg': f'Erro ao registrar projeto no banco de dados: {str(e)}', 'status': 500}

    @staticmethod
    def edit_projeto(user_email, projeto_id, vagas, titulacao, curso, titulo, linhaDePesquisa, situacao, descricao,
                     palavrasChave, localizacao, populacao, justificativa, objetivoGeral, objetivoEspecifico,
                     metodologia, cronogramaDeAtividade, referencias, termos):
        try:
            professor = Professor.query.filter(Professor.email == user_email).first()
            if not professor or professor.permissao != 'professor' or not professor.aprovado:
                return {'msg': 'Unauthorized'}, 401

            projeto = Projeto.query.filter_by(id=projeto_id, professor_id=professor.id).first()
            if not projeto:
                return {'msg': 'Projeto não encontrado ou você não tem permissão para editá-lo'}, 404

            if projeto.data_limite_edicao and datetime.utcnow() > projeto.data_limite_edicao:
                if not projeto.aprovado:
                    return {'msg': 'O período para editar este projeto expirou'}, 403
                else:
                    return {'msg': 'Este projeto já foi aprovado e não pode mais ser editado'}, 403

            projeto.vagas = vagas
            projeto.titulacao = titulacao
            projeto.curso = curso
            projeto.titulo = titulo
            projeto.linhaDePesquisa = linhaDePesquisa
            projeto.situacao = situacao
            projeto.descricao = descricao
            projeto.palavrasChave = palavrasChave
            projeto.localizacao = localizacao
            projeto.populacao = populacao
            projeto.justificativa = justificativa
            projeto.objetivoGeral = objetivoGeral
            projeto.objetivoEspecifico = objetivoEspecifico
            projeto.metodologia = metodologia
            projeto.cronogramaDeAtividade = cronogramaDeAtividade
            projeto.referencias = referencias
            projeto.termos = termos

            db.session.commit()

            return {'msg': 'Projeto atualizado com sucesso', 'status': 200}

        except SQLAlchemyError as e:
            db.session.rollback()
            return {'msg': f'Erro ao acessar o banco de dados: {str(e)}', 'status': 500}

        except Exception as e:
            db.session.rollback()
            return {'msg': f'Ocorreu um erro inesperado ao editar o projeto: {str(e)}', 'status': 500}
