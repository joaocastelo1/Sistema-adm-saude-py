from src.models.user import db
from datetime import datetime

class Medico(db.Model):
    __tablename__ = 'medicos'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    crm = db.Column(db.String(20), unique=True, nullable=False)
    especialidade = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamento com consultas
    consultas = db.relationship('Consulta', backref='medico', lazy=True)

    def __repr__(self):
        return f'<Medico {self.nome} - CRM: {self.crm}>'

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'crm': self.crm,
            'especialidade': self.especialidade,
            'telefone': self.telefone,
            'email': self.email,
            'data_cadastro': self.data_cadastro.isoformat() if self.data_cadastro else None
        }

