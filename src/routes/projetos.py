from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError
from src.utils.models import Professor, Projeto
from ..services.project_service import ProjetoService
from src.utils.schemas import ProjetoSchema

bp = Blueprint('projetos', __name__)

@bp.route('/api/create', methods=['POST'])
@jwt_required()
def create_projeto():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'message': 'Nenhum dado foi fornecido'}), 400

        current_user = get_jwt_identity()
        professor = Professor.query.filter(Professor.email == current_user['email']).first()

        if not professor or professor.permissao != 'professor' or not professor.aprovado:
            return jsonify({'message': 'Unauthorized'}), 401

        schema = ProjetoSchema()
        errors = schema.validate(data)
        if errors:
            return jsonify(errors), 400

        response = ProjetoService.register_projeto(professor.id, **data)
        return jsonify({'message': response['msg']}), response['status']

    except Exception as e:
        return jsonify({'message': f'Ocorreu um erro inesperado: {str(e)}'}), 500


@bp.route('/api/listar/projetos_aprovados', methods=['GET'])
@jwt_required()
def list_projects_aprovado():
    try:
        projetos = Projeto.query.filter(Projeto.aprovado == True).all()

        if not projetos:
            return jsonify({'message': 'Não existem projetos aprovados ou estão em processo de aprovação'}), 404

        projetos_data = [{
            'id': projeto.id,
            'nome': projeto.nome,
            'descricao': projeto.descricao,
            'alunos_cadastrados': projeto.alunos_cadastrados,
            'professor': projeto.professor.nome if projeto.professor else None,
            'edital_pdf': projeto.edital_pdf
        } for projeto in projetos]

        return jsonify(projetos_data), 200

    except SQLAlchemyError as e:
        return jsonify({'message': 'Erro ao acessar o banco de dados', 'error': str(e)}), 500

    except Exception as e:
        return jsonify({'message': f'Ocorreu um erro inesperado: {str(e)}'}), 500

@bp.route('/api/editar/projeto', methods=['PUT'])
@jwt_required()
def editar_projeto():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'msg': 'Nenhum dado foi fornecido'}), 400

        current_user = get_jwt_identity()
        projeto_id = data.get('projeto_id')
        if not projeto_id:
            return jsonify({'msg': 'O ID do projeto é obrigatório'}), 400

        campos_obrigatorios = ['vagas','titulacao', 'curso', 'titulo', 'linhaDePesquisa', 'situacao', 'descricao',
                               'palavrasChave', 'localizacao', 'populacao', 'justificativa', 'objetivoGeral',
                               'objetivoEspecifico', 'metodologia', 'cronogramaDeAtividade', 'referencias', 'termos']

        for campo in campos_obrigatorios:
            if not data.get(campo):
                return jsonify({'msg': f'O campo "{campo}" é obrigatório e não pode estar vazio'}), 400

        response = ProjetoService.edit_projeto(
            user_email=current_user['email'],
            projeto_id=projeto_id,
            vagas=data.get('vagas'),
            titulacao=data.get('titulacao'),
            curso=data.get('curso'),
            titulo=data.get('titulo'),
            linhaDePesquisa=data.get('linhaDePesquisa'),
            situacao=data.get('situacao'),
            descricao=data.get('descricao'),
            palavrasChave=data.get('palavrasChave'),
            localizacao=data.get('localizacao'),
            populacao=data.get('populacao'),
            justificativa=data.get('justificativa'),
            objetivoGeral=data.get('objetivoGeral'),
            objetivoEspecifico=data.get('objetivoEspecifico'),
            metodologia=data.get('metodologia'),
            cronogramaDeAtividade=data.get('cronogramaDeAtividade'),
            referencias=data.get('referencias'),
            termos=data.get('termos')
        )

        return jsonify({'msg': response['msg']}), response['status']

    except KeyError as e:
        return jsonify({'msg': f'Campo obrigatório ausente: {str(e)}'}), 400

    except ValueError as e:
        return jsonify({'msg': f'Valor inválido: {str(e)}'}), 400

    except Exception as e:
        return jsonify({'msg': f'Ocorreu um erro inesperado: {str(e)}'}), 500
