"""
Sistema de Autenticação Multi-usuário
Implementa login/senha seguro com isolamento completo de dados por usuário
"""

import streamlit as st
import hashlib
import json
import os
import re
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple

class AuthenticationSystem:
    """Sistema de autenticação e gestão de usuários"""
    
    def __init__(self):
        self.users_file = "users_database.json"
        self.session_timeout = 120  # 2 horas em minutos
        self.load_users_database()
    
    def load_users_database(self):
        """Carrega base de dados de usuários"""
        if os.path.exists(self.users_file):
            try:
                with open(self.users_file, 'r', encoding='utf-8') as f:
                    self.users_db = json.load(f)
            except:
                self.users_db = {}
        else:
            self.users_db = {}
            # Criar usuário padrão do Rômulo
            self.create_default_user()
    
    def save_users_database(self):
        """Salva base de dados de usuários"""
        with open(self.users_file, 'w', encoding='utf-8') as f:
            json.dump(self.users_db, f, ensure_ascii=False, indent=2)
    
    def create_default_user(self):
        """Cria usuário padrão do Rômulo"""
        username = "Rômulo"
        password = "965874+Rr"
        password_hash = self.hash_password(password)
        
        self.users_db[username] = {
            "password_hash": password_hash,
            "created_at": datetime.now().isoformat(),
            "last_login": None,
            "data_folder": f"user_data_{username.lower().replace(' ', '_')}",
            "profile": {
                "full_name": "Rômulo",
                "email": "",
                "role": "admin"
            },
            "security": {
                "question": "Qual sua primeira ótica de referência?",
                "answer_hash": self.hash_password("brasil ocular"),
                "recovery_attempts": 0,
                "last_recovery_attempt": None
            }
        }
        self.save_users_database()
    
    def hash_password(self, password: str) -> str:
        """Gera hash seguro da senha"""
        salt = "optical_business_plan_2025"
        return hashlib.sha256((password + salt).encode()).hexdigest()
    
    def validate_password_strength(self, password: str) -> Tuple[bool, str]:
        """Valida força da senha conforme critérios"""
        if len(password) < 8:
            return False, "Senha deve ter no mínimo 8 caracteres"
        
        if not re.search(r'[a-z]', password):
            return False, "Senha deve conter pelo menos uma letra minúscula"
        
        if not re.search(r'[A-Z]', password):
            return False, "Senha deve conter pelo menos uma letra maiúscula"
        
        if not re.search(r'\d', password):
            return False, "Senha deve conter pelo menos um número"
        
        # Caracteres especiais permitidos
        allowed_special = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        if not re.search(f'[{re.escape(allowed_special)}]', password):
            return False, f"Senha deve conter pelo menos um caractere especial: {allowed_special}"
        
        return True, "Senha válida"
    
    def register_user(self, username: str, password: str, full_name: str = "", email: str = "", 
                     security_question: str = "", security_answer: str = "") -> Tuple[bool, str]:
        """Registra novo usuário"""
        # Validar se usuário já existe
        if username in self.users_db:
            return False, "Usuário já existe"
        
        # Validar força da senha
        is_valid, message = self.validate_password_strength(password)
        if not is_valid:
            return False, message
        
        # Criar usuário
        password_hash = self.hash_password(password)
        data_folder = f"user_data_{username.lower().replace(' ', '_')}"
        
        self.users_db[username] = {
            "password_hash": password_hash,
            "created_at": datetime.now().isoformat(),
            "last_login": None,
            "data_folder": data_folder,
            "profile": {
                "full_name": full_name or username,
                "email": email,
                "role": "user"
            },
            "security": {
                "question": security_question,
                "answer_hash": self.hash_password(security_answer.lower().strip()) if security_answer else "",
                "recovery_attempts": 0,
                "last_recovery_attempt": None
            }
        }
        
        # Criar pasta de dados do usuário
        os.makedirs(data_folder, exist_ok=True)
        
        self.save_users_database()
        return True, "Usuário criado com sucesso"
    
    def authenticate_user(self, username: str, password: str) -> Tuple[bool, str]:
        """Autentica usuário"""
        if username not in self.users_db:
            return False, "Usuário não encontrado"
        
        password_hash = self.hash_password(password)
        stored_hash = self.users_db[username]["password_hash"]
        
        if password_hash != stored_hash:
            return False, "Senha incorreta"
        
        # Atualizar último login
        self.users_db[username]["last_login"] = datetime.now().isoformat()
        self.save_users_database()
        
        return True, "Login realizado com sucesso"
    
    def create_user_session(self, username: str):
        """Cria sessão do usuário"""
        user_data = self.users_db[username]
        
        st.session_state.authenticated = True
        st.session_state.current_user = username
        st.session_state.user_profile = user_data["profile"]
        st.session_state.user_data_folder = user_data["data_folder"]
        st.session_state.login_time = datetime.now()
        
        # Carregar dados específicos do usuário
        self.load_user_business_data(username)
    
    def load_user_business_data(self, username: str):
        """Carrega dados de negócio específicos do usuário"""
        user_folder = self.users_db[username]["data_folder"]
        user_data_file = os.path.join(user_folder, "business_data.json")
        
        if os.path.exists(user_data_file):
            try:
                with open(user_data_file, 'r', encoding='utf-8') as f:
                    business_data = json.load(f)
                st.session_state.business_data = business_data
            except:
                st.session_state.business_data = {}
        else:
            # Dados limpos para novo usuário
            st.session_state.business_data = {}
    
    def save_user_business_data(self, username: str):
        """Salva dados de negócio específicos do usuário"""
        if username not in self.users_db:
            return
        
        user_folder = self.users_db[username]["data_folder"]
        os.makedirs(user_folder, exist_ok=True)
        
        user_data_file = os.path.join(user_folder, "business_data.json")
        
        # Salvar dados do session_state
        business_data = st.session_state.get('business_data', {})
        
        with open(user_data_file, 'w', encoding='utf-8') as f:
            json.dump(business_data, f, ensure_ascii=False, indent=2)
    
    def logout_user(self):
        """Realiza logout do usuário"""
        # Salvar dados antes do logout
        if hasattr(st.session_state, 'current_user'):
            self.save_user_business_data(st.session_state.current_user)
        
        # Limpar sessão
        for key in list(st.session_state.keys()):
            del st.session_state[key]
    
    def is_session_valid(self) -> bool:
        """Verifica se sessão ainda é válida"""
        if not hasattr(st.session_state, 'authenticated'):
            return False
        
        if not st.session_state.authenticated:
            return False
        
        if not hasattr(st.session_state, 'login_time'):
            return False
        
        # Verificar timeout da sessão
        elapsed = datetime.now() - st.session_state.login_time
        if elapsed.total_seconds() / 60 > self.session_timeout:
            return False
        
        return True
    
    def verify_security_answer(self, username: str, answer: str) -> bool:
        """Verifica resposta de segurança"""
        if username not in self.users_db:
            return False
        
        security = self.users_db[username].get("security", {})
        stored_hash = security.get("answer_hash", "")
        answer_hash = self.hash_password(answer.lower().strip())
        
        return stored_hash == answer_hash
    
    def reset_password(self, username: str, new_password: str) -> Tuple[bool, str]:
        """Reset senha do usuário"""
        if username not in self.users_db:
            return False, "Usuário não encontrado"
        
        # Validar força da nova senha
        is_valid, message = self.validate_password_strength(new_password)
        if not is_valid:
            return False, message
        
        # Atualizar senha
        new_hash = self.hash_password(new_password)
        self.users_db[username]["password_hash"] = new_hash
        
        # Reset tentativas de recuperação
        if "security" in self.users_db[username]:
            self.users_db[username]["security"]["recovery_attempts"] = 0
            self.users_db[username]["security"]["last_recovery_attempt"] = None
        
        self.save_users_database()
        return True, "Senha alterada com sucesso"
    
    def can_attempt_recovery(self, username: str) -> Tuple[bool, str]:
        """Verifica se pode tentar recuperação"""
        if username not in self.users_db:
            return False, "Usuário não encontrado"
        
        security = self.users_db[username].get("security", {})
        attempts = security.get("recovery_attempts", 0)
        last_attempt = security.get("last_recovery_attempt")
        
        # Máximo 3 tentativas por hora
        if attempts >= 3:
            if last_attempt:
                last_time = datetime.fromisoformat(last_attempt)
                if datetime.now() - last_time < timedelta(hours=1):
                    return False, "Muitas tentativas. Tente novamente em 1 hora."
            
            # Reset se passou mais de 1 hora
            self.users_db[username]["security"]["recovery_attempts"] = 0
            self.save_users_database()
        
        return True, "Pode tentar recuperação"
    
    def record_recovery_attempt(self, username: str, success: bool):
        """Registra tentativa de recuperação"""
        if username not in self.users_db:
            return
        
        security = self.users_db[username].get("security", {})
        
        if success:
            security["recovery_attempts"] = 0
        else:
            security["recovery_attempts"] = security.get("recovery_attempts", 0) + 1
        
        security["last_recovery_attempt"] = datetime.now().isoformat()
        self.users_db[username]["security"] = security
        self.save_users_database()

    def show_login_form(self):
        """Exibe formulário de login"""
        st.title("🔐 Sistema de Autenticação")
        st.markdown("**Acesso ao Sistema de Planos de Negócio para Óticas**")
        
        # Tabs para Login, Registro e Recuperação
        tab_login, tab_register, tab_recovery = st.tabs(["🔑 Login", "👤 Novo Usuário", "🔓 Recuperar Senha"])
        
        with tab_login:
            st.markdown("### Fazer Login")
            
            with st.form("login_form"):
                username = st.text_input("Usuário", placeholder="Digite seu nome de usuário")
                password = st.text_input("Senha", type="password", placeholder="Digite sua senha")
                
                col1, col2 = st.columns([1, 2])
                with col1:
                    login_button = st.form_submit_button("🔑 Entrar", type="primary", use_container_width=True)
                
                if login_button:
                    if username and password:
                        success, message = self.authenticate_user(username, password)
                        
                        if success:
                            self.create_user_session(username)
                            st.success(f"Bem-vindo, {username}!")
                            st.rerun()
                        else:
                            st.error(f"Erro: {message}")
                    else:
                        st.error("Preencha usuário e senha")
        
        with tab_register:
            st.markdown("### Criar Novo Usuário")
            
            with st.form("register_form"):
                new_username = st.text_input("Nome de Usuário", placeholder="Escolha um nome de usuário")
                new_full_name = st.text_input("Nome Completo", placeholder="Seu nome completo")
                new_email = st.text_input("Email (opcional)", placeholder="seu@email.com")
                new_password = st.text_input("Senha", type="password", placeholder="Crie uma senha forte")
                confirm_password = st.text_input("Confirmar Senha", type="password", placeholder="Digite a senha novamente")
                
                # Mostrar critérios de senha
                with st.expander("📋 Critérios de Senha"):
                    st.markdown("""
                    **Sua senha deve conter:**
                    - Mínimo 8 caracteres
                    - Pelo menos 1 letra minúscula (a-z)
                    - Pelo menos 1 letra maiúscula (A-Z)
                    - Pelo menos 1 número (0-9)
                    - Pelo menos 1 caractere especial: !@#$%^&*()_+-=[]{}|;:,.<>?
                    """)
                
                register_button = st.form_submit_button("👤 Criar Usuário", type="secondary", use_container_width=True)
                
                if register_button:
                    if not all([new_username, new_password, confirm_password]):
                        st.error("Preencha todos os campos obrigatórios")
                    elif new_password != confirm_password:
                        st.error("Senhas não coincidem")
                    else:
                        success, message = self.register_user(new_username, new_password, new_full_name, new_email)
                        
                        if success:
                            st.success(f"Usuário '{new_username}' criado com sucesso! Faça login na aba ao lado.")
                        else:
                            st.error(f"Erro: {message}")
        
        with tab_recovery:
            st.markdown("### 🔓 Recuperar Senha")
            st.info("Se esqueceu sua senha, use sua pergunta de segurança para recuperar o acesso.")
            
            # Verificar se há dados de recuperação
            recovery_username = st.text_input("Nome de usuário", key="recovery_username")
            
            if recovery_username and recovery_username in self.users_db:
                # Verificar se pode tentar recuperação
                can_attempt, message = self.can_attempt_recovery(recovery_username)
                
                if not can_attempt:
                    st.error(message)
                else:
                    security = self.users_db[recovery_username].get("security", {})
                    security_question = security.get("question", "")
                    
                    if security_question:
                        st.markdown(f"**Pergunta de Segurança:** {security_question}")
                        
                        # Resposta de segurança
                        security_answer = st.text_input("Sua resposta:", key="security_answer")
                        
                        # Nova senha
                        new_password = st.text_input("Nova senha:", type="password", key="new_password_recovery")
                        confirm_password = st.text_input("Confirme a nova senha:", type="password", key="confirm_password_recovery")
                        
                        if st.button("🔄 Resetar Senha", key="reset_password_btn"):
                            if not security_answer:
                                st.error("Por favor, responda a pergunta de segurança.")
                            elif not new_password:
                                st.error("Por favor, digite a nova senha.")
                            elif new_password != confirm_password:
                                st.error("As senhas não coincidem.")
                            else:
                                # Verificar resposta de segurança
                                if self.verify_security_answer(recovery_username, security_answer):
                                    # Resetar senha
                                    success, message = self.reset_password(recovery_username, new_password)
                                    if success:
                                        st.success("Senha alterada com sucesso! Agora você pode fazer login com sua nova senha.")
                                        self.record_recovery_attempt(recovery_username, True)
                                    else:
                                        st.error(f"Erro ao alterar senha: {message}")
                                        self.record_recovery_attempt(recovery_username, False)
                                else:
                                    st.error("Resposta de segurança incorreta.")
                                    self.record_recovery_attempt(recovery_username, False)
                    else:
                        st.warning("Este usuário não possui pergunta de segurança configurada.")
            elif recovery_username:
                st.error("Usuário não encontrado.")
            
            # Informações sobre o usuário padrão
            with st.expander("🆘 Informações de Emergência"):
                st.markdown("""
                **Usuário Padrão do Sistema:**
                - **Usuário:** Rômulo
                - **Pergunta:** Qual sua primeira ótica de referência?
                - **Resposta:** brasil ocular
                
                **Limitações de Segurança:**
                - Máximo 3 tentativas de recuperação por hora
                - Respostas não são case-sensitive
                - Espaços extras são ignorados
                """)
        
        # Informações do sistema
        st.markdown("---")
        st.markdown("### ℹ️ Sobre o Sistema")
        st.info("""
        **Sistema Multi-usuário de Planos de Negócio**
        
        - Cada usuário tem seu próprio espaço isolado de dados
        - Todos os planos e configurações são privados por usuário
        - Sessões automáticas com timeout de segurança
        - Dados salvos automaticamente por usuário
        """)
    
    def show_user_header(self):
        """Exibe cabeçalho com informações do usuário"""
        if not hasattr(st.session_state, 'current_user'):
            return
        
        user = st.session_state.current_user
        profile = st.session_state.get('user_profile', {})
        
        # Header no sidebar
        with st.sidebar:
            st.markdown("---")
            st.markdown(f"**👤 Usuário:** {profile.get('full_name', user)}")
            st.caption(f"Logado como: {user}")
            
            # Informações da sessão
            if hasattr(st.session_state, 'login_time'):
                login_time = st.session_state.login_time
                st.caption(f"Login: {login_time.strftime('%H:%M - %d/%m/%Y')}")
            
            # Botão de logout
            if st.button("🚪 Sair", type="secondary", use_container_width=True):
                self.logout_user()
                st.rerun()
            
            st.markdown("---")

def init_auth_system() -> AuthenticationSystem:
    """Inicializa sistema de autenticação"""
    if 'auth_system' not in st.session_state:
        st.session_state.auth_system = AuthenticationSystem()
    
    return st.session_state.auth_system

def require_authentication():
    """Decorator para exigir autenticação em páginas"""
    auth = init_auth_system()
    
    if not auth.is_session_valid():
        auth.show_login_form()
        st.stop()
    
    # Mostrar header do usuário
    auth.show_user_header()
    
    # Auto-save de dados do usuário a cada interação
    if hasattr(st.session_state, 'current_user'):
        auth.save_user_business_data(st.session_state.current_user)
    
    return auth