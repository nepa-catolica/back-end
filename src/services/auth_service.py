import re
from argon2 import PasswordHasher, exceptions
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import SQLAlchemyError
from src.utils.extensions import db
from src.utils.models import Aluno, Professor, Admin

ph = PasswordHasher()


class AuthService:
    @staticmethod
    def is_strong_password(password):
        return len(password) >= 8 and any(c.isdigit() for c in password) and any(c.isalpha() for c in password)

    @staticmethod
    def create_user_aluno(nome, email, matricula, curso, telefone, password):
        try:
            if not AuthService.is_strong_password(password):
                return {'msg': 'Senha fraca. A senha deve conter ao menos 8 caracteres, incluindo letras e números.',
                        'status': 400}

            if Aluno.query.filter_by(email=email).first() or Aluno.query.filter_by(matricula=matricula).first():
                return {'msg': 'Email ou matrícula já cadastrados', 'status': 400}

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

            return {'msg': 'Aluno criado com sucesso', 'aluno': aluno.nome, 'status': 201}

        except SQLAlchemyError as e:
            db.session.rollback()
            return {'msg': f'Erro ao criar aluno no banco de dados: {str(e)}', 'status': 500}

    @staticmethod
    def create_user_professor(nome, email, matricula, curso, telefone, password):
        try:
            if not AuthService.is_strong_password(password):
                return {'msg': 'Senha fraca. A senha deve conter ao menos 8 caracteres, incluindo letras e números.',
                        'status': 400}

            if Professor.query.filter_by(email=email).first() or Professor.query.filter_by(matricula=matricula).first():
                return {'msg': 'Email ou matrícula já cadastrados', 'status': 400}

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

            return {'msg': 'Professor criado com sucesso. Aguardando aprovação.', 'professor': professor.nome, 'status': 201}

        except SQLAlchemyError as e:
            db.session.rollback()
            return {'msg': f'Erro ao criar professor no banco de dados: {str(e)}', 'status': 500}

    @staticmethod
    def create_user_admin(nome, email, password):
        try:
            if not AuthService.is_strong_password(password):
                return {'msg': 'Senha fraca. A senha deve conter ao menos 8 caracteres, incluindo letras e números.',
                        'status': 400}

            if Admin.query.filter_by(email=email).first():
                return {'msg': 'Email já cadastrado', 'status': 400}

            hashed_password = ph.hash(password)

            admin = Admin(
                nome=nome,
                email=email,
                password=hashed_password
            )

            db.session.add(admin)
            db.session.commit()

            return {'msg': 'Administrador criado com sucesso', 'admin': admin.nome, 'status': 201}

        except SQLAlchemyError as e:
            db.session.rollback()
            return {'msg': f'Erro ao criar admin no banco de dados: {str(e)}', 'status': 500}

    @staticmethod
    def checkProfessor(identifier):
        try:
            if identifier.isdigit():
                matricula = int(identifier)
                professor = Professor.query.filter_by(matricula=matricula).first()
            else:
                professor = Professor.query.filter_by(email=identifier).first()

            if professor and not professor.aprovado:
                return professor

            return None
        except SQLAlchemyError as e:
            return {'msg': f'Erro ao acessar o banco de dados: {str(e)}', 'status': 500}

    @staticmethod
    def login(identifier, password):
        try:
            user = AuthService.get_user_by_identifier(identifier)

            if user and AuthService.check_password(user.password, password):
                return AuthService.generate_token(user)

            return {'msg': 'Credenciais inválidas', 'status': 401}

        except SQLAlchemyError as e:
            return {'msg': f'Erro ao acessar o banco de dados: {str(e)}', 'status': 500}
        except exceptions.VerifyMismatchError:
            return {'msg': 'Senha incorreta', 'status': 401}

    @staticmethod
    def get_user_by_identifier(identifier):
        if identifier.isdigit():
            matricula = int(identifier)
            user = Professor.query.filter_by(matricula=matricula).first() or \
                   Aluno.query.filter_by(matricula=matricula).first()
        else:
            user = Admin.query.filter_by(email=identifier).first() or \
                   Professor.query.filter_by(email=identifier).first() or \
                   Aluno.query.filter_by(email=identifier).first()

        return user

    @staticmethod
    def check_password(hashed_password, password):
        try:
            ph.verify(hashed_password, password)
            return True
        except exceptions.VerifyMismatchError:
            return False
        except exceptions.VerificationError:
            return False
        except Exception:
            return False

    @staticmethod
    def generate_token(user):
        identifier_payload = {'email': user.email}
        role = None
        if isinstance(user, Admin):
            role = 'Admin'
        elif isinstance(user, Professor):
            role = 'professor'
            identifier_payload['matricula'] = user.matricula
        elif isinstance(user, Aluno):
            role = 'aluno'
            identifier_payload['matricula'] = user.matricula

        identifier_payload['role'] = role
        access_token = create_access_token(identity=identifier_payload)

        return {'access_token': access_token, 'status': 200}

    # @staticmethod
    # def is_strong_password(password):
    #     return bool(re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$', password))