from flask import Blueprint, request, jsonify
from ..services.auth_service import AuthService
import sentry_sdk as sentry

bp = Blueprint('auth', __name__)


@bp.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        identifier = data.get('identifier')
        password = data.get('password')

        if not identifier or not password:
            return jsonify({'message': 'Identifier and password are required'}), 400

        checkProf = AuthService.checkProfessor(identifier)
        if checkProf:
            return jsonify({"message": "Professor account not approved"}), 401

        access_token = AuthService.login(identifier, password)
        if not access_token:
            return jsonify({'message': 'Invalid credentials'}), 401
    except Exception as e:
        sentry.capture_exception(e)
        return jsonify({"message": "Erro no login", "error": str(e)}), 500

    return jsonify(access_token=access_token), 200


@bp.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"message": "Nenhum dado JSON foi enviado ou o formato está inválido."}), 400

        role = data.get('role')

        if role == 'aluno':
            try:
                matricula_str = str(data['matricula'])
                if len(matricula_str) > 15:
                    return jsonify({"message": "Erro ao registrar aluno, matricula possui mais de 15 caracteres."}), 500
                else:
                    response = AuthService.create_user_aluno(
                        nome=data['nome'],
                        email=data['email'],
                        matricula=data['matricula'],
                        curso=data['curso'],
                        telefone=data['telefone'],
                        password=data['password']
                    )
                    return jsonify(response), response['status']
            except Exception as e:
                sentry.capture_exception(e)
                return jsonify({"message": "Erro ao registrar aluno", "error": str(e)}), 500

        elif role == 'professor':
            try:
                response = AuthService.create_user_professor(
                    nome=data['nome'],
                    email=data['email'],
                    codigo_curso=data['codigo_curso'],
                    telefone=data['telefone'],
                    password=data['password']
                )
                if 'professor' in response:
                    return jsonify({"message": "Professor registrado com sucesso, aguardando aprovação",
                                    "professor": response['professor']}), response['status']
                return jsonify(response), response['status']
            except Exception as e:
                sentry.capture_exception(e)
                return jsonify({"message": "Erro ao registrar professor", "error": str(e)}), 500

        else:
            return jsonify({"message": "Role inválido"}), 400
    except Exception as e:
        sentry.capture_exception(e)
        return jsonify({"message": "Erro ao processar o registro", "error": str(e)}), 500