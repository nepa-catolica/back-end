from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..models import Professor
from ..services.project_service import ProjectService

bp = Blueprint('projetos', __name__)

@bp.route('/api/create', methods=['POST'])
@jwt_required()
def create_projeto():
    current_user = get_jwt_identity()
    if current_user['role'] != 'professor':
        return jsonify({'msg': 'Unauthorized'}), 401

    professor = Professor.query.filter(Professor.id == current_user['id']).first()
    if not professor or not professor.aprovado:
        return jsonify({'msg': "Acesso negado: Professor não aprovado"}), 403

    nome = request.json.get('nome')
    descricao = request.json.get('descricao')
    arquivo_pdf = request.json.get('edital_pdf')

    if not nome or not descricao:
        return jsonify({"message": "Nome e descrição são obrigatórios"}), 400

    try:
        novo_projeto = ProjectService.register_project(nome, descricao, professor.id, arquivo_pdf)
        return jsonify({'msg': 'Projeto registrado com sucesso', 'projeto': {
            'id': novo_projeto.id,
            'nome': novo_projeto.nome,
            'descricao': novo_projeto.descricao,
            'data_criacao': novo_projeto.data_criacao,
            'edital_pdf': novo_projeto.edital_pdf,
        }}), 201

    except Exception as e:
        return jsonify({"message": "Erro ao criar projeto", "error": str(e)}), 400
