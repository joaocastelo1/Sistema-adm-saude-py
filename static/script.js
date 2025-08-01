// Sistema Administrativo de Saúde - JavaScript

// Configuração da API
const API_BASE = '/api';

// Estado global da aplicação
let currentSection = 'dashboard';
let pacientes = [];
let medicos = [];
let consultas = [];

// Inicialização da aplicação
document.addEventListener('DOMContentLoaded', function() {
    loadDashboard();
    setupEventListeners();
});

// Configurar event listeners
function setupEventListeners() {
    // Busca de pacientes
    document.getElementById('search-pacientes').addEventListener('input', function() {
        const termo = this.value;
        if (termo.length >= 2) {
            buscarPacientes(termo);
        } else if (termo.length === 0) {
            loadPacientes();
        }
    });

    // Busca de médicos
    document.getElementById('search-medicos').addEventListener('input', function() {
        const termo = this.value;
        if (termo.length >= 2) {
            buscarMedicos(termo);
        } else if (termo.length === 0) {
            loadMedicos();
        }
    });
}

// Navegação entre seções
function showSection(section) {
    // Esconder todas as seções
    document.querySelectorAll('.content-section').forEach(el => {
        el.style.display = 'none';
    });
    
    // Remover classe active de todos os links
    document.querySelectorAll('.nav-link').forEach(el => {
        el.classList.remove('active');
    });
    
    // Mostrar seção selecionada
    document.getElementById(section + '-section').style.display = 'block';
    
    // Adicionar classe active ao link correspondente
    event.target.classList.add('active');
    
    currentSection = section;
    
    // Carregar dados da seção
    switch(section) {
        case 'dashboard':
            loadDashboard();
            break;
        case 'pacientes':
            loadPacientes();
            break;
        case 'medicos':
            loadMedicos();
            break;
        case 'consultas':
            loadConsultas();
            break;
        case 'relatorios':
            loadRelatorios();
            break;
    }
}

// Funções de API
async function apiRequest(endpoint, options = {}) {
    try {
        const response = await fetch(API_BASE + endpoint, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        showAlert('Erro na comunicação com o servidor', 'danger');
        throw error;
    }
}

// Dashboard
async function loadDashboard() {
    try {
        const data = await apiRequest('/relatorios/dashboard');
        
        // Atualizar estatísticas
        document.getElementById('total-pacientes').textContent = data.estatisticas.total_pacientes;
        document.getElementById('total-medicos').textContent = data.estatisticas.total_medicos;
        document.getElementById('consultas-hoje').textContent = data.estatisticas.consultas_hoje;
        document.getElementById('consultas-mes').textContent = data.estatisticas.consultas_mes;
        
        // Atualizar próximas consultas
        updateProximasConsultas(data.proximas_consultas);
        
        // Atualizar gráfico de status
        updateStatusChart(data.consultas_por_status);
        
    } catch (error) {
        console.error('Erro ao carregar dashboard:', error);
    }
}

function updateProximasConsultas(consultas) {
    const tbody = document.getElementById('proximas-consultas');
    
    if (consultas.length === 0) {
        tbody.innerHTML = '<tr><td colspan="4" class="text-center">Nenhuma consulta agendada</td></tr>';
        return;
    }
    
    tbody.innerHTML = consultas.map(consulta => `
        <tr>
            <td>${formatDateTime(consulta.data_hora)}</td>
            <td>${consulta.paciente_nome || 'N/A'}</td>
            <td>${consulta.medico_nome || 'N/A'}</td>
            <td><span class="badge bg-info">${consulta.tipo_consulta}</span></td>
        </tr>
    `).join('');
}

function updateStatusChart(data) {
    const ctx = document.getElementById('statusChart').getContext('2d');
    
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: data.map(item => item.status),
            datasets: [{
                data: data.map(item => item.quantidade),
                backgroundColor: [
                    '#17a2b8',
                    '#28a745',
                    '#dc3545'
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}

// Pacientes
async function loadPacientes() {
    try {
        pacientes = await apiRequest('/pacientes');
        updatePacientesTable(pacientes);
    } catch (error) {
        console.error('Erro ao carregar pacientes:', error);
    }
}

function updatePacientesTable(data) {
    const tbody = document.getElementById('pacientes-table');
    
    if (data.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" class="text-center">Nenhum paciente encontrado</td></tr>';
        return;
    }
    
    tbody.innerHTML = data.map(paciente => `
        <tr>
            <td>${paciente.nome}</td>
            <td>${paciente.cpf}</td>
            <td>${formatDate(paciente.data_nascimento)}</td>
            <td>${paciente.telefone || '-'}</td>
            <td>${paciente.email || '-'}</td>
            <td>
                <button class="btn btn-sm btn-outline-primary" onclick="editPaciente(${paciente.id})">
                    <i class="fas fa-edit"></i>
                </button>
                <button class="btn btn-sm btn-outline-danger" onclick="deletePaciente(${paciente.id})">
                    <i class="fas fa-trash"></i>
                </button>
            </td>
        </tr>
    `).join('');
}

async function buscarPacientes(termo) {
    try {
        const data = await apiRequest(`/pacientes/buscar?q=${encodeURIComponent(termo)}`);
        updatePacientesTable(data);
    } catch (error) {
        console.error('Erro ao buscar pacientes:', error);
    }
}

function showPacienteModal(paciente = null) {
    const modal = new bootstrap.Modal(document.getElementById('pacienteModal'));
    
    if (paciente) {
        // Edição
        document.getElementById('paciente-id').value = paciente.id;
        document.getElementById('paciente-nome').value = paciente.nome;
        document.getElementById('paciente-cpf').value = paciente.cpf;
        document.getElementById('paciente-data-nascimento').value = paciente.data_nascimento;
        document.getElementById('paciente-telefone').value = paciente.telefone || '';
        document.getElementById('paciente-email').value = paciente.email || '';
        document.getElementById('paciente-endereco').value = paciente.endereco || '';
    } else {
        // Novo
        document.getElementById('pacienteForm').reset();
        document.getElementById('paciente-id').value = '';
    }
    
    modal.show();
}

async function salvarPaciente() {
    const form = document.getElementById('pacienteForm');
    if (!form.checkValidity()) {
        form.reportValidity();
        return;
    }
    
    const id = document.getElementById('paciente-id').value;
    const data = {
        nome: document.getElementById('paciente-nome').value,
        cpf: document.getElementById('paciente-cpf').value,
        data_nascimento: document.getElementById('paciente-data-nascimento').value,
        telefone: document.getElementById('paciente-telefone').value,
        email: document.getElementById('paciente-email').value,
        endereco: document.getElementById('paciente-endereco').value
    };
    
    try {
        if (id) {
            // Atualizar
            await apiRequest(`/pacientes/${id}`, {
                method: 'PUT',
                body: JSON.stringify(data)
            });
            showAlert('Paciente atualizado com sucesso!', 'success');
        } else {
            // Criar
            await apiRequest('/pacientes', {
                method: 'POST',
                body: JSON.stringify(data)
            });
            showAlert('Paciente cadastrado com sucesso!', 'success');
        }
        
        bootstrap.Modal.getInstance(document.getElementById('pacienteModal')).hide();
        loadPacientes();
    } catch (error) {
        console.error('Erro ao salvar paciente:', error);
    }
}

async function editPaciente(id) {
    try {
        const paciente = await apiRequest(`/pacientes/${id}`);
        showPacienteModal(paciente);
    } catch (error) {
        console.error('Erro ao carregar paciente:', error);
    }
}

async function deletePaciente(id) {
    if (!confirm('Tem certeza que deseja excluir este paciente?')) {
        return;
    }
    
    try {
        await apiRequest(`/pacientes/${id}`, { method: 'DELETE' });
        showAlert('Paciente excluído com sucesso!', 'success');
        loadPacientes();
    } catch (error) {
        console.error('Erro ao excluir paciente:', error);
    }
}

// Médicos
async function loadMedicos() {
    try {
        medicos = await apiRequest('/medicos');
        updateMedicosTable(medicos);
    } catch (error) {
        console.error('Erro ao carregar médicos:', error);
    }
}

function updateMedicosTable(data) {
    const tbody = document.getElementById('medicos-table');
    
    if (data.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" class="text-center">Nenhum médico encontrado</td></tr>';
        return;
    }
    
    tbody.innerHTML = data.map(medico => `
        <tr>
            <td>${medico.nome}</td>
            <td>${medico.crm}</td>
            <td>${medico.especialidade}</td>
            <td>${medico.telefone || '-'}</td>
            <td>${medico.email || '-'}</td>
            <td>
                <button class="btn btn-sm btn-outline-primary" onclick="editMedico(${medico.id})">
                    <i class="fas fa-edit"></i>
                </button>
                <button class="btn btn-sm btn-outline-danger" onclick="deleteMedico(${medico.id})">
                    <i class="fas fa-trash"></i>
                </button>
            </td>
        </tr>
    `).join('');
}

async function buscarMedicos(termo) {
    try {
        const data = await apiRequest(`/medicos/buscar?q=${encodeURIComponent(termo)}`);
        updateMedicosTable(data);
    } catch (error) {
        console.error('Erro ao buscar médicos:', error);
    }
}

function showMedicoModal(medico = null) {
    const modal = new bootstrap.Modal(document.getElementById('medicoModal'));
    
    if (medico) {
        // Edição
        document.getElementById('medico-id').value = medico.id;
        document.getElementById('medico-nome').value = medico.nome;
        document.getElementById('medico-crm').value = medico.crm;
        document.getElementById('medico-especialidade').value = medico.especialidade;
        document.getElementById('medico-telefone').value = medico.telefone || '';
        document.getElementById('medico-email').value = medico.email || '';
    } else {
        // Novo
        document.getElementById('medicoForm').reset();
        document.getElementById('medico-id').value = '';
    }
    
    modal.show();
}

async function salvarMedico() {
    const form = document.getElementById('medicoForm');
    if (!form.checkValidity()) {
        form.reportValidity();
        return;
    }
    
    const id = document.getElementById('medico-id').value;
    const data = {
        nome: document.getElementById('medico-nome').value,
        crm: document.getElementById('medico-crm').value,
        especialidade: document.getElementById('medico-especialidade').value,
        telefone: document.getElementById('medico-telefone').value,
        email: document.getElementById('medico-email').value
    };
    
    try {
        if (id) {
            // Atualizar
            await apiRequest(`/medicos/${id}`, {
                method: 'PUT',
                body: JSON.stringify(data)
            });
            showAlert('Médico atualizado com sucesso!', 'success');
        } else {
            // Criar
            await apiRequest('/medicos', {
                method: 'POST',
                body: JSON.stringify(data)
            });
            showAlert('Médico cadastrado com sucesso!', 'success');
        }
        
        bootstrap.Modal.getInstance(document.getElementById('medicoModal')).hide();
        loadMedicos();
    } catch (error) {
        console.error('Erro ao salvar médico:', error);
    }
}

async function editMedico(id) {
    try {
        const medico = await apiRequest(`/medicos/${id}`);
        showMedicoModal(medico);
    } catch (error) {
        console.error('Erro ao carregar médico:', error);
    }
}

async function deleteMedico(id) {
    if (!confirm('Tem certeza que deseja excluir este médico?')) {
        return;
    }
    
    try {
        await apiRequest(`/medicos/${id}`, { method: 'DELETE' });
        showAlert('Médico excluído com sucesso!', 'success');
        loadMedicos();
    } catch (error) {
        console.error('Erro ao excluir médico:', error);
    }
}

// Consultas
async function loadConsultas() {
    try {
        consultas = await apiRequest('/consultas');
        updateConsultasTable(consultas);
        await loadSelectOptions();
    } catch (error) {
        console.error('Erro ao carregar consultas:', error);
    }
}

function updateConsultasTable(data) {
    const tbody = document.getElementById('consultas-table');
    
    if (data.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" class="text-center">Nenhuma consulta encontrada</td></tr>';
        return;
    }
    
    tbody.innerHTML = data.map(consulta => `
        <tr>
            <td>${formatDateTime(consulta.data_hora)}</td>
            <td>${consulta.paciente_nome || 'N/A'}</td>
            <td>${consulta.medico_nome || 'N/A'}</td>
            <td><span class="badge bg-info">${consulta.tipo_consulta}</span></td>
            <td><span class="badge status-${consulta.status}">${consulta.status}</span></td>
            <td>
                <button class="btn btn-sm btn-outline-primary" onclick="editConsulta(${consulta.id})">
                    <i class="fas fa-edit"></i>
                </button>
                <button class="btn btn-sm btn-outline-danger" onclick="deleteConsulta(${consulta.id})">
                    <i class="fas fa-trash"></i>
                </button>
            </td>
        </tr>
    `).join('');
}

async function loadSelectOptions() {
    try {
        // Carregar pacientes para o select
        const pacientesData = await apiRequest('/pacientes');
        const pacienteSelect = document.getElementById('consulta-paciente');
        pacienteSelect.innerHTML = '<option value="">Selecione um paciente</option>' +
            pacientesData.map(p => `<option value="${p.id}">${p.nome}</option>`).join('');
        
        // Carregar médicos para o select
        const medicosData = await apiRequest('/medicos');
        const medicoSelect = document.getElementById('consulta-medico');
        medicoSelect.innerHTML = '<option value="">Selecione um médico</option>' +
            medicosData.map(m => `<option value="${m.id}">${m.nome} - ${m.especialidade}</option>`).join('');
    } catch (error) {
        console.error('Erro ao carregar opções:', error);
    }
}

async function filtrarConsultas() {
    const dataInicio = document.getElementById('filter-data-inicio').value;
    const dataFim = document.getElementById('filter-data-fim').value;
    const status = document.getElementById('filter-status').value;
    
    let url = '/consultas?';
    const params = [];
    
    if (dataInicio) params.push(`data_inicio=${dataInicio}`);
    if (dataFim) params.push(`data_fim=${dataFim}`);
    if (status) params.push(`status=${status}`);
    
    url += params.join('&');
    
    try {
        const data = await apiRequest(url);
        updateConsultasTable(data);
    } catch (error) {
        console.error('Erro ao filtrar consultas:', error);
    }
}

function showConsultaModal(consulta = null) {
    const modal = new bootstrap.Modal(document.getElementById('consultaModal'));
    
    if (consulta) {
        // Edição
        document.getElementById('consulta-id').value = consulta.id;
        document.getElementById('consulta-paciente').value = consulta.paciente_id;
        document.getElementById('consulta-medico').value = consulta.medico_id;
        document.getElementById('consulta-data-hora').value = consulta.data_hora.slice(0, 16);
        document.getElementById('consulta-tipo').value = consulta.tipo_consulta;
        document.getElementById('consulta-status').value = consulta.status;
        document.getElementById('consulta-observacoes').value = consulta.observacoes || '';
    } else {
        // Nova
        document.getElementById('consultaForm').reset();
        document.getElementById('consulta-id').value = '';
        document.getElementById('consulta-status').value = 'agendada';
    }
    
    modal.show();
}

async function salvarConsulta() {
    const form = document.getElementById('consultaForm');
    if (!form.checkValidity()) {
        form.reportValidity();
        return;
    }
    
    const id = document.getElementById('consulta-id').value;
    const data = {
        paciente_id: parseInt(document.getElementById('consulta-paciente').value),
        medico_id: parseInt(document.getElementById('consulta-medico').value),
        data_hora: document.getElementById('consulta-data-hora').value,
        tipo_consulta: document.getElementById('consulta-tipo').value,
        status: document.getElementById('consulta-status').value,
        observacoes: document.getElementById('consulta-observacoes').value
    };
    
    try {
        if (id) {
            // Atualizar
            await apiRequest(`/consultas/${id}`, {
                method: 'PUT',
                body: JSON.stringify(data)
            });
            showAlert('Consulta atualizada com sucesso!', 'success');
        } else {
            // Criar
            await apiRequest('/consultas', {
                method: 'POST',
                body: JSON.stringify(data)
            });
            showAlert('Consulta agendada com sucesso!', 'success');
        }
        
        bootstrap.Modal.getInstance(document.getElementById('consultaModal')).hide();
        loadConsultas();
    } catch (error) {
        console.error('Erro ao salvar consulta:', error);
    }
}

async function editConsulta(id) {
    try {
        const consulta = await apiRequest(`/consultas/${id}`);
        showConsultaModal(consulta);
    } catch (error) {
        console.error('Erro ao carregar consulta:', error);
    }
}

async function deleteConsulta(id) {
    if (!confirm('Tem certeza que deseja excluir esta consulta?')) {
        return;
    }
    
    try {
        await apiRequest(`/consultas/${id}`, { method: 'DELETE' });
        showAlert('Consulta excluída com sucesso!', 'success');
        loadConsultas();
    } catch (error) {
        console.error('Erro ao excluir consulta:', error);
    }
}

// Relatórios
async function loadRelatorios() {
    try {
        // Carregar dados para os gráficos
        const consultasPorMedico = await apiRequest('/relatorios/consultas-por-medico');
        const especialidadesMaisProcuradas = await apiRequest('/relatorios/especialidades-mais-procuradas');
        
        updateMedicoChart(consultasPorMedico);
        updateEspecialidadeChart(especialidadesMaisProcuradas);
    } catch (error) {
        console.error('Erro ao carregar relatórios:', error);
    }
}

function updateMedicoChart(data) {
    const ctx = document.getElementById('medicoChart').getContext('2d');
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.map(item => item.medico),
            datasets: [{
                label: 'Consultas',
                data: data.map(item => item.total_consultas),
                backgroundColor: 'rgba(54, 162, 235, 0.8)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

function updateEspecialidadeChart(data) {
    const ctx = document.getElementById('especialidadeChart').getContext('2d');
    
    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: data.map(item => item.especialidade),
            datasets: [{
                data: data.map(item => item.total_consultas),
                backgroundColor: [
                    '#FF6384',
                    '#36A2EB',
                    '#FFCE56',
                    '#4BC0C0',
                    '#9966FF',
                    '#FF9F40'
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}

// Funções utilitárias
function formatDate(dateString) {
    if (!dateString) return '-';
    const date = new Date(dateString);
    return date.toLocaleDateString('pt-BR');
}

function formatDateTime(dateTimeString) {
    if (!dateTimeString) return '-';
    const date = new Date(dateTimeString);
    return date.toLocaleString('pt-BR');
}

function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    alertDiv.style.top = '20px';
    alertDiv.style.right = '20px';
    alertDiv.style.zIndex = '9999';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alertDiv);
    
    // Remover automaticamente após 5 segundos
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.parentNode.removeChild(alertDiv);
        }
    }, 5000);
}

