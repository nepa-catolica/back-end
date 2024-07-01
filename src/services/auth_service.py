from argon2 import PasswordHasher, exceptions
from flask_jwt_extended import create_access_token
from sqlalchemy import or_

from ..extensions import db
from ..models import Aluno, Professor, Admin

ph = PasswordHasher()

class AuthService:

    @staticmethod
    def create_user_aluno(nome, email, matricula, curso, telefone, password):
        hashed_password = ph.hash(password)
        aluno = Aluno(
            nome=nome,
            email=email,
            matricula=matricula,
            curso=curso,
            telefone=telefone,
            password=hashed_password
        )

        db.session.add(aluno)
        db.session.commit()

        return aluno

    @staticmethod
    def create_user_admin(nome, email, password):
        hashed_password = ph.hash(password)
        admin = Admin(
            nome=nome,
            email=email,
            password=hashed_password
        )

        db.session.add(admin)
        db.session.commit()

        return admin

    @staticmethod
    def create_user_professor(nome, email, matricula, curso, telefone, password):
        hashed_password = ph.hash(password)
        professor = Professor(
            nome=nome,
            email=email,
            matricula=matricula,
            curso=curso,
            telefone=telefone,
            password=hashed_password
        )

        db.session.add(professor)
        db.session.commit()

        return professor

    @staticmethod
    def aprovar_professor(professor_id):
        professor = Professor.query.get(professor_id)

        if professor:
            professor.aprovado = True
            db.session.commit()
            return professor

        return None

    @staticmethod
    def login(identifier, password):
        user = Admin.query.filter(
            or_(Admin.email == identifier, Admin.matricula == identifier)
        ).first() or Professor.query.filter(
            or_(Professor.email == identifier, Professor.matricula == identifier)
        ).first() or Aluno.query.filter(
            or_(Aluno.email == identifier, Aluno.matricula == identifier)
        ).first()

        if user and AuthService.check_password(user.password, password):
            access_token = create_access_token(identity={'email': user.email, 'role': user.permissao})
            return access_token
        return None

    @staticmethod
    def check_password(hashed_password, password):
        try:
            ph.verify(hashed_password, password)
            return True
        except exceptions.VerifyMismatchError:
            return False
