import os
from werkzeug.utils import secure_filename
from src.utils.extensions import db
from src.utils.models import Professor, Projeto, Edital

class AdminService:

    @staticmethod
    def edital_selecao(nome, descricao, admin_id, arquivo_pdf):
        filename = secure_filename(arquivo_pdf.filename)
        file_path = os.path.join('uploads', filename)  # Define o caminho para salvar o arquivo

        try:
            arquivo_pdf.save(file_path)

            novo_edital = Edital(
                nome=nome,
                descricao=descricao,
                admin_id=admin_id,
                arquivo_pdf=file_path
            )

            db.session.add(novo_edital)
            db.session.commit()

            return novo_edital

        except Exception as e:
            db.session.rollback()
            raise Exception(f"Erro ao criar o edital: {str(e)}")

    @staticmethod
    def aprovar_professor(professor_id):
        professor = Professor.query.get(professor_id)
        if professor:
            professor.aprovado = True
            db.session.commit()
            return professor
        return None

    @staticmethod
    def rejeitar_professor(professor_id):
        professor = Professor.query.get(professor_id)
        if professor:
            professor.aprovado = False
            db.session.commit()
            return professor
        return None

    @staticmethod
    def listar_professor_pendentes():
        return Professor.query.filter_by(aprovado=False).all()

    @staticmethod
    def listar_professores_aprovados():
        return Professor.query.filter_by(aprovado=True).all()

    @staticmethod
    def aprovar_projeto(projeto_id):
        projeto = Projeto.query.get(projeto_id)
        if projeto:
            projeto.aprovado = True
            db.session.commit()
            return projeto
        return None


    @staticmethod
    def rejeitar_projeto(projeto_id):
        projeto = Projeto.query.get(projeto_id)
        if projeto:
            projeto.aprovado = False
            db.session.commit()
            return projeto
        return None