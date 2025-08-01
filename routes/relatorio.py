from flask import Blueprint, request, jsonify
from src.models.user import db
from src.models.consulta import Consulta
from src.models.paciente import Paciente
from src.models.medico import Medico
from datetime import datetime, timedelta
from sqlalchemy import func, and_, extract

relatorio_bp = Blueprint('relatorio', __name__)

@relatorio_bp.route('/relatorios/dashboard', methods=['GET'])
def dashboard():
    try:
        hoje = datetime.now().date()
        inicio_mes = hoje.replace(day=1)
        
        # Estatísticas gerais
        total_pacientes = Paciente.query.count()
        total_medicos = Medico.query.count()
        total_consultas = Consulta.query.count()
        
        # Consultas do mês atual
        consultas_mes = Consulta.query.filter(
            Consulta.data_hora >= inicio_mes
        ).count()
        
        # Consultas de hoje
        consultas_hoje = Consulta.query.filter(
            func.date(Consulta.data_hora) == hoje
        ).count()
        
        # Consultas por status
        consultas_por_status = db.session.query(
            Consulta.status,
            func.count(Consulta.id)
        ).group_by(Consulta.status).all()
        
        # Próximas consultas (próximos 7 dias)
        proximas_consultas = Consulta.query.filter(
            and_(
                Consulta.data_hora >= datetime.now(),
                Consulta.data_hora <= datetime.now() + timedelta(days=7),
                Consulta.status == 'agendada'
            )
        ).order_by(Consulta.data_hora).limit(10).all()
        
        return jsonify({
            'estatisticas': {
                'total_pacientes': total_pacientes,
                'total_medicos': total_medicos,
                'total_consultas': total_consultas,
                'consultas_mes': consultas_mes,
                'consultas_hoje': consultas_hoje
            },
            'consultas_por_status': [
                {'status': status, 'quantidade': quantidade}
                for status, quantidade in consultas_por_status
            ],
            'proximas_consultas': [consulta.to_dict() for consulta in proximas_consultas]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@relatorio_bp.route('/relatorios/consultas-por-medico', methods=['GET'])
def consultas_por_medico():
    try:
        data_inicio = request.args.get('data_inicio')
        data_fim = request.args.get('data_fim')
        
        query = db.session.query(
            Medico.nome,
            Medico.especialidade,
            func.count(Consulta.id).label('total_consultas')
        ).join(Consulta, Medico.id == Consulta.medico_id)
        
        if data_inicio:
            data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d')
            query = query.filter(Consulta.data_hora >= data_inicio)
        
        if data_fim:
            data_fim = datetime.strptime(data_fim, '%Y-%m-%d')
            query = query.filter(Consulta.data_hora <= data_fim)
        
        resultados = query.group_by(Medico.id).order_by(func.count(Consulta.id).desc()).all()
        
        return jsonify([
            {
                'medico': nome,
                'especialidade': especialidade,
                'total_consultas': total
            }
            for nome, especialidade, total in resultados
        ]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@relatorio_bp.route('/relatorios/consultas-por-periodo', methods=['GET'])
def consultas_por_periodo():
    try:
        data_inicio = request.args.get('data_inicio')
        data_fim = request.args.get('data_fim')
        agrupamento = request.args.get('agrupamento', 'dia')  # dia, mes, ano
        
        if not data_inicio or not data_fim:
            return jsonify({'error': 'data_inicio e data_fim são obrigatórios'}), 400
        
        data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d')
        data_fim = datetime.strptime(data_fim, '%Y-%m-%d')
        
        if agrupamento == 'dia':
            query = db.session.query(
                func.date(Consulta.data_hora).label('periodo'),
                func.count(Consulta.id).label('total')
            )
        elif agrupamento == 'mes':
            query = db.session.query(
                func.strftime('%Y-%m', Consulta.data_hora).label('periodo'),
                func.count(Consulta.id).label('total')
            )
        else:  # ano
            query = db.session.query(
                extract('year', Consulta.data_hora).label('periodo'),
                func.count(Consulta.id).label('total')
            )
        
        resultados = query.filter(
            and_(
                Consulta.data_hora >= data_inicio,
                Consulta.data_hora <= data_fim
            )
        ).group_by('periodo').order_by('periodo').all()
        
        return jsonify([
            {
                'periodo': str(periodo),
                'total_consultas': total
            }
            for periodo, total in resultados
        ]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@relatorio_bp.route('/relatorios/especialidades-mais-procuradas', methods=['GET'])
def especialidades_mais_procuradas():
    try:
        data_inicio = request.args.get('data_inicio')
        data_fim = request.args.get('data_fim')
        
        query = db.session.query(
            Medico.especialidade,
            func.count(Consulta.id).label('total_consultas')
        ).join(Consulta, Medico.id == Consulta.medico_id)
        
        if data_inicio:
            data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d')
            query = query.filter(Consulta.data_hora >= data_inicio)
        
        if data_fim:
            data_fim = datetime.strptime(data_fim, '%Y-%m-%d')
            query = query.filter(Consulta.data_hora <= data_fim)
        
        resultados = query.group_by(Medico.especialidade).order_by(func.count(Consulta.id).desc()).all()
        
        return jsonify([
            {
                'especialidade': especialidade,
                'total_consultas': total
            }
            for especialidade, total in resultados
        ]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@relatorio_bp.route('/relatorios/pacientes-frequentes', methods=['GET'])
def pacientes_frequentes():
    try:
        limite = request.args.get('limite', 10, type=int)
        
        resultados = db.session.query(
            Paciente.nome,
            Paciente.cpf,
            func.count(Consulta.id).label('total_consultas')
        ).join(Consulta, Paciente.id == Consulta.paciente_id).group_by(
            Paciente.id
        ).order_by(func.count(Consulta.id).desc()).limit(limite).all()
        
        return jsonify([
            {
                'paciente': nome,
                'cpf': cpf,
                'total_consultas': total
            }
            for nome, cpf, total in resultados
        ]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

