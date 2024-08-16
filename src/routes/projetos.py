from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..models import Professor
from ..models import Projeto

from ..services.project_service import ProjectService

bp = Blueprint('projetos', __name__)

@bp.route('api/create', methods=['POST'])
@jwt_required()
def create_projeto():
    data = request.get_json()
    current_user = get_jwt_identity()

    professor = Professor.query.filter(Professor.email == current_user['email']).first()

    if professor.permissao != 'professor':
        return jsonify({'msg': 'Unauthorized'}), 401

    if not professor or not professor.aprovado:
        return jsonify({'msg': "Acesso negado: Professor não aprovado"}), 403

    nome = data['nome']
    descricao = data['descricao']
    arquivo_pdf = data.get('edital_pdf')

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

@bp.route('/api/listar/projetos_aprovados', methods=['GET'])
@jwt_required()
def list_projects_aprovado():
    try:
        projetos = Projeto.query.filter(Projeto.aprovado == True).all()

        if not projetos:
            return jsonify({'message': 'Não existem projetos aprovados ou estão em processo de aprovação'}), 400

        projetos_data = [{
            'id': projeto.id,
            'nome': projeto.nome,
            'descricao': projeto.descricao,
            'alunos_cadastrados': projeto.alunos_cadastrados,
            'professor': projeto.professor.nome if projeto.professor else None,
            'edital_pdf': projeto.edital_pdf
        } for projeto in projetos]

        return jsonify(projetos_data), 200

    except Exception as e:
        return jsonify({'message': 'Erro ao listar projetos', 'error': str(e)}), 400
