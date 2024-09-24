from argon2 import PasswordHasher, exceptions
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import SQLAlchemyError
from ..extensions import db
from ..models import Aluno, Professor, Admin

ph = PasswordHasher()

class AuthService:

    @staticmethod
    def create_user_aluno(nome, email, matricula, curso, telefone, password):
        try:
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

        except SQLAlchemyError as e:
            db.session.rollback()
            return {'msg': f'Erro ao criar aluno no banco de dados: {str(e)}', 'status': 500}

        except Exception as e:
            db.session.rollback()
            return {'msg': f'Ocorreu um erro inesperado ao criar aluno: {str(e)}', 'status': 500}

    @staticmethod
    def create_user_admin(nome, email, password):
        try:
            hashed_password = ph.hash(password)
            admin = Admin(
                nome=nome,
                email=email,
                password=hashed_password
            )

            db.session.add(admin)
            db.session.commit()

            return admin

        except SQLAlchemyError as e:
            db.session.rollback()
            return {'msg': f'Erro ao criar admin no banco de dados: {str(e)}', 'status': 500}

        except Exception as e:
            db.session.rollback()
            return {'msg': f'Ocorreu um erro inesperado ao criar admin: {str(e)}', 'status': 500}

    @staticmethod
    def create_user_professor(nome, email, matricula, curso, telefone, password):
        try:
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

        except SQLAlchemyError as e:
            db.session.rollback()
            return {'msg': f'Erro ao criar professor no banco de dados: {str(e)}', 'status': 500}

        except Exception as e:
            db.session.rollback()
            return {'msg': f'Ocorreu um erro inesperado ao criar professor: {str(e)}', 'status': 500}

    @staticmethod
    def checkProfessor(identifier):
        try:
            matricula = int(identifier)
            professor = Professor.query.filter_by(matricula=matricula).first()
        except ValueError:
            professor = Professor.query.filter_by(email=identifier).first()
        except SQLAlchemyError as e:
            return {'msg': f'Erro ao acessar o banco de dados: {str(e)}', 'status': 500}

        if professor and not professor.aprovado:
            return professor

        return None

    @staticmethod
    def login(identifier, password):
        try:
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
                identifier_payload = {'email': user.email}
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

                return access_token

            return {'msg': 'Credenciais inválidas', 'status': 401}

        except SQLAlchemyError as e:
            return {'msg': f'Erro ao acessar o banco de dados: {str(e)}', 'status': 500}

        except exceptions.VerifyMismatchError:
            return {'msg': 'Senha incorreta', 'status': 401}

        except Exception as e:
            return {'msg': f'Ocorreu um erro inesperado durante o login: {str(e)}', 'status': 500}

    @staticmethod
    def check_password(hashed_password, password):
        try:
            ph.verify(hashed_password, password)
            return True
        except exceptions.VerifyMismatchError:
            return False
        except exceptions.VerificationError:
            return False
        except Exception as e:
            return False
