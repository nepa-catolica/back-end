```markdown
# Backend do Sistema NEPA

Este é o backend do sistema desenvolvido para o **Núcleo de Extensão e Pesquisa Acadêmica (NEPA)** da **Faculdade Católica da Paraíba**. O sistema foi projetado para automatizar e otimizar o processo de gerenciamento, aprovação e inscrição de projetos acadêmicos, proporcionando mais eficiência e transparência.

---

## Estrutura do Projeto

```plaintext
back-end/
│
├── src/
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── auth.py
│   │   ├── projetos.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── admin_service.py
│   │   ├── auth_service.py
│   │   ├── project_service.py
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── extensions.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── utils.py
│
├── .env
├── .gitignore
├── app.py
├── requirements.txt
```

---

## Configuração do Ambiente

### Instalação de Dependências

Antes de começar, certifique-se de que você possui o **Python 3.8+** e o **PostgreSQL** instalados em seu sistema. Execute os comandos abaixo:

1. Crie e ative um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate   # No Windows: venv\Scripts\activate
   ```

2. Instale as dependências listadas no arquivo `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

### Configuração do Banco de Dados

1. Certifique-se de que o PostgreSQL está em execução.
2. Crie o banco de dados chamado `nepa`:
   ```sql
   CREATE DATABASE nepa;
   ```

### Configuração do Arquivo `.env`

Crie um arquivo `.env` na raiz do projeto e configure as variáveis de ambiente conforme o exemplo abaixo:

```plaintext
UPLOAD_FOLDER=uploads/edital_pdfs
ALLOWED_EXTENSIONS=pdf
MAX_FILE_SIZE=5242880
SECRET_KEY=7265c9aa4297a05c0b7ded86bd2e76f98b244ef5699bfbf71cefd924a66081a9
SQLALCHEMY_DATABASE_URI=postgresql+psycopg2://postgres:admin@localhost:5432/nepa
SQLALCHEMY_TRACK_MODIFICATIONS=False
JWT_SECRET_KEY=308664db6f669929beb8a7e873e2be12e60ea0e9e1b1ff8cef4c8affa35b9fc4
```

Certifique-se de ajustar as configurações, como `SQLALCHEMY_DATABASE_URI`, conforme suas credenciais locais.

---

## Como Executar

1. Certifique-se de que o ambiente virtual está ativado:
   ```bash
   source venv/bin/activate   # No Windows: venv\Scripts\activate
   ```

2. Execute o servidor Flask:
   ```bash
   python app.py
   ```

3. O servidor estará disponível em:
   ```
   http://127.0.0.1:5000
   ```

---

## Tecnologias Utilizadas

- **Flask**: Framework principal.
- **SQLAlchemy**: ORM para gerenciar o banco de dados.
- **PostgreSQL**: Banco de dados relacional.
- **JWT**: Para autenticação e autorização segura.

---

## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir uma *issue* ou enviar um *pull request*.

```
