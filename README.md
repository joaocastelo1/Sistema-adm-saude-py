# Sistema Administrativo de Saúde

Um sistema completo para gestão administrativa de clínicas e consultórios médicos, desenvolvido em **Python** com **Flask** e uma interface web moderna.

---

## Visão Geral

Este projeto visa fornecer uma solução robusta e intuitiva para a administração de clínicas e consultórios, cobrindo desde o cadastro de pacientes e médicos até o agendamento de consultas e a geração de relatórios.

---

## Funcionalidades Principais

- **Gestão de Pacientes**: Cadastro, edição, busca e listagem detalhada de pacientes.
- **Gestão de Médicos**: Controle de informações de médicos, incluindo CRM e especialidades.
- **Agendamento de Consultas**: Sistema inteligente de agendamento com validação de conflitos de horário.
- **Relatórios Administrativos**: Geração de relatórios e gráficos para análise de dados da clínica.
- **Interface Web Responsiva**: Acesso fácil e otimizado em diferentes dispositivos (desktop, tablet, mobile).
- **Autenticação de Usuários**: Controle de acesso seguro para diferentes perfis (admin, médico, recepcionista).

---

## Tecnologias Utilizadas

### Backend

- **Python**: Linguagem de programação principal.
- **Flask**: Microframework web para a construção da API RESTful.
- **SQLAlchemy**: ORM (Object-Relational Mapper) para interação com o banco de dados.
- **SQLite**: Banco de dados leve e integrado (pode ser facilmente configurado para PostgreSQL, MySQL, etc.).
- **Flask-CORS**: Para permitir requisições de diferentes origens (frontend).
- **Werkzeug**: Para segurança de senhas (hashing).

### Frontend

- **HTML5**: Estrutura da interface do usuário.
- **CSS3**: Estilização e design responsivo (com Bootstrap).
- **JavaScript (ES6+)**: Lógica interativa do lado do cliente.
- **Bootstrap 5**: Framework CSS para um design moderno e responsivo.
- **Chart.js**: Biblioteca JavaScript para criação de gráficos interativos.
- **Font Awesome**: Biblioteca de ícones.

---

## Fases do Desenvolvimento

### 1. Planejamento e Análise de Requisitos
- Definição das funcionalidades essenciais do sistema (gestão de pacientes, médicos, consultas, relatórios).
- Escolha das tecnologias a serem utilizadas (Flask, SQLAlchemy, HTML/CSS/JS).
- Esboço inicial da estrutura do banco de dados e das relações entre as entidades.

### 2. Estruturação do Banco de Dados e Modelos
- Criação do esquema detalhado do banco de dados.
- Definição dos modelos SQLAlchemy para as entidades principais: `Paciente`, `Medico`, `Consulta` e `User` (para autenticação).
- Estabelecimento dos relacionamentos entre os modelos.

### 3. Desenvolvimento do Backend Flask
- Configuração do ambiente Flask e integração com SQLAlchemy.
- Implementação das rotas da API RESTful para operações CRUD de pacientes, médicos e consultas.
- Desenvolvimento da lógica de autenticação e autorização de usuários, incluindo hashing de senhas e controle de acesso por perfis.
- Criação de endpoints para funcionalidades de busca e filtragem.

### 4. Criação da Interface Web Frontend
- Desenvolvimento das páginas HTML, estilização com CSS (Bootstrap) e lógica interativa com JavaScript.
- Criação de formulários para cadastro e edição de pacientes, médicos e consultas.
- Implementação da exibição de listas de registros e detalhes individuais.
- Design responsivo para garantir a usabilidade em diferentes tamanhos de tela.

### 5. Implementação de Funcionalidades Administrativas
- Desenvolvimento de endpoints e lógica para geração de relatórios administrativos (consultas por médico, especialidades mais procuradas, consultas por período, pacientes mais frequentes).
- Integração de gráficos interativos utilizando Chart.js para visualização dos dados.

### 6. Testes e Documentação
- Realização de testes manuais exaustivos para garantir a funcionalidade e a usabilidade do sistema.
- Geração de documentação técnica detalhada para o código-fonte e a arquitetura do sistema.
- Criação de um manual do usuário (`MANUAL_USUARIO.md`) e um guia de instalação (`INSTALACAO.md`).

### 7. Entrega do Sistema ao Usuário
- Preparação do sistema para implantação, incluindo a criação de um pacote `.zip` com todos os arquivos necessários.
- Entrega do código-fonte completo e de toda a documentação gerada ao usuário.

---

## Como Rodar o Projeto (Localmente)

Para executar este sistema em seu ambiente local, siga as instruções detalhadas no arquivo `INSTALACAO.md`. Resumo dos passos:

1. Clone o repositório ou baixe o arquivo `.zip` do projeto.
2. Navegue até a pasta raiz do projeto no terminal.
3. Crie e ative um ambiente virtual Python.
4. Instale as dependências listadas em `requirements.txt`.
5. Execute o arquivo principal do Flask:

   ```bash
   python src/main.py

sistema_saude/
├── src/
│   ├── models/          # Definições dos modelos de banco de dados
│   ├── routes/          # Endpoints da API RESTful
│   ├── static/          # Arquivos estáticos do frontend (HTML, CSS, JS)
│   ├── database/        # Arquivo do banco de dados SQLite (app.db)
│   └── main.py          # Ponto de entrada da aplicação Flask
├── venv/                # Ambiente virtual Python
├── requirements.txt     # Dependências do projeto Python
├── README.md            # Este arquivo
├── MANUAL_USUARIO.md    # Manual detalhado para o usuário final
└── INSTALACAO.md        # Guia passo a passo para instalação local
