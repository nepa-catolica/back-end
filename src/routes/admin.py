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
