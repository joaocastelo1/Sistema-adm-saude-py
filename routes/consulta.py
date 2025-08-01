from flask import Blueprint, request, jsonify
from src.models.user import db
from src.models.consulta import Consulta
from src.models.paciente import Paciente
from src.models.medico import Medico
from datetime import datetime
from sqlalchemy import and_, or_

consulta_bp = Blueprint('consulta', __name__)

@consulta_bp.route('/consultas', methods=['GET'])
def listar_consultas():
    try:
        # Parâmetros de filtro
        data_inicio = request.args.get('data_inicio')
        data_fim = request.args.get('data_fim')
        medico_id = request.args.get('medico_id')
        paciente_id = request.args.get('paciente_id')
        status = request.args.get('status')
        
        query = Consulta.query
        
        # Aplicar filtros
        if data_inicio:
            data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d')
            query = query.filter(Consulta.data_hora >= data_inicio)
        
        if data_fim:
            data_fim = datetime.strptime(data_fim, '%Y-%m-%d')
            query = query.filter(Consulta.data_hora <= data_fim)
        
        if medico_id:
            query = query.filter(Consulta.medico_id == medico_id)
        
        if paciente_id:
            query = query.filter(Consulta.paciente_id == paciente_id)
        
        if status:
            query = query.filter(Consulta.status == status)
        
        consultas = query.order_by(Consulta.data_hora.desc()).all()
        return jsonify([consulta.to_dict() for consulta in consultas]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@consulta_bp.route('/consultas/<int:id>', methods=['GET'])
def obter_consulta(id):
    try:
        consulta = Consulta.query.get_or_404(id)
        return jsonify(consulta.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@consulta_bp.route('/consultas', methods=['POST'])
def criar_consulta():
    try:
        data = request.get_json()
        
        # Validação básica
        required_fields = ['paciente_id', 'medico_id', 'data_hora', 'tipo_consulta']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} é obrigatório'}), 400
        
        # Verificar se paciente e médico existem
        paciente = Paciente.query.get(data['paciente_id'])
        if not paciente:
            return jsonify({'error': 'Paciente não encontrado'}), 404
        
        medico = Medico.query.get(data['medico_id'])
        if not medico:
            return jsonify({'error': 'Médico não encontrado'}), 404
        
        # Converter data e hora
        data_hora = datetime.strptime(data['data_hora'], '%Y-%m-%dT%H:%M')
        
        # Verificar conflito de horário para o médico
        conflito = Consulta.query.filter(
            and_(
                Consulta.medico_id == data['medico_id'],
                Consulta.data_hora == data_hora,
                Consulta.status != 'cancelada'
            )
        ).first()
        
        if conflito:
            return jsonify({'error': 'Médico já possui consulta agendada neste horário'}), 400
        
        consulta = Consulta(
            paciente_id=data['paciente_id'],
            medico_id=data['medico_id'],
            data_hora=data_hora,
            tipo_consulta=data['tipo_consulta'],
            observacoes=data.get('observacoes'),
            status=data.get('status', 'agendada')
        )
        
        db.session.add(consulta)
        db.session.commit()
        
        return jsonify(consulta.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@consulta_bp.route('/consultas/<int:id>', methods=['PUT'])
def atualizar_consulta(id):
    try:
        consulta = Consulta.query.get_or_404(id)
        data = request.get_json()
        
        # Verificar conflito de horário se data/hora ou médico mudaram
        if data.get('data_hora') or data.get('medico_id'):
            nova_data_hora = datetime.strptime(data['data_hora'], '%Y-%m-%dT%H:%M') if data.get('data_hora') else consulta.data_hora
            novo_medico_id = data.get('medico_id', consulta.medico_id)
            
            conflito = Consulta.query.filter(
                and_(
                    Consulta.id != id,
                    Consulta.medico_id == novo_medico_id,
                    Consulta.data_hora == nova_data_hora,
                    Consulta.status != 'cancelada'
                )
            ).first()
            
            if conflito:
                return jsonify({'error': 'Médico já possui consulta agendada neste horário'}), 400
        
        # Atualizar campos
        if data.get('paciente_id'):
            if not Paciente.query.get(data['paciente_id']):
                return jsonify({'error': 'Paciente não encontrado'}), 404
            consulta.paciente_id = data['paciente_id']
        
        if data.get('medico_id'):
            if not Medico.query.get(data['medico_id']):
                return jsonify({'error': 'Médico não encontrado'}), 404
            consulta.medico_id = data['medico_id']
        
        if data.get('data_hora'):
            consulta.data_hora = datetime.strptime(data['data_hora'], '%Y-%m-%dT%H:%M')
        
        if data.get('tipo_consulta'):
            consulta.tipo_consulta = data['tipo_consulta']
        
        if 'observacoes' in data:
            consulta.observacoes = data['observacoes']
        
        if data.get('status'):
            consulta.status = data['status']
        
        db.session.commit()
        return jsonify(consulta.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@consulta_bp.route('/consultas/<int:id>', methods=['DELETE'])
def deletar_consulta(id):
    try:
        consulta = Consulta.query.get_or_404(id)
        db.session.delete(consulta)
        db.session.commit()
        return jsonify({'message': 'Consulta deletada com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@consulta_bp.route('/consultas/<int:id>/status', methods=['PATCH'])
def atualizar_status_consulta(id):
    try:
        consulta = Consulta.query.get_or_404(id)
        data = request.get_json()
        
        if not data.get('status'):
            return jsonify({'error': 'Status é obrigatório'}), 400
        
        consulta.status = data['status']
        db.session.commit()
        
        return jsonify(consulta.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

