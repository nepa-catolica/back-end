import os

from sqlalchemy.exc import SQLAlchemyError
from werkzeug.utils import secure_filename
from src.utils.extensions import db
from dotenv import load_dotenv
from src.utils.models import Professor, Projeto, Edital

load_dotenv()

UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads/edital_pdfs/')
ALLOWED_EXTENSIONS = {'pdf'}
MAX_FILE_SIZE = int(os.getenv('MAX_FILE_SIZE', 5 * 1024 * 1024))


class AdminService:

    @staticmethod
    def is_valid_file(file):
        if '.' not in file.filename:
            return False
        extension = file.filename.rsplit('.', 1)[1].lower()
        return extension in ALLOWED_EXTENSIONS

    @staticmethod
    def edital_selecao(nome, descricao, arquivo_pdf, admin_id):
        if not AdminService.is_valid_file(arquivo_pdf):
            raise ValueError("O arquivo enviado deve ser um PDF válido.")

        arquivo_pdf.seek(0, os.SEEK_END)
        file_size = arquivo_pdf.tell()
        arquivo_pdf.seek(0)

        if file_size > MAX_FILE_SIZE:
            raise ValueError(f"O arquivo PDF excede o limite de {MAX_FILE_SIZE // (1024 * 1024)}MB.")

        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

        filename = secure_filename(arquivo_pdf.filename)
        file_path = os.path.abspath(os.path.join(UPLOAD_FOLDER, filename))
        relative_path = os.path.relpath(file_path, start=UPLOAD_FOLDER)

        arquivo_existente = Edital.query.filter_by(arquivo_pdf=relative_path).first()
        if arquivo_existente:
            raise ValueError("O arquivo PDF já está registrado no sistema.")

        if os.path.exists(file_path):
            raise ValueError("O arquivo PDF já está presente no servidor.")

        try:
            arquivo_pdf.save(file_path)

            new_edital = Edital(
                nome=nome,
                descricao=descricao,
                arquivo_pdf=relative_path,
                admin_id=admin_id
            )
            new_edital.generate_slug()

            db.session.add(new_edital)
            db.session.commit()

            return new_edital

        except FileNotFoundError as e:
            raise Exception(f"Erro ao salvar o arquivo: {str(e)}")

        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"Erro ao salvar o edital no banco de dados: {str(e)}")

        except Exception as e:
            db.session.rollback()
            raise Exception(f"Erro inesperado: {str(e)}")

    @staticmethod
    def deletar_edital_by_id(edital_id, admin_id):
        try:
            edital = Edital.query.filter_by(id=edital_id).first()

            if not edital:
                return {'message': 'Edital não encontrado.', 'status': 404}

            if edital.admin_id != admin_id:
                return {'message': 'Você não tem permissão para deletar este edital.', 'status': 403}

            pdf_path = os.path.abspath(os.path.join(UPLOAD_FOLDER, edital.arquivo_pdf))
            if os.path.exists(pdf_path):
                os.remove(pdf_path)

            db.session.delete(edital)
            db.session.commit()

            return {'message': 'Edital deletado com sucesso.', 'status': 200}

        except SQLAlchemyError as e:
            db.session.rollback()
            return {'message': f'Erro ao deletar o edital no banco de dados: {str(e)}', 'status': 500}

        except Exception as e:
            return {'message': f'Erro inesperado: {str(e)}', 'status': 500}

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
