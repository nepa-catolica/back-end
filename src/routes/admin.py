from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import Admin
from ..services.admin_service import AdminService

bp = Blueprint('admin', __name__)

@bp.route('/api/publicar/edital', methods=['POST'])
@jwt_required
def publicar_edital():
    current_user = get_jwt_identity()
    if current_user['role'] != 'admin':
        return jsonify({'msg': 'Unauthorized'}), 401

    admin = Admin.query.filter(Admin.id == current_user['id']).first()

    nome = request.json.get('nome')
    descricao = request.json.get('descricao')
    arquivo_pdf = request.json.get('edital_pdf')

    if not nome or not descricao or not arquivo_pdf:
        return jsonify({"msg": "Nome, descricao e arquivo pdf são obrigatórios."}), 400

    try:
        novo_edital = AdminService.edital_selecao(nome, descricao, admin.id,arquivo_pdf)
        return jsonify({'msg': 'Novo edital registrado e publicado com sucesso', 'edital': {
            'id': novo_edital.id,
            'nome': novo_edital.nome,
            'descricao': novo_edital.descricao,
            'data_criacao': novo_edital.data_criacao,
            'arquivo_pdf': novo_edital.arquivo_pdf
        }})

    except Exception as e:
        return jsonify({'msg': 'Erro ao criar e publicar o edital.', 'error': str(e)}), 400



@bp.route('/api/aprovar/professor/<int:professor_id>', methods=['POST'])
@jwt_required()
def aprovar_professor(professor_id):
    current_user = get_jwt_identity()
    if current_user['role'] != 'admin':
        return jsonify({"message": "Access denied"}), 403

    try:
        professor_aprovado = AdminService.aprovar_professor(professor_id)
        if professor_aprovado:
            return jsonify({"message": "Professor aprovado com sucesso", "professor": professor_aprovado.nome}), 200
        else:
            return jsonify({"message": "Professor não encontrado"}), 404
    except Exception as e:
        return jsonify({"message": "Erro ao aprovar professor", "error": str(e)}), 400

@bp.route('/api/rejeitar/professor/<int:professor_id>', methods=['POST'])
@jwt_required()
def rejeitar_professor(professor_id):
    current_user = get_jwt_identity()
    if current_user['role'] != 'admin':
        return jsonify({"message": "Access denied"}), 403
    try:
        professor_rejeitado = AdminService.rejeitar_professor(professor_id)
        if professor_rejeitado:
            return jsonify({"message": "Professor rejeitado com sucesso", "professor": professor_rejeitado.nome}), 200

        else:
            return jsonify({"message": "Professor não encontrado"}), 404

    except Exception as e:
        return jsonify({"message": "Erro ao rejeitar professor", "error": str(e)}), 400

@bp.route('/api/lista/professores-pendentes', methods=['GET'])
@jwt_required()
def listar_professores_pendentes():
    current_user = get_jwt_identity()
    if current_user['role'] != 'admin':
        return jsonify({"message": "Access denied"}), 403

    try:
        professor_list = AdminService.listar_professor_pendentes()
        professores_data = [{'Id': prof.id, 'Nome': prof.nome, 'Email': prof.email, 'Matricula': prof.matricula, 'Curso': prof.curso} for prof in professor_list]
        return jsonify(professores_data), 200

    except Exception as e:
        return jsonify({"message": "Erro ao listar professores", "error": str(e)}), 400

@bp.route('/api/lista/professores-aprovados', methods=['GET'])
@jwt_required()
def listar_professores_aprovados():
    current_user = get_jwt_identity()
    if current_user['role'] != 'admin':
        return jsonify({"message": "Access denied"}), 403

    try:
        professor_list = AdminService.listar_professores_aprovados()
        professores_data = [
            {'Id': prof.id, 'Nome': prof.nome, 'Email': prof.email, 'Matricula': prof.matricula, 'Curso': prof.curso}
            for prof in professor_list]
        return jsonify(professores_data), 200

    except Exception as e:
        return jsonify({"message": "Erro ao listar professores", "error": str(e)}), 400
