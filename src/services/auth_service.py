from argon2 import PasswordHasher, exceptions
from flask_jwt_extended import create_access_token

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
    def checkProfessor(identifier):
        try:
            matricula = int(identifier)
            professor = Professor.query.filter_by(matricula=matricula).first()
        except ValueError:
            professor = Professor.query.filter_by(email=identifier).first()

        if professor and not professor.aprovado:
            return professor

        return None

    @staticmethod
    def login(identifier, password):
        user = None

        if identifier.isdigit():
            matricula = int(identifier)
            user = Professor.query.filter_by(matricula=matricula).first() or \
                   Aluno.query.filter_by(matricula=matricula).first()
        else:
            user = Admin.query.filter_by(email=identifier).first() or \
                   Professor.query.filter_by(email=identifier).first() or \
                   Aluno.query.filter_by(email=identifier).first()

        if user and AuthService.check_password(user.password, password):
            role = None
            if isinstance(user, Admin):
                role = 'Admin'
            elif isinstance(user, Professor):
                role = 'professor'
            elif isinstance(user, Aluno):
                role = 'aluno'

            access_token = create_access_token(identity={'matricula': user.matricula, 'email': user.email, 'role': role})

            return access_token

        return None
    @staticmethod
    def check_password(hashed_password, password):
        try:
            ph.verify(hashed_password, password)
            return True
        except exceptions.VerifyMismatchError:
            return False
