from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import Professor
from ..services.auth_service import AuthService

bp = Blueprint('admin', __name__)

@bp.route('/api/aprovar/professor/<int:professor_id>', methods=['POST'])
@jwt_required()
def aprovar_professor(professor_id):
    current_user = get_jwt_identity()
    if current_user['role'] != 'admin':
        return jsonify({"message": "Access denied"}), 403

    try:
        professor_aprovado = AuthService.aprovar_professor(professor_id)
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
        professor_rejeitado = AuthService.rejeitar_professor(professor_id)
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
        professor_list = AuthService.listar_professor_pendentes()
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
        professor_list = AuthService.listar_professores_aprovados()
        professores_data = [
            {'Id': prof.id, 'Nome': prof.nome, 'Email': prof.email, 'Matricula': prof.matricula, 'Curso': prof.curso}
            for prof in professor_list]
        return jsonify(professores_data), 200

    except Exception as e:
        return jsonify({"message": "Erro ao listar professores", "error": str(e)}), 400
