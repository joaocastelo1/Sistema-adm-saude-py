from flask import Blueprint, request, jsonify
from src.models.user import db
from src.models.paciente import Paciente
from datetime import datetime

paciente_bp = Blueprint('paciente', __name__)

@paciente_bp.route('/pacientes', methods=['GET'])
def listar_pacientes():
    try:
        pacientes = Paciente.query.all()
        return jsonify([paciente.to_dict() for paciente in pacientes]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@paciente_bp.route('/pacientes/<int:id>', methods=['GET'])
def obter_paciente(id):
    try:
        paciente = Paciente.query.get_or_404(id)
        return jsonify(paciente.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@paciente_bp.route('/pacientes', methods=['POST'])
def criar_paciente():
    try:
        data = request.get_json()
        
        # Validação básica
        if not data.get('nome') or not data.get('cpf') or not data.get('data_nascimento'):
            return jsonify({'error': 'Nome, CPF e data de nascimento são obrigatórios'}), 400
        
        # Verificar se CPF já existe
        if Paciente.query.filter_by(cpf=data['cpf']).first():
            return jsonify({'error': 'CPF já cadastrado'}), 400
        
        # Converter data de nascimento
        data_nascimento = datetime.strptime(data['data_nascimento'], '%Y-%m-%d').date()
        
        paciente = Paciente(
            nome=data['nome'],
            data_nascimento=data_nascimento,
            cpf=data['cpf'],
            endereco=data.get('endereco'),
            telefone=data.get('telefone'),
            email=data.get('email')
        )
        
        db.session.add(paciente)
        db.session.commit()
        
        return jsonify(paciente.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@paciente_bp.route('/pacientes/<int:id>', methods=['PUT'])
def atualizar_paciente(id):
    try:
        paciente = Paciente.query.get_or_404(id)
        data = request.get_json()
        
        # Verificar se CPF já existe em outro paciente
        if data.get('cpf') and data['cpf'] != paciente.cpf:
            if Paciente.query.filter_by(cpf=data['cpf']).first():
                return jsonify({'error': 'CPF já cadastrado'}), 400
        
        # Atualizar campos
        if data.get('nome'):
            paciente.nome = data['nome']
        if data.get('data_nascimento'):
            paciente.data_nascimento = datetime.strptime(data['data_nascimento'], '%Y-%m-%d').date()
        if data.get('cpf'):
            paciente.cpf = data['cpf']
        if 'endereco' in data:
            paciente.endereco = data['endereco']
        if 'telefone' in data:
            paciente.telefone = data['telefone']
        if 'email' in data:
            paciente.email = data['email']
        
        db.session.commit()
        return jsonify(paciente.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@paciente_bp.route('/pacientes/<int:id>', methods=['DELETE'])
def deletar_paciente(id):
    try:
        paciente = Paciente.query.get_or_404(id)
        db.session.delete(paciente)
        db.session.commit()
        return jsonify({'message': 'Paciente deletado com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@paciente_bp.route('/pacientes/buscar', methods=['GET'])
def buscar_pacientes():
    try:
        termo = request.args.get('q', '')
        if not termo:
            return jsonify([]), 200
        
        pacientes = Paciente.query.filter(
            Paciente.nome.contains(termo) | 
            Paciente.cpf.contains(termo)
        ).all()
        
        return jsonify([paciente.to_dict() for paciente in pacientes]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

