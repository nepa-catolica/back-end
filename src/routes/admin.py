from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.utils.models import Admin, Projeto, Professor
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

@bp.route('/api/professor/<int:professor_id>/detalhes', methods=['GET'])
@jwt_required()
@role_required('admin')
def detalhes_professor(professor_id):
    try:
        professor = Professor.query.filter_by(id=professor_id).first()

        if not professor:
            return jsonify({'message': 'Professor não encontrado'}), 404

        projetos = Projeto.query.filter_by(professor_id=professor_id).all()

        professor_data = {
            'id': professor.id,
            'nome': professor.nome,
            'email': professor.email,
            'matricula': professor.matricula,
            'curso': professor.curso,
            'aprovado': professor.aprovado,
        }

        return jsonify({'professor': professor_data}), 200

    except Exception as e:
        return jsonify({'message': f'Erro ao obter detalhes do professor: {str(e)}'}), 500

@bp.route('/api/projeto/<int:projeto_id>/detalhes', methods=['GET'])
@jwt_required()
@role_required('admin')
def detalhes_projeto(projeto_id):
    try:
        projeto = Projeto.query.filter_by(id=projeto_id).first()

        if not projeto:
            return jsonify({'message': 'Projeto não encontrado'}), 404

        projeto_data = {
            'id': projeto.id,
            'titulo': projeto.titulo,
            'descricao': projeto.descricao,
            'vagas': projeto.vagas,
            'titulacao': projeto.titulacao,
            'curso': projeto.curso,
            'linhaDePesquisa': projeto.linhaDePesquisa,
            'situacao': projeto.situacao,
            'palavrasChave': projeto.palavrasChave,
            'localizacao': projeto.localizacao,
            'populacao': projeto.populacao,
            'justificativa': projeto.justificativa,
            'objetivoGeral': projeto.objetivoGeral,
            'objetivoEspecifico': projeto.objetivoEspecifico,
            'metodologia': projeto.metodologia,
            'cronogramaDeAtividade': projeto.cronogramaDeAtividade,
            'referencias': projeto.referencias,
            'termos': projeto.termos,
            'data_criacao': projeto.data_criacao.strftime('%Y-%m-%d'),
            'aprovado': projeto.aprovado,
            'professor': {
                'id': projeto.professor.id,
                'nome': projeto.professor.nome
            } if projeto.professor else None
        }

        return jsonify({'projeto': projeto_data}), 200

    except Exception as e:
        return jsonify({'message': f'Erro ao obter detalhes do projeto: {str(e)}'}), 500


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
            {'id': prof.id, 'nome': prof.nome, 'email': prof.email, 'matricula': prof.matricula, 'curso': prof.curso}
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
            {'id': prof.id, 'nome': prof.nome, 'email': prof.email, 'matricula': prof.matricula, 'curso': prof.curso}
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


@bp.route('/api/rejeitar/projeto/<int:projeto_id>', methods=['POST'])
@jwt_required()
@role_required('admin')
def rejeitar_projeto(projeto_id):
    current_user = get_jwt_identity()

    if current_user['role'] != 'admin':
        return jsonify({"message": "Access denied"}), 403

    try:
        projeto_rejeitado = AdminService.rejeitar_projeto(projeto_id)

        if projeto_rejeitado:
            return jsonify({
                "message": "Projeto rejeitado com sucesso",
                "projeto": {
                    "id": projeto_rejeitado.id,
                    "titulo": projeto_rejeitado.titulo,
                    "descricao": projeto_rejeitado.descricao,
                    "data_criacao": projeto_rejeitado.data_criacao,
                    "professor_id": projeto_rejeitado.professor_id
                }
            }), 200
        else:
            return jsonify({"message": "Projeto não encontrado"}), 404

    except Exception as e:
        return jsonify({"message": "Erro ao rejeitar o projeto", "error": str(e)}), 400
