from dotenv import load_dotenv
from flask import Blueprint, jsonify, request, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.utils.models import Admin, Projeto, Professor, Edital
from ..services.admin_service import AdminService
from src.utils.utils import role_required
import os
from uuid import UUID

load_dotenv()

UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads/edital_pdfs/')

bp = Blueprint('admin', __name__)


@bp.route('/api/edital/publicar', methods=['POST'])
@jwt_required()
@role_required('Admin')
def publicar_edital():
    current_user = get_jwt_identity()

    admin = Admin.query.filter(Admin.email == current_user.get('email')).first()
    if not admin:
        return jsonify({"message": "Usuário administrador não encontrado ou sem permissão."}), 403

    if not request.form or not request.files:
        return jsonify({"message": "Dados inválidos. Certifique-se de enviar os campos e o arquivo corretamente."}), 400

    try:
        nome = request.form.get('nome')
        descricao = request.form.get('descricao')
        arquivo_pdf = request.files.get('arquivo')

        if not nome or not descricao or not arquivo_pdf:
            return jsonify({"message": "Nome, descrição e arquivo PDF são obrigatórios."}), 400

        novo_edital = AdminService.edital_selecao(nome, descricao, arquivo_pdf, admin.id)

        return jsonify({
            'message': 'Novo edital registrado e publicado com sucesso.',
            'edital': {
                'id': novo_edital.id,
                'slug': novo_edital.slug,
                'nome': novo_edital.nome,
                'descricao': novo_edital.descricao,
                'data_criacao': novo_edital.data_criacao.strftime('%Y-%m-%d'),
                'arquivo_pdf': novo_edital.arquivo_pdf
            }
        }), 201

    except ValueError as e:
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        return jsonify({"message": "Erro ao criar e publicar o edital.", "error": str(e)}), 500


@bp.route('/api/edital/exibir', methods=['GET'])
@jwt_required()
@role_required(['Admin', 'professor'])
def listar_editais():
    try:
        editais = Edital.query.all()

        if not editais:
            return jsonify({"message": "Nenhum edital encontrado."}), 404

        editais_data = [{
            "id": edital.id,
            "slug": edital.slug,
            "nome": edital.nome,
            "descricao": edital.descricao,
            "data_criacao": edital.data_criacao.strftime('%Y-%m-%d'),
            "arquivo_pdf": edital.arquivo_pdf
        } for edital in editais]

        return jsonify(editais_data), 200

    except Exception as e:
        return jsonify({"message": "Erro ao listar os editais.", "error": str(e)}), 500


@bp.route('/api/edital/exibir/<string:slug>', methods=['GET'])
@jwt_required()
@role_required(['Admin', 'professor'])
def exibir_edital(slug):
    try:
        edital = Edital.query.filter_by(slug=slug).first()

        if not edital:
            return jsonify({"message": "Edital não encontrado."}), 404

        pdf_path = os.path.abspath(os.path.join(UPLOAD_FOLDER, edital.arquivo_pdf))

        if not os.path.exists(pdf_path):
            return jsonify({"message": "Arquivo PDF não encontrado."}), 404

        return send_file(
            pdf_path,
            mimetype='application/pdf',
            as_attachment=False
        )

    except Exception as e:
        return jsonify({"message": "Erro ao exibir o edital.", "error": str(e)}), 500


@bp.route('/api/edital/deletar/<uuid:edital_id>', methods=['DELETE'])
@jwt_required()
@role_required('Admin')
def deletar_edital(edital_id):
    current_user = get_jwt_identity()
    admin = Admin.query.filter_by(email=current_user.get('email')).first()

    if not admin:
        return jsonify({"message": "Administrador não encontrado ou sem permissão."}), 403

    response = AdminService.deletar_edital_by_id(str(edital_id), str(admin.id))
    return jsonify({"message": response['message']}), response['status']


@bp.route('/api/aprovar/professor/<uuid:professor_id>', methods=['POST'])
@jwt_required()
@role_required('Admin')
def aprovar_professor(professor_id):
    try:
        professor_aprovado = AdminService.aprovar_professor(str(professor_id))
        if professor_aprovado:
            return jsonify({"message": "Professor aprovado com sucesso", "professor": professor_aprovado.nome}), 200
        else:
            return jsonify({"message": "Professor não encontrado"}), 404
    except Exception as e:
        return jsonify(
            {"message": "Erro ao aprovar professor", "error": 'Erro interno, tente novamente mais tarde'}), 500


@bp.route('/api/rejeitar/professor/<uuid:professor_id>', methods=['POST'])
@jwt_required()
@role_required('Admin')
def rejeitar_professor(professor_id):
    try:
        professor_rejeitado = AdminService.rejeitar_professor(str(professor_id))
        if professor_rejeitado:
            return jsonify({"message": "Professor rejeitado com sucesso", "professor": professor_rejeitado.nome}), 200
        else:
            return jsonify({"message": "Professor não encontrado"}), 404

    except Exception as e:
        return jsonify(
            {"message": "Erro ao rejeitar professor", "error": 'Erro interno, tente novamente mais tarde'}), 500


@bp.route('/api/professor/<uuid:professor_id>/detalhes', methods=['GET'])
@jwt_required()
@role_required('Admin')
def detalhes_professor(professor_id):
    try:
        professor = Professor.query.filter(Professor.id == str(professor_id)).first()

        if not professor:
            return jsonify({'message': 'Professor não encontrado'}), 404

        projetos = Projeto.query.filter_by(professor_id=str(professor_id)).all()

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


@bp.route('/api/projeto/<uuid:projeto_id>/detalhes', methods=['GET'])
@jwt_required()
@role_required('Admin')
def detalhes_projeto(projeto_id):
    try:
        projeto = Projeto.query.filter(Projeto.id == str(projeto_id)).first()

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
@role_required('Admin')
def listar_professores_pendentes():
    try:
        current_user = get_jwt_identity()
        print(f"JWT Identity: {current_user}")

        professor_list = AdminService.listar_professor_pendentes()
        print(f"Professores Pendentes: {professor_list}")

        if not professor_list:
            return jsonify({"message": "Nenhum professor pendente encontrado."}), 200

        professores_data = [
            {
                'id': str(prof.id),
                'nome': prof.nome,
                'email': prof.email,
                'matricula': prof.matricula,
                'curso': prof.curso
            }
            for prof in professor_list
        ]
        return jsonify(professores_data), 200

    except Exception as e:
        print(f"Erro ao listar professores pendentes: {e}")
        return jsonify({"message": "Erro ao listar professores pendentes", "error": str(e)}), 500


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


@bp.route('/api/aprovar/projeto/<uuid:projeto_id>', methods=['POST'])
@jwt_required()
@role_required('Admin')
def aprovar_projeto(projeto_id):
    current_user = get_jwt_identity()

    if current_user['role'] != 'Admin':
        return jsonify({"message": "Access denied"}), 403

    try:
        projeto_aprovado = AdminService.aprovar_projeto(str(projeto_id))

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
@role_required('Admin')
def rejeitar_projeto(projeto_id):
    current_user = get_jwt_identity()

    if current_user['role'] != 'Admin':
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
