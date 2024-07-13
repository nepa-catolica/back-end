import os

from ..models import Projeto
from werkzeug.utils import secure_filename
from flask import current_app
from ..extensions import db


class ProjectService:

    @staticmethod
    def register_project(nome, descricao, professor_id, arquivo_pdf=None):
        projeto = Projeto(nome=nome, descricao=descricao, professor_id=professor_id)

        if arquivo_pdf:
            filename = secure_filename(arquivo_pdf.filename)
            arquivo_pdf.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            projeto.edital_pdf = filename

        db.session.add(projeto)
        db.session.commit()

        return projeto