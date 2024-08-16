import os

from flask import current_app
from werkzeug.utils import secure_filename

from ..extensions import db
from ..models import Edital, Professor, Admin


class AdminService:

    @staticmethod
    def edital_selecao(nome, descricao, admin_id, arquivo_pdf=None):
        edital = Edital(nome=nome, descricao=descricao, admin_id=admin_id)

        if arquivo_pdf:
            filename = secure_filename(arquivo_pdf.filename)
            arquivo_pdf.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            edital.edital_pdf = filename

        db.session.add(edital)
        db.session.commit()

        return edital

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
        professors = Professor.query.filter(Professor.aprovado==False).all()
        return professors

    @staticmethod
    def listar_professores_aprovados():
        professors = Professor.query.filter(Professor.aprovado==True).all()
        return professors
