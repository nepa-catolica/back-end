from flask import Blueprint, request, jsonify
from ..services.auth_service import AuthService

bp = Blueprint('auth', __name__)

@bp.route('/api/login', methods=['POST'])
def login():
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

    return jsonify(access_token=access_token), 200
@bp.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    role = data.get('role')

    if role == 'aluno':
        try:
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
            return jsonify({"message": "Erro ao registrar aluno", "error": str(e)}), 500

    elif role == 'professor':
        try:
            response = AuthService.create_user_professor(
                nome=data['nome'],
                email=data['email'],
                matricula=data['matricula'],
                curso=data['curso'],
                telefone=data['telefone'],
                password=data['password']
            )
            if 'professor' in response:
                return jsonify({"message": "Professor registrado com sucesso, aguardando aprovação",
                                "professor": response['professor']}), response['status']
            return jsonify(response), response['status']
        except Exception as e:
            return jsonify({"message": "Erro ao registrar professor", "error": str(e)}), 500

    else:
        return jsonify({"message": "Role inválido"}), 400
