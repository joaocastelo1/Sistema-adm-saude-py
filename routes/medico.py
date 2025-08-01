from flask import Blueprint, request, jsonify
from src.models.user import db
from src.models.medico import Medico

medico_bp = Blueprint('medico', __name__)

@medico_bp.route('/medicos', methods=['GET'])
def listar_medicos():
    try:
        medicos = Medico.query.all()
        return jsonify([medico.to_dict() for medico in medicos]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@medico_bp.route('/medicos/<int:id>', methods=['GET'])
def obter_medico(id):
    try:
        medico = Medico.query.get_or_404(id)
        return jsonify(medico.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@medico_bp.route('/medicos', methods=['POST'])
def criar_medico():
    try:
        data = request.get_json()
        
        # Validação básica
        if not data.get('nome') or not data.get('crm') or not data.get('especialidade'):
            return jsonify({'error': 'Nome, CRM e especialidade são obrigatórios'}), 400
        
        # Verificar se CRM já existe
        if Medico.query.filter_by(crm=data['crm']).first():
            return jsonify({'error': 'CRM já cadastrado'}), 400
        
        medico = Medico(
            nome=data['nome'],
            crm=data['crm'],
            especialidade=data['especialidade'],
            telefone=data.get('telefone'),
            email=data.get('email')
        )
        
        db.session.add(medico)
        db.session.commit()
        
        return jsonify(medico.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@medico_bp.route('/medicos/<int:id>', methods=['PUT'])
def atualizar_medico(id):
    try:
        medico = Medico.query.get_or_404(id)
        data = request.get_json()
        
        # Verificar se CRM já existe em outro médico
        if data.get('crm') and data['crm'] != medico.crm:
            if Medico.query.filter_by(crm=data['crm']).first():
                return jsonify({'error': 'CRM já cadastrado'}), 400
        
        # Atualizar campos
        if data.get('nome'):
            medico.nome = data['nome']
        if data.get('crm'):
            medico.crm = data['crm']
        if data.get('especialidade'):
            medico.especialidade = data['especialidade']
        if 'telefone' in data:
            medico.telefone = data['telefone']
        if 'email' in data:
            medico.email = data['email']
        
        db.session.commit()
        return jsonify(medico.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@medico_bp.route('/medicos/<int:id>', methods=['DELETE'])
def deletar_medico(id):
    try:
        medico = Medico.query.get_or_404(id)
        db.session.delete(medico)
        db.session.commit()
        return jsonify({'message': 'Médico deletado com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@medico_bp.route('/medicos/buscar', methods=['GET'])
def buscar_medicos():
    try:
        termo = request.args.get('q', '')
        if not termo:
            return jsonify([]), 200
        
        medicos = Medico.query.filter(
            Medico.nome.contains(termo) | 
            Medico.crm.contains(termo) |
            Medico.especialidade.contains(termo)
        ).all()
        
        return jsonify([medico.to_dict() for medico in medicos]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@medico_bp.route('/medicos/especialidades', methods=['GET'])
def listar_especialidades():
    try:
        especialidades = db.session.query(Medico.especialidade).distinct().all()
        return jsonify([esp[0] for esp in especialidades]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

