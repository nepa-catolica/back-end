from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.utils.models import Admin
from ..services.admin_service import AdminService
from src.utils.utils import role_required

bp = Blueprint('admin', __name__)

@bp.route('/api/publicar/edital', methods=['POST'])
@jwt_required
@role_required('admin')
def publicar_edital():
    current_user = get_jwt_identity()
    admin = Admin.query.filter(Admin.id == current_user['id']).first()

    nome = request.json.get('nome')
    descricao = request.json.get('descricao')
    arquivo_pdf = request.json.get('edital_pdf')

    if not nome or not descricao or not arquivo_pdf:
        return jsonify({"message": "Nome, descricao e arquivo pdf são obrigatórios."}), 400

    try:
        novo_edital = AdminService.edital_selecao(nome, descricao, admin.id, arquivo_pdf)
        return jsonify({'message': 'Novo edital registrado e publicado com sucesso', 'edital': {
            'id': novo_edital.id,
            'nome': novo_edital.nome,
            'descricao': novo_edital.descricao,
            'data_criacao': novo_edital.data_criacao,
            'arquivo_pdf': novo_edital.arquivo_pdf
        }})

    except Exception as e:
        return jsonify({'message': 'Erro ao criar e publicar o edital.', 'error': 'Erro interno, tente novamente mais tarde'}), 500

@bp.route('/api/aprovar/professor/<int:professor_id>', methods=['POST'])
@jwt_required()
@role_required('admin')
def aprovar_professor(professor_id):
    try:
        professor_aprovado = AdminService.aprovar_professor(professor_id)
        if professor_aprovado:
            return jsonify({"message": "Professor aprovado com sucesso", "professor": professor_aprovado.nome}), 200
        else:
            return jsonify({"message": "Professor não encontrado"}), 404
    except Exception as e:
        return jsonify({"message": "Erro ao aprovar professor", "error": 'Erro interno, tente novamente mais tarde'}), 500

@bp.route('/api/rejeitar/professor/<int:professor_id>', methods=['POST'])
@jwt_required()
@role_required('admin')
def rejeitar_professor(professor_id):
    try:
        professor_rejeitado = AdminService.rejeitar_professor(professor_id)
        if professor_rejeitado:
            return jsonify({"message": "Professor rejeitado com sucesso", "professor": professor_rejeitado.nome}), 200
        else:
            return jsonify({"message": "Professor não encontrado"}), 404

    except Exception as e:
        return jsonify({"message": "Erro ao rejeitar professor", "error": 'Erro interno, tente novamente mais tarde'}), 500



@bp.route('/api/lista/professores-pendentes', methods=['GET'])
@jwt_required()
@role_required('admin')
def listar_professores_pendentes():
    current_user = get_jwt_identity()
    if current_user['role'] != 'admin':
        return jsonify({"message": "Access denied"}), 403

    try:
        professor_list = AdminService.listar_professor_pendentes()
        professores_data = [
            {'Id': prof.id, 'Nome': prof.nome, 'Email': prof.email, 'Matricula': prof.matricula, 'Curso': prof.curso}
            for prof in professor_list]
        return jsonify(professores_data), 200

    except Exception as e:
        return jsonify({"message": "Erro ao listar professores", "error": str(e)}), 400


@bp.route('/api/lista/professores-aprovados', methods=['GET'])
@jwt_required()
@role_required('Admin')
def listar_professores_aprovados():
    current_user = get_jwt_identity()
    if current_user['role'] != 'Admin':
        return jsonify({"message": "Access denied"}), 403

    try:
        professor_list = AdminService.listar_professores_aprovados()
        professores_data = [
            {'Id': prof.id, 'Nome': prof.nome, 'Email': prof.email, 'Matricula': prof.matricula, 'Curso': prof.curso}
            for prof in professor_list]
        return jsonify(professores_data), 200

    except Exception as e:
        return jsonify({"message": "Erro ao listar professores", "error": str(e)}), 400


@bp.route('/api/aprovar/projeto/<int:projeto_id>', methods=['POST'])
@jwt_required()
@role_required('admin')
def aprovar_projeto(projeto_id):
    current_user = get_jwt_identity()

    if current_user['role'] != 'admin':
        return jsonify({"message": "Access denied"}), 403

    try:
        projeto_aprovado = AdminService.aprovar_projeto(projeto_id)

        if projeto_aprovado:
            return jsonify({
                "message": "Projeto aprovado com sucesso",
                "projeto": {
                    "id": projeto_aprovado.id,
                    "titulo": projeto_aprovado.titulo,
                    "descricao": projeto_aprovado.descricao,
                    "data_criacao": projeto_aprovado.data_criacao,
                    "professor_id": projeto_aprovado.professor_id
                }
            }), 200
        else:
            return jsonify({"message": "Projeto não encontrado"}), 404
    except Exception as e:
        return jsonify({"message": "Erro ao aprovar o projeto", "error": str(e)}), 400


@bp.route('/api/aprovar/projeto/professor/<int:professor_id>', methods=['POST'])
@jwt_required()
@role_required('admin')
def aprovar_projeto_por_professor(professor_id):
    current_user = get_jwt_identity()

    if current_user['role'] != 'admin':
        return jsonify({"message": "Access denied"}), 403

    try:
        projeto_aprovado = AdminService.aprovar_projeto_por_professor(professor_id)

        if projeto_aprovado:
            return jsonify({
                "message": "Projeto aprovado com sucesso",
                "projeto": {
                    "professor": projeto_aprovado.professor.nome,
                    "titulo": projeto_aprovado.titulo,
                    "descricao": projeto_aprovado.descricao
                }
            }), 200
        else:
            return jsonify({"message": "Nenhum projeto pendente para este professor ou professor não encontrado"}), 404
    except Exception as e:
        return jsonify({"message": "Erro ao aprovar o projeto", "error": str(e)}), 400
