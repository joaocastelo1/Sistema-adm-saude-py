from src.models.user import db
from datetime import datetime

class Consulta(db.Model):
    __tablename__ = 'consultas'
    
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id'), nullable=False)
    medico_id = db.Column(db.Integer, db.ForeignKey('medicos.id'), nullable=False)
    data_hora = db.Column(db.DateTime, nullable=False)
    tipo_consulta = db.Column(db.String(50), nullable=False)  # consulta, retorno, emergência
    observacoes = db.Column(db.Text)
    status = db.Column(db.String(20), default='agendada')  # agendada, realizada, cancelada
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Consulta {self.id} - Paciente: {self.paciente_id} - Médico: {self.medico_id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'paciente_id': self.paciente_id,
            'medico_id': self.medico_id,
            'data_hora': self.data_hora.isoformat() if self.data_hora else None,
            'tipo_consulta': self.tipo_consulta,
            'observacoes': self.observacoes,
            'status': self.status,
            'data_cadastro': self.data_cadastro.isoformat() if self.data_cadastro else None,
            'paciente_nome': self.paciente.nome if self.paciente else None,
            'medico_nome': self.medico.nome if self.medico else None
        }

