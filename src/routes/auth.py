from flask import Blueprint, request, jsonify
from ..services.auth_service import AuthService

bp = Blueprint('auth', __name__)

@bp.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    identifier = data['identifier']
    password = data['password']

    access_token = AuthService.login(identifier, password)
    if access_token:
        return jsonify(access_token=access_token), 200

    return jsonify({"message": "Invalid credentials"}), 401

@bp.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    role = data.get('role')

    if role == 'aluno':
        try:
            novo_aluno = AuthService.create_user_aluno(
                nome=data['nome'],
                email=data['email'],
                matricula=data['matricula'],
                curso=data['curso'],
                telefone=data['telefone'],
                password=data['password']
            )
            return jsonify({"message": "Aluno registrado com sucesso", "aluno": novo_aluno.nome}), 201
        except Exception as e:
            return jsonify({"message": "Erro ao registrar aluno", "error": str(e)}), 400

    elif role == 'professor':
        try:
            novo_professor = AuthService.create_user_professor(
                nome=data['nome'],
                email=data['email'],
                matricula=data['matricula'],
                curso=data['curso'],
                telefone=data['telefone'],
                password=data['password']
            )
            return jsonify({"message": "Professor registrado com sucesso, aguardando aprovação",
                            "professor": novo_professor.nome}), 201
        except Exception as e:
            return jsonify({"message": "Erro ao registrar professor", "error": str(e)}), 400

    else:
        return jsonify({"message": "Role inválido"}), 400
