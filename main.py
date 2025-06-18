import streamlit as st

# Page configuration DEVE ser a primeira linha Streamlit
st.set_page_config(
    page_title="Plano de Negócios - Ótica",
    page_icon="👓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS para eliminar COMPLETAMENTE problemas de fonte itálica ilegível
st.markdown("""
<style>
/* FORÇAR FONTE NORMAL EM TODO O SISTEMA - PRIORITY MÁXIMA */
*, *::before, *::after,
html, body, div, span, applet, object, iframe,
h1, h2, h3, h4, h5, h6, p, blockquote, pre,
a, abbr, acronym, address, big, cite, code,
del, dfn, em, img, ins, kbd, q, s, samp,
small, strike, strong, sub, sup, tt, var,
b, u, i, center,
dl, dt, dd, ol, ul, li,
fieldset, form, label, legend,
table, caption, tbody, tfoot, thead, tr, th, td,
article, aside, canvas, details, embed,
figure, figcaption, footer, header, hgroup,
menu, nav, output, ruby, section, summary,
time, mark, audio, video {
    font-style: normal !important;
    font-weight: normal !important;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif !important;
}

/* ELIMINAR ITÁLICO AGRESSIVAMENTE */
em, i, .italic, cite, dfn, var,
.stMarkdown em, .stMarkdown i,
.stAlert em, .stAlert i,
.stInfo em, .stInfo i,
.stSuccess em, .stSuccess i,
.stWarning em, .stWarning i,
.stError em, .stError i {
    font-style: normal !important;
    font-weight: normal !important;
    text-decoration: none !important;
}

/* CORRIGIR TODOS OS COMPONENTES STREAMLIT */
.stTextInput, .stTextInput *,
.stNumberInput, .stNumberInput *,
.stSelectbox, .stSelectbox *,
.stMultiSelect, .stMultiSelect *,
.stTextArea, .stTextArea *,
.stSlider, .stSlider *,
.stCheckbox, .stCheckbox *,
.stRadio, .stRadio *,
.stButton, .stButton *,
.stMetric, .stMetric *,
.stContainer, .stContainer *,
.stColumns, .stColumns *,
.stTabs, .stTabs *,
.stExpander, .stExpander *,
.stSidebar, .stSidebar * {
    font-style: normal !important;
    font-family: inherit !important;
}

/* CORRIGIR ESPECIFICAMENTE ELEMENTOS DE INPUT */
input, textarea, select, option,
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stSelectbox > div > div > div,
.stMultiSelect > div > div > div,
.stTextArea > div > div > textarea {
    font-style: normal !important;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif !important;
    font-weight: 400 !important;
}

/* CORRIGIR LABELS E HELP TEXT */
label, .stLabel, 
.help, .stHelp,
.caption, .stCaption,
.description, .stDescription {
    font-style: normal !important;
    font-family: inherit !important;
}

/* CORRIGIR TOOLTIPS E BALÕES */
.stTooltip, .stTooltipContent,
.stBalloons, .stSnow,
.tooltip, [data-tooltip] {
    font-style: normal !important;
}

/* CORRIGIR NÚMEROS E VALORES MONETÁRIOS */
.currency, .number, .metric-value,
.stMetric .metric-value,
.stMetric .metric-delta {
    font-family: 'Consolas', 'Monaco', 'Courier New', monospace !important;
    font-style: normal !important;
    font-weight: 500 !important;
}

/* OVERRIDE GLOBAL DE EMERGÊNCIA */
[style*="font-style: italic"] {
    font-style: normal !important;
}

[style*="font-style:italic"] {
    font-style: normal !important;  
}

/* APLICAR A TODA ÁRVORE DOM */
.main * {
    font-style: normal !important;
}

.stApp * {
    font-style: normal !important;
}

/* FORÇA BRUTA FINAL */
body * {
    font-style: normal !important;
}
</style>
""", unsafe_allow_html=True)

import pandas as pd
import numpy as np
import json
import os
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt

# Import calculators
from tax_calculator import TaxCalculator
from labor_calculator import LaborCalculator
from dre_generator import DREGenerator
from pdf_generator import PDFGenerator
from product_cost_calculator import ProductCostCalculator
from construction_cost_calculator import ConstructionCostCalculator
from pricing_suggestions import LensPricingSuggestions
from investor_report_generator import InvestorReportGenerator
from multilingual_pdf_generator import MultilingualInvestorPDFGenerator
from structured_investor_report import StructuredInvestorReport
from unified_cost_analyzer import show_unified_cost_analyzer
from integrated_cost_analyzer_step10 import show_integrated_cost_analyzer_step10

# Import authentication system
from auth_system import require_authentication, init_auth_system

# Page configuration já foi definida no início do arquivo

# Initialize session state for 12 steps
if 'step' not in st.session_state:
    st.session_state.step = 1

if 'business_data' not in st.session_state:
    st.session_state.business_data = {}

if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files = {}

if 'show_lens_pricing' not in st.session_state:
    st.session_state.show_lens_pricing = False

if 'show_employee_manager' not in st.session_state:
    st.session_state.show_employee_manager = False

if 'show_investor_report' not in st.session_state:
    st.session_state.show_investor_report = False

# Utility functions
def format_currency(value):
    """Format currency with Brazilian format (R$ 30.000,00)"""
    if value == 0:
        return "R$ 0,00"
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def format_number(value):
    """Format number with Brazilian format (30.000)"""
    if value == 0:
        return "0"
    return f"{value:,.0f}".replace(",", ".")

def round_price_to_tens(price):
    """Round price to nearest 10 reais (no cents)"""
    return round(price / 10) * 10

def calcular_custo_captador_mensal():
    """Calcula o custo mensal do captador baseado nas configurações da Gestão de Pessoas"""
    
    # Verificar se o sistema de captação está ativo
    usar_sistema_captacao = st.session_state.business_data.get('usar_sistema_captacao', False)
    if not usar_sistema_captacao:
        return 0.0
    
    # Obter projeções de vendas das Projeções Financeiras
    vendas_mes_1 = st.session_state.business_data.get('vendas_mes_1', 0)
    ticket_medio = st.session_state.business_data.get('ticket_medio', 500)
    oculos_meta = int(vendas_mes_1 / ticket_medio) if ticket_medio > 0 and vendas_mes_1 > 0 else 30
    
    # VERIFICAR GATILHO MÍNIMO (a partir de 5 vendas)
    meta_minima_captador = st.session_state.business_data.get('meta_minima_captador', 5)
    if oculos_meta < meta_minima_captador:
        # Não há pagamento se não atingir o mínimo
        st.session_state.business_data['custo_captador_mensal_calculado'] = 0.0
        st.session_state.business_data['memoria_calculo_captador'] = f"Meta {oculos_meta} óculos < gatilho mínimo {meta_minima_captador} vendas = R$ 0,00"
        return 0.0
    
    # Obter configurações de comissão da Gestão de Pessoas
    comissao_avista = st.session_state.business_data.get('comissao_avista', 30.0)  # R$ 30 por venda à vista
    comissao_parcelada = st.session_state.business_data.get('comissao_parcelada', 5.0)  # R$ 5 por venda parcelada
    
    # Distribuição entre à vista e parcelada (padrão 50% cada)
    percentual_avista = st.session_state.business_data.get('percentual_vendas_avista', 50)
    percentual_parcelada = 100 - percentual_avista
    
    # Calcular vendas por modalidade
    vendas_avista = int(oculos_meta * (percentual_avista / 100))
    vendas_parcelada = oculos_meta - vendas_avista
    
    # Calcular comissões (SEMPRE valor fixo por venda conforme configuração)
    total_comissao_avista = vendas_avista * comissao_avista
    total_comissao_parcelada = vendas_parcelada * comissao_parcelada
    
    # Total mensal
    custo_total_captador = total_comissao_avista + total_comissao_parcelada
    
    # MEMÓRIA DE CÁLCULO COMPLETA
    memoria_calculo = f"""
    CÁLCULO CAPTADOR:
    • Meta de óculos: {oculos_meta} vendas/mês
    • Gatilho mínimo: {meta_minima_captador} vendas ✓
    • Distribuição: {percentual_avista}% à vista, {percentual_parcelada}% parcelada
    
    VENDAS POR MODALIDADE:
    • À vista: {vendas_avista} vendas × R$ {comissao_avista:.2f} = R$ {total_comissao_avista:.2f}
    • Parcelada: {vendas_parcelada} vendas × R$ {comissao_parcelada:.2f} = R$ {total_comissao_parcelada:.2f}
    
    TOTAL: R$ {custo_total_captador:.2f}/mês
    """
    
    # Salvar para referência e auditoria
    st.session_state.business_data['custo_captador_mensal_calculado'] = custo_total_captador
    st.session_state.business_data['memoria_calculo_captador'] = memoria_calculo
    
    return custo_total_captador

def safe_multiselect_default(stored_values, available_options, fallback_default=None):
    """Ensure multiselect default values are valid options"""
    if not stored_values:
        return fallback_default or []
    
    # Filter stored values to only include valid options
    valid_values = [v for v in stored_values if v in available_options]
    return valid_values if valid_values else (fallback_default or [])

# Business plan management functions
def get_saved_plans():
    """Get list of saved business plans"""
    if not os.path.exists('saved_plans'):
        os.makedirs('saved_plans')
    
    plans = []
    for filename in os.listdir('saved_plans'):
        if filename.endswith('.json'):
            try:
                with open(f'saved_plans/{filename}', 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    plans.append({
                        'filename': filename,
                        'name': data.get('plan_name', filename.replace('.json', '')),
                        'shop_name': data.get('business_data', {}).get('nome_otica', 'Sem nome'),
                        'created': data.get('created_at', 'Data desconhecida'),
                        'last_modified': data.get('last_modified', 'Não modificado')
                    })
            except:
                continue
    
    return sorted(plans, key=lambda x: x.get('last_modified', ''), reverse=True)

def save_business_plan(plan_name=None, force_new_version=False):
    """Save current business plan - replaces existing unless force_new_version=True"""
    if not os.path.exists('saved_plans'):
        os.makedirs('saved_plans')
    
    # Use shop name as plan name if not provided
    shop_name = st.session_state.business_data.get('nome_otica', '').strip()
    if not plan_name:
        plan_name = shop_name if shop_name else f"Plano_{datetime.now().strftime('%Y%m%d_%H%M')}"
    
    # Check if plan with same name exists
    base_filename = f"{plan_name}.json"
    filename = base_filename
    
    # Only create versioned name if force_new_version is True
    if force_new_version and os.path.exists(f'saved_plans/{base_filename}'):
        version = 2
        while os.path.exists(f'saved_plans/{plan_name}_Versao_{version}.json'):
            version += 1
        filename = f"{plan_name}_Versao_{version}.json"
    
    # Get existing creation date if file exists and we're updating
    created_at = datetime.now().isoformat()
    if os.path.exists(f'saved_plans/{filename}') and not force_new_version:
        try:
            with open(f'saved_plans/{filename}', 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
                created_at = existing_data.get('created_at', created_at)
        except:
            pass  # Use new creation date if can't read existing
    
    # Prepare data to save
    save_data = {
        'plan_name': plan_name,
        'business_data': st.session_state.business_data,
        'uploaded_files': {},  # File content would be saved separately in production
        'current_step': st.session_state.step,
        'created_at': created_at,
        'last_modified': datetime.now().isoformat()
    }
    
    # Save to file
    filepath = f'saved_plans/{filename}'
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(save_data, f, ensure_ascii=False, indent=2, default=str)
    
    return filename

def load_business_plan(file_path):
    """Load business plan from file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Load business data
        st.session_state.business_data = data.get('business_data', {})
        st.session_state.step = data.get('current_step', 1)
        
        # Restore uploaded files (simplified for this demo)
        st.session_state.uploaded_files = data.get('uploaded_files', {})
        
        return True
    except Exception as e:
        st.error(f"Erro ao carregar plano: {e}")
        return False

def delete_business_plan(file_path, plan_name):
    """Delete business plan file"""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
    except Exception as e:
        st.error(f"Erro ao excluir plano {plan_name}: {e}")
        return False

def create_new_plan():
    """Create new business plan (clear current data)"""
    # Clear all business data
    st.session_state.business_data = {}
    st.session_state.uploaded_files = {}
    st.session_state.step = 1
    
    # Clear drill-down selections
    keys_to_delete = []
    for key in list(st.session_state.keys()):
        if str(key).startswith(('show_', 'drill_')):
            keys_to_delete.append(key)
    for key in keys_to_delete:
        del st.session_state[key]
    
    # Clear legacy data file
    try:
        if os.path.exists('user_data.json'):
            os.remove('user_data.json')
    except:
        pass

def show_plan_manager():
    """Show business plan manager interface"""
    st.sidebar.subheader("📋 Projetos")
    
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        if st.button("📄 Novo", key="new_plan_btn", use_container_width=True):
            create_new_plan()
            st.sidebar.success("Novo plano criado!")
            st.rerun()
    
    with col2:
        if st.button("💾 Salvar", key="save_plan_btn", use_container_width=True):
            filename = save_business_plan()
            st.sidebar.success(f"Salvo: {filename}")
            st.rerun()
    
    # Show saved plans
    saved_plans = get_saved_plans()
    
    if saved_plans:
        st.sidebar.markdown("**Planos Salvos:**")
        
        for plan in saved_plans[:5]:  # Show only last 5
            col1, col2 = st.sidebar.columns([3, 1])
            
            with col1:
                if st.button(f"📂 {plan['name']}", key=f"load_{plan['filename']}", use_container_width=True):
                    if load_business_plan(f"saved_plans/{plan['filename']}"):
                        st.sidebar.success(f"Carregado: {plan['name']}")
                        st.rerun()
            
            with col2:
                # Usar form para fazer o botão HTML funcionar com Streamlit
                with st.form(key=f"delete_form_{plan['filename']}"):
                    st.markdown(f"""
                    <style>
                    div[data-testid="stForm"] {{
                        border: none !important;
                        padding: 0 !important;
                    }}
                    div[data-testid="stForm"] button[type="submit"] {{
                        background: linear-gradient(135deg, #ff4757 0%, #ff3742 50%, #e63946 100%) !important;
                        color: white !important;
                        border: 2px solid #ff6b7a !important;
                        border-radius: 15px !important;
                        font-size: 1.4rem !important;
                        font-weight: 700 !important;
                        padding: 0.8rem 1rem !important;
                        width: 100% !important;
                        min-height: 3rem !important;
                        box-shadow: 0 6px 20px rgba(255, 71, 87, 0.4), inset 0 2px 0 rgba(255, 255, 255, 0.3) !important;
                        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
                        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3) !important;
                        cursor: pointer !important;
                        outline: none !important;
                    }}
                    div[data-testid="stForm"] button[type="submit"]:hover {{
                        background: linear-gradient(135deg, #ff3742 0%, #e63946 50%, #c62d42 100%) !important;
                        transform: translateY(-3px) scale(1.05) !important;
                        box-shadow: 0 8px 25px rgba(255, 71, 87, 0.6), inset 0 2px 0 rgba(255, 255, 255, 0.4) !important;
                    }}
                    div[data-testid="stForm"] button[type="submit"]:active {{
                        transform: translateY(-1px) scale(0.98) !important;
                        box-shadow: 0 4px 15px rgba(255, 71, 87, 0.7), inset 0 3px 8px rgba(0, 0, 0, 0.3) !important;
                    }}
                    </style>
                    """, unsafe_allow_html=True)
                    
                    delete_clicked = st.form_submit_button("🗑️", help=f"Excluir {plan['name']}")
                    
                if delete_clicked:
                    st.session_state.confirm_delete_plan = plan
                    st.rerun()

# Legacy data functions (for backward compatibility)
def load_user_data():
    """Load user data from JSON file (legacy support)"""
    try:
        if os.path.exists('user_data.json'):
            with open('user_data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Only load if business_data is empty
            if not st.session_state.business_data:
                st.session_state.business_data = data.get('business_data', {})
                st.session_state.step = data.get('current_step', 1)
                st.session_state.uploaded_files = data.get('uploaded_files', {})
    except Exception as e:
        pass  # Silently fail for backward compatibility
    


def save_user_data():
    """Save user data to JSON file (legacy support + auto-save)"""
    if st.session_state.business_data:  # Only save if there's data
        try:
            # Garantir sincronização do DP antes de salvar
            if hasattr(st.session_state, 'funcionarios') and st.session_state.funcionarios:
                st.session_state.business_data['funcionarios_dp'] = st.session_state.funcionarios
            
            data = {
                'business_data': st.session_state.business_data,
                'uploaded_files': st.session_state.uploaded_files,
                'current_step': st.session_state.step,
                'last_saved': datetime.now().isoformat()
            }
            
            # Auto-save to legacy file
            with open('user_data.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2, default=str)
        except Exception as e:
            print(f"Auto-save failed: {e}")  # Debug for development

def auto_save_drill_down_selection(key, value):
    """Save drill-down selection immediately"""
    st.session_state.business_data[f"drill_{key}"] = value
    save_user_data()

def get_drill_down_selection(key, default=None):
    """Get saved drill-down selection"""
    return st.session_state.business_data.get(f"drill_{key}", default)

def main():
    # Sistema de autenticação - Verificar login obrigatório
    auth = require_authentication()
    
    # CSS com paleta de cores personalizada
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Paleta de cores */
    :root {
        --primary-gold: #d4af37;
        --secondary-gold: #b8860b;
        --warm-cream: #f0ede5;
        --soft-brown: #8b7355;
        --dark-brown: #5d4e37;
        --navy-blue: #2c3e50;
        --text-primary: #2c3e50;
        --text-secondary: #5d4e37;
        --background-primary: #f0ede5;
        --background-secondary: #e8e3db;
    }
    
    html, body, [class*="css"] {
        font-family: 'Inter', 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif !important;
    }
    
    .stApp {
        font-family: 'Inter', 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif !important;
        background: linear-gradient(135deg, var(--background-secondary) 0%, var(--background-primary) 100%) !important;
        color: var(--text-primary) !important;
    }
    
    /* Títulos principais com cores da paleta */
    h1 {
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
        color: var(--text-primary) !important;
        line-height: 1.2 !important;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1) !important;
    }
    
    h2, h3 {
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        color: var(--text-secondary) !important;
        line-height: 1.3 !important;
    }
    
    h4, h5, h6 {
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        color: var(--soft-brown) !important;
        line-height: 1.3 !important;
    }
    
    /* Textos principais com melhor contraste */
    .stMarkdown, .stText, p, span, div, li {
        font-family: 'Inter', 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif !important;
        line-height: 1.6 !important;
        font-weight: 400 !important;
        color: var(--text-primary) !important;
    }
    
    /* Sidebar escura e elegante */
    .css-1d391kg, [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a252f 0%, #2c3e50 100%) !important;
        font-family: 'Inter', sans-serif !important;
        backdrop-filter: blur(20px) !important;
        border-right: 1px solid rgba(212, 175, 55, 0.3) !important;
        box-shadow: 2px 0 20px rgba(0, 0, 0, 0.3) !important;
    }
    
    /* Força sidebar em todas as variações de classe */
    .stSidebar, .stSidebar > div, section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a252f 0%, #2c3e50 100%) !important;
    }
    
    .css-1d391kg::before, [data-testid="stSidebar"]::before {
        content: '' !important;
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        right: 0 !important;
        height: 2px !important;
        background: linear-gradient(90deg, var(--primary-gold), var(--secondary-gold), var(--primary-gold)) !important;
    }
    
    .css-1d391kg h1, .css-1d391kg h2, .css-1d391kg h3, 
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: var(--primary-gold) !important;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2) !important;
    }
    
    .css-1d391kg p, .css-1d391kg span, .css-1d391kg div, .css-1d391kg li,
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] div, [data-testid="stSidebar"] li {
        color: rgba(255, 255, 255, 0.95) !important;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1) !important;
    }
    
    /* Botões da sidebar com efeito 3D premium */
    .stSidebar .stButton > button {
        background: linear-gradient(145deg, rgba(26, 37, 47, 0.8), rgba(15, 25, 35, 0.9)) !important;
        color: rgba(255, 255, 255, 0.85) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        font-weight: 500 !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        backdrop-filter: blur(15px) !important;
        margin: 3px 0 !important;
        padding: 10px 18px !important;
        box-shadow: 
            0 4px 8px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.1),
            inset 0 -1px 0 rgba(0, 0, 0, 0.2) !important;
        position: relative !important;
    }
    
    .stSidebar .stButton > button:hover {
        background: linear-gradient(145deg, rgba(212, 175, 55, 0.2), rgba(184, 134, 11, 0.15)) !important;
        border-color: rgba(212, 175, 55, 0.4) !important;
        color: rgba(255, 255, 255, 0.95) !important;
        transform: translateY(-2px) translateX(3px) scale(1.02) !important;
        box-shadow: 
            0 8px 20px rgba(0, 0, 0, 0.4),
            0 2px 10px rgba(212, 175, 55, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.2),
            inset 0 -1px 0 rgba(0, 0, 0, 0.3) !important;
    }
    
    /* Botão ativo na sidebar com efeito 3D dourado */
    .stSidebar .stButton > button[kind="primary"] {
        background: linear-gradient(145deg, var(--primary-gold), var(--secondary-gold)) !important;
        color: white !important;
        border: none !important;
        font-weight: 600 !important;
        transform: translateX(5px) !important;
        box-shadow: 
            0 6px 16px rgba(212, 175, 55, 0.5),
            0 2px 8px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.3),
            inset 0 -1px 0 rgba(184, 134, 11, 0.8) !important;
    }
    
    /* Botões não-selecionados com efeito 3D suave */
    .stSidebar .stButton > button:not([kind="primary"]):not(:hover) {
        background: linear-gradient(145deg, rgba(26, 37, 47, 0.7), rgba(15, 25, 35, 0.8)) !important;
        border-color: rgba(255, 255, 255, 0.08) !important;
        color: rgba(255, 255, 255, 0.75) !important;
        box-shadow: 
            0 2px 6px rgba(0, 0, 0, 0.25),
            inset 0 1px 0 rgba(255, 255, 255, 0.08),
            inset 0 -1px 0 rgba(0, 0, 0, 0.15) !important;
    }
    
    /* Melhorar contraste dos textos na sidebar */
    .stSidebar .stMarkdown h1, .stSidebar .stMarkdown h2, .stSidebar .stMarkdown h3 {
        color: var(--primary-gold) !important;
        text-shadow: 0 1px 3px rgba(0, 0, 0, 0.3) !important;
    }
    
    /* Texto da navegação mais visível */
    .stSidebar .stMarkdown p, .stSidebar .stText {
        color: rgba(255, 255, 255, 0.9) !important;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2) !important;
    }
    
    /* Botões primários com efeito 3D premium */
    .stButton > button[kind="primary"] {
        background: linear-gradient(145deg, var(--primary-gold) 0%, var(--secondary-gold) 100%) !important;
        border: none !important;
        color: white !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        border-radius: 12px !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        padding: 0.6rem 1.5rem !important;
        text-shadow: 0 1px 3px rgba(0, 0, 0, 0.4) !important;
        box-shadow: 
            0 6px 16px rgba(212, 175, 55, 0.4),
            0 2px 8px rgba(0, 0, 0, 0.25),
            inset 0 1px 0 rgba(255, 255, 255, 0.3),
            inset 0 -1px 0 rgba(184, 134, 11, 0.8) !important;
        position: relative !important;
    }
    
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(145deg, var(--secondary-gold) 0%, var(--primary-gold) 100%) !important;
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 
            0 10px 25px rgba(212, 175, 55, 0.5),
            0 4px 15px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.4),
            inset 0 -1px 0 rgba(184, 134, 11, 0.9) !important;
    }
    
    /* Botões secundários com efeito 3D suave */
    .stButton > button[kind="secondary"] {
        background: linear-gradient(145deg, rgba(255, 255, 255, 0.95), rgba(245, 242, 235, 0.9)) !important;
        backdrop-filter: blur(15px) !important;
        border: 2px solid var(--soft-brown) !important;
        color: var(--text-secondary) !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        border-radius: 12px !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        padding: 0.6rem 1.5rem !important;
        box-shadow: 
            0 4px 12px rgba(139, 115, 85, 0.2),
            0 1px 4px rgba(0, 0, 0, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.8),
            inset 0 -1px 0 rgba(139, 115, 85, 0.2) !important;
        position: relative !important;
    }
    
    .stButton > button[kind="secondary"]:hover {
        background: linear-gradient(135deg, var(--olive-brown) 0%, var(--dark-brown) 100%) !important;
        color: white !important;
        box-shadow: 0 6px 20px rgba(133, 115, 75, 0.3) !important;
        transform: translateY(-2px) !important;
    }
    
    /* Botões normais com design sofisticado */
    .stButton > button {
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        font-size: 14px !important;
        border-radius: 10px !important;
        border: 1px solid rgba(189, 154, 110, 0.3) !important;
        color: var(--dark-brown) !important;
        background: rgba(255, 255, 255, 0.8) !important;
        backdrop-filter: blur(5px) !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1) !important;
        transition: all 0.3s ease !important;
        padding: 0.5rem 1.2rem !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, var(--primary-gold) 0%, var(--secondary-gold) 100%) !important;
        color: white !important;
        border-color: transparent !important;
        box-shadow: 0 4px 15px rgba(189, 154, 110, 0.3) !important;
        transform: translateY(-1px) !important;
    }
    
    /* Inputs suaves com fundo creme */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > select,
    .stTextArea > div > div > textarea {
        font-family: 'Inter', sans-serif !important;
        font-size: 14px !important;
        line-height: 1.5 !important;
        border: 2px solid rgba(212, 175, 55, 0.2) !important;
        border-radius: 8px !important;
        background: var(--background-primary) !important;
        color: var(--text-primary) !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05) !important;
        transition: all 0.3s ease !important;
        padding: 0.75rem 1rem !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--primary-gold) !important;
        box-shadow: 0 0 0 3px rgba(212, 175, 55, 0.15), 0 4px 12px rgba(0, 0, 0, 0.1) !important;
        background: #ffffff !important;
        outline: none !important;
    }
    
    /* Labels dos inputs */
    .stTextInput > label,
    .stNumberInput > label,
    .stSelectbox > label,
    .stMultiSelect > label,
    .stTextArea > label {
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        font-size: 14px !important;
        color: var(--dark-brown) !important;
    }
    
    /* Abas suaves com design harmonioso */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: var(--warm-cream) !important;
        border-radius: 12px !important;
        padding: 4px !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1) !important;
        border: 1px solid rgba(212, 175, 55, 0.1) !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        color: var(--text-secondary) !important;
        border-radius: 8px !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        padding: 0.75rem 1.5rem !important;
        margin: 0 !important;
        border: none !important;
        transition: all 0.3s ease !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, var(--primary-gold) 0%, var(--secondary-gold) 100%) !important;
        color: white !important;
        box-shadow: 0 2px 8px rgba(212, 175, 55, 0.3) !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover:not([aria-selected="true"]) {
        background: rgba(212, 175, 55, 0.1) !important;
        color: var(--text-primary) !important;
    }
    
    /* Alertas com cores da paleta */
    .stAlert {
        border-radius: 8px !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    .stSuccess {
        background-color: rgba(189, 154, 110, 0.1) !important;
        border: 1px solid var(--primary-gold) !important;
        color: var(--dark-brown) !important;
    }
    
    .stWarning {
        background-color: rgba(133, 115, 75, 0.1) !important;
        border: 1px solid var(--olive-brown) !important;
        color: var(--dark-brown) !important;
    }
    
    .stError {
        background-color: rgba(122, 64, 34, 0.1) !important;
        border: 1px solid var(--dark-brown) !important;
        color: var(--dark-brown) !important;
    }
    
    /* Remover todas as cores vermelhas/rosas do sistema */
    div[data-testid="stMarkdownContainer"] > div > p > strong {
        color: var(--dark-brown) !important;
    }
    
    /* Progress indicator da navegação */
    .stProgress {
        background-color: var(--olive-brown) !important;
    }
    
    /* Remover cor vermelha de elementos específicos */
    .css-1544g2n, .css-1d391kg .css-1544g2n {
        color: var(--primary-gold) !important;
    }
    
    /* Substituir qualquer vermelho por cores da paleta */
    [style*="color: red"], [style*="color: #ff"], [style*="color: rgb(255"] {
        color: var(--dark-brown) !important;
    }
    
    /* Seletores específicos para remover vermelho */
    .stSelectbox > div > div > div {
        color: var(--dark-gray) !important;
    }
    
    /* Info boxes */
    .stInfo {
        background-color: rgba(171, 140, 110, 0.1) !important;
        border: 1px solid var(--secondary-gold) !important;
        color: var(--dark-brown) !important;
    }
    
    /* Métricas elegantes com glassmorphism */
    [data-testid="metric-container"] {
        font-family: 'Inter', sans-serif !important;
        background: linear-gradient(135deg, var(--primary-gold), var(--secondary-gold)) !important;
        color: white !important;
        padding: 1.5rem !important;
        border-radius: 16px !important;
        box-shadow: 0 8px 32px rgba(189, 154, 110, 0.3) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    [data-testid="metric-container"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 12px 40px rgba(189, 154, 110, 0.4) !important;
    }
    
    [data-testid="metric-container"]::before {
        content: '' !important;
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        right: 0 !important;
        height: 1px !important;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent) !important;
    }
    
    /* Expander elegante com glassmorphism */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, var(--secondary-gold) 0%, var(--olive-brown) 100%) !important;
        color: white !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 15px rgba(171, 140, 110, 0.3) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        backdrop-filter: blur(10px) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        padding: 1rem 1.5rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    .streamlit-expanderHeader:hover {
        background: linear-gradient(135deg, var(--primary-gold) 0%, var(--secondary-gold) 100%) !important;
        box-shadow: 0 6px 20px rgba(189, 154, 110, 0.4) !important;
        transform: translateY(-1px) !important;
    }
    
    .streamlit-expanderContent {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 0 0 12px 12px !important;
        border: 1px solid rgba(189, 154, 110, 0.1) !important;
        border-top: none !important;
        padding: 1.5rem !important;
        margin-top: -0.5rem !important;
    }
    
    /* Progress bar elegante */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, var(--primary-gold), var(--secondary-gold)) !important;
        border-radius: 10px !important;
        box-shadow: 0 2px 8px rgba(189, 154, 110, 0.3) !important;
    }
    
    .stProgress > div > div {
        background-color: rgba(189, 154, 110, 0.1) !important;
        border-radius: 10px !important;
        backdrop-filter: blur(5px) !important;
    }
    
    /* Multiselect elegante */
    .stMultiSelect > div > div {
        border: 2px solid rgba(189, 154, 110, 0.3) !important;
        border-radius: 12px !important;
        background: rgba(255, 255, 255, 0.8) !important;
        backdrop-filter: blur(10px) !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    
    .stMultiSelect > div > div:focus-within {
        border-color: var(--primary-gold) !important;
        box-shadow: 0 0 0 3px rgba(189, 154, 110, 0.2), 0 8px 25px rgba(0, 0, 0, 0.1) !important;
        background: rgba(255, 255, 255, 0.95) !important;
        transform: translateY(-1px) !important;
    }
    
    /* Botão de lixeira elegante com gradiente vermelho e efeito 3D - múltiplos seletores */
    button[data-testid*="del_"],
    button[key*="del_"],
    .stButton > button:has-text("🗑️"),
    .stButton > button[title*="Excluir"],
    .stButton button:contains("🗑️") {
        background: linear-gradient(135deg, #ff4757 0%, #ff3838 50%, #c44569 100%) !important;
        color: white !important;
        border: 2px solid #ff6b7a !important;
        border-radius: 15px !important;
        font-size: 1.4rem !important;
        font-weight: 700 !important;
        padding: 0.8rem 1.2rem !important;
        box-shadow: 
            0 8px 25px rgba(255, 71, 87, 0.4),
            inset 0 2px 0 rgba(255, 255, 255, 0.3),
            0 0 0 0 rgba(255, 71, 87, 0) !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        position: relative !important;
        overflow: hidden !important;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3) !important;
        cursor: pointer !important;
    }
    
    button[data-testid*="del_"]:hover,
    button[key*="del_"]:hover,
    .stButton > button:has-text("🗑️"):hover,
    .stButton > button[title*="Excluir"]:hover,
    .stButton button:contains("🗑️"):hover {
        background: linear-gradient(135deg, #ff3838 0%, #ff2f2f 50%, #b73e56 100%) !important;
        border-color: #ff5757 !important;
        transform: translateY(-3px) scale(1.05) !important;
        box-shadow: 
            0 12px 35px rgba(255, 71, 87, 0.6),
            inset 0 2px 0 rgba(255, 255, 255, 0.4),
            0 0 0 3px rgba(255, 71, 87, 0.3) !important;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.4) !important;
    }
    
    button[data-testid*="del_"]:active,
    button[key*="del_"]:active,
    .stButton > button:has-text("🗑️"):active,
    .stButton > button[title*="Excluir"]:active,
    .stButton button:contains("🗑️"):active {
        transform: translateY(-1px) scale(0.98) !important;
        box-shadow: 
            0 6px 20px rgba(255, 71, 87, 0.7),
            inset 0 3px 8px rgba(0, 0, 0, 0.3) !important;
    }
    
    /* Fallback para todos os botões na coluna da lixeira */
    .stColumns > div:last-child .stButton > button {
        background: linear-gradient(135deg, #ff4757 0%, #ff3838 50%, #c44569 100%) !important;
        color: white !important;
        border: 2px solid #ff6b7a !important;
        border-radius: 15px !important;
        font-size: 1.4rem !important;
        font-weight: 700 !important;
        padding: 0.8rem 1.2rem !important;
        box-shadow: 
            0 8px 25px rgba(255, 71, 87, 0.4),
            inset 0 2px 0 rgba(255, 255, 255, 0.3) !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3) !important;
    }
    
    .stColumns > div:last-child .stButton > button:hover {
        background: linear-gradient(135deg, #ff3838 0%, #ff2f2f 50%, #b73e56 100%) !important;
        transform: translateY(-3px) scale(1.05) !important;
        box-shadow: 
            0 12px 35px rgba(255, 71, 87, 0.6),
            inset 0 2px 0 rgba(255, 255, 255, 0.4),
            0 0 0 3px rgba(255, 71, 87, 0.3) !important;
    }
    
    /* Containers principais com fundo suave */
    .main > div {
        background: var(--background-primary) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(212, 175, 55, 0.1) !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08) !important;
        margin: 1rem !important;
        padding: 2rem !important;
    }
    
    /* Cards com efeito de elevação */
    .element-container {
        transition: all 0.3s ease !important;
    }
    
    .element-container:hover {
        transform: translateY(-2px) !important;
    }
    
    /* Checkboxes e radio buttons */
    .stCheckbox > label, .stRadio > label {
        color: var(--dark-brown) !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
    }
    
    /* Eliminar completamente qualquer cor vermelha/rosa */
    * {
        color: inherit !important;
    }
    
    /* Forçar cores da paleta em elementos problemáticos */
    .css-1629p8f, .css-1629p8f *, 
    .css-10trblm, .css-10trblm *,
    .css-1aumxhk, .css-1aumxhk * {
        color: var(--dark-brown) !important;
    }
    
    /* Navigation e progresso */
    .css-1vbkxwb, .css-1vbkxwb * {
        color: var(--primary-gold) !important;
    }
    
    /* Remover bordas vermelhas de qualquer elemento */
    * {
        border-color: inherit !important;
    }
    
    /* Sobrescrever qualquer cor de fundo vermelha */
    div[style*="background-color: red"], 
    div[style*="background-color: #ff"],
    div[style*="background: red"],
    div[style*="background: #ff"] {
        background-color: var(--secondary-gold) !important;
    }
    
    /* Tags específicas que podem ter cor vermelha */
    .stTag, .css-16huue1, .css-1cpxqw2 {
        background-color: var(--olive-brown) !important;
        color: white !important;
        border: 1px solid var(--olive-brown) !important;
    }
    
    /* Seletores de cores do multiselect */
    .stMultiSelect span[data-baseweb="tag"] {
        background-color: var(--secondary-gold) !important;
        color: white !important;
    }
    
    /* Links */
    a, a:visited, a:hover, a:active {
        color: var(--primary-gold) !important;
    }
    
    /* Headers específicos */
    .css-1avcm0n, .css-1avcm0n * {
        color: var(--dark-brown) !important;
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        font-family: 'Inter', 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif !important;
        font-weight: 500 !important;
        font-size: 14px !important;
    }
    
    /* Alertas e notificações */
    .stAlert {
        font-family: 'Inter', 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif !important;
        line-height: 1.5 !important;
    }
    
    /* Tabelas */
    .stDataFrame {
        font-family: 'Inter', 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif !important;
        font-size: 13px !important;
    }
    
    /* Código e texto monospace */
    code, pre {
        font-family: 'SF Mono', 'Monaco', 'Inconsolata', 'Roboto Mono', monospace !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    load_user_data()
    
    # Check for delete confirmation dialog (full screen overlay)
    if st.session_state.get('confirm_delete_plan'):
        plan = st.session_state.confirm_delete_plan
        
        # Create full-screen overlay with dark background
        st.markdown("""
        <style>
        .delete-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: rgba(0, 0, 0, 0.8);
            z-index: 9999;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .delete-dialog {
            background: white;
            padding: 3rem;
            border-radius: 20px;
            text-align: center;
            max-width: 500px;
            width: 90%;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
            border: 3px solid #dc3545;
        }
        .delete-icon {
            font-size: 4rem;
            color: #dc3545;
            margin-bottom: 1rem;
        }
        .delete-title {
            font-size: 1.5rem;
            font-weight: bold;
            color: #dc3545;
            margin-bottom: 1rem;
        }
        .delete-message {
            font-size: 1.1rem;
            color: #333;
            margin-bottom: 2rem;
            line-height: 1.5;
        }
        .plan-name {
            background: #f8f9fa;
            padding: 0.5rem 1rem;
            border-radius: 8px;
            border-left: 4px solid #dc3545;
            margin: 1rem 0;
            font-weight: bold;
            color: #dc3545;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Large confirmation dialog
        st.markdown("### 🗑️ CONFIRMAÇÃO DE EXCLUSÃO")
        st.error("⚠️ **ATENÇÃO: Esta ação não pode ser desfeita!**")
        
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #fee2e2, #fecaca);
            padding: 2rem;
            border-radius: 15px;
            border: 2px solid #dc3545;
            text-align: center;
            margin: 2rem 0;
            box-shadow: 0 8px 25px rgba(220, 53, 69, 0.3);
        ">
            <div style="font-size: 4rem; margin-bottom: 1rem;">🗑️</div>
            <div style="font-size: 1.3rem; font-weight: bold; color: #dc3545; margin-bottom: 1rem;">
                Você tem certeza que deseja excluir seu plano de negócio?
            </div>
            <div style="
                background: white;
                padding: 1rem;
                border-radius: 8px;
                border-left: 4px solid #dc3545;
                margin: 1rem 0;
                font-weight: bold;
                color: #dc3545;
                font-size: 1.1rem;
            ">
                📄 {plan['name']}
            </div>
            <div style="color: #666; font-size: 1rem; margin-top: 1rem;">
                Todo o trabalho que você fez será perdido permanentemente.<br>
                Não será possível recuperar este plano depois de excluído.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Action buttons
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            col_cancel, col_delete = st.columns(2)
            
            with col_cancel:
                if st.button("❌ Cancelar", key="cancel_delete", use_container_width=True, type="secondary"):
                    del st.session_state.confirm_delete_plan
                    st.rerun()
            
            with col_delete:
                if st.button("🗑️ SIM, EXCLUIR", key="confirm_delete", use_container_width=True, type="primary"):
                    if delete_business_plan(f"saved_plans/{plan['filename']}", plan['name']):
                        st.success(f"✅ Plano '{plan['name']}' foi excluído com sucesso!")
                        del st.session_state.confirm_delete_plan
                        st.rerun()
                    else:
                        st.error("❌ Erro ao excluir o plano. Tente novamente.")
        
        st.stop()  # Don't show the rest of the interface
    
    # Sidebar with navigation and project management
    st.sidebar.title("📊 Plano de Negócios")
    
    # Project management section
    show_plan_manager()
    
    st.sidebar.markdown("---")
    
    # Navigation for exactly 12 steps
    st.sidebar.markdown("### 🧭 Navegação")
    
    steps = {
        1: "1. Sumário Executivo",
        2: "2. Análise de Mercado", 
        3: "3. Público-Alvo",
        4: "4. Concorrência",
        5: "5. Produtos e Serviços",
        6: "6. Estratégia de Marketing",
        7: "7. Plano Operacional",
        8: "8. Gestão de Pessoas",
        9: "9. Investimento Inicial",
        10: "10. Projeções Financeiras",
        11: "11. Análise de Viabilidade",
        12: "12. Cenários e Riscos"
    }
    
    # Current step indicator
    current_step = st.session_state.step
    st.sidebar.markdown(f"**📍 Etapa Atual:** {steps.get(current_step, 'N/A')}")
    
    # Progress bar
    progress = min(current_step / 12, 1.0)
    st.sidebar.progress(progress)
    st.sidebar.caption(f"Progresso: {progress*100:.0f}% concluído")
    
    # Navigation mode selector - Initialize to steps if not exists
    if 'current_view' not in st.session_state:
        st.session_state.current_view = 'steps'
    
    # Home button - always returns to main steps
    if st.sidebar.button("🏠 Início (Etapas)", key="home_button", type="primary", use_container_width=True):
        # Clear all tool flags to return to main steps
        for key in ['show_premissas', 'show_integrated_cost_analyzer', 'show_unified_cost_analyzer', 'show_plan_validator', 'show_lens_pricing', 'show_employee_manager', 'show_simulation_simple', 'show_fluxo_vital', 'show_investor_report', 'show_entrepreneur_summary']:
            if key in st.session_state:
                del st.session_state[key]
        st.session_state.current_view = 'steps'
        st.rerun()
    
    st.sidebar.markdown("---")
    
    # Direct navigation to all steps
    st.sidebar.markdown("**Acesso Direto às Etapas:**")
    
    for step_num, step_name in steps.items():
        button_type = "primary" if (step_num == current_step and st.session_state.current_view == 'steps') else "secondary"
        if st.sidebar.button(step_name, key=f"nav_step_{step_num}", type=button_type, use_container_width=True):
            st.session_state.step = step_num
            st.session_state.current_view = 'steps'
            # Clear all tool flags
            for key in ['show_premissas', 'show_integrated_cost_analyzer', 'show_unified_cost_analyzer', 'show_plan_validator', 'show_lens_pricing', 'show_employee_manager', 'show_fluxo_vital', 'show_investor_report', 'show_entrepreneur_summary']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
    
    st.sidebar.markdown("---")
    
    # Tools navigation with unified system
    tools = {
        'premissas': {'name': '⚙️ Premissas', 'key': 'show_premissas'},
        'integrated_cost': {'name': '🔬 Análise Integrada de Custos', 'key': 'show_integrated_cost_analyzer'},
        'validator': {'name': '🔍 Validador do Plano', 'key': 'show_plan_validator'},
        'employee': {'name': '👥 DP e Tributação', 'key': 'show_employee_manager'},
        'vital': {'name': '🚀 Fluxo Vital', 'key': 'show_fluxo_vital'},
        'investor': {'name': '📊 Relatório Investidor', 'key': 'show_investor_report'},
        'entrepreneur': {'name': '💡 Resumo Empreendedor', 'key': 'show_entrepreneur_summary'}
    }
    
    for tool_id, tool_info in tools.items():
        button_type = "primary" if st.session_state.current_view == tool_id else "secondary"
        if st.sidebar.button(tool_info['name'], key=f"nav_{tool_id}", type=button_type, use_container_width=True):
            # Clear all other tool flags
            for key in ['show_premissas', 'show_integrated_cost_analyzer', 'show_unified_cost_analyzer', 'show_plan_validator', 'show_lens_pricing', 'show_employee_manager', 'show_fluxo_vital', 'show_investor_report', 'show_entrepreneur_summary']:
                if key in st.session_state:
                    del st.session_state[key]
            # Set the selected tool
            st.session_state[tool_info['key']] = True
            st.session_state.current_view = tool_id
            st.rerun()
    
    # Show tools or main content - Only if explicitly requested
    if st.session_state.current_view == 'premissas' and st.session_state.get('show_premissas', False):
        show_premissas()
    elif st.session_state.current_view == 'integrated_cost' and st.session_state.get('show_integrated_cost_analyzer', False):
        show_integrated_cost_analyzer_step10()
    elif st.session_state.current_view == 'unified_cost' and st.session_state.get('show_unified_cost_analyzer', False):
        show_unified_cost_analyzer()
    elif st.session_state.current_view == 'validator' and st.session_state.get('show_plan_validator', False):
        show_plan_validator_tool()

    elif st.session_state.current_view == 'employee' and st.session_state.get('show_employee_manager', False):
        show_employee_manager()
    elif st.session_state.current_view == 'vital' and st.session_state.get('show_fluxo_vital', False):
        show_fluxo_vital_tool()
    elif st.session_state.current_view == 'investor' and st.session_state.get('show_investor_report', False):
        show_investor_report_tool()
    elif st.session_state.current_view == 'entrepreneur' and st.session_state.get('show_entrepreneur_summary', False):
        show_entrepreneur_summary_tool()
    else:
        # Main content based on step (exactly 12 steps)
        if st.session_state.step == 1:
            show_step_1()  # Sumário Executivo
        elif st.session_state.step == 2:
            show_step_2()  # Análise de Mercado
        elif st.session_state.step == 3:
            show_step_3()  # Público-Alvo
        elif st.session_state.step == 4:
            show_step_4()  # Concorrência
        elif st.session_state.step == 5:
            show_step_5()  # Produtos e Serviços (antigo 3.5)
        elif st.session_state.step == 6:
            show_step_6()  # Estratégia de Marketing
        elif st.session_state.step == 7:
            show_step_7()  # Plano Operacional
        elif st.session_state.step == 8:
            show_step_8()  # Gestão de Pessoas
        elif st.session_state.step == 9:
            show_step_9()  # Investimento Inicial
        elif st.session_state.step == 10:
            show_step_10()  # Projeções Financeiras
        elif st.session_state.step == 11:
            show_step_11()  # Análise de Viabilidade
        elif st.session_state.step == 12:
            show_step_12()  # Cenários e Riscos

# Step functions (exactly 12 steps)
def show_step_1():
    """Etapa 1: Informações Iniciais"""
    st.header("1️⃣ Informações Iniciais")
    st.markdown("**FASE 1: CONCEITO** - Defina a identidade e visão da sua ótica")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🏪 Informações Básicas")
        
        nome_otica = st.text_input(
            "Nome da ótica *",
            value=st.session_state.business_data.get('nome_otica', ''),
            placeholder="Ex: Ótica Vista Clara"
        )
        # Auto-save nome_otica
        if nome_otica != st.session_state.business_data.get('nome_otica'):
            st.session_state.business_data['nome_otica'] = nome_otica
            save_user_data()
        
        cnpj = st.text_input(
            "CNPJ",
            value=st.session_state.business_data.get('cnpj', ''),
            placeholder="00.000.000/0001-00"
        )
        # Auto-save cnpj
        if cnpj != st.session_state.business_data.get('cnpj'):
            st.session_state.business_data['cnpj'] = cnpj
            save_user_data()
        
        tipos_empresa_list = ["MEI", "Microempresa", "Empresa de Pequeno Porte", "Ltda", "Outro"]
        current_tipo_empresa = st.session_state.business_data.get('tipo_empresa', 'MEI')
        current_tipo_empresa_index = tipos_empresa_list.index(current_tipo_empresa) if current_tipo_empresa in tipos_empresa_list else 0
        
        tipo_empresa = st.selectbox(
            "Tipo de empresa *",
            tipos_empresa_list,
            index=current_tipo_empresa_index
        )
        # Auto-save tipo_empresa com validação crítica
        if tipo_empresa != st.session_state.business_data.get('tipo_empresa'):
            # Validação crítica de mudança de regime
            old_regime = st.session_state.business_data.get('tipo_empresa', 'MEI')
            
            # Validar compatibilidade com receita
            objetivo_faturamento = st.session_state.business_data.get('objetivo_faturamento', 0)
            receita_anual = objetivo_faturamento * 12
            
            # Validar limites MEI
            if tipo_empresa == 'MEI':
                if receita_anual > 81000:
                    st.error(f"🚨 **PROBLEMA**: Sua meta é muito alta para MEI")
                    st.write(f"Você quer faturar R$ {receita_anual:,.0f} por ano, mas o MEI só permite até R$ 81.000")
                    st.warning("**Escolha uma das opções:**")
                    st.write("• 💡 Diminuir sua meta para R$ 6.750 por mês (máximo do MEI)")
                    st.write("• 🏢 Mudar para 'Microempresa' (pode faturar mais, mas paga mais impostos)")
                    st.info("💰 **Dica**: MEI paga só R$ 76 por mês. Microempresa paga % sobre as vendas.")
                    st.stop()
                
                # Validar funcionários
                funcionarios_count = len(st.session_state.business_data.get('funcionarios_planejados', []))
                if funcionarios_count > 1:
                    st.error(f"🚨 **PROBLEMA**: Você tem muitos funcionários para MEI")
                    st.write(f"Você planejou {funcionarios_count} funcionários, mas o MEI só permite 1 pessoa trabalhando")
                    st.warning("**Escolha uma das opções:**")
                    st.write("• 👤 Trabalhar só você (sem funcionários)")
                    st.write("• 🏢 Mudar para 'Microempresa' (pode ter até 9 funcionários)")
                    st.info("💡 **Explicação**: MEI é para negócios pequenos, só o dono trabalhando.")
                    st.stop()
            
            # Alertar sobre mudanças importantes
            if old_regime != tipo_empresa:
                if old_regime == 'MEI' and tipo_empresa != 'MEI':
                    st.warning(f"🔄 **MUDANÇA DE REGIME**: {old_regime} → {tipo_empresa}")
                    
                    # Calcular impacto tributário
                    if tipo_empresa == 'Microempresa':
                        custo_mei_mes = 76.60  # MEI 2024
                        custo_simples_estimado = receita_anual * 0.06 / 12  # ~6% Simples Nacional
                        diferenca_mensal = custo_simples_estimado - custo_mei_mes
                        
                        st.info(f"**Impacto Tributário Estimado:**")
                        st.write(f"• MEI: R$ {custo_mei_mes:.2f}/mês")
                        st.write(f"• Simples Nacional: R$ {custo_simples_estimado:.2f}/mês")
                        st.write(f"• Diferença: +R$ {diferenca_mensal:.2f}/mês")
                        
                        if diferenca_mensal > 500:
                            st.warning("⚠️ Impacto tributário significativo! Revisar viabilidade.")
            
            st.session_state.business_data['tipo_empresa'] = tipo_empresa
            save_user_data()
        
        endereco = st.text_input(
            "Endereço *",
            value=st.session_state.business_data.get('endereco', ''),
            placeholder="Rua, número, bairro"
        )
        # Auto-save endereco
        if endereco != st.session_state.business_data.get('endereco'):
            st.session_state.business_data['endereco'] = endereco
            save_user_data()
        
        col3, col4 = st.columns(2)
        with col3:
            cidade = st.text_input(
                "Cidade *",
                value=st.session_state.business_data.get('cidade', ''),
                placeholder="Ex: São Paulo"
            )
            # Auto-save cidade
            if cidade != st.session_state.business_data.get('cidade'):
                st.session_state.business_data['cidade'] = cidade
                save_user_data()
        
        with col4:
            # Get current state value
            estados_list = ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"]
            current_estado = st.session_state.business_data.get('estado', 'SP')
            current_index = estados_list.index(current_estado) if current_estado in estados_list else 22
            
            estado = st.selectbox(
                "Estado",
                estados_list,
                index=current_index
            )
            
            # Auto-save immediately when changed
            if estado != st.session_state.business_data.get('estado'):
                st.session_state.business_data['estado'] = estado
                save_user_data()
    
    with col2:
        st.subheader("📊 Características")
        
        area_loja = st.number_input(
            "Área da loja (m²) *",
            min_value=0.0,
            value=float(st.session_state.business_data.get('area_loja', 50)),
            step=5.0
        )
        # Auto-save area_loja
        if area_loja != st.session_state.business_data.get('area_loja'):
            st.session_state.business_data['area_loja'] = area_loja
            save_user_data()
        
        tipos_list = ["Loja de Rua", "Shopping Center", "Galeria", "Centro Comercial"]
        current_tipo = st.session_state.business_data.get('tipo_estabelecimento', 'Loja de Rua')
        current_tipo_index = tipos_list.index(current_tipo) if current_tipo in tipos_list else 0
        
        tipo_estabelecimento = st.selectbox(
            "Tipo de estabelecimento",
            tipos_list,
            index=current_tipo_index
        )
        
        # Auto-save immediately when changed
        if tipo_estabelecimento != st.session_state.business_data.get('tipo_estabelecimento'):
            st.session_state.business_data['tipo_estabelecimento'] = tipo_estabelecimento
            save_user_data()
        
        exp_list = ["Nenhuma", "1-2 anos", "3-5 anos", "5+ anos"]
        current_exp = st.session_state.business_data.get('experiencia', 'Nenhuma')
        current_exp_index = exp_list.index(current_exp) if current_exp in exp_list else 0
        
        experiencia = st.selectbox(
            "Experiência no setor",
            exp_list,
            index=current_exp_index
        )
        
        # Auto-save immediately when changed
        if experiencia != st.session_state.business_data.get('experiencia'):
            st.session_state.business_data['experiencia'] = experiencia
            save_user_data()
        
        objetivo_faturamento = st.number_input(
            "Objetivo de faturamento mensal",
            min_value=0.0,
            value=float(st.session_state.business_data.get('objetivo_faturamento', 30000)),
            step=1000.0,
            format="%.0f"
        )
        
        # Auto-save com validação tributária crítica
        if objetivo_faturamento != st.session_state.business_data.get('objetivo_faturamento'):
            # Validação crítica baseada no regime tributário
            tipo_empresa = st.session_state.business_data.get('tipo_empresa', 'MEI')
            receita_anual = objetivo_faturamento * 12
            
            if tipo_empresa == 'MEI' and receita_anual > 81000:
                st.error(f"⚠️ **LIMITE MEI EXCEDIDO**: Faturamento anual (R$ {receita_anual:,.0f}) > R$ 81.000")
                st.warning("**Correções necessárias:**")
                col_corr1, col_corr2 = st.columns(2)
                with col_corr1:
                    if st.button("🔧 Ajustar para limite MEI", type="secondary"):
                        objetivo_faturamento = 6750  # R$ 81.000 / 12
                        st.session_state.business_data['objetivo_faturamento'] = objetivo_faturamento
                        save_user_data()
                        st.success("Meta ajustada para R$ 6.750/mês (limite MEI)")
                        st.rerun()
                with col_corr2:
                    if st.button("📈 Migrar para Microempresa", type="primary"):
                        st.session_state.business_data['tipo_empresa'] = 'Microempresa'
                        st.session_state.business_data['objetivo_faturamento'] = objetivo_faturamento
                        save_user_data()
                        st.success("Regime alterado para Microempresa!")
                        st.rerun()
                st.stop()
            
            st.session_state.business_data['objetivo_faturamento'] = objetivo_faturamento
            save_user_data()
        st.caption(f"💰 {format_currency(objetivo_faturamento)}")
    
    # Visão do negócio
    st.markdown("---")
    st.subheader("💼 Visão do Negócio")
    
    col5, col6 = st.columns(2)
    
    with col5:
        missao = st.text_area(
            "Missão da empresa",
            value=st.session_state.business_data.get('missao', ''),
            height=80,
            placeholder="Qual é o propósito da sua ótica? Como ela ajuda os clientes?"
        )
        
        visao = st.text_area(
            "Visão de futuro",
            value=st.session_state.business_data.get('visao', ''),
            height=80,
            placeholder="Como você vê sua ótica no futuro? Onde quer chegar?"
        )
    
    with col6:
        principais_diferenciais = st.multiselect(
            "Principais diferenciais",
            [
                "Atendimento personalizado",
                "Preços competitivos", 
                "Localização privilegiada",
                "Tecnologia avançada",
                "Variedade de produtos",
                "Facilidade de pagamento",
                "Pós-venda diferenciado",
                "Especialização técnica"
            ],
            default=safe_multiselect_default(
                st.session_state.business_data.get('principais_diferenciais', []),
                [
                    "Atendimento personalizado",
                    "Preços competitivos", 
                    "Localização privilegiada",
                    "Tecnologia avançada",
                    "Variedade de produtos",
                    "Facilidade de pagamento",
                    "Pós-venda diferenciado",
                    "Especialização técnica"
                ],
                ["Atendimento personalizado"]
            )
        )
        
        valores = st.text_area(
            "Valores e princípios",
            value=st.session_state.business_data.get('valores', ''),
            height=80,
            placeholder="Quais valores guiam o trabalho da sua ótica?"
        )
    
    # Estimativa automática de custos de reforma
    if area_loja > 0 and cidade and estado:
        st.markdown("---")
        st.subheader("🏗️ Estimativa Automática de Custos de Reforma")
        
        try:
            calc = ConstructionCostCalculator()
            tipo_reforma_list = ["basica", "intermediaria", "completa"]
            current_tipo_reforma = st.session_state.business_data.get('tipo_reforma', 'basica')
            current_tipo_reforma_index = tipo_reforma_list.index(current_tipo_reforma) if current_tipo_reforma in tipo_reforma_list else 0
            
            tipo_reforma = st.selectbox(
                "Tipo de reforma/adequação",
                tipo_reforma_list,
                index=current_tipo_reforma_index,
                format_func=lambda x: {
                    "basica": "Básica - Pintura e pequenos ajustes",
                    "intermediaria": "Intermediária - Reforma moderada", 
                    "completa": "Completa - Reforma total"
                }[x]
            )
            # Auto-save tipo_reforma
            if tipo_reforma != st.session_state.business_data.get('tipo_reforma'):
                st.session_state.business_data['tipo_reforma'] = tipo_reforma
                save_user_data()
            
            custos_reforma = calc.calculate_reform_cost(estado, cidade, area_loja, tipo_reforma)
            
            if custos_reforma and custos_reforma.get('custo_total_com_adicional', 0) > 0:
                col7, col8 = st.columns([2, 1])
                
                with col7:
                    st.success(f"💰 **Custo estimado da reforma:** {format_currency(custos_reforma['custo_total_com_adicional'])}")
                    st.info(f"📍 **Baseado em:** {custos_reforma['regiao']} - {cidade}/{estado}")
                    
                    # Breakdown detalhado
                    if st.checkbox("Ver detalhamento dos custos"):
                        breakdown = calc.format_cost_breakdown(custos_reforma)
                        st.text(breakdown)
                
                with col8:
                    # Comparação regional
                    if st.checkbox("Comparar com outras regiões"):
                        comparacao = calc.get_market_comparison(estado)
                        if comparacao:
                            df_comp = pd.DataFrame(comparacao).T
                            df_comp = df_comp.round(0)
                            
                            # Format as currency
                            for col in df_comp.columns:
                                df_comp[col] = df_comp[col].apply(lambda x: format_currency(x))
                            
                            st.dataframe(df_comp, use_container_width=True)
                
                # Store reform data for use in investment calculation
                st.session_state.business_data['custos_reforma'] = custos_reforma
                st.session_state.business_data['tipo_reforma_escolhida'] = tipo_reforma
        except Exception as e:
            st.warning("Sistema de reforma temporariamente indisponível")
    else:
        st.info("ℹ️ Complete área da loja, cidade e estado para ver estimativa de reforma automaticamente")
    
    # Store all data
    st.session_state.business_data.update({
        'nome_otica': nome_otica,
        'cnpj': cnpj,
        'tipo_empresa': tipo_empresa,
        'endereco': endereco,
        'cidade': cidade,
        'estado': estado,
        'area_loja': area_loja,
        'tipo_estabelecimento': tipo_estabelecimento,
        'experiencia': experiencia,
        'objetivo_faturamento': objetivo_faturamento,
        'missao': missao,
        'visao': visao,
        'principais_diferenciais': principais_diferenciais,
        'valores': valores
    })
    
    # Auto-save
    save_user_data()
    
    st.markdown("---")
    
    # Navigation
    col1, col2, col3 = st.columns([1, 1, 1])
    with col3:
        if st.button("Próxima Etapa ➡️", type="primary", key="next_step1"):
            st.session_state.step = 2
            st.rerun()

def show_step_2():
    """Etapa 2: Análise de Mercado"""
    st.header("2️⃣ Análise de Mercado")
    st.markdown("**FASE 2: MERCADO** - Entenda seu mercado e concorrência")
    
    # Tabs para organizar análise de mercado
    tab1, tab2 = st.tabs(["📊 Panorama do Mercado", "📈 Oportunidades"])
    
    with tab1:
        st.subheader("📊 Mercado Óptico Local")
        
        col1, col2 = st.columns(2)
        
        with col1:
            populacao_cidade = st.number_input(
                "População estimada da cidade",
                min_value=0,
                value=int(st.session_state.business_data.get('populacao_cidade', 100000)),
                step=5000
            )
            # Auto-save populacao_cidade
            if populacao_cidade != st.session_state.business_data.get('populacao_cidade'):
                st.session_state.business_data['populacao_cidade'] = populacao_cidade
                save_user_data()
            
            renda_list = ["Baixa (até R$ 2.000)", "Média (R$ 2.000-5.000)", "Alta (R$ 5.000+)", "Mista"]
            current_renda = st.session_state.business_data.get('renda_media', 'Média (R$ 2.000-5.000)')
            current_renda_index = renda_list.index(current_renda) if current_renda in renda_list else 1
            
            renda_media = st.selectbox(
                "Renda média da população",
                renda_list,
                index=current_renda_index
            )
            # Auto-save renda_media
            if renda_media != st.session_state.business_data.get('renda_media'):
                st.session_state.business_data['renda_media'] = renda_media
                save_user_data()
            
            potencial_list = ["Baixo", "Médio", "Alto", "Muito Alto"]
            current_potencial = st.session_state.business_data.get('potencial_mercado', 'Médio')
            current_potencial_index = potencial_list.index(current_potencial) if current_potencial in potencial_list else 1
            
            potencial_mercado = st.selectbox(
                "Potencial do mercado local",
                potencial_list,
                index=current_potencial_index
            )
            # Auto-save potencial_mercado
            if potencial_mercado != st.session_state.business_data.get('potencial_mercado'):
                st.session_state.business_data['potencial_mercado'] = potencial_mercado
                save_user_data()
        
        with col2:
            concorrencia_local = st.number_input(
                "Número de óticas concorrentes na região",
                min_value=0,
                value=int(st.session_state.business_data.get('concorrencia_local', 3)),
                step=1
            )
            # Auto-save concorrencia_local
            if concorrencia_local != st.session_state.business_data.get('concorrencia_local'):
                st.session_state.business_data['concorrencia_local'] = concorrencia_local
                save_user_data()
            
            sazonalidade = st.multiselect(
                "Períodos de maior demanda",
                ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", 
                 "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro", "O ano todo"],
                default=safe_multiselect_default(
                    st.session_state.business_data.get('sazonalidade', []),
                    ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", 
                     "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro", "O ano todo"],
                    ["Janeiro"]
                )
            )
            # Auto-save sazonalidade
            if sazonalidade != st.session_state.business_data.get('sazonalidade'):
                st.session_state.business_data['sazonalidade'] = sazonalidade
                save_user_data()
            
            tendencias_mercado = st.text_area(
                "Tendências observadas no mercado",
                value=st.session_state.business_data.get('tendencias_mercado', ''),
                height=100,
                placeholder="Ex: Aumento da miopia, lentes multifocais, óculos de proteção..."
            )
            # Auto-save tendencias_mercado
            if tendencias_mercado != st.session_state.business_data.get('tendencias_mercado'):
                st.session_state.business_data['tendencias_mercado'] = tendencias_mercado
                save_user_data()
    
    with tab2:
        st.subheader("📈 Oportunidades de Mercado")
        
        col3, col4 = st.columns(2)
        
        with col3:
            oportunidades = st.multiselect(
                "Oportunidades identificadas",
                ["Mercado não saturado", "Poucos concorrentes", "Demanda crescente", "Localização estratégica", 
                 "Falta de especialização", "Preços elevados na região", "Atendimento deficiente dos concorrentes"],
                default=safe_multiselect_default(
                    st.session_state.business_data.get('oportunidades', []),
                    ["Mercado não saturado", "Poucos concorrentes", "Demanda crescente", "Localização estratégica", 
                     "Falta de especialização", "Preços elevados na região", "Atendimento deficiente dos concorrentes"],
                    ["Demanda crescente"]
                )
            )
            # Auto-save oportunidades
            if oportunidades != st.session_state.business_data.get('oportunidades'):
                st.session_state.business_data['oportunidades'] = oportunidades
                save_user_data()
            
            publicos_nao_atendidos = st.text_area(
                "Públicos não bem atendidos",
                value=st.session_state.business_data.get('publicos_nao_atendidos', ''),
                height=100,
                placeholder="Idosos, crianças, pessoas com necessidades especiais..."
            )
            # Auto-save publicos_nao_atendidos
            if publicos_nao_atendidos != st.session_state.business_data.get('publicos_nao_atendidos'):
                st.session_state.business_data['publicos_nao_atendidos'] = publicos_nao_atendidos
                save_user_data()
        
        with col4:
            barreiras_entrada = st.multiselect(
                "Principais barreiras de entrada",
                ["Alto investimento inicial", "Necessidade de especialização", "Concorrência estabelecida", 
                 "Regulamentações", "Fornecedores limitados", "Localização escassa"],
                default=safe_multiselect_default(
                    st.session_state.business_data.get('barreiras_entrada', []),
                    ["Alto investimento inicial", "Necessidade de especialização", "Concorrência estabelecida", 
                     "Regulamentações", "Fornecedores limitados", "Localização escassa"],
                    ["Alto investimento inicial"]
                )
            )
            # Auto-save barreiras_entrada
            if barreiras_entrada != st.session_state.business_data.get('barreiras_entrada'):
                st.session_state.business_data['barreiras_entrada'] = barreiras_entrada
                save_user_data()
            
            estrategia_entrada = st.text_area(
                "Estratégia para superar barreiras",
                value=st.session_state.business_data.get('estrategia_entrada', ''),
                height=100,
                placeholder="Como você pretende entrar e se estabelecer no mercado?"
            )
            # Auto-save estrategia_entrada
            if estrategia_entrada != st.session_state.business_data.get('estrategia_entrada'):
                st.session_state.business_data['estrategia_entrada'] = estrategia_entrada
                save_user_data()
    
    # Store all data
    st.session_state.business_data.update({
        'populacao_cidade': populacao_cidade,
        'renda_media': renda_media,
        'potencial_mercado': potencial_mercado,
        'concorrencia_local': concorrencia_local,
        'sazonalidade': sazonalidade,
        'tendencias_mercado': tendencias_mercado,
        'oportunidades': oportunidades,
        'publicos_nao_atendidos': publicos_nao_atendidos,
        'barreiras_entrada': barreiras_entrada,
        'estrategia_entrada': estrategia_entrada
    })
    
    # Auto-save
    save_user_data()
    
    st.markdown("---")
    
    # Navigation
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("⬅️ Etapa Anterior", key="prev_step2"):
            st.session_state.step = 1
            st.rerun()
    with col3:
        if st.button("Próxima Etapa ➡️", type="primary", key="next_step2"):
            st.session_state.step = 3
            st.rerun()

def show_step_3():
    """Etapa 3: Público-Alvo"""
    st.header("3️⃣ Público-Alvo")
    st.markdown("**FASE 3: CLIENTES** - Defina e entenda seu público-alvo")
    
    # Segmentação do público
    st.subheader("🎯 Segmentação do Público-Alvo")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**👥 Demografia Principal**")
        
        faixa_etaria_principal = st.multiselect(
            "Faixa etária principal",
            ["18-25 anos", "26-35 anos", "36-45 anos", "46-60 anos", "60+ anos"],
            default=safe_multiselect_default(
                st.session_state.business_data.get('faixa_etaria_principal', []),
                ["18-25 anos", "26-35 anos", "36-45 anos", "46-60 anos", "60+ anos"],
                ["36-45 anos"]
            )
        )
        # Auto-save faixa_etaria_principal
        if faixa_etaria_principal != st.session_state.business_data.get('faixa_etaria_principal'):
            st.session_state.business_data['faixa_etaria_principal'] = faixa_etaria_principal
            save_user_data()
        
        classe_social = st.multiselect(
            "Classe social",
            ["Classe A", "Classe B", "Classe C", "Classe D"],
            default=safe_multiselect_default(
                st.session_state.business_data.get('classe_social', []),
                ["Classe A", "Classe B", "Classe C", "Classe D"],
                ["Classe B", "Classe C"]
            )
        )
        # Auto-save classe_social
        if classe_social != st.session_state.business_data.get('classe_social'):
            st.session_state.business_data['classe_social'] = classe_social
            save_user_data()
        
        perfil_profissional = st.multiselect(
            "Perfil profissional",
            ["Estudantes", "Profissionais liberais", "Funcionários CLT", "Aposentados", "Autônomos", "Empresários"],
            default=safe_multiselect_default(
                st.session_state.business_data.get('perfil_profissional', []),
                ["Estudantes", "Profissionais liberais", "Funcionários CLT", "Aposentados", "Autônomos", "Empresários"],
                ["Funcionários CLT"]
            )
        )
        # Auto-save perfil_profissional
        if perfil_profissional != st.session_state.business_data.get('perfil_profissional'):
            st.session_state.business_data['perfil_profissional'] = perfil_profissional
            save_user_data()
    
    with col2:
        st.markdown("**🛍️ Comportamento de Compra**")
        
        necessidades_principais = st.multiselect(
            "Necessidades principais",
            ["Óculos de grau", "Óculos de sol", "Lentes de contato", "Exames oftalmológicos", "Óculos infantis", "Óculos de proteção"],
            default=safe_multiselect_default(
                st.session_state.business_data.get('necessidades_principais', []),
                ["Óculos de grau", "Óculos de sol", "Lentes de contato", "Exames oftalmológicos", "Óculos infantis", "Óculos de proteção"],
                ["Óculos de grau"]
            )
        )
        # Auto-save necessidades_principais
        if necessidades_principais != st.session_state.business_data.get('necessidades_principais'):
            st.session_state.business_data['necessidades_principais'] = necessidades_principais
            save_user_data()
        
        freq_list = ["Anual", "A cada 2 anos", "A cada 3-4 anos", "Esporádica"]
        current_freq = st.session_state.business_data.get('frequencia_compra', 'A cada 2 anos')
        current_freq_index = freq_list.index(current_freq) if current_freq in freq_list else 1
        
        frequencia_compra = st.selectbox(
            "Frequência de compra",
            freq_list,
            index=current_freq_index
        )
        # Auto-save frequencia_compra
        if frequencia_compra != st.session_state.business_data.get('frequencia_compra'):
            st.session_state.business_data['frequencia_compra'] = frequencia_compra
            save_user_data()
        
        # Usar o mesmo ticket_medio da Etapa 10 para consistência
        ticket_medio_etapa10 = st.session_state.business_data.get('ticket_medio', 460)
        ticket_medio_esperado = st.number_input(
            "Ticket médio esperado",
            min_value=0.0,
            value=float(ticket_medio_etapa10),
            step=50.0,
            format="%.0f",
            help=f"Valor sincronizado com Etapa 10: {format_currency(ticket_medio_etapa10)}"
        )
        # Sincronizar ambas as chaves para manter consistência
        if ticket_medio_esperado != st.session_state.business_data.get('ticket_medio'):
            st.session_state.business_data['ticket_medio'] = ticket_medio_esperado
            st.session_state.business_data['ticket_medio_esperado'] = ticket_medio_esperado
            save_user_data()
        st.caption(f"💰 {format_currency(ticket_medio_esperado)}")
        
        fatores_decisao = st.multiselect(
            "Fatores de decisão de compra",
            ["Preço", "Qualidade", "Atendimento", "Localização", "Variedade", "Marca", "Facilidade de pagamento"],
            default=safe_multiselect_default(
                st.session_state.business_data.get('fatores_decisao', []),
                ["Preço", "Qualidade", "Atendimento", "Localização", "Variedade", "Marca", "Facilidade de pagamento"],
                ["Preço", "Qualidade"]
            )
        )
        # Auto-save fatores_decisao
        if fatores_decisao != st.session_state.business_data.get('fatores_decisao'):
            st.session_state.business_data['fatores_decisao'] = fatores_decisao
            save_user_data()
    
    # Estratégias de abordagem
    st.markdown("---")
    st.subheader("📢 Estratégias de Abordagem do Público")
    
    col3, col4 = st.columns(2)
    
    with col3:
        canais_comunicacao = st.multiselect(
            "Canais de comunicação preferidos",
            ["Instagram", "Facebook", "WhatsApp", "Google Ads", "Panfletos", "Rádio local", "Indicações"],
            default=safe_multiselect_default(
                st.session_state.business_data.get('canais_comunicacao', []),
                ["Instagram", "Facebook", "WhatsApp", "Google Ads", "Panfletos", "Rádio local", "Indicações"],
                ["Instagram", "Facebook"]
            )
        )
        
        horarios_preferidos = st.multiselect(
            "Horários de maior movimento",
            ["Manhã (8h-12h)", "Tarde (12h-18h)", "Noite (18h-22h)", "Finais de semana"],
            default=safe_multiselect_default(
                st.session_state.business_data.get('horarios_preferidos', []),
                ["Manhã (8h-12h)", "Tarde (12h-18h)", "Noite (18h-22h)", "Finais de semana"],
                ["Tarde (12h-18h)"]
            )
        )
    
    with col4:
        perfil_detalhado = st.text_area(
            "Perfil detalhado do cliente ideal",
            value=st.session_state.business_data.get('perfil_detalhado', ''),
            height=120,
            placeholder="Descreva seu cliente ideal: necessidades, comportamento, poder aquisitivo, motivações..."
        )
        
        estrategia_atracao = st.text_area(
            "Estratégia para atrair este público",
            value=st.session_state.business_data.get('estrategia_atracao', ''),
            height=120,
            placeholder="Como você pretende atrair e conquistar estes clientes?"
        )
    
    # Store all data
    st.session_state.business_data.update({
        'faixa_etaria_principal': faixa_etaria_principal,
        'classe_social': classe_social,
        'perfil_profissional': perfil_profissional,
        'necessidades_principais': necessidades_principais,
        'frequencia_compra': frequencia_compra,
        'ticket_medio_esperado': ticket_medio_esperado,
        'fatores_decisao': fatores_decisao,
        'canais_comunicacao': canais_comunicacao,
        'horarios_preferidos': horarios_preferidos,
        'perfil_detalhado': perfil_detalhado,
        'estrategia_atracao': estrategia_atracao
    })
    
    # Auto-save
    save_user_data()
    
    st.markdown("---")
    
    # Navigation
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("⬅️ Etapa Anterior", key="prev_step3"):
            st.session_state.step = 2
            st.rerun()
    with col3:
        if st.button("Próxima Etapa ➡️", type="primary", key="next_step3"):
            st.session_state.step = 4
            st.rerun()

def show_step_4():
    """Etapa 4: Concorrência"""
    st.header("4️⃣ Análise da Concorrência")
    st.markdown("**FASE 4: CONCORRÊNCIA** - Conheça seus concorrentes e defina vantagens")
    
    # Tabs para organizar análise da concorrência
    tab1, tab2, tab3 = st.tabs(["🏪 Mapeamento de Concorrentes", "📊 Análise Comparativa", "🎯 Posicionamento"])
    
    with tab1:
        st.subheader("🏪 Identificação dos Concorrentes")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Concorrentes Diretos**")
            
            num_concorrentes = st.number_input(
                "Quantos concorrentes diretos identificou?",
                min_value=0,
                max_value=20,
                value=int(st.session_state.business_data.get('num_concorrentes', 3)),
                step=1
            )
            # Auto-save num_concorrentes
            if num_concorrentes != st.session_state.business_data.get('num_concorrentes'):
                st.session_state.business_data['num_concorrentes'] = num_concorrentes
                save_user_data()
            
            if num_concorrentes > 0:
                concorrentes_info = st.session_state.business_data.get('concorrentes_info', [])
                
                # Ensure we have enough entries
                while len(concorrentes_info) < num_concorrentes:
                    concorrentes_info.append({
                        'nome': '',
                        'localizacao': '',
                        'porte': 'Pequeno',
                        'tempo_mercado': 'Menos de 2 anos'
                    })
                
                # Remove excess entries
                concorrentes_info = concorrentes_info[:num_concorrentes]
                
                for i in range(num_concorrentes):
                    with st.expander(f"Concorrente {i+1}"):
                        concorrentes_info[i]['nome'] = st.text_input(
                            "Nome da ótica",
                            value=concorrentes_info[i].get('nome', ''),
                            key=f"conc_nome_{i}"
                        )
                        
                        concorrentes_info[i]['localizacao'] = st.text_input(
                            "Localização",
                            value=concorrentes_info[i].get('localizacao', ''),
                            key=f"conc_loc_{i}",
                            placeholder="Rua/Bairro"
                        )
                        
                        porte_list = ["Pequeno", "Médio", "Grande", "Rede"]
                        current_porte = concorrentes_info[i].get('porte', 'Pequeno')
                        current_porte_index = porte_list.index(current_porte) if current_porte in porte_list else 0
                        
                        concorrentes_info[i]['porte'] = st.selectbox(
                            "Porte",
                            porte_list,
                            index=current_porte_index,
                            key=f"conc_porte_{i}"
                        )
                        
                        tempo_list = ["Menos de 2 anos", "2-5 anos", "5-10 anos", "Mais de 10 anos"]
                        current_tempo = concorrentes_info[i].get('tempo_mercado', 'Menos de 2 anos')
                        current_tempo_index = tempo_list.index(current_tempo) if current_tempo in tempo_list else 0
                        
                        concorrentes_info[i]['tempo_mercado'] = st.selectbox(
                            "Tempo no mercado",
                            tempo_list,
                            index=current_tempo_index,
                            key=f"conc_tempo_{i}"
                        )
                
                # Auto-save concorrentes_info
                if concorrentes_info != st.session_state.business_data.get('concorrentes_info'):
                    st.session_state.business_data['concorrentes_info'] = concorrentes_info
                    save_user_data()
        
        with col2:
            st.markdown("**Análise do Ambiente Competitivo**")
            
            nivel_list = ["Baixa", "Moderada", "Alta", "Muito Alta"]
            current_nivel = st.session_state.business_data.get('nivel_concorrencia', 'Moderada')
            current_nivel_index = nivel_list.index(current_nivel) if current_nivel in nivel_list else 1
            
            nivel_concorrencia = st.selectbox(
                "Nível de concorrência na região",
                nivel_list,
                index=current_nivel_index
            )
            # Auto-save nivel_concorrencia
            if nivel_concorrencia != st.session_state.business_data.get('nivel_concorrencia'):
                st.session_state.business_data['nivel_concorrencia'] = nivel_concorrencia
                save_user_data()
            
            tipos_concorrentes = st.multiselect(
                "Tipos de concorrentes presentes",
                ["Óticas independentes", "Redes nacionais", "Óticas de farmácias", "Óticas online", "Consultórios oftalmológicos"],
                default=safe_multiselect_default(
                    st.session_state.business_data.get('tipos_concorrentes', []),
                    ["Óticas independentes", "Redes nacionais", "Óticas de farmácias", "Óticas online", "Consultórios oftalmológicos"],
                    ["Óticas independentes"]
                )
            )
            # Auto-save tipos_concorrentes
            if tipos_concorrentes != st.session_state.business_data.get('tipos_concorrentes'):
                st.session_state.business_data['tipos_concorrentes'] = tipos_concorrentes
                save_user_data()
            
            barreiras_competitivas = st.multiselect(
                "Principais barreiras competitivas",
                ["Preços baixos", "Localização privilegiada", "Marca consolidada", "Variedade de produtos", 
                 "Atendimento especializado", "Convênios", "Facilidades de pagamento"],
                default=safe_multiselect_default(
                    st.session_state.business_data.get('barreiras_competitivas', []),
                    ["Preços baixos", "Localização privilegiada", "Marca consolidada", "Variedade de produtos", 
                     "Atendimento especializado", "Convênios", "Facilidades de pagamento"],
                    ["Preços baixos"]
                )
            )
            # Auto-save barreiras_competitivas
            if barreiras_competitivas != st.session_state.business_data.get('barreiras_competitivas'):
                st.session_state.business_data['barreiras_competitivas'] = barreiras_competitivas
                save_user_data()
    
    with tab2:
        st.subheader("📊 Análise Comparativa")
        
        if num_concorrentes > 0:
            st.markdown("**Comparação por Critérios**")
            
            # Create comparison matrix
            criterios = ["Preços", "Variedade", "Atendimento", "Localização", "Marketing", "Tecnologia"]
            
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.markdown("**Critérios de Avaliação:**")
                for criterio in criterios:
                    st.markdown(f"• {criterio}")
                
                st.markdown("**Escala:** 1-5 (1=Muito Fraco, 5=Excelente)")
            
            with col2:
                # Initialize comparison data
                comparacao_data = st.session_state.business_data.get('comparacao_concorrentes', {})
                
                for criterio in criterios:
                    if criterio not in comparacao_data:
                        comparacao_data[criterio] = {}
                    
                    st.markdown(f"**{criterio}**")
                    cols = st.columns(min(num_concorrentes + 1, 4))  # Limit columns to prevent layout issues
                    
                    # Your business column
                    with cols[0]:
                        st.markdown("*Sua ótica*")
                        comparacao_data[criterio]['sua_otica'] = st.slider(
                            "Sua nota",
                            1, 5, 
                            comparacao_data[criterio].get('sua_otica', 3),
                            key=f"sua_{criterio.lower()}"
                        )
                    
                    # Competitor columns
                    for i in range(min(num_concorrentes, 3)):  # Show max 3 competitors
                        if i + 1 < len(cols):
                            with cols[i + 1]:
                                conc_name = concorrentes_info[i].get('nome', f'Concorrente {i+1}')[:15]
                                st.markdown(f"*{conc_name}*")
                                comparacao_data[criterio][f'concorrente_{i}'] = st.slider(
                                    "Nota",
                                    1, 5,
                                    comparacao_data[criterio].get(f'concorrente_{i}', 3),
                                    key=f"conc_{i}_{criterio.lower()}"
                                )
                
                # Auto-save comparison data
                st.session_state.business_data['comparacao_concorrentes'] = comparacao_data
                save_user_data()
        
        else:
            st.info("Configure os concorrentes na primeira aba para fazer a análise comparativa")
    
    with tab3:
        st.subheader("🎯 Seu Posicionamento Competitivo")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Análise dos Pontos Fortes e Fracos**")
            
            forcas = st.text_area(
                "✅ Pontos Fortes do seu negócio",
                value=st.session_state.business_data.get('forcas', ''),
                height=100,
                placeholder="Ex: Atendimento personalizado, localização estratégica, preços justos..."
            )
            # Auto-save forcas
            if forcas != st.session_state.business_data.get('forcas'):
                st.session_state.business_data['forcas'] = forcas
                save_user_data()
            
            fraquezas = st.text_area(
                "⚠️ Pontos que precisa melhorar",
                value=st.session_state.business_data.get('fraquezas', ''),
                height=100,
                placeholder="Ex: Marca nova no mercado, orçamento limitado, pouca experiência..."
            )
            # Auto-save fraquezas
            if fraquezas != st.session_state.business_data.get('fraquezas'):
                st.session_state.business_data['fraquezas'] = fraquezas
                save_user_data()
        
        with col2:
            oportunidades = st.text_area(
                "🎯 Oportunidades no mercado",
                value=st.session_state.business_data.get('oportunidades_swot', ''),
                height=100,
                placeholder="Ex: Mercado crescente, concorrentes com atendimento ruim, poucos especialistas..."
            )
            # Auto-save oportunidades_swot
            if oportunidades != st.session_state.business_data.get('oportunidades_swot'):
                st.session_state.business_data['oportunidades_swot'] = oportunidades
                save_user_data()
            
            ameacas = st.text_area(
                "🚨 Riscos externos",
                value=st.session_state.business_data.get('ameacas', ''),
                height=100,
                placeholder="Ex: Entrada de grandes redes, crise econômica, mudanças na legislação..."
            )
            # Auto-save ameacas
            if ameacas != st.session_state.business_data.get('ameacas'):
                st.session_state.business_data['ameacas'] = ameacas
                save_user_data()
        
        st.markdown("---")
        
        col3, col4 = st.columns(2)
        
        with col3:
            diferenciais_competitivos = st.multiselect(
                "Seus principais diferenciais competitivos",
                ["Preços competitivos", "Atendimento personalizado", "Tecnologia avançada", 
                 "Variedade de produtos", "Rapidez na entrega", "Localização privilegiada",
                 "Especialização técnica", "Parcerias estratégicas", "Horário diferenciado"],
                default=safe_multiselect_default(
                    st.session_state.business_data.get('diferenciais_competitivos', []),
                    ["Preços competitivos", "Atendimento personalizado", "Tecnologia avançada", 
                     "Variedade de produtos", "Rapidez na entrega", "Localização privilegiada",
                     "Especialização técnica", "Parcerias estratégicas", "Horário diferenciado"],
                    ["Atendimento personalizado"]
                )
            )
            # Auto-save diferenciais_competitivos
            if diferenciais_competitivos != st.session_state.business_data.get('diferenciais_competitivos'):
                st.session_state.business_data['diferenciais_competitivos'] = diferenciais_competitivos
                save_user_data()
        
        with col4:
            estrategia_posicionamento = st.text_area(
                "Estratégia de posicionamento",
                value=st.session_state.business_data.get('estrategia_posicionamento', ''),
                height=120,
                placeholder="Como você pretende se posicionar no mercado em relação aos concorrentes?"
            )
            # Auto-save estrategia_posicionamento
            if estrategia_posicionamento != st.session_state.business_data.get('estrategia_posicionamento'):
                st.session_state.business_data['estrategia_posicionamento'] = estrategia_posicionamento
                save_user_data()
    
    # Store all data
    st.session_state.business_data.update({
        'num_concorrentes': num_concorrentes,
        'nivel_concorrencia': nivel_concorrencia,
        'tipos_concorrentes': tipos_concorrentes,
        'barreiras_competitivas': barreiras_competitivas,
        'forcas': forcas,
        'fraquezas': fraquezas,
        'oportunidades_swot': oportunidades,
        'ameacas': ameacas,
        'diferenciais_competitivos': diferenciais_competitivos,
        'estrategia_posicionamento': estrategia_posicionamento
    })
    
    # Auto-save
    save_user_data()
    
    st.markdown("---")
    
    # Navigation
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("⬅️ Etapa Anterior", key="prev_step4"):
            st.session_state.step = 3
            st.rerun()
    with col3:
        if st.button("Próxima Etapa ➡️", type="primary", key="next_step4"):
            st.session_state.step = 5
            st.rerun()

def show_step_5():
    """Etapa 5: Produtos e Serviços"""
    st.header("5️⃣ Produtos e Serviços")
    st.markdown("**FASE 5: PRODUTOS** - Configure produtos, fornecedores e margens")
    
    # Tabs para organizar produtos e serviços
    tab1, tab2, tab3 = st.tabs(["👓 Produtos Principais", "🔧 Serviços", "💰 Estratégia de Preços"])
    
    with tab1:
        st.subheader("👓 Catálogo de Produtos")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Categorias de Produtos**")
            
            categorias_produtos = st.multiselect(
                "Produtos que pretende vender",
                ["Óculos de grau", "Óculos de sol", "Lentes de contato", "Armações", 
                 "Lentes oftálmicas", "Óculos infantis", "Óculos de proteção", "Acessórios"],
                default=safe_multiselect_default(
                    st.session_state.business_data.get('categorias_produtos', []),
                    ["Óculos de grau", "Óculos de sol", "Lentes de contato", "Armações", 
                     "Lentes oftálmicas", "Óculos infantis", "Óculos de proteção", "Acessórios"],
                    ["Óculos de grau", "Óculos de sol"]
                )
            )
            # Auto-save categorias_produtos
            if categorias_produtos != st.session_state.business_data.get('categorias_produtos'):
                st.session_state.business_data['categorias_produtos'] = categorias_produtos
                save_user_data()
            
            marcas_trabalhar = st.text_area(
                "Marcas que pretende trabalhar",
                value=st.session_state.business_data.get('marcas_trabalhar', ''),
                height=100,
                placeholder="Ex: Ray-Ban, Oakley, Chilli Beans, Atitude, Prada..."
            )
            # Auto-save marcas_trabalhar
            if marcas_trabalhar != st.session_state.business_data.get('marcas_trabalhar'):
                st.session_state.business_data['marcas_trabalhar'] = marcas_trabalhar
                save_user_data()
            
            faixa_preco_produtos = st.selectbox(
                "Faixa de preço principal dos produtos",
                ["Econômica (R$ 50-200)", "Intermediária (R$ 200-500)", "Premium (R$ 500-1000)", "Luxo (R$ 1000+)", "Mista"],
                index=["Econômica (R$ 50-200)", "Intermediária (R$ 200-500)", "Premium (R$ 500-1000)", "Luxo (R$ 1000+)", "Mista"].index(
                    st.session_state.business_data.get('faixa_preco_produtos', 'Intermediária (R$ 200-500)')
                )
            )
            # Auto-save faixa_preco_produtos
            if faixa_preco_produtos != st.session_state.business_data.get('faixa_preco_produtos'):
                st.session_state.business_data['faixa_preco_produtos'] = faixa_preco_produtos
                save_user_data()
        
        with col2:
            st.markdown("**Fornecedores e Parcerias**")
            
            tipos_fornecedores = st.multiselect(
                "Tipos de fornecedores",
                ["Distribuidores nacionais", "Importadores", "Fabricantes diretos", "Representantes regionais", 
                 "Marketplace B2B", "Cooperativas de compra"],
                default=safe_multiselect_default(
                    st.session_state.business_data.get('tipos_fornecedores', []),
                    ["Distribuidores nacionais", "Importadores", "Fabricantes diretos", "Representantes regionais", 
                     "Marketplace B2B", "Cooperativas de compra"],
                    ["Distribuidores nacionais"]
                )
            )
            # Auto-save tipos_fornecedores
            if tipos_fornecedores != st.session_state.business_data.get('tipos_fornecedores'):
                st.session_state.business_data['tipos_fornecedores'] = tipos_fornecedores
                save_user_data()
            
            criterios_fornecedores = st.multiselect(
                "Critérios para escolha de fornecedores",
                ["Preço competitivo", "Qualidade dos produtos", "Prazo de entrega", "Condições de pagamento", 
                 "Suporte técnico", "Variedade de produtos", "Exclusividade territorial"],
                default=safe_multiselect_default(
                    st.session_state.business_data.get('criterios_fornecedores', []),
                    ["Preço competitivo", "Qualidade dos produtos", "Prazo de entrega", "Condições de pagamento", 
                     "Suporte técnico", "Variedade de produtos", "Exclusividade territorial"],
                    ["Preço competitivo", "Qualidade dos produtos"]
                )
            )
            # Auto-save criterios_fornecedores
            if criterios_fornecedores != st.session_state.business_data.get('criterios_fornecedores'):
                st.session_state.business_data['criterios_fornecedores'] = criterios_fornecedores
                save_user_data()
            
            estoque_inicial = st.number_input(
                "Investimento inicial em estoque (R$)",
                min_value=0.0,
                value=float(st.session_state.business_data.get('estoque_inicial', 15000)),
                step=1000.0,
                format="%.0f"
            )
            # Auto-save estoque_inicial
            if estoque_inicial != st.session_state.business_data.get('estoque_inicial'):
                st.session_state.business_data['estoque_inicial'] = estoque_inicial
                save_user_data()
            st.caption(f"💰 {format_currency(estoque_inicial)}")
    
    with tab2:
        st.subheader("🔧 Serviços Oferecidos")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Serviços Principais**")
            
            servicos_oferecidos = st.multiselect(
                "Serviços que pretende oferecer",
                ["Exame de vista", "Montagem de óculos", "Ajustes e reparos", "Limpeza e manutenção", 
                 "Consultoria em óculos", "Entrega domiciliar", "Garantia estendida", "Troca de lentes"],
                default=safe_multiselect_default(
                    st.session_state.business_data.get('servicos_oferecidos', []),
                    ["Exame de vista", "Montagem de óculos", "Ajustes e reparos", "Limpeza e manutenção", 
                     "Consultoria em óculos", "Entrega domiciliar", "Garantia estendida", "Troca de lentes"],
                    ["Montagem de óculos", "Ajustes e reparos"]
                )
            )
            # Auto-save servicos_oferecidos
            if servicos_oferecidos != st.session_state.business_data.get('servicos_oferecidos'):
                st.session_state.business_data['servicos_oferecidos'] = servicos_oferecidos
                save_user_data()
            
            if "Exame de vista" in servicos_oferecidos:
                parcerias_medicas = st.text_area(
                    "Parcerias com oftalmologistas",
                    value=st.session_state.business_data.get('parcerias_medicas', ''),
                    height=80,
                    placeholder="Descreva como pretende oferecer exames de vista..."
                )
                # Auto-save parcerias_medicas
                if parcerias_medicas != st.session_state.business_data.get('parcerias_medicas'):
                    st.session_state.business_data['parcerias_medicas'] = parcerias_medicas
                    save_user_data()
        
        with col2:
            st.markdown("**Diferenciais nos Serviços**")
            
            diferenciais_servicos = st.multiselect(
                "Diferenciais que oferecerá",
                ["Atendimento personalizado", "Serviço 24h/emergência", "Garantia vitalícia de ajustes", 
                 "Programa de fidelidade", "Parcelamento facilitado", "Troca sem custos", "Consultoria especializada"],
                default=safe_multiselect_default(
                    st.session_state.business_data.get('diferenciais_servicos', []),
                    ["Atendimento personalizado", "Serviço 24h/emergência", "Garantia vitalícia de ajustes", 
                     "Programa de fidelidade", "Parcelamento facilitado", "Troca sem custos", "Consultoria especializada"],
                    ["Atendimento personalizado"]
                )
            )
            # Auto-save diferenciais_servicos
            if diferenciais_servicos != st.session_state.business_data.get('diferenciais_servicos'):
                st.session_state.business_data['diferenciais_servicos'] = diferenciais_servicos
                save_user_data()
            
            tempo_entrega = st.selectbox(
                "Tempo de entrega prometido",
                ["Mesmo dia", "24 horas", "2-3 dias", "1 semana", "Conforme complexidade"],
                index=["Mesmo dia", "24 horas", "2-3 dias", "1 semana", "Conforme complexidade"].index(
                    st.session_state.business_data.get('tempo_entrega', '2-3 dias')
                )
            )
            # Auto-save tempo_entrega
            if tempo_entrega != st.session_state.business_data.get('tempo_entrega'):
                st.session_state.business_data['tempo_entrega'] = tempo_entrega
                save_user_data()
    
    with tab3:
        st.subheader("💰 Estratégia de Preços")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Política de Preços**")
            
            estrategia_precificacao = st.selectbox(
                "Estratégia de precificação",
                ["Preços competitivos", "Premium/diferenciação", "Penetração (preços baixos)", "Preços psicológicos", "Valor percebido"],
                index=["Preços competitivos", "Premium/diferenciação", "Penetração (preços baixos)", "Preços psicológicos", "Valor percebido"].index(
                    st.session_state.business_data.get('estrategia_precificacao', 'Preços competitivos')
                )
            )
            # Auto-save estrategia_precificacao
            if estrategia_precificacao != st.session_state.business_data.get('estrategia_precificacao'):
                st.session_state.business_data['estrategia_precificacao'] = estrategia_precificacao
                save_user_data()
            
            margem_produtos = st.slider(
                "Margem de lucro média nos produtos (%)",
                min_value=10,
                max_value=900,
                value=int(st.session_state.business_data.get('margem_produtos', 100)),
                step=10
            )
            # Auto-save margem_produtos
            if margem_produtos != st.session_state.business_data.get('margem_produtos'):
                st.session_state.business_data['margem_produtos'] = margem_produtos
                save_user_data()
            st.caption(f"Margem: {margem_produtos}%")
            
            formas_pagamento = st.multiselect(
                "Formas de pagamento aceitas",
                ["Dinheiro", "PIX", "Cartão débito", "Cartão crédito", "Cartão crediário", "Boleto", "Financiamento próprio"],
                default=safe_multiselect_default(
                    st.session_state.business_data.get('formas_pagamento', []),
                    ["Dinheiro", "PIX", "Cartão débito", "Cartão crédito", "Cartão crediário", "Boleto", "Financiamento próprio"],
                    ["Dinheiro", "PIX", "Cartão débito", "Cartão crédito"]
                )
            )
            # Auto-save formas_pagamento
            if formas_pagamento != st.session_state.business_data.get('formas_pagamento'):
                st.session_state.business_data['formas_pagamento'] = formas_pagamento
                save_user_data()
        
        with col2:
            st.markdown("**Políticas Comerciais**")
            
            parcelamento_maximo = st.selectbox(
                "Parcelamento máximo no cartão",
                ["À vista apenas", "3x", "6x", "10x", "12x", "18x", "24x"],
                index=["À vista apenas", "3x", "6x", "10x", "12x", "18x", "24x"].index(
                    st.session_state.business_data.get('parcelamento_maximo', '10x')
                )
            )
            # Auto-save parcelamento_maximo
            if parcelamento_maximo != st.session_state.business_data.get('parcelamento_maximo'):
                st.session_state.business_data['parcelamento_maximo'] = parcelamento_maximo
                save_user_data()
            
            desconto_avista = st.slider(
                "Desconto para pagamento à vista (%)",
                min_value=0,
                max_value=20,
                value=int(st.session_state.business_data.get('desconto_avista', 5)),
                step=1
            )
            # Auto-save desconto_avista
            if desconto_avista != st.session_state.business_data.get('desconto_avista'):
                st.session_state.business_data['desconto_avista'] = desconto_avista
                save_user_data()
            st.caption(f"Desconto: {desconto_avista}%")
            
            politica_garantia = st.text_area(
                "Política de garantia e trocas",
                value=st.session_state.business_data.get('politica_garantia', ''),
                height=100,
                placeholder="Ex: 30 dias para troca, garantia de 1 ano contra defeitos..."
            )
            # Auto-save politica_garantia
            if politica_garantia != st.session_state.business_data.get('politica_garantia'):
                st.session_state.business_data['politica_garantia'] = politica_garantia
                save_user_data()
        
        st.markdown("---")
        st.subheader("💳 Condições de Pagamento e Recebimento")
        st.markdown("*Configure os percentuais de vendas à vista vs prazo e prazos de recebimento*")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Divisão de Recebimentos**")
            
            percentual_avista = st.slider(
                "Vendas à vista (%)",
                min_value=0,
                max_value=100,
                value=int(st.session_state.business_data.get('percentual_avista', 70)),
                step=5,
                help="Percentual das vendas que recebe no mesmo mês"
            )
            # Auto-save percentual_avista
            if percentual_avista != st.session_state.business_data.get('percentual_avista'):
                st.session_state.business_data['percentual_avista'] = percentual_avista
                save_user_data()
            
            percentual_prazo = 100 - percentual_avista
            st.info(f"**Vendas a prazo: {percentual_prazo}%**")
            
            st.markdown("**Prazos de Recebimento**")
            
            prazo_options = [0, 15, 30, 45, 60, 90]
            prazo_labels = ["Na hora! (À vista)", "15 dias", "30 dias", "45 dias", "60 dias", "90 dias"]
            
            # Mapear valor salvo para índice
            current_prazo = st.session_state.business_data.get('prazo_medio_recebimento', 30)
            try:
                current_index = prazo_options.index(current_prazo)
            except ValueError:
                current_index = 2  # Default para 30 dias
            
            prazo_medio_recebimento = st.selectbox(
                "Prazo médio de recebimento (vendas a prazo)",
                options=prazo_options,
                format_func=lambda x: prazo_labels[prazo_options.index(x)],
                index=current_index,
                help="Quantos dias em média para receber vendas a prazo"
            )
            # Auto-save prazo_medio_recebimento
            if prazo_medio_recebimento != st.session_state.business_data.get('prazo_medio_recebimento'):
                st.session_state.business_data['prazo_medio_recebimento'] = prazo_medio_recebimento
                save_user_data()
        
        with col2:
            st.markdown("**Modalidades de Recebimento**")
            
            # Explicar a diferença entre venda parcelada e recebimento
            st.info("**💡 Importante:** Cliente pode parcelar em 3x, mas você pode receber antecipado!")
            
            st.markdown("**Cenários de Recebimento:**")
            
            if prazo_medio_recebimento == 0:
                st.success("🚀 **Na Hora! (À vista)**")
                st.write("• Cliente: Paga à vista (dinheiro/PIX/débito)")
                st.write("• Você: Recebe na hora, sem intermediários")
                st.write("• Financeira: Sem taxas")
                st.write("• Fluxo de caixa: Instantâneo, sem risco")
            elif prazo_medio_recebimento <= 30:
                st.success("✅ **Recebimento Antecipado (D+1 a D+30)**")
                st.write("• Cliente: Paga em 3x no cartão")
                st.write("• Você: Recebe tudo em até 30 dias")
                st.write("• Financeira: Desconta taxa (3-5%)")
                st.write("• Fluxo de caixa: Rápido")
            elif prazo_medio_recebimento <= 60:
                st.warning("⚠️ **Recebimento Parcelado (30-60 dias)**")
                st.write("• Cliente: Paga em 3x no cartão")
                st.write("• Você: Recebe parcelado conforme cliente paga")
                st.write("• Financeira: Taxa menor (1-3%)")
                st.write("• Fluxo de caixa: Moderado")
            else:
                st.error("🚨 **Recebimento Direto (60+ dias)**")
                st.write("• Cliente: Paga diretamente à você")
                st.write("• Você: Assume risco de inadimplência")
                st.write("• Financeira: Sem taxas")
                st.write("• Fluxo de caixa: Lento, maior risco")
            
            # Taxa da financeira configurável
            st.markdown("**💳 Taxa da Financeira (Editável):**")
            
            # Taxa da financeira baseada nas taxas reais do Mercado Pago
            st.markdown("**💳 Taxas do Mercado Pago (2024):**")
            
            # Opções de recebimento baseadas nas taxas reais
            opcao_recebimento = st.selectbox(
                "Modalidade de recebimento",
                [
                    "PIX - Na hora (0%)",
                    "Débito - Na hora (1,99%)",
                    "Crédito à vista - Na hora (4,98%)",
                    "Crédito 2x-12x - Na hora (5,31%)",
                    "Crédito à vista - 14 dias (3,79%)",
                    "Crédito 2x-12x - 14 dias (4,36%)",
                    "Crédito à vista - 30 dias (3,03%)",
                    "Crédito 2x-12x - 30 dias (3,60%)"
                ],
                index=0
            )
            
            # Mapear taxas baseadas na seleção
            taxas_mercado_pago = {
                "PIX - Na hora (0%)": 0.0,
                "Débito - Na hora (1,99%)": 1.99,
                "Crédito à vista - Na hora (4,98%)": 4.98,
                "Crédito 2x-12x - Na hora (5,31%)": 5.31,
                "Crédito à vista - 14 dias (3,79%)": 3.79,
                "Crédito 2x-12x - 14 dias (4,36%)": 4.36,
                "Crédito à vista - 30 dias (3,03%)": 3.03,
                "Crédito 2x-12x - 30 dias (3,60%)": 3.60
            }
            
            taxa_selecionada = taxas_mercado_pago[opcao_recebimento]
            
            # Salvar configuração
            st.session_state.business_data['opcao_recebimento_mp'] = opcao_recebimento
            st.session_state.business_data['taxa_mercado_pago'] = taxa_selecionada
            save_user_data()
            
            # Mostrar detalhes da taxa selecionada
            if taxa_selecionada == 0:
                st.success("**PIX:** Recebimento gratuito e instantâneo")
                st.write("• **Taxa: 0%** - sem custos")
                st.write("• Recebimento imediato")
                st.write("• Sem risco de chargeback")
            elif "Na hora" in opcao_recebimento:
                st.info("**Recebimento Imediato:** Taxa mais alta, mas dinheiro na conta na hora")
                st.write(f"• **Taxa: {taxa_selecionada}%**")
                exemplo_desconto = 1000 * (taxa_selecionada / 100)
                st.write(f"• Exemplo: R$ 1.000 → você recebe R$ {1000 - exemplo_desconto:,.2f}")
                st.write("• Dinheiro disponível em segundos")
            else:
                st.warning("**Recebimento a Prazo:** Taxa menor, mas aguarda prazo para receber")
                st.write(f"• **Taxa: {taxa_selecionada}%**")
                exemplo_desconto = 1000 * (taxa_selecionada / 100)
                st.write(f"• Exemplo: R$ 1.000 → você recebe R$ {1000 - exemplo_desconto:,.2f}")
                prazo = "14 dias" if "14 dias" in opcao_recebimento else "30 dias"
                st.write(f"• Recebimento em {prazo}")
            
            # Configuração customizada (opcional)
            st.markdown("**🔧 Configuração Personalizada:**")
            usar_customizada = st.checkbox("Usar taxa customizada diferente do Mercado Pago")
            
            if usar_customizada:
                taxa_customizada = st.number_input(
                    "Taxa customizada (%)",
                    min_value=0.0,
                    max_value=15.0,
                    value=taxa_selecionada,
                    step=0.01,
                    format="%.2f",
                    help="Caso use outra operadora ou tenha condições especiais"
                )
                st.session_state.business_data['taxa_customizada'] = taxa_customizada
                st.session_state.business_data['usar_taxa_customizada'] = True
                save_user_data()
                
                st.write(f"• **Taxa customizada: {taxa_customizada}%**")
                exemplo_desconto = 1000 * (taxa_customizada / 100)
                st.write(f"• Exemplo: R$ 1.000 → você recebe R$ {1000 - exemplo_desconto:,.2f}")
            else:
                st.session_state.business_data['usar_taxa_customizada'] = False
                save_user_data()
            
            # Mostrar formas de pagamento aceitas
            st.markdown("**Formas de Pagamento:**")
            for forma in formas_pagamento:
                if forma == "Dinheiro":
                    st.write(f"💵 {forma} → Recebe na hora ({percentual_avista}%)")
                elif forma in ["PIX", "Débito"]:
                    st.write(f"💳 {forma} → Recebe D+1 ({percentual_avista}%)")
                else:
                    st.write(f"💰 {forma} → Recebe conforme configurado ({percentual_prazo}%)")
            
        st.markdown("---")
        st.info(f"**💡 Resumo:** {percentual_avista}% à vista (recebe no mês) + {percentual_prazo}% a prazo (recebe em {prazo_medio_recebimento} dias)")
    
    # Store all data including payment conditions and configured fees
    st.session_state.business_data.update({
        'categorias_produtos': categorias_produtos,
        'marcas_trabalhar': marcas_trabalhar,
        'faixa_preco_produtos': faixa_preco_produtos,
        'tipos_fornecedores': tipos_fornecedores,
        'criterios_fornecedores': criterios_fornecedores,
        'estoque_inicial': estoque_inicial,
        'servicos_oferecidos': servicos_oferecidos,
        'diferenciais_servicos': diferenciais_servicos,
        'tempo_entrega': tempo_entrega,
        'estrategia_precificacao': estrategia_precificacao,
        'margem_produtos': margem_produtos,
        'formas_pagamento': formas_pagamento,
        'parcelamento_maximo': parcelamento_maximo,
        'desconto_avista': desconto_avista,
        'politica_garantia': politica_garantia,
        'percentual_avista': percentual_avista,
        'prazo_medio_recebimento': prazo_medio_recebimento
    })
    
    # Auto-save
    save_user_data()
    
    # Valores calculados para outras etapas (sem interface visual)
    diaria_optometrista = st.session_state.business_data.get('diaria_optometrista', 150.0)
    dias_optometrista_mes = st.session_state.business_data.get('dias_optometrista_mes', 4)
    custo_optometrista_mensal = diaria_optometrista * dias_optometrista_mes
    meta_oculos_mes = st.session_state.business_data.get('meta_oculos_mes', 80)
    custo_exame_por_oculos = custo_optometrista_mensal / meta_oculos_mes if meta_oculos_mes > 0 else 0
    
    # Custos básicos para cálculos (sem interface visual)
    custo_materiais_fisicos = 89.80  # Soma dos materiais básicos
    custo_total_com_exame_visual = custo_materiais_fisicos + custo_exame_por_oculos
    
    # Armazenar valores para outras etapas
    st.session_state.business_data.update({
        'custo_exame_por_oculos': custo_exame_por_oculos,
        'custo_materiais_fisicos': custo_materiais_fisicos,
        'custo_total_com_exame_visual': custo_total_com_exame_visual
    })
    save_user_data()
    
    st.markdown("---")
    
    # Navigation
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("⬅️ Etapa Anterior", key="prev_step5"):
            st.session_state.step = 4
            st.rerun()
    with col3:
        if st.button("Próxima Etapa ➡️", type="primary", key="next_step5"):
            st.session_state.step = 6
            st.rerun()

# Additional step functions will be implemented similarly...
def show_step_6():
    """Etapa 6: Estratégia de Marketing"""
    st.header("6️⃣ Estratégia de Marketing")
    st.markdown("**FASE 6: MARKETING** - Defina como atrair e manter clientes")
    
    # Tabs para organizar estratégia de marketing
    tab1, tab2, tab3 = st.tabs(["📢 Estratégia Geral", "🎯 Canais de Marketing", "💡 Campanhas e Promoções"])
    
    with tab1:
        st.subheader("📢 Posicionamento e Marca")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Identidade da Marca**")
            
            proposta_valor = st.text_area(
                "Proposta de valor (o que oferece de único)",
                value=st.session_state.business_data.get('proposta_valor', ''),
                height=100,
                placeholder="Ex: Óculos de qualidade com atendimento personalizado e preços justos..."
            )
            # Auto-save proposta_valor
            if proposta_valor != st.session_state.business_data.get('proposta_valor'):
                st.session_state.business_data['proposta_valor'] = proposta_valor
                save_user_data()
            
            publico_alvo_marketing = st.multiselect(
                "Público-alvo prioritário para marketing",
                ["Jovens (18-30)", "Adultos (30-50)", "Idosos (50+)", "Crianças/Pais", "Profissionais", "Estudantes"],
                default=safe_multiselect_default(
                    st.session_state.business_data.get('publico_alvo_marketing', []),
                    ["Jovens (18-30)", "Adultos (30-50)", "Idosos (50+)", "Crianças/Pais", "Profissionais", "Estudantes"],
                    ["Adultos (30-50)"]
                )
            )
            # Auto-save publico_alvo_marketing
            if publico_alvo_marketing != st.session_state.business_data.get('publico_alvo_marketing'):
                st.session_state.business_data['publico_alvo_marketing'] = publico_alvo_marketing
                save_user_data()
            
            tom_comunicacao = st.selectbox(
                "Tom de comunicação",
                ["Profissional e técnico", "Amigável e próximo", "Moderno e descontraído", "Elegante e sofisticado", "Familiar e caloroso"],
                index=["Profissional e técnico", "Amigável e próximo", "Moderno e descontraído", "Elegante e sofisticado", "Familiar e caloroso"].index(
                    st.session_state.business_data.get('tom_comunicacao', 'Amigável e próximo')
                )
            )
            # Auto-save tom_comunicacao
            if tom_comunicacao != st.session_state.business_data.get('tom_comunicacao'):
                st.session_state.business_data['tom_comunicacao'] = tom_comunicacao
                save_user_data()
        
        with col2:
            st.markdown("**Objetivos de Marketing**")
            
            objetivos_marketing = st.multiselect(
                "Principais objetivos",
                ["Aumentar conhecimento da marca", "Gerar leads qualificados", "Aumentar vendas", "Fidelizar clientes", 
                 "Melhorar reputação", "Expandir base de clientes", "Posicionar como referência"],
                default=safe_multiselect_default(
                    st.session_state.business_data.get('objetivos_marketing', []),
                    ["Aumentar conhecimento da marca", "Gerar leads qualificados", "Aumentar vendas", "Fidelizar clientes", 
                     "Melhorar reputação", "Expandir base de clientes", "Posicionar como referência"],
                    ["Aumentar vendas", "Fidelizar clientes"]
                )
            )
            # Auto-save objetivos_marketing
            if objetivos_marketing != st.session_state.business_data.get('objetivos_marketing'):
                st.session_state.business_data['objetivos_marketing'] = objetivos_marketing
                save_user_data()
            
            orcamento_marketing = st.number_input(
                "Orçamento mensal para marketing (R$)",
                min_value=0.0,
                value=float(st.session_state.business_data.get('orcamento_marketing', 1000)),
                step=100.0,
                format="%.0f"
            )
            # Auto-save orcamento_marketing
            if orcamento_marketing != st.session_state.business_data.get('orcamento_marketing'):
                st.session_state.business_data['orcamento_marketing'] = orcamento_marketing
                save_user_data()
            st.caption(f"💰 {format_currency(orcamento_marketing)}/mês")
            
            estrategias_diferenciacao = st.multiselect(
                "Como se diferenciará dos concorrentes",
                ["Preços mais baixos", "Melhor atendimento", "Maior variedade", "Tecnologia avançada", 
                 "Rapidez na entrega", "Localização conveniente", "Parcerias exclusivas", "Garantias estendidas"],
                default=safe_multiselect_default(
                    st.session_state.business_data.get('estrategias_diferenciacao', []),
                    ["Preços mais baixos", "Melhor atendimento", "Maior variedade", "Tecnologia avançada", 
                     "Rapidez na entrega", "Localização conveniente", "Parcerias exclusivas", "Garantias estendidas"],
                    ["Melhor atendimento"]
                )
            )
            # Auto-save estrategias_diferenciacao
            if estrategias_diferenciacao != st.session_state.business_data.get('estrategias_diferenciacao'):
                st.session_state.business_data['estrategias_diferenciacao'] = estrategias_diferenciacao
                save_user_data()
    
    with tab2:
        st.subheader("🎯 Canais de Marketing e Divulgação")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Marketing Digital**")
            
            canais_digitais = st.multiselect(
                "Canais digitais que utilizará",
                ["Facebook", "Instagram", "WhatsApp Business", "Google Ads", "Google Meu Negócio", 
                 "Site próprio", "YouTube", "TikTok", "Email marketing"],
                default=safe_multiselect_default(
                    st.session_state.business_data.get('canais_digitais', []),
                    ["Facebook", "Instagram", "WhatsApp Business", "Google Ads", "Google Meu Negócio", 
                     "Site próprio", "YouTube", "TikTok", "Email marketing"],
                    ["Facebook", "Instagram", "WhatsApp Business"]
                )
            )
            # Auto-save canais_digitais
            if canais_digitais != st.session_state.business_data.get('canais_digitais'):
                st.session_state.business_data['canais_digitais'] = canais_digitais
                save_user_data()
            
            frequencia_posts = st.selectbox(
                "Frequência de postagens nas redes sociais",
                ["Diariamente", "3-4 vezes por semana", "1-2 vezes por semana", "Esporadicamente"],
                index=["Diariamente", "3-4 vezes por semana", "1-2 vezes por semana", "Esporadicamente"].index(
                    st.session_state.business_data.get('frequencia_posts', '3-4 vezes por semana')
                )
            )
            # Auto-save frequencia_posts
            if frequencia_posts != st.session_state.business_data.get('frequencia_posts'):
                st.session_state.business_data['frequencia_posts'] = frequencia_posts
                save_user_data()
            
            tipos_conteudo = st.multiselect(
                "Tipos de conteúdo para redes sociais",
                ["Produtos em destaque", "Dicas de cuidados", "Tendências de moda", "Depoimentos de clientes", 
                 "Bastidores da ótica", "Promoções", "Educativo sobre visão", "Antes e depois"],
                default=safe_multiselect_default(
                    st.session_state.business_data.get('tipos_conteudo', []),
                    ["Produtos em destaque", "Dicas de cuidados", "Tendências de moda", "Depoimentos de clientes", 
                     "Bastidores da ótica", "Promoções", "Educativo sobre visão", "Antes e depois"],
                    ["Produtos em destaque", "Promoções"]
                )
            )
            # Auto-save tipos_conteudo
            if tipos_conteudo != st.session_state.business_data.get('tipos_conteudo'):
                st.session_state.business_data['tipos_conteudo'] = tipos_conteudo
                save_user_data()
        
        with col2:
            st.markdown("**Marketing Tradicional**")
            
            canais_tradicionais = st.multiselect(
                "Canais tradicionais que utilizará",
                ["Panfletos", "Cartões de visita", "Banner na loja", "Anúncios em jornal local", 
                 "Rádio local", "Parcerias com médicos", "Indicações boca a boca", "Eventos locais"],
                default=safe_multiselect_default(
                    st.session_state.business_data.get('canais_tradicionais', []),
                    ["Panfletos", "Cartões de visita", "Banner na loja", "Anúncios em jornal local", 
                     "Rádio local", "Parcerias com médicos", "Indicações boca a boca", "Eventos locais"],
                    ["Cartões de visita", "Indicações boca a boca"]
                )
            )
            # Auto-save canais_tradicionais
            if canais_tradicionais != st.session_state.business_data.get('canais_tradicionais'):
                st.session_state.business_data['canais_tradicionais'] = canais_tradicionais
                save_user_data()
            
            parcerias_marketing = st.text_area(
                "Parcerias estratégicas para marketing",
                value=st.session_state.business_data.get('parcerias_marketing', ''),
                height=100,
                placeholder="Ex: Oftalmologistas, clínicas, escolas, empresas locais..."
            )
            # Auto-save parcerias_marketing
            if parcerias_marketing != st.session_state.business_data.get('parcerias_marketing'):
                st.session_state.business_data['parcerias_marketing'] = parcerias_marketing
                save_user_data()
            
            programa_indicacoes = st.selectbox(
                "Programa de indicações",
                ["Não pretendo ter", "Desconto para quem indica", "Desconto para ambos", "Sistema de pontos", "Brindes especiais"],
                index=["Não pretendo ter", "Desconto para quem indica", "Desconto para ambos", "Sistema de pontos", "Brindes especiais"].index(
                    st.session_state.business_data.get('programa_indicacoes', 'Desconto para ambos')
                )
            )
            # Auto-save programa_indicacoes
            if programa_indicacoes != st.session_state.business_data.get('programa_indicacoes'):
                st.session_state.business_data['programa_indicacoes'] = programa_indicacoes
                save_user_data()
    
    with tab3:
        st.subheader("💡 Campanhas e Estratégias Promocionais")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Promoções Sazonais**")
            
            campanhas_sazonais = st.multiselect(
                "Campanhas sazonais planejadas",
                ["Volta às aulas", "Dia das Mães", "Dia dos Pais", "Black Friday", "Natal", 
                 "Férias escolares", "Dia da Visão", "Aniversário da loja"],
                default=safe_multiselect_default(
                    st.session_state.business_data.get('campanhas_sazonais', []),
                    ["Volta às aulas", "Dia das Mães", "Dia dos Pais", "Black Friday", "Natal", 
                     "Férias escolares", "Dia da Visão", "Aniversário da loja"],
                    ["Volta às aulas", "Black Friday"]
                )
            )
            # Auto-save campanhas_sazonais
            if campanhas_sazonais != st.session_state.business_data.get('campanhas_sazonais'):
                st.session_state.business_data['campanhas_sazonais'] = campanhas_sazonais
                save_user_data()
            
            tipos_promocoes = st.multiselect(
                "Tipos de promoções que oferecerá",
                ["Desconto percentual", "2ª unidade com desconto", "Frete grátis", "Brinde", 
                 "Parcelamento sem juros", "Cashback", "Troca garantida", "Combo promocional"],
                default=safe_multiselect_default(
                    st.session_state.business_data.get('tipos_promocoes', []),
                    ["Desconto percentual", "2ª unidade com desconto", "Frete grátis", "Brinde", 
                     "Parcelamento sem juros", "Cashback", "Troca garantida", "Combo promocional"],
                    ["Desconto percentual", "Parcelamento sem juros"]
                )
            )
            # Auto-save tipos_promocoes
            if tipos_promocoes != st.session_state.business_data.get('tipos_promocoes'):
                st.session_state.business_data['tipos_promocoes'] = tipos_promocoes
                save_user_data()
        
        with col2:
            st.markdown("**Fidelização de Clientes**")
            
            estrategias_fidelizacao = st.multiselect(
                "Estratégias de fidelização",
                ["Programa de pontos", "Desconto para clientes antigos", "Aniversário do cliente", 
                 "Newsletter exclusiva", "Pré-venda de novidades", "Atendimento VIP", "Evento exclusivo"],
                default=safe_multiselect_default(
                    st.session_state.business_data.get('estrategias_fidelizacao', []),
                    ["Programa de pontos", "Desconto para clientes antigos", "Aniversário do cliente", 
                     "Newsletter exclusiva", "Pré-venda de novidades", "Atendimento VIP", "Evento exclusivo"],
                    ["Aniversário do cliente"]
                )
            )
            # Auto-save estrategias_fidelizacao
            if estrategias_fidelizacao != st.session_state.business_data.get('estrategias_fidelizacao'):
                st.session_state.business_data['estrategias_fidelizacao'] = estrategias_fidelizacao
                save_user_data()
            
            metricas_acompanhar = st.multiselect(
                "Métricas que acompanhará",
                ["Número de seguidores", "Engajamento nas redes", "Conversões de vendas", "CAC (Custo de Aquisição)", 
                 "LTV (Valor do cliente)", "Taxa de retenção", "NPS (Satisfação)", "ROI do marketing"],
                default=safe_multiselect_default(
                    st.session_state.business_data.get('metricas_acompanhar', []),
                    ["Número de seguidores", "Engajamento nas redes", "Conversões de vendas", "CAC (Custo de Aquisição)", 
                     "LTV (Valor do cliente)", "Taxa de retenção", "NPS (Satisfação)", "ROI do marketing"],
                    ["Conversões de vendas", "NPS (Satisfação)"]
                )
            )
            # Auto-save metricas_acompanhar
            if metricas_acompanhar != st.session_state.business_data.get('metricas_acompanhar'):
                st.session_state.business_data['metricas_acompanhar'] = metricas_acompanhar
                save_user_data()
            
            plano_lancamento = st.text_area(
                "Plano para lançamento/inauguração",
                value=st.session_state.business_data.get('plano_lancamento', ''),
                height=100,
                placeholder="Ex: Evento de inauguração, promoções especiais, parcerias para divulgação..."
            )
            # Auto-save plano_lancamento
            if plano_lancamento != st.session_state.business_data.get('plano_lancamento'):
                st.session_state.business_data['plano_lancamento'] = plano_lancamento
                save_user_data()
    
    # Store all data
    st.session_state.business_data.update({
        'proposta_valor': proposta_valor,
        'publico_alvo_marketing': publico_alvo_marketing,
        'tom_comunicacao': tom_comunicacao,
        'objetivos_marketing': objetivos_marketing,
        'orcamento_marketing': orcamento_marketing,
        'estrategias_diferenciacao': estrategias_diferenciacao,
        'canais_digitais': canais_digitais,
        'frequencia_posts': frequencia_posts,
        'tipos_conteudo': tipos_conteudo,
        'canais_tradicionais': canais_tradicionais,
        'parcerias_marketing': parcerias_marketing,
        'programa_indicacoes': programa_indicacoes,
        'campanhas_sazonais': campanhas_sazonais,
        'tipos_promocoes': tipos_promocoes,
        'estrategias_fidelizacao': estrategias_fidelizacao,
        'metricas_acompanhar': metricas_acompanhar,
        'plano_lancamento': plano_lancamento
    })
    
    # Auto-save
    save_user_data()
    
    st.markdown("---")
    
    # Navigation
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("⬅️ Etapa Anterior", key="prev_step6"):
            st.session_state.step = 5
            st.rerun()
    with col3:
        if st.button("Próxima Etapa ➡️", type="primary", key="next_step6"):
            st.session_state.step = 7
            st.rerun()

def show_step_7():
    """Etapa 7: Plano Operacional"""
    st.header("7️⃣ Plano Operacional")
    st.markdown("**FASE 7: OPERAÇÕES** - Defina como sua ótica funcionará no dia a dia")
    
    # Tabs para organizar plano operacional
    tab1, tab2, tab3 = st.tabs(["🏪 Estrutura da Loja", "⚙️ Processos Operacionais", "📋 Gestão e Controles"])
    
    with tab1:
        st.subheader("🏪 Layout e Infraestrutura")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Layout da Loja**")
            
            layout_areas = st.multiselect(
                "Áreas que terá na loja",
                ["Área de atendimento", "Exposição de armações", "Exposição de óculos de sol", "Área de ajustes", 
                 "Estoque", "Caixa", "Área de espera", "Consultório/Exames", "Escritório"],
                default=safe_multiselect_default(
                    st.session_state.business_data.get('layout_areas', []),
                    ["Área de atendimento", "Exposição de armações", "Exposição de óculos de sol", "Área de ajustes", 
                     "Estoque", "Caixa", "Área de espera", "Consultório/Exames", "Escritório"],
                    ["Área de atendimento", "Exposição de armações", "Caixa"]
                )
            )
            # Auto-save layout_areas
            if layout_areas != st.session_state.business_data.get('layout_areas'):
                st.session_state.business_data['layout_areas'] = layout_areas
                save_user_data()
            
            equipamentos_necessarios = st.multiselect(
                "Equipamentos necessários",
                ["Computador/PDV", "Impressora", "Leitor de cartão", "Balança de precisão", 
                 "Kit de ajustes", "Expositor de armações", "Vitrine com segurança", "Sistema de segurança"],
                default=safe_multiselect_default(
                    st.session_state.business_data.get('equipamentos_necessarios', []),
                    ["Computador/PDV", "Impressora", "Leitor de cartão", "Balança de precisão", 
                     "Kit de ajustes", "Expositor de armações", "Vitrine com segurança", "Sistema de segurança"],
                    ["Computador/PDV", "Kit de ajustes"]
                )
            )
            # Auto-save equipamentos_necessarios
            if equipamentos_necessarios != st.session_state.business_data.get('equipamentos_necessarios'):
                st.session_state.business_data['equipamentos_necessarios'] = equipamentos_necessarios
                save_user_data()
            
            investimento_equipamentos = st.number_input(
                "Investimento em equipamentos (R$)",
                min_value=0.0,
                value=float(st.session_state.business_data.get('investimento_equipamentos', 10000)),
                step=1000.0,
                format="%.0f"
            )
            # Auto-save investimento_equipamentos
            if investimento_equipamentos != st.session_state.business_data.get('investimento_equipamentos'):
                st.session_state.business_data['investimento_equipamentos'] = investimento_equipamentos
                save_user_data()
            st.caption(f"💰 {format_currency(investimento_equipamentos)}")
        
        with col2:
            st.markdown("**Funcionamento**")
            
            horario_funcionamento = st.text_input(
                "Horário de funcionamento",
                value=st.session_state.business_data.get('horario_funcionamento', ''),
                placeholder="Ex: Segunda a Sexta 8h às 18h, Sábado 8h às 12h"
            )
            # Auto-save horario_funcionamento
            if horario_funcionamento != st.session_state.business_data.get('horario_funcionamento'):
                st.session_state.business_data['horario_funcionamento'] = horario_funcionamento
                save_user_data()
            
            dias_funcionamento = st.multiselect(
                "Dias de funcionamento",
                ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"],
                default=safe_multiselect_default(
                    st.session_state.business_data.get('dias_funcionamento', []),
                    ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"],
                    ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado"]
                )
            )
            # Auto-save dias_funcionamento
            if dias_funcionamento != st.session_state.business_data.get('dias_funcionamento'):
                st.session_state.business_data['dias_funcionamento'] = dias_funcionamento
                save_user_data()
            
            capacidade_atendimento = st.number_input(
                "Capacidade de atendimento (clientes/dia)",
                min_value=1,
                value=int(st.session_state.business_data.get('capacidade_atendimento', 20)),
                step=5
            )
            # Auto-save capacidade_atendimento
            if capacidade_atendimento != st.session_state.business_data.get('capacidade_atendimento'):
                st.session_state.business_data['capacidade_atendimento'] = capacidade_atendimento
                save_user_data()
            
            sistema_gestao = st.selectbox(
                "Sistema de gestão que utilizará",
                ["Planilhas Excel", "Software específico para óticas", "Sistema ERP", "Software customizado", "Ainda não definido"],
                index=["Planilhas Excel", "Software específico para óticas", "Sistema ERP", "Software customizado", "Ainda não definido"].index(
                    st.session_state.business_data.get('sistema_gestao', 'Software específico para óticas')
                )
            )
            # Auto-save sistema_gestao
            if sistema_gestao != st.session_state.business_data.get('sistema_gestao'):
                st.session_state.business_data['sistema_gestao'] = sistema_gestao
                save_user_data()
    
    with tab2:
        st.subheader("⚙️ Fluxos de Trabalho")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Processo de Atendimento**")
            
            fluxo_atendimento = st.text_area(
                "Descreva o fluxo de atendimento ao cliente",
                value=st.session_state.business_data.get('fluxo_atendimento', ''),
                height=120,
                placeholder="Ex: 1. Recepção e identificação da necessidade\n2. Análise da receita\n3. Orientação sobre produtos..."
            )
            # Auto-save fluxo_atendimento
            if fluxo_atendimento != st.session_state.business_data.get('fluxo_atendimento'):
                st.session_state.business_data['fluxo_atendimento'] = fluxo_atendimento
                save_user_data()
            
            tempo_medio_atendimento = st.selectbox(
                "Tempo médio de atendimento por cliente",
                ["15-20 minutos", "20-30 minutos", "30-45 minutos", "45-60 minutos", "Mais de 1 hora"],
                index=["15-20 minutos", "20-30 minutos", "30-45 minutos", "45-60 minutos", "Mais de 1 hora"].index(
                    st.session_state.business_data.get('tempo_medio_atendimento', '30-45 minutos')
                )
            )
            # Auto-save tempo_medio_atendimento
            if tempo_medio_atendimento != st.session_state.business_data.get('tempo_medio_atendimento'):
                st.session_state.business_data['tempo_medio_atendimento'] = tempo_medio_atendimento
                save_user_data()
            
            politicas_atendimento = st.multiselect(
                "Políticas de atendimento",
                ["Atendimento por ordem de chegada", "Agendamento obrigatório", "Agendamento opcional", 
                 "Prioridade para idosos", "Atendimento domiciliar", "Televendas", "WhatsApp"],
                default=safe_multiselect_default(
                    st.session_state.business_data.get('politicas_atendimento', []),
                    ["Atendimento por ordem de chegada", "Agendamento obrigatório", "Agendamento opcional", 
                     "Prioridade para idosos", "Atendimento domiciliar", "Televendas", "WhatsApp"],
                    ["Atendimento por ordem de chegada", "WhatsApp"]
                )
            )
            # Auto-save politicas_atendimento
            if politicas_atendimento != st.session_state.business_data.get('politicas_atendimento'):
                st.session_state.business_data['politicas_atendimento'] = politicas_atendimento
                save_user_data()
        
        with col2:
            st.markdown("**Gestão de Estoque**")
            
            controle_estoque = st.selectbox(
                "Método de controle de estoque",
                ["Manual/Planilhas", "Sistema automatizado", "Código de barras", "RFID", "Controle misto"],
                index=["Manual/Planilhas", "Sistema automatizado", "Código de barras", "RFID", "Controle misto"].index(
                    st.session_state.business_data.get('controle_estoque', 'Sistema automatizado')
                )
            )
            # Auto-save controle_estoque
            if controle_estoque != st.session_state.business_data.get('controle_estoque'):
                st.session_state.business_data['controle_estoque'] = controle_estoque
                save_user_data()
            
            giro_estoque_planejado = st.selectbox(
                "Giro de estoque planejado",
                ["1-2 vezes por ano", "3-4 vezes por ano", "5-6 vezes por ano", "Mais de 6 vezes por ano"],
                index=["1-2 vezes por ano", "3-4 vezes por ano", "5-6 vezes por ano", "Mais de 6 vezes por ano"].index(
                    st.session_state.business_data.get('giro_estoque_planejado', '3-4 vezes por ano')
                )
            )
            # Auto-save giro_estoque_planejado
            if giro_estoque_planejado != st.session_state.business_data.get('giro_estoque_planejado'):
                st.session_state.business_data['giro_estoque_planejado'] = giro_estoque_planejado
                save_user_data()
            
            politicas_compra = st.text_area(
                "Políticas de compra e reposição",
                value=st.session_state.business_data.get('politicas_compra', ''),
                height=100,
                placeholder="Ex: Compras mensais, estoque mínimo de 30 dias, análise ABC..."
            )
            # Auto-save politicas_compra
            if politicas_compra != st.session_state.business_data.get('politicas_compra'):
                st.session_state.business_data['politicas_compra'] = politicas_compra
                save_user_data()
    
    with tab3:
        st.subheader("📋 Controles e Indicadores")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Indicadores de Performance**")
            
            kpis_acompanhar = st.multiselect(
                "KPIs que acompanhará",
                ["Faturamento diário", "Ticket médio", "Conversão de vendas", "Satisfação do cliente", 
                 "Giro de estoque", "Margem de lucro", "Custo por cliente", "Taxa de retorno"],
                default=safe_multiselect_default(
                    st.session_state.business_data.get('kpis_acompanhar', []),
                    ["Faturamento diário", "Ticket médio", "Conversão de vendas", "Satisfação do cliente", 
                     "Giro de estoque", "Margem de lucro", "Custo por cliente", "Taxa de retorno"],
                    ["Faturamento diário", "Ticket médio", "Satisfação do cliente"]
                )
            )
            # Auto-save kpis_acompanhar
            if kpis_acompanhar != st.session_state.business_data.get('kpis_acompanhar'):
                st.session_state.business_data['kpis_acompanhar'] = kpis_acompanhar
                save_user_data()
            
            frequencia_relatorios = st.selectbox(
                "Frequência dos relatórios gerenciais",
                ["Diário", "Semanal", "Quinzenal", "Mensal", "Conforme necessidade"],
                index=["Diário", "Semanal", "Quinzenal", "Mensal", "Conforme necessidade"].index(
                    st.session_state.business_data.get('frequencia_relatorios', 'Semanal')
                )
            )
            # Auto-save frequencia_relatorios
            if frequencia_relatorios != st.session_state.business_data.get('frequencia_relatorios'):
                st.session_state.business_data['frequencia_relatorios'] = frequencia_relatorios
                save_user_data()
            
            # Sincronização com projeções financeiras
            valor_projecao = st.session_state.business_data.get('vendas_mes_1', None)
            valor_atual_meta = st.session_state.business_data.get('metas_mensais', None)
            
            if valor_projecao:
                col_sync1, col_sync2 = st.columns([3, 1])
                with col_sync1:
                    if valor_projecao != valor_atual_meta:
                        st.warning(f"Valor das Projeções Financeiras: {format_currency(valor_projecao)} (diferente da meta atual)")
                    else:
                        st.success(f"Sincronizado com Projeções Financeiras: {format_currency(valor_projecao)}")
                
                with col_sync2:
                    if st.button("🔄 Sincronizar", help="Atualizar com valor das Projeções Financeiras"):
                        st.session_state.business_data['metas_mensais'] = valor_projecao
                        save_user_data()
                        st.rerun()
            
            valor_atual = st.session_state.business_data.get('metas_mensais', valor_projecao if valor_projecao else 20831)
            
            metas_mensais = st.number_input(
                "Meta de faturamento mensal (R$)",
                min_value=0.0,
                value=float(valor_atual),
                step=1000.0,
                format="%.0f"
            )
            # Auto-save metas_mensais
            if metas_mensais != st.session_state.business_data.get('metas_mensais'):
                st.session_state.business_data['metas_mensais'] = metas_mensais
                save_user_data()
            st.caption(f"💰 {format_currency(metas_mensais)}/mês")
        
        with col2:
            st.markdown("**Controles Operacionais**")
            
            controles_qualidade = st.multiselect(
                "Controles de qualidade implementados",
                ["Checklist de atendimento", "Pesquisa de satisfação", "Controle de prazos", 
                 "Verificação dupla de receitas", "Testes de equipamentos", "Auditorias internas"],
                default=safe_multiselect_default(
                    st.session_state.business_data.get('controles_qualidade', []),
                    ["Checklist de atendimento", "Pesquisa de satisfação", "Controle de prazos", 
                     "Verificação dupla de receitas", "Testes de equipamentos", "Auditorias internas"],
                    ["Pesquisa de satisfação", "Controle de prazos"]
                )
            )
            # Auto-save controles_qualidade
            if controles_qualidade != st.session_state.business_data.get('controles_qualidade'):
                st.session_state.business_data['controles_qualidade'] = controles_qualidade
                save_user_data()
            
            backup_dados = st.selectbox(
                "Política de backup de dados",
                ["Backup diário automático", "Backup semanal", "Backup mensal", "Backup em nuvem", "Não planejado ainda"],
                index=["Backup diário automático", "Backup semanal", "Backup mensal", "Backup em nuvem", "Não planejado ainda"].index(
                    st.session_state.business_data.get('backup_dados', 'Backup em nuvem')
                )
            )
            # Auto-save backup_dados
            if backup_dados != st.session_state.business_data.get('backup_dados'):
                st.session_state.business_data['backup_dados'] = backup_dados
                save_user_data()
            
            plano_contingencia = st.text_area(
                "Plano de contingência/emergência",
                value=st.session_state.business_data.get('plano_contingencia', ''),
                height=100,
                placeholder="Ex: Procedimentos em caso de falha do sistema, falta de energia, ausência de funcionários..."
            )
            # Auto-save plano_contingencia
            if plano_contingencia != st.session_state.business_data.get('plano_contingencia'):
                st.session_state.business_data['plano_contingencia'] = plano_contingencia
                save_user_data()
    
    # Store all data
    st.session_state.business_data.update({
        'layout_areas': layout_areas,
        'equipamentos_necessarios': equipamentos_necessarios,
        'investimento_equipamentos': investimento_equipamentos,
        'horario_funcionamento': horario_funcionamento,
        'dias_funcionamento': dias_funcionamento,
        'capacidade_atendimento': capacidade_atendimento,
        'sistema_gestao': sistema_gestao,
        'fluxo_atendimento': fluxo_atendimento,
        'tempo_medio_atendimento': tempo_medio_atendimento,
        'politicas_atendimento': politicas_atendimento,
        'controle_estoque': controle_estoque,
        'giro_estoque_planejado': giro_estoque_planejado,
        'politicas_compra': politicas_compra,
        'kpis_acompanhar': kpis_acompanhar,
        'frequencia_relatorios': frequencia_relatorios,
        'metas_mensais': metas_mensais,
        'controles_qualidade': controles_qualidade,
        'backup_dados': backup_dados,
        'plano_contingencia': plano_contingencia
    })
    
    # Auto-save
    save_user_data()
    
    st.markdown("---")
    
    # Navigation
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("⬅️ Etapa Anterior", key="prev_step7"):
            st.session_state.step = 6
            st.rerun()
    with col3:
        if st.button("Próxima Etapa ➡️", type="primary", key="next_step7"):
            st.session_state.step = 8
            st.rerun()

def show_step_8():
    """Etapa 8: Gestão de Pessoas"""
    st.header("8️⃣ Gestão de Pessoas")
    st.markdown("**FASE 8: PESSOAS** - Planeje sua equipe e gestão de recursos humanos")
    
    # Tabs para organizar gestão de pessoas
    tab1, tab2, tab3, tab4 = st.tabs(["👥 Estrutura da Equipe", "📋 Pessoas e Parceiros", "🎯 Sistema de Captação", "💰 Custos Trabalhistas"])
    
    with tab1:
        st.subheader("👥 Planejamento da Equipe")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Cargos e Funções**")
            
            num_funcionarios = st.number_input(
                "Número total de funcionários (incluindo você)",
                min_value=0,
                value=int(st.session_state.business_data.get('num_funcionarios', 1)),
                step=1,
                help="Para começar apenas aos sábados, você pode usar 0 e trabalhar só com comissionistas"
            )
            # Auto-save num_funcionarios
            if num_funcionarios != st.session_state.business_data.get('num_funcionarios'):
                st.session_state.business_data['num_funcionarios'] = num_funcionarios
                save_user_data()
            
            cargos_necessarios = st.multiselect(
                "Cargos que pretende ter na equipe",
                ["Proprietário/Gerente", "Vendedor/Atendente", "Técnico em óptica", "Recepcionista", 
                 "Auxiliar administrativo", "Técnico em lentes", "Oftalmologista parceiro", "Limpeza/Segurança"],
                default=safe_multiselect_default(
                    st.session_state.business_data.get('cargos_necessarios', []),
                    ["Proprietário/Gerente", "Vendedor/Atendente", "Técnico em óptica", "Recepcionista", 
                     "Auxiliar administrativo", "Técnico em lentes", "Oftalmologista parceiro", "Limpeza/Segurança"],
                    ["Proprietário/Gerente", "Vendedor/Atendente"]
                )
            )
            # Auto-save cargos_necessarios
            if cargos_necessarios != st.session_state.business_data.get('cargos_necessarios'):
                st.session_state.business_data['cargos_necessarios'] = cargos_necessarios
                save_user_data()
            
            perfil_funcionarios = st.text_area(
                "Perfil desejado dos funcionários",
                value=st.session_state.business_data.get('perfil_funcionarios', ''),
                height=100,
                placeholder="Ex: Experiência em vendas, comunicativo, conhecimento em óptica..."
            )
            # Auto-save perfil_funcionarios
            if perfil_funcionarios != st.session_state.business_data.get('perfil_funcionarios'):
                st.session_state.business_data['perfil_funcionarios'] = perfil_funcionarios
                save_user_data()
            
            estrategia_contratacao = st.selectbox(
                "Estratégia de contratação",
                ["Contratação imediata", "Contratação gradual", "Terceirização", "Parcerias", "Família/Conhecidos"],
                index=["Contratação imediata", "Contratação gradual", "Terceirização", "Parcerias", "Família/Conhecidos"].index(
                    st.session_state.business_data.get('estrategia_contratacao', 'Contratação gradual')
                )
            )
            # Auto-save estrategia_contratacao
            if estrategia_contratacao != st.session_state.business_data.get('estrategia_contratacao'):
                st.session_state.business_data['estrategia_contratacao'] = estrategia_contratacao
                save_user_data()
        
        with col2:
            st.markdown("**Organização da Equipe**")
            
            jornada_trabalho = st.selectbox(
                "Jornada de trabalho padrão",
                ["44h semanais", "40h semanais", "36h semanais", "Meio período", "Horário flexível"],
                index=["44h semanais", "40h semanais", "36h semanais", "Meio período", "Horário flexível"].index(
                    st.session_state.business_data.get('jornada_trabalho', '44h semanais')
                )
            )
            # Auto-save jornada_trabalho
            if jornada_trabalho != st.session_state.business_data.get('jornada_trabalho'):
                st.session_state.business_data['jornada_trabalho'] = jornada_trabalho
                save_user_data()
            
            escala_trabalho = st.multiselect(
                "Organização dos turnos",
                ["Turno único", "Dois turnos", "Escala de revezamento", "Horário corrido", "Plantão aos sábados"],
                default=safe_multiselect_default(
                    st.session_state.business_data.get('escala_trabalho', []),
                    ["Turno único", "Dois turnos", "Escala de revezamento", "Horário corrido", "Plantão aos sábados"],
                    ["Turno único"]
                )
            )
            # Auto-save escala_trabalho
            if escala_trabalho != st.session_state.business_data.get('escala_trabalho'):
                st.session_state.business_data['escala_trabalho'] = escala_trabalho
                save_user_data()
            
            faixa_salarial = st.text_area(
                "Faixa salarial prevista por cargo",
                value=st.session_state.business_data.get('faixa_salarial', ''),
                height=100,
                placeholder="Ex: Vendedor: R$ 1.500-2.000\nTécnico: R$ 2.000-2.500"
            )
            # Auto-save faixa_salarial
            if faixa_salarial != st.session_state.business_data.get('faixa_salarial'):
                st.session_state.business_data['faixa_salarial'] = faixa_salarial
                save_user_data()
            
            plano_crescimento_equipe = st.text_area(
                "Plano de crescimento da equipe",
                value=st.session_state.business_data.get('plano_crescimento_equipe', ''),
                height=80,
                placeholder="Como pretende expandir a equipe conforme o negócio cresce?"
            )
            # Auto-save plano_crescimento_equipe
            if plano_crescimento_equipe != st.session_state.business_data.get('plano_crescimento_equipe'):
                st.session_state.business_data['plano_crescimento_equipe'] = plano_crescimento_equipe
                save_user_data()
    
    with tab2:
        st.subheader("👥 Funcionários Planejados")
        
        # Inicializar lista de funcionários planejados
        if 'funcionarios_planejados' not in st.session_state.business_data:
            st.session_state.business_data['funcionarios_planejados'] = []
        
        # Verificar se existem funcionários do DP e Tributação para sincronizar
        funcionarios_dp = st.session_state.get('funcionarios', [])
        
        if funcionarios_dp and len(st.session_state.business_data['funcionarios_planejados']) == 0:
            st.info("🔄 **Sincronização com DP e Tributação**: Encontrados funcionários cadastrados no DP. Deseja sincronizá-los?")
            
            col_sync1, col_sync2 = st.columns(2)
            with col_sync1:
                if st.button("✅ Sincronizar do DP e Tributação", type="primary"):
                    funcionarios_sincronizados = []
                    for func in funcionarios_dp:
                        funcionarios_sincronizados.append({
                            'nome': func.get('nome', 'Funcionário'),
                            'cargo': func.get('cargo', 'Vendedor(a)'),
                            'salario': func.get('salario_base', 1518.00),
                            'tipo_contrato': func.get('tipo_contrato', 'CLT'),
                            'data_admissao': func.get('data_admissao', '2024-01-01'),
                            'vale_transporte': func.get('vale_transporte', True),
                            'vale_refeicao': func.get('vale_refeicao', 25.00),
                            'plano_saude': func.get('plano_saude', False),
                            'comissao': func.get('comissao_percentual', 0.0),
                            'escolaridade': func.get('grau_instrucao', 'Ensino Médio'),
                            'dependentes': func.get('dependentes', 0)
                        })
                    
                    st.session_state.business_data['funcionarios_planejados'] = funcionarios_sincronizados
                    save_user_data()
                    st.success(f"✅ {len(funcionarios_sincronizados)} funcionário(s) sincronizado(s) do DP!")
                    st.rerun()
            
            with col_sync2:
                if st.button("🔄 Manter Separado", type="secondary"):
                    st.info("Os dados permanecem separados. Você pode gerenciar independentemente.")
        
        # Interface para adicionar funcionários planejados
        with st.expander("➕ Adicionar Funcionário Planejado"):
            col1, col2 = st.columns(2)
            
            with col1:
                nome_planejado = st.text_input("Nome do funcionário", key="nome_planejado")
                cargo_planejado = st.selectbox(
                    "Cargo planejado",
                    ["Vendedor(a)", "Optometrista", "Gerente", "Recepcionista", "Técnico em Ótica", "Auxiliar Administrativo"],
                    key="cargo_planejado"
                )
                salario_planejado = st.number_input(
                    "Salário planejado (R$)",
                    min_value=1518.00,
                    value=1600.00,
                    step=100.00,
                    key="salario_planejado"
                )
                tipo_contrato_planejado = st.selectbox(
                    "Tipo de contrato",
                    ["CLT", "MEI", "Prestador de Serviços"],
                    key="tipo_contrato_planejado"
                )
            
            with col2:
                data_admissao_planejada = st.date_input("Data de admissão planejada", key="data_planejada")
                vale_transporte_planejado = st.checkbox("Vale transporte", key="vt_planejado")
                vale_refeicao_planejado = st.number_input(
                    "Vale refeição diário (R$)",
                    min_value=0.00,
                    value=25.00,
                    step=5.00,
                    key="vr_planejado"
                )
                plano_saude_planejado = st.checkbox("Plano de saúde", key="plano_planejado")
            
            if st.button("➕ Adicionar Funcionário Planejado", type="primary"):
                if nome_planejado:
                    novo_funcionario = {
                        'nome': nome_planejado,
                        'cargo': cargo_planejado,
                        'salario': salario_planejado,
                        'tipo_contrato': tipo_contrato_planejado,
                        'data_admissao': str(data_admissao_planejada),
                        'vale_transporte': vale_transporte_planejado,
                        'vale_refeicao': vale_refeicao_planejado,
                        'plano_saude': plano_saude_planejado,
                        'comissao': 0.0,
                        'escolaridade': 'Ensino Médio',
                        'dependentes': 0
                    }
                    st.session_state.business_data['funcionarios_planejados'].append(novo_funcionario)
                    save_user_data()
                    st.success(f"✅ Funcionário {nome_planejado} adicionado com sucesso!")
                    st.rerun()
                else:
                    st.error("⚠️ Por favor, preencha o nome do funcionário.")
        
        # Exibir funcionários planejados
        if st.session_state.business_data['funcionarios_planejados']:
            st.markdown("### 👥 Funcionários Planejados Cadastrados")
            
            for i, func in enumerate(st.session_state.business_data['funcionarios_planejados']):
                with st.container():
                    col1, col2, col3 = st.columns([3, 2, 1])
                    
                    with col1:
                        st.markdown(f"**{func['nome']}**")
                        st.caption(f"{func['cargo']} • {func['tipo_contrato']} • {format_currency(func['salario'])}")
                    
                    with col2:
                        st.markdown(f"**Admissão:** {func['data_admissao']}")
                        beneficios = []
                        if func['vale_transporte']: beneficios.append("VT")
                        if func['vale_refeicao'] > 0: beneficios.append(f"VR R${func['vale_refeicao']:.0f}")
                        if func['plano_saude']: beneficios.append("Plano Saúde")
                        st.caption(f"Benefícios: {', '.join(beneficios) if beneficios else 'Nenhum'}")
                    
                    with col3:
                        if st.button("🗑️", key=f"remove_planejado_{i}", help="Remover funcionário"):
                            st.session_state.business_data['funcionarios_planejados'].pop(i)
                            save_user_data()
                            st.rerun()
                    
                    st.divider()
            
            # Resumo de custos
            total_salarios_planejados = sum(func['salario'] for func in st.session_state.business_data['funcionarios_planejados'])
            total_funcionarios_planejados = len(st.session_state.business_data['funcionarios_planejados'])
            
            col_resumo1, col_resumo2, col_resumo3 = st.columns(3)
            
            with col_resumo1:
                st.metric("Total de Funcionários", total_funcionarios_planejados)
            
            with col_resumo2:
                st.metric("Folha Salarial Base", format_currency(total_salarios_planejados))
            
            with col_resumo3:
                # Usar os dados diretamente do session_state
                folha_com_encargos = 0
                
                # Usar dados do session_state
                for func in st.session_state.business_data['funcionarios_planejados']:
                    salario = float(func.get('salario', 0))
                    tipo_contrato = func.get('tipo_contrato', 'CLT')
                    
                    if tipo_contrato == 'CLT':
                        # Calcular encargos detalhados como na aba de custos
                        inss_empresa = salario * 0.20
                        fgts = salario * 0.08
                        ferias = (salario * 1.33) / 12
                        decimo_terceiro = salario / 12
                        outros_encargos = salario * 0.10
                        encargos_total = inss_empresa + fgts + ferias + decimo_terceiro + outros_encargos
                        folha_com_encargos += salario + encargos_total
                    else:
                        # Prestadores sem encargos
                        folha_com_encargos += salario
                
                st.metric("Custo Total Estimado", format_currency(folha_com_encargos))
                
                # Salvar o valor calculado para consistência entre abas
                st.session_state.business_data['custo_total_estimado'] = folha_com_encargos
                save_user_data()
            
            st.info("💡 **Dica**: Estes funcionários podem ser importados automaticamente para o **DP e Tributação** para cálculos detalhados.")
        
        else:
            st.info("📝 Nenhum funcionário planejado cadastrado. Use o formulário acima para adicionar.")
    
    with tab3:
        st.subheader("📋 Pessoas e Parceiros")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Políticas Trabalhistas**")
            
            regime_contratacao = st.multiselect(
                "Regimes de contratação que utilizará",
                ["CLT", "MEI parceiro", "Prestação de serviço", "Estágio", "Terceirização", "Comissionista"],
                default=safe_multiselect_default(
                    st.session_state.business_data.get('regime_contratacao', []),
                    ["CLT", "MEI parceiro", "Prestação de serviço", "Estágio", "Terceirização", "Comissionista"],
                    ["CLT"]
                )
            )
            # Auto-save regime_contratacao
            if regime_contratacao != st.session_state.business_data.get('regime_contratacao'):
                st.session_state.business_data['regime_contratacao'] = regime_contratacao
                save_user_data()
            
            beneficios_oferecidos = st.multiselect(
                "Benefícios que oferecerá",
                ["Vale transporte", "Vale alimentação", "Plano de saúde", "Comissões", 
                 "Desconto em produtos", "13º salário", "Férias", "FGTS"],
                default=safe_multiselect_default(
                    st.session_state.business_data.get('beneficios_oferecidos', []),
                    ["Vale transporte", "Vale alimentação", "Plano de saúde", "Comissões", 
                     "Desconto em produtos", "13º salário", "Férias", "FGTS"],
                    ["Vale transporte", "13º salário", "Férias", "FGTS"]
                )
            )
            # Auto-save beneficios_oferecidos
            if beneficios_oferecidos != st.session_state.business_data.get('beneficios_oferecidos'):
                st.session_state.business_data['beneficios_oferecidos'] = beneficios_oferecidos
                save_user_data()
            
            politica_comissoes = st.text_area(
                "Política de comissões/metas",
                value=st.session_state.business_data.get('politica_comissoes', ''),
                height=100,
                placeholder="Ex: 3% sobre vendas acima da meta, bônus por satisfação do cliente..."
            )
            # Auto-save politica_comissoes
            if politica_comissoes != st.session_state.business_data.get('politica_comissoes'):
                st.session_state.business_data['politica_comissoes'] = politica_comissoes
                save_user_data()
        
        with col2:
            st.markdown("**Desenvolvimento e Treinamento**")
            
            plano_treinamento = st.multiselect(
                "Treinamentos que oferecerá",
                ["Atendimento ao cliente", "Conhecimentos em óptica", "Vendas", "Sistema/Software", 
                 "Produtos e marcas", "Ajustes técnicos", "Compliance/Segurança"],
                default=safe_multiselect_default(
                    st.session_state.business_data.get('plano_treinamento', []),
                    ["Atendimento ao cliente", "Conhecimentos em óptica", "Vendas", "Sistema/Software", 
                     "Produtos e marcas", "Ajustes técnicos", "Compliance/Segurança"],
                    ["Atendimento ao cliente", "Vendas"]
                )
            )
            # Auto-save plano_treinamento
            if plano_treinamento != st.session_state.business_data.get('plano_treinamento'):
                st.session_state.business_data['plano_treinamento'] = plano_treinamento
                save_user_data()
            
            frequencia_treinamento = st.selectbox(
                "Frequência dos treinamentos",
                ["Mensal", "Trimestral", "Semestral", "Anual", "Conforme necessidade"],
                index=["Mensal", "Trimestral", "Semestral", "Anual", "Conforme necessidade"].index(
                    st.session_state.business_data.get('frequencia_treinamento', 'Trimestral')
                )
            )
            # Auto-save frequencia_treinamento
            if frequencia_treinamento != st.session_state.business_data.get('frequencia_treinamento'):
                st.session_state.business_data['frequencia_treinamento'] = frequencia_treinamento
                save_user_data()
            
            avaliacao_desempenho = st.text_area(
                "Sistema de avaliação de desempenho",
                value=st.session_state.business_data.get('avaliacao_desempenho', ''),
                height=100,
                placeholder="Como avaliará e acompanhará o desempenho da equipe?"
            )
            # Auto-save avaliacao_desempenho
            if avaliacao_desempenho != st.session_state.business_data.get('avaliacao_desempenho'):
                st.session_state.business_data['avaliacao_desempenho'] = avaliacao_desempenho
                save_user_data()
    
    with tab3:
        st.subheader("🎯 Sistema de Captação e Comissões")
        st.markdown("Configure comissões diferenciadas por modalidade de venda e tipo de produto")
        
        # Ativar sistema de captação
        usar_sistema_captacao = st.checkbox(
            "Ativar sistema de captação com comissões",
            value=st.session_state.business_data.get('usar_sistema_captacao', False),
            help="Permite configurar comissões diferentes para vendas à vista e parceladas"
        )
        
        if usar_sistema_captacao != st.session_state.business_data.get('usar_sistema_captacao'):
            st.session_state.business_data['usar_sistema_captacao'] = usar_sistema_captacao
            save_user_data()
        
        if usar_sistema_captacao:
            st.markdown("### 💰 Configuração de Comissões por Modalidade")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**🟢 Vendas À Vista**")
                comissao_avista = st.number_input(
                    "Comissão por venda à vista (R$)",
                    min_value=0.0,
                    value=float(st.session_state.business_data.get('comissao_avista', 30.0)),
                    step=5.0,
                    format="%.2f",
                    help="Valor fixo pago por cada venda à vista convertida"
                )
                
                if comissao_avista != st.session_state.business_data.get('comissao_avista'):
                    st.session_state.business_data['comissao_avista'] = comissao_avista
                    save_user_data()
                
                # Tipo de comissão à vista
                tipo_comissao_avista = st.selectbox(
                    "Tipo de comissão à vista",
                    ["Valor fixo por venda", "Percentual sobre valor"],
                    index=0 if st.session_state.business_data.get('tipo_comissao_avista', 'Valor fixo por venda') == 'Valor fixo por venda' else 1
                )
                
                if tipo_comissao_avista != st.session_state.business_data.get('tipo_comissao_avista'):
                    st.session_state.business_data['tipo_comissao_avista'] = tipo_comissao_avista
                    save_user_data()
                
                if tipo_comissao_avista == "Percentual sobre valor":
                    percentual_avista = st.number_input(
                        "Percentual sobre vendas à vista (%)",
                        min_value=0.0,
                        max_value=15.0,
                        value=float(st.session_state.business_data.get('percentual_comissao_avista', 3.0)),
                        step=0.5,
                        format="%.1f"
                    )
                    
                    if percentual_avista != st.session_state.business_data.get('percentual_comissao_avista'):
                        st.session_state.business_data['percentual_comissao_avista'] = percentual_avista
                        save_user_data()
            
            with col2:
                st.markdown("**🟡 Vendas Parceladas**")
                comissao_parcelada = st.number_input(
                    "Comissão por venda parcelada (R$)",
                    min_value=0.0,
                    value=float(st.session_state.business_data.get('comissao_parcelada', 20.0)),
                    step=5.0,
                    format="%.2f",
                    help="Valor fixo pago por cada venda parcelada convertida"
                )
                
                if comissao_parcelada != st.session_state.business_data.get('comissao_parcelada'):
                    st.session_state.business_data['comissao_parcelada'] = comissao_parcelada
                    save_user_data()
                
                # Tipo de comissão parcelada
                tipo_comissao_parcelada = st.selectbox(
                    "Tipo de comissão parcelada",
                    ["Valor fixo por venda", "Percentual sobre valor"],
                    index=0 if st.session_state.business_data.get('tipo_comissao_parcelada', 'Valor fixo por venda') == 'Valor fixo por venda' else 1
                )
                
                if tipo_comissao_parcelada != st.session_state.business_data.get('tipo_comissao_parcelada'):
                    st.session_state.business_data['tipo_comissao_parcelada'] = tipo_comissao_parcelada
                    save_user_data()
                
                if tipo_comissao_parcelada == "Percentual sobre valor":
                    percentual_parcelada = st.number_input(
                        "Percentual sobre vendas parceladas (%)",
                        min_value=0.0,
                        max_value=15.0,
                        value=float(st.session_state.business_data.get('percentual_comissao_parcelada', 2.0)),
                        step=0.5,
                        format="%.1f"
                    )
                    
                    if percentual_parcelada != st.session_state.business_data.get('percentual_comissao_parcelada'):
                        st.session_state.business_data['percentual_comissao_parcelada'] = percentual_parcelada
                        save_user_data()
            
            # Configurações adicionais
            st.markdown("### 🎯 Configurações Adicionais do Sistema")
            
            col3, col4 = st.columns(2)
            
            with col3:
                st.markdown("**Comissões por Tipo de Produto**")
                
                usar_comissao_produto = st.checkbox(
                    "Diferenciar comissão por tipo de produto",
                    value=st.session_state.business_data.get('usar_comissao_produto', False)
                )
                
                if usar_comissao_produto != st.session_state.business_data.get('usar_comissao_produto'):
                    st.session_state.business_data['usar_comissao_produto'] = usar_comissao_produto
                    save_user_data()
                
                if usar_comissao_produto:
                    comissao_lentes = st.number_input(
                        "Comissão extra por lentes (R$)",
                        min_value=0.0,
                        value=float(st.session_state.business_data.get('comissao_lentes', 10.0)),
                        step=2.5,
                        format="%.2f"
                    )
                    
                    if comissao_lentes != st.session_state.business_data.get('comissao_lentes'):
                        st.session_state.business_data['comissao_lentes'] = comissao_lentes
                        save_user_data()
                    
                    comissao_armacoes = st.number_input(
                        "Comissão extra por armações (R$)",
                        min_value=0.0,
                        value=float(st.session_state.business_data.get('comissao_armacoes', 5.0)),
                        step=2.5,
                        format="%.2f"
                    )
                    
                    if comissao_armacoes != st.session_state.business_data.get('comissao_armacoes'):
                        st.session_state.business_data['comissao_armacoes'] = comissao_armacoes
                        save_user_data()
            
            with col4:
                st.markdown("**Configurações de Pagamento**")
                
                frequencia_pagamento = st.selectbox(
                    "Frequência de pagamento das comissões",
                    ["Semanal", "Quinzenal", "Mensal", "Por venda (imediato)"],
                    index=["Semanal", "Quinzenal", "Mensal", "Por venda (imediato)"].index(
                        st.session_state.business_data.get('frequencia_pagamento_comissao', 'Quinzenal')
                    )
                )
                
                if frequencia_pagamento != st.session_state.business_data.get('frequencia_pagamento_comissao'):
                    st.session_state.business_data['frequencia_pagamento_comissao'] = frequencia_pagamento
                    save_user_data()
                
                carencia_pagamento = st.number_input(
                    "Carência para pagamento (dias)",
                    min_value=0,
                    max_value=30,
                    value=int(st.session_state.business_data.get('carencia_pagamento', 7)),
                    step=1,
                    help="Dias após a venda para garantir que não há cancelamento"
                )
                
                if carencia_pagamento != st.session_state.business_data.get('carencia_pagamento'):
                    st.session_state.business_data['carencia_pagamento'] = carencia_pagamento
                    save_user_data()
                
                meta_minima = st.number_input(
                    "Meta mínima para receber comissão (vendas/mês)",
                    min_value=0,
                    value=int(st.session_state.business_data.get('meta_minima_comissao', 0)),
                    step=1,
                    help="Número mínimo de vendas no mês para receber comissão (0 = sem meta)"
                )
                
                if meta_minima != st.session_state.business_data.get('meta_minima_comissao'):
                    st.session_state.business_data['meta_minima_comissao'] = meta_minima
                    save_user_data()
            
            # Simulador de comissões
            st.markdown("### 📊 Simulador de Comissões")
            
            with st.expander("🧮 Simular Ganhos do Captador"):
                col_sim1, col_sim2, col_sim3 = st.columns(3)
                
                with col_sim1:
                    vendas_avista_sim = st.number_input("Vendas à vista no mês", min_value=0, value=15, step=1)
                    ticket_medio_avista = st.number_input("Ticket médio à vista (R$)", min_value=0.0, value=450.0, step=50.0)
                
                with col_sim2:
                    vendas_parcelada_sim = st.number_input("Vendas parceladas no mês", min_value=0, value=25, step=1)
                    ticket_medio_parcelada = st.number_input("Ticket médio parcelado (R$)", min_value=0.0, value=380.0, step=50.0)
                
                with col_sim3:
                    if usar_comissao_produto:
                        vendas_com_lentes = st.number_input("Vendas com lentes", min_value=0, value=30, step=1)
                        vendas_com_armacoes = st.number_input("Vendas com armações", min_value=0, value=40, step=1)
                
                # Calcular comissões simuladas
                if tipo_comissao_avista == "Valor fixo por venda":
                    total_comissao_avista = vendas_avista_sim * comissao_avista
                else:
                    total_comissao_avista = (vendas_avista_sim * ticket_medio_avista) * (percentual_avista / 100)
                
                if tipo_comissao_parcelada == "Valor fixo por venda":
                    total_comissao_parcelada = vendas_parcelada_sim * comissao_parcelada
                else:
                    total_comissao_parcelada = (vendas_parcelada_sim * ticket_medio_parcelada) * (percentual_parcelada / 100)
                
                total_comissao_produtos = 0
                if usar_comissao_produto:
                    total_comissao_produtos = (vendas_com_lentes * comissao_lentes) + (vendas_com_armacoes * comissao_armacoes)
                
                total_comissao_mensal = total_comissao_avista + total_comissao_parcelada + total_comissao_produtos
                
                st.markdown("**Resultado da Simulação:**")
                st.write(f"• Comissão vendas à vista: R$ {total_comissao_avista:,.2f}")
                st.write(f"• Comissão vendas parceladas: R$ {total_comissao_parcelada:,.2f}")
                if usar_comissao_produto:
                    st.write(f"• Comissão produtos extras: R$ {total_comissao_produtos:,.2f}")
                st.markdown(f"**Total mensal: R$ {total_comissao_mensal:,.2f}**")
                
                # Salvar projeção de comissões
                st.session_state.business_data['projecao_comissoes_mensal'] = total_comissao_mensal
                save_user_data()
        
        else:
            st.info("📋 Sistema de captação desativado. Ative para configurar comissões diferenciadas.")
    
    with tab4:
        st.subheader("💰 Custos Trabalhistas Calculados Automaticamente")
        
        # Buscar dados dos funcionários planejados
        funcionarios_planejados = st.session_state.business_data.get('funcionarios_planejados', [])
        
        if funcionarios_planejados:
            st.success(f"📊 **Calculando custos baseado em {len(funcionarios_planejados)} funcionários planejados**")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Breakdown por Funcionário:**")
                
                total_salarios_base = 0
                total_encargos = 0
                
                for i, func in enumerate(funcionarios_planejados):
                    nome = func.get('nome', f'Funcionário {i+1}')
                    cargo = func.get('cargo', 'N/A')
                    salario = float(func.get('salario', 0))
                    tipo_contrato = func.get('tipo_contrato', 'CLT')
                    
                    if salario > 0:
                        # Verificar tipo de contrato para aplicar encargos corretos
                        if tipo_contrato == 'CLT':
                            # Cálculo de encargos CLT
                            inss_empresa = salario * 0.20  # INSS empresa
                            fgts = salario * 0.08          # FGTS
                            ferias = (salario * 1.33) / 12 # Férias + 1/3
                            decimo_terceiro = salario / 12  # 13º salário
                            outros_encargos = salario * 0.10 # Provisões e outros
                            
                            encargos_funcionario = inss_empresa + fgts + ferias + decimo_terceiro + outros_encargos
                            custo_total_funcionario = salario + encargos_funcionario
                            
                            with st.expander(f"💼 {nome} - {cargo} (CLT)"):
                                st.write(f"• Salário base: {format_currency(salario)}")
                                st.write(f"• INSS empresa: {format_currency(inss_empresa)}")
                                st.write(f"• FGTS: {format_currency(fgts)}")
                                st.write(f"• Férias + 1/3: {format_currency(ferias)}")
                                st.write(f"• 13º salário: {format_currency(decimo_terceiro)}")
                                st.write(f"• Outros encargos: {format_currency(outros_encargos)}")
                                st.markdown(f"**Custo total: {format_currency(custo_total_funcionario)}**")
                        
                        else:
                            # Prestador de serviços - sem encargos trabalhistas
                            encargos_funcionario = 0
                            custo_total_funcionario = salario
                            
                            with st.expander(f"💼 {nome} - {cargo} (Prestador de Serviços)"):
                                st.write(f"• Valor do serviço: {format_currency(salario)}")
                                st.write("• Sem encargos trabalhistas (prestador de serviços)")
                                st.markdown(f"**Custo total: {format_currency(custo_total_funcionario)}**")
                        
                        total_salarios_base += salario
                        total_encargos += encargos_funcionario
            
            with col2:
                st.markdown("**Resumo dos Custos Trabalhistas:**")
                
                # Usar os mesmos totais calculados no loop anterior para consistência
                folha_total_com_encargos = total_salarios_base + total_encargos
                
                # Separar CLT de Prestadores para análise detalhada
                total_clt = 0
                total_prestadores = 0
                encargos_clt = 0
                
                for func in st.session_state.business_data.get('funcionarios_planejados', []):
                    salario = float(func.get('salario', 0))
                    tipo_contrato = func.get('tipo_contrato', 'CLT')
                    
                    if tipo_contrato == 'CLT':
                        total_clt += salario
                        # Usar exatamente o mesmo cálculo do primeiro loop
                        inss_empresa = salario * 0.20
                        fgts = salario * 0.08
                        ferias = (salario * 1.33) / 12
                        decimo_terceiro = salario / 12
                        outros_encargos = salario * 0.10
                        encargos_func = inss_empresa + fgts + ferias + decimo_terceiro + outros_encargos
                        encargos_clt += encargos_func
                    else:
                        total_prestadores += salario
                
                # Verificar se os totais batem
                folha_total_verificacao = total_clt + total_prestadores + encargos_clt
                if abs(folha_total_com_encargos - folha_total_verificacao) > 0.01:
                    # Usar o cálculo verificado para garantir consistência
                    folha_total_com_encargos = folha_total_verificacao
                
                # Análise separada
                st.markdown("**💼 Funcionários CLT:**")
                if total_clt > 0:
                    st.metric("Salários CLT", format_currency(total_clt))
                    st.metric("Encargos CLT", format_currency(encargos_clt), 
                             f"{(encargos_clt/total_clt*100):.1f}% dos salários")
                else:
                    st.info("Nenhum funcionário CLT")
                
                st.markdown("**🤝 Prestadores de Serviços:**")
                if total_prestadores > 0:
                    st.metric("Total Prestadores", format_currency(total_prestadores))
                    st.caption("Sem encargos trabalhistas")
                else:
                    st.info("Nenhum prestador de serviços")
                
                st.markdown("---")
                st.metric("💼 **Custo Total Mensal**", format_currency(folha_total_com_encargos))
                
                # Projeção anual
                folha_anual = folha_total_com_encargos * 12
                st.metric("📅 Projeção Anual", format_currency(folha_anual))
                
                # Análise de impacto no faturamento
                vendas_mes_1 = st.session_state.business_data.get('vendas_mes_1', 25000)
                if vendas_mes_1 > 0:
                    percentual_faturamento = (folha_total_com_encargos / vendas_mes_1) * 100
                    st.info(f"📈 **A folha representa {percentual_faturamento:.1f}% do faturamento mensal**")
                    
                    if percentual_faturamento > 30:
                        st.warning("⚠️ Folha alta (>30% do faturamento). Considere otimizar.")
                    elif percentual_faturamento < 15:
                        st.success("✅ Folha equilibrada (<15% do faturamento)")
                    else:
                        st.info("ℹ️ Folha dentro da média (15-30% do faturamento)")
                
                # Salvar dados calculados automaticamente
                st.session_state.business_data.update({
                    'folha_total_com_encargos': folha_total_com_encargos,
                    'folha_anual': folha_anual,
                    'total_salarios_clt': total_clt,
                    'total_prestadores': total_prestadores,
                    'total_encargos_clt': encargos_clt,
                    'total_salarios_base': total_salarios_base,
                    'total_encargos': total_encargos
                })
                save_user_data()
        
        else:
            st.info("📝 **Primeiro planeje sua equipe na aba 'Estrutura da Equipe'**")
            st.write("Depois os custos trabalhistas serão calculados automaticamente aqui.")
            
            # Calculadora simples para referência
            with st.expander("🧮 Calculadora de Referência (apenas para simular)"):
                st.markdown("**Use para entender custos antes de planejar a equipe:**")
                
                salario_referencia = st.number_input(
                    "Salário para simular (R$)",
                    min_value=1518.0,  # Salário mínimo 2025
                    value=2000.0,
                    step=100.0,
                    format="%.0f",
                    help="Este é apenas um exemplo para você entender os custos"
                )
                
                if salario_referencia > 0:
                    # Cálculo dos encargos
                    inss_empresa = salario_referencia * 0.20
                    fgts = salario_referencia * 0.08
                    ferias = (salario_referencia * 1.33) / 12
                    decimo_terceiro = salario_referencia / 12
                    outros_encargos = salario_referencia * 0.10
                    
                    encargos_total = inss_empresa + fgts + ferias + decimo_terceiro + outros_encargos
                    custo_total = salario_referencia + encargos_total
                    percentual = (encargos_total / salario_referencia) * 100
                    
                    st.write(f"• Salário: {format_currency(salario_referencia)}")
                    st.write(f"• Encargos: {format_currency(encargos_total)} ({percentual:.1f}%)")
                    st.write(f"• **Custo total: {format_currency(custo_total)}**")
                    st.caption("💡 Esta é apenas uma simulação. Os valores reais virão dos funcionários planejados.")
    
    # Store all data
    st.session_state.business_data.update({
        'num_funcionarios': num_funcionarios,
        'cargos_necessarios': cargos_necessarios,
        'perfil_funcionarios': perfil_funcionarios,
        'estrategia_contratacao': estrategia_contratacao,
        'jornada_trabalho': jornada_trabalho,
        'escala_trabalho': escala_trabalho,
        'faixa_salarial': faixa_salarial,
        'plano_crescimento_equipe': plano_crescimento_equipe,
        'regime_contratacao': regime_contratacao,
        'beneficios_oferecidos': beneficios_oferecidos,
        'politica_comissoes': politica_comissoes,
        'plano_treinamento': plano_treinamento,
        'frequencia_treinamento': frequencia_treinamento,
        'avaliacao_desempenho': avaliacao_desempenho
    })
    
    # Auto-save
    save_user_data()
    
    st.markdown("---")
    
    # Navigation
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("⬅️ Etapa Anterior", key="prev_step8"):
            st.session_state.step = 7
            st.rerun()
    with col3:
        if st.button("Próxima Etapa ➡️", type="primary", key="next_step8"):
            st.session_state.step = 9
            st.rerun()

def show_step_9():
    """Etapa 9: Investimento Inicial"""
    st.header("9️⃣ Investimento Inicial")
    st.markdown("**FASE 9: INVESTIMENTO** - Calcule todos os custos de abertura")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💰 Custos de Instalação")
        
        # Usar valor do sumário executivo se disponível
        custos_reforma_obj = st.session_state.business_data.get('custos_reforma', {})
        reforma_automatica = custos_reforma_obj.get('custo_total_com_adicional', 0) if custos_reforma_obj else 0
        
        if reforma_automatica > 0:
            st.info(f"💡 Valor automático do Sumário Executivo: {format_currency(reforma_automatica)}")
            # Persistir estado do checkbox
            checkbox_state = st.session_state.business_data.get('usar_reforma_auto', True)
            usar_automatico = st.checkbox("Usar valor calculado automaticamente", value=checkbox_state, key="usar_reforma_auto")
            
            # Salvar estado do checkbox
            if usar_automatico != st.session_state.business_data.get('usar_reforma_auto'):
                st.session_state.business_data['usar_reforma_auto'] = usar_automatico
                save_user_data()
            
            if usar_automatico:
                reforma_loja = reforma_automatica
                st.metric("Reforma/adequação (automática)", format_currency(reforma_loja))
            else:
                reforma_loja = st.number_input(
                    "Reforma/adequação da loja (R$) - Manual",
                    min_value=0.0,
                    value=float(st.session_state.business_data.get('reforma_loja_manual', reforma_automatica)),
                    step=1000.0,
                    format="%.0f",
                    key="reforma_loja_manual_input"
                )
                # Salvar valor manual separadamente
                if reforma_loja != st.session_state.business_data.get('reforma_loja_manual'):
                    st.session_state.business_data['reforma_loja_manual'] = reforma_loja
        else:
            st.warning("⚠️ Configure a reforma no Sumário Executivo (Etapa 1) para cálculo automático")
            reforma_loja = st.number_input(
                "Reforma/adequação da loja (R$)",
                min_value=0.0,
                value=float(st.session_state.business_data.get('reforma_loja', 15000)),
                step=1000.0,
                format="%.0f"
            )
        
        if reforma_loja != st.session_state.business_data.get('reforma_loja'):
            st.session_state.business_data['reforma_loja'] = reforma_loja
            save_user_data()
        
        # Usar valor do plano operacional se disponível
        equipamentos_automatico = st.session_state.business_data.get('investimento_equipamentos', 0)
        
        if equipamentos_automatico > 0:
            st.info(f"💡 Valor do Plano Operacional: {format_currency(equipamentos_automatico)}")
            # Persistir estado do checkbox
            checkbox_equip_state = st.session_state.business_data.get('usar_equip_auto', True)
            usar_equip_auto = st.checkbox("Usar valor do Plano Operacional", value=checkbox_equip_state, key="usar_equip_auto")
            
            # Salvar estado do checkbox
            if usar_equip_auto != st.session_state.business_data.get('usar_equip_auto'):
                st.session_state.business_data['usar_equip_auto'] = usar_equip_auto
                save_user_data()
            
            if usar_equip_auto:
                equipamentos_total = equipamentos_automatico
                st.metric("Equipamentos (automático)", format_currency(equipamentos_total))
            else:
                equipamentos_total = st.number_input(
                    "Equipamentos e mobiliário (R$) - Manual",
                    min_value=0.0,
                    value=float(st.session_state.business_data.get('equipamentos_total_manual', equipamentos_automatico)),
                    step=1000.0,
                    format="%.0f",
                    key="equipamentos_total_manual_input"
                )
                # Salvar valor manual separadamente
                if equipamentos_total != st.session_state.business_data.get('equipamentos_total_manual'):
                    st.session_state.business_data['equipamentos_total_manual'] = equipamentos_total
        else:
            equipamentos_total = st.number_input(
                "Equipamentos e mobiliário (R$)",
                min_value=0.0,
                value=float(st.session_state.business_data.get('equipamentos_total', 12000)),
                step=1000.0,
                format="%.0f"
            )
        
        if equipamentos_total != st.session_state.business_data.get('equipamentos_total'):
            st.session_state.business_data['equipamentos_total'] = equipamentos_total
            save_user_data()
        
        # Estoque inicial - vem da etapa Produtos e Serviços
        estoque_automatico = st.session_state.business_data.get('estoque_inicial', 0)
        # Verifica se existe no context da etapa atual para evitar conflito
        estoque_atual_contexto = float(st.session_state.business_data.get('estoque_inicial_investimento', 0))
        
        # Se já foi definido no contexto do investimento, usa esse valor
        if estoque_atual_contexto > 0 and estoque_atual_contexto != estoque_automatico:
            estoque_automatico = estoque_atual_contexto
        
        if estoque_automatico > 0:
            st.info(f"💡 Valor da etapa Produtos e Serviços: {format_currency(estoque_automatico)}")
            # Persistir estado do checkbox
            checkbox_estoque_state = st.session_state.business_data.get('usar_estoque_auto', True)
            usar_estoque_auto = st.checkbox("Usar valor da etapa Produtos e Serviços", value=checkbox_estoque_state, key="usar_estoque_auto")
            
            # Salvar estado do checkbox
            if usar_estoque_auto != st.session_state.business_data.get('usar_estoque_auto'):
                st.session_state.business_data['usar_estoque_auto'] = usar_estoque_auto
                save_user_data()
            
            if usar_estoque_auto:
                estoque_inicial = estoque_automatico
                st.metric("Estoque inicial (automático)", format_currency(estoque_inicial))
            else:
                estoque_inicial = st.number_input(
                    "Estoque inicial (R$) - Manual",
                    min_value=0.0,
                    value=float(st.session_state.business_data.get('estoque_inicial_manual', estoque_automatico)),
                    step=1000.0,
                    format="%.0f",
                    key="estoque_inicial_manual_input"
                )
                # Salvar valor manual separadamente
                if estoque_inicial != st.session_state.business_data.get('estoque_inicial_manual'):
                    st.session_state.business_data['estoque_inicial_manual'] = estoque_inicial
        else:
            estoque_inicial = st.number_input(
                "Estoque inicial (R$)",
                min_value=0.0,
                value=float(st.session_state.business_data.get('estoque_inicial', 25000)),
                step=1000.0,
                format="%.0f"
            )
        
        if estoque_inicial != st.session_state.business_data.get('estoque_inicial'):
            st.session_state.business_data['estoque_inicial'] = estoque_inicial
            save_user_data()
        
        # Capital de giro - calcular automaticamente baseado no faturamento
        objetivo_faturamento = st.session_state.business_data.get('objetivo_faturamento', 0)
        capital_giro_automatico = objetivo_faturamento * 3 if objetivo_faturamento > 0 else 0  # 3 meses
        
        if capital_giro_automatico > 0:
            st.info(f"💡 Sugestão: 3 meses de faturamento = {format_currency(capital_giro_automatico)}")
            # Persistir estado do checkbox
            checkbox_capital_state = st.session_state.business_data.get('usar_capital_auto', True)
            usar_capital_auto = st.checkbox("Usar 3 meses de faturamento objetivo", value=checkbox_capital_state, key="usar_capital_auto")
            
            # Salvar estado do checkbox
            if usar_capital_auto != st.session_state.business_data.get('usar_capital_auto'):
                st.session_state.business_data['usar_capital_auto'] = usar_capital_auto
                save_user_data()
            
            if usar_capital_auto:
                capital_giro = capital_giro_automatico
                st.metric("Capital de giro (automático)", format_currency(capital_giro))
            else:
                capital_giro = st.number_input(
                    "Capital de giro (3-6 meses) (R$) - Manual",
                    min_value=0.0,
                    value=float(st.session_state.business_data.get('capital_giro_manual', capital_giro_automatico)),
                    step=1000.0,
                    format="%.0f",
                    key="capital_giro_manual_input"
                )
                # Salvar valor manual separadamente
                if capital_giro != st.session_state.business_data.get('capital_giro_manual'):
                    st.session_state.business_data['capital_giro_manual'] = capital_giro
        else:
            capital_giro = st.number_input(
                "Capital de giro (3-6 meses) (R$)",
                min_value=0.0,
                value=float(st.session_state.business_data.get('capital_giro', 18000)),
                step=1000.0,
                format="%.0f"
            )
        
        if capital_giro != st.session_state.business_data.get('capital_giro'):
            st.session_state.business_data['capital_giro'] = capital_giro
            save_user_data()
    
    with col2:
        st.subheader("📊 Custos Legais e Marketing")
        
        # Abertura da empresa - pode vir do plano operacional
        abertura_automatica = st.session_state.business_data.get('custos_licencas', 0)
        if abertura_automatica == 0:
            abertura_automatica = st.session_state.business_data.get('licencas_alvara', 0)
        
        if abertura_automatica > 0:
            st.info(f"💡 Valor do Plano Operacional: {format_currency(abertura_automatica)}")
            # Persistir estado do checkbox
            checkbox_abertura_state = st.session_state.business_data.get('usar_abertura_auto', True)
            usar_abertura_auto = st.checkbox("Usar valor do Plano Operacional", value=checkbox_abertura_state, key="usar_abertura_auto")
            
            # Salvar estado do checkbox
            if usar_abertura_auto != st.session_state.business_data.get('usar_abertura_auto'):
                st.session_state.business_data['usar_abertura_auto'] = usar_abertura_auto
                save_user_data()
            
            if usar_abertura_auto:
                abertura_empresa = abertura_automatica
                st.metric("Abertura/licenças (automática)", format_currency(abertura_empresa))
            else:
                abertura_empresa = st.number_input(
                    "Abertura da empresa/licenças (R$) - Manual",
                    min_value=0.0,
                    value=float(st.session_state.business_data.get('abertura_empresa_manual', abertura_automatica)),
                    step=500.0,
                    format="%.0f",
                    key="abertura_empresa_manual_input"
                )
                # Salvar valor manual separadamente
                if abertura_empresa != st.session_state.business_data.get('abertura_empresa_manual'):
                    st.session_state.business_data['abertura_empresa_manual'] = abertura_empresa
        else:
            abertura_empresa = st.number_input(
                "Abertura da empresa/licenças (R$)",
                min_value=0.0,
                value=float(st.session_state.business_data.get('abertura_empresa', 3000)),
                step=500.0,
                format="%.0f"
            )
        
        if abertura_empresa != st.session_state.business_data.get('abertura_empresa'):
            st.session_state.business_data['abertura_empresa'] = abertura_empresa
            save_user_data()
        
        # Marketing de lançamento - pode vir da estratégia de marketing
        marketing_automatico = st.session_state.business_data.get('orcamento_marketing_inicial', 0)
        if marketing_automatico == 0:
            marketing_automatico = st.session_state.business_data.get('investimento_marketing_lancamento', 0)
        
        if marketing_automatico > 0:
            st.info(f"💡 Valor da Estratégia de Marketing: {format_currency(marketing_automatico)}")
            # Persistir estado do checkbox
            checkbox_marketing_state = st.session_state.business_data.get('usar_marketing_auto', True)
            usar_marketing_auto = st.checkbox("Usar valor da Estratégia de Marketing", value=checkbox_marketing_state, key="usar_marketing_auto")
            
            # Salvar estado do checkbox
            if usar_marketing_auto != st.session_state.business_data.get('usar_marketing_auto'):
                st.session_state.business_data['usar_marketing_auto'] = usar_marketing_auto
                save_user_data()
            
            if usar_marketing_auto:
                marketing_lancamento = marketing_automatico
                st.metric("Marketing (automático)", format_currency(marketing_lancamento))
            else:
                marketing_lancamento = st.number_input(
                    "Marketing de lançamento (R$) - Manual",
                    min_value=0.0,
                    value=float(st.session_state.business_data.get('marketing_lancamento_manual', marketing_automatico)),
                    step=500.0,
                    format="%.0f",
                    key="marketing_lancamento_manual_input"
                )
                # Salvar valor manual separadamente
                if marketing_lancamento != st.session_state.business_data.get('marketing_lancamento_manual'):
                    st.session_state.business_data['marketing_lancamento_manual'] = marketing_lancamento
        else:
            marketing_lancamento = st.number_input(
                "Marketing de lançamento (R$)",
                min_value=0.0,
                value=float(st.session_state.business_data.get('marketing_lancamento', 2000)),
                step=500.0,
                format="%.0f"
            )
        
        if marketing_lancamento != st.session_state.business_data.get('marketing_lancamento'):
            st.session_state.business_data['marketing_lancamento'] = marketing_lancamento
            save_user_data()
        
        seguros_iniciais = st.number_input(
            "Seguros e garantias (R$)",
            min_value=0.0,
            value=float(st.session_state.business_data.get('seguros_iniciais', 1500)),
            step=500.0,
            format="%.0f"
        )
        if seguros_iniciais != st.session_state.business_data.get('seguros_iniciais'):
            st.session_state.business_data['seguros_iniciais'] = seguros_iniciais
            save_user_data()
        
        contingencia = st.number_input(
            "Reserva de contingência (R$)",
            min_value=0.0,
            value=float(st.session_state.business_data.get('contingencia', 5000)),
            step=1000.0,
            format="%.0f"
        )
        if contingencia != st.session_state.business_data.get('contingencia'):
            st.session_state.business_data['contingencia'] = contingencia
            save_user_data()
    
    # Usar valores finais corretos (manual ou automático)
    reforma_final = reforma_loja
    equipamentos_final = equipamentos_total  
    estoque_final = estoque_inicial
    capital_final = capital_giro
    abertura_final = abertura_empresa
    marketing_final = marketing_lancamento
    
    # Cálculo total
    investimento_total = reforma_final + equipamentos_final + estoque_final + capital_final + abertura_final + marketing_final + seguros_iniciais + contingencia
    
    st.markdown("---")
    st.subheader("💯 Resumo do Investimento")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Investimento Fixo", format_currency(reforma_loja + equipamentos_total))
        st.metric("Investimento Variável", format_currency(estoque_inicial + capital_giro))
    
    with col2:
        st.metric("Custos Iniciais", format_currency(abertura_empresa + marketing_lancamento + seguros_iniciais))
        st.metric("Contingência", format_currency(contingencia))
    
    with col3:
        st.metric("**INVESTIMENTO TOTAL**", format_currency(investimento_total), delta=None)
        
        # Explicação simples em reais
        if investimento_total > 0:
            valor_fixo = reforma_loja + equipamentos_total
            valor_estoque = estoque_inicial
            st.caption(f"💡 Dinheiro para reforma/equipamentos: {format_currency(valor_fixo)}")
            st.caption(f"💡 Dinheiro para produtos na loja: {format_currency(valor_estoque)}")
    
    # Store total
    st.session_state.business_data['investimento_total'] = investimento_total
    save_user_data()
    
    # Navigation
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("⬅️ Etapa Anterior", key="prev_step9"):
            st.session_state.step = 8
            st.rerun()
    with col3:
        if st.button("Próxima Etapa ➡️", type="primary", key="next_step9"):
            st.session_state.step = 10
            st.rerun()

def show_step_10():
    """Etapa 10: Projeções Financeiras"""
    st.header("📊 Etapa 10: Projeções Financeiras")
    st.markdown("**FASE 3: FINANÇAS** - Calcule receitas, custos e lucratividade")
    
    # Import pandas no início da função
    import pandas as pd
    
    # Carregar dados salvos
    vendas_mes_1 = st.session_state.business_data.get('vendas_mes_1', 20831)
    crescimento_mensal = st.session_state.business_data.get('crescimento_mensal', 2.0)
    ticket_medio = st.session_state.business_data.get('ticket_medio', 180)
    
    # Abas para organizar o conteúdo
    tab1, tab2, tab3, tab4 = st.tabs(["💰 Receitas", "💸 Custos", "📊 DRE Mês a Mês", "💸 Fluxo de Caixa"])
    
    with tab1:
        st.subheader("💰 Projeção de Receitas")
        
        col1, col2 = st.columns(2)
        
        with col1:
            vendas_mes_1 = st.number_input(
                "Vendas no primeiro mês (R$)",
                min_value=1000.0,
                value=float(vendas_mes_1),
                step=500.0,
                format="%.0f"
            )
            if vendas_mes_1 != st.session_state.business_data.get('vendas_mes_1'):
                st.session_state.business_data['vendas_mes_1'] = vendas_mes_1
                save_user_data()
            
            crescimento_mensal = st.slider(
                "Crescimento mensal (%)",
                min_value=0.0,
                max_value=10.0,
                value=float(crescimento_mensal),
                step=0.5
            )
            if crescimento_mensal != st.session_state.business_data.get('crescimento_mensal'):
                st.session_state.business_data['crescimento_mensal'] = crescimento_mensal
                save_user_data()
        
        with col2:
            ticket_medio = st.number_input(
                "Ticket médio (R$)",
                min_value=50.0,
                value=max(50.0, float(ticket_medio)),
                step=10.0,
                format="%.0f"
            )
            if ticket_medio != st.session_state.business_data.get('ticket_medio'):
                st.session_state.business_data['ticket_medio'] = ticket_medio
                save_user_data()
            
            vendas_quantidade = vendas_mes_1 / ticket_medio if ticket_medio > 0 else 0
            st.metric("Vendas por mês", f"{vendas_quantidade:.0f} unidades")
        
        # Projeção anual
        receita_anual = vendas_mes_1 * 12 * (1 + crescimento_mensal/100 * 6)  # Crescimento médio
        st.session_state.business_data['receita_anual'] = receita_anual
        st.metric("Receita Anual Projetada", format_currency(receita_anual))
        
        # Análise de sazonalidade
        st.markdown("### 📈 Análise de Sazonalidade")
        col_saz1, col_saz2 = st.columns(2)
        
        with col_saz1:
            meses_alta = st.multiselect(
                "Meses de alta temporada",
                ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
                 "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"],
                default=st.session_state.business_data.get('meses_alta', ["Janeiro", "Fevereiro", "Dezembro"])
            )
            if meses_alta != st.session_state.business_data.get('meses_alta'):
                st.session_state.business_data['meses_alta'] = meses_alta
                save_user_data()
        
        with col_saz2:
            incremento_alta = st.slider(
                "Incremento na alta temporada (%)",
                min_value=0,
                max_value=50,
                value=st.session_state.business_data.get('incremento_alta', 25),
                step=5
            )
            if incremento_alta != st.session_state.business_data.get('incremento_alta'):
                st.session_state.business_data['incremento_alta'] = incremento_alta
                save_user_data()
        
        # Projeção com sazonalidade
        receita_com_sazonalidade = 0
        for mes in range(12):
            mes_nome = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
                       "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"][mes]
            
            if mes == 0:
                receita_mes = vendas_mes_1
            else:
                receita_mes = vendas_mes_1 * (1 + crescimento_mensal/100) ** mes
            
            if mes_nome in meses_alta:
                receita_mes *= (1 + incremento_alta/100)
            
            receita_com_sazonalidade += receita_mes
        
        st.session_state.business_data['receita_com_sazonalidade'] = receita_com_sazonalidade
        st.metric("Receita Anual com Sazonalidade", format_currency(receita_com_sazonalidade))
    
    with tab2:
        st.subheader("💸 Estrutura de Custos")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Custos Fixos Mensais**")
            
            # Calcular custos separados por tipo
            folha_clt_total = 0
            servicos_prestadores_total = 0
            
            if hasattr(st.session_state, 'funcionarios') and st.session_state.funcionarios:
                for func in st.session_state.funcionarios:
                    if func['tipo_contrato'] == 'CLT':
                        folha_clt_total += func['salario_base'] * 1.68  # CLT com encargos
                    else:
                        servicos_prestadores_total += func['salario_base']  # MEI/Prestador
            
            # Calcular aluguel sugerido baseado no plano operacional
            area_loja = st.session_state.business_data.get('area_loja', 0)
            cidade = st.session_state.business_data.get('cidade', '')
            aluguel_sugerido = 3500  # valor padrão
            if area_loja > 0:
                # Estimativa baseada na área e localização
                preco_m2 = {"São Paulo": 80, "Rio de Janeiro": 70, "Fortaleza": 35, "Salvador": 40}.get(cidade, 50)
                aluguel_sugerido = area_loja * preco_m2
            
            # Auto-aplicar valores integrados se ainda não foram definidos
            if folha_clt_total > 0 and st.session_state.business_data.get('salarios_clt', 0) <= 0:
                st.session_state.business_data['salarios_clt'] = folha_clt_total
                save_user_data()
            
            if servicos_prestadores_total > 0 and st.session_state.business_data.get('total_optometrista', 0) <= 0:
                st.session_state.business_data['total_optometrista'] = servicos_prestadores_total
                save_user_data()
            
            # Para aluguel, só aplicar sugestão se nunca foi definido (None)
            if area_loja > 0 and 'aluguel' not in st.session_state.business_data:
                st.session_state.business_data['aluguel'] = aluguel_sugerido
                save_user_data()
            
            # Usar dados salvos, incluindo zero se foi explicitamente definido
            aluguel_salvo = st.session_state.business_data.get('aluguel', None)
            if aluguel_salvo is not None:
                aluguel_default = aluguel_salvo  # Usar valor salvo (incluindo zero)
            else:
                aluguel_default = aluguel_sugerido  # Usar sugestão apenas se nunca foi salvo
            
            # Priorizar sempre o valor calculado do DP se disponível para CLT
            if folha_clt_total > 0:
                salarios_clt_default = folha_clt_total
                if st.session_state.business_data.get('salarios_clt', 0) != folha_clt_total:
                    st.session_state.business_data['salarios_clt'] = folha_clt_total
                    save_user_data()
            else:
                salarios_clt_salvo = st.session_state.business_data.get('salarios_clt', 0)
                salarios_clt_default = salarios_clt_salvo  # Usar valor salvo, mesmo se for zero
            
            # Priorizar sempre o valor calculado do DP se disponível para prestadores
            if servicos_prestadores_total > 0:
                servicos_default = servicos_prestadores_total
                if st.session_state.business_data.get('total_optometrista', 0) != servicos_prestadores_total:
                    st.session_state.business_data['total_optometrista'] = servicos_prestadores_total
                    save_user_data()
            else:
                servicos_salvo = st.session_state.business_data.get('total_optometrista', 0)
                servicos_default = servicos_salvo  # Usar valor salvo, mesmo se for zero
            
            # Sistema flexível de aluguel: mensal ou diária
            st.markdown("**💼 Configuração de Aluguel**")
            col_alug1, col_alug2 = st.columns([1, 2])
            
            with col_alug1:
                tipo_aluguel = st.selectbox(
                    "Tipo de Aluguel",
                    ["Mensal", "Diária"],
                    index=0 if st.session_state.business_data.get('tipo_aluguel', 'Mensal') == 'Mensal' else 1,
                    help="Para interior: use diária. Para ponto fixo: use mensal"
                )
                if tipo_aluguel != st.session_state.business_data.get('tipo_aluguel'):
                    st.session_state.business_data['tipo_aluguel'] = tipo_aluguel
                    save_user_data()
            
            with col_alug2:
                if tipo_aluguel == "Mensal":
                    aluguel_valor = st.number_input(
                        "Aluguel mensal (R$)",
                        min_value=0.0,
                        value=float(aluguel_default),
                        step=100.0,
                        format="%.0f",
                        help=f"Sugestão baseada na área: {format_currency(aluguel_sugerido)}" if area_loja > 0 else "Valor para ponto fixo"
                    )
                    aluguel_mensal = aluguel_valor
                else:
                    # Aluguel por diária - layout vertical para evitar colunas aninhadas
                    aluguel_diaria = st.number_input(
                        "Valor da diária (R$)",
                        min_value=0.0,
                        value=float(st.session_state.business_data.get('aluguel_diaria', 150)),
                        step=10.0,
                        format="%.0f",
                        help="Valor da diária da sala/espaço no interior"
                    )
                    if aluguel_diaria != st.session_state.business_data.get('aluguel_diaria'):
                        st.session_state.business_data['aluguel_diaria'] = aluguel_diaria
                        save_user_data()
                    
                    # Predefinições para facilitar a configuração
                    frequencia_opcoes = {
                        "Apenas sábados (4 dias/mês)": 4,
                        "Sábados + domingos (8 dias/mês)": 8,
                        "Finais de semana + feriados (10 dias/mês)": 10,
                        "Dias úteis (22 dias/mês)": 22,
                        "Personalizado": 0
                    }
                    
                    frequencia_selecionada = st.selectbox(
                        "Frequência de trabalho",
                        list(frequencia_opcoes.keys()),
                        index=0,  # Default: apenas sábados
                        help="Escolha uma opção comum ou personalize"
                    )
                    
                    if frequencia_selecionada == "Personalizado":
                        dias_mes = st.number_input(
                            "Dias por mês",
                            min_value=1,
                            max_value=31,
                            value=int(st.session_state.business_data.get('dias_mes_diaria', 4)),
                            help="Digite o número exato de dias"
                        )
                    else:
                        dias_mes = frequencia_opcoes[frequencia_selecionada]
                        st.info(f"📅 {frequencia_selecionada}")
                    
                    if dias_mes != st.session_state.business_data.get('dias_mes_diaria'):
                        st.session_state.business_data['dias_mes_diaria'] = dias_mes
                        st.session_state.business_data['frequencia_trabalho'] = frequencia_selecionada
                        save_user_data()
                    
                    aluguel_mensal = aluguel_diaria * dias_mes
                    st.info(f"💡 **{dias_mes} dias × {format_currency(aluguel_diaria)} = {format_currency(aluguel_mensal)}/mês**")
            
            # Salvar o aluguel final calculado
            if aluguel_mensal != st.session_state.business_data.get('aluguel'):
                st.session_state.business_data['aluguel'] = aluguel_mensal
                save_user_data()
                
            # Calculadora de combustível para trabalho no interior  
            if tipo_aluguel == "Diária":
                st.markdown("**⛽ Calculadora de Combustível (Interior)**")
                with st.expander("🚗 Configurar custos de deslocamento", expanded=False):
                    
                    distancia_km = st.number_input(
                        "Distância (km ida/volta)",
                        min_value=0.0,
                        value=float(st.session_state.business_data.get('distancia_km', 0)),
                        step=10.0,
                        help="Distância total ida e volta até o local"
                    )
                    if distancia_km != st.session_state.business_data.get('distancia_km'):
                        st.session_state.business_data['distancia_km'] = distancia_km
                        save_user_data()
                    
                    preco_combustivel = st.number_input(
                        "Preço combustível (R$/L)",
                        min_value=0.0,
                        value=float(st.session_state.business_data.get('preco_combustivel', 5.50)),
                        step=0.10,
                        format="%.2f",
                        help="Preço atual do combustível na região"
                    )
                    if preco_combustivel != st.session_state.business_data.get('preco_combustivel'):
                        st.session_state.business_data['preco_combustivel'] = preco_combustivel
                        save_user_data()
                    
                    autonomia_km_l = st.number_input(
                        "Autonomia (km/L)",
                        min_value=1.0,
                        value=float(st.session_state.business_data.get('autonomia_km_l', 12.0)),
                        step=0.5,
                        help="Quantos km seu veículo faz por litro"
                    )
                    if autonomia_km_l != st.session_state.business_data.get('autonomia_km_l'):
                        st.session_state.business_data['autonomia_km_l'] = autonomia_km_l
                        save_user_data()
                    
                    # Calcular custos de combustível
                    if distancia_km > 0 and preco_combustivel > 0 and autonomia_km_l > 0:
                        dias_mes_combustivel = st.session_state.business_data.get('dias_mes_diaria', 4)
                        litros_necessarios = distancia_km / autonomia_km_l
                        custo_combustivel_dia = litros_necessarios * preco_combustivel
                        custo_combustivel_mes = custo_combustivel_dia * dias_mes_combustivel
                        
                        st.session_state.business_data['custo_combustivel_mensal'] = custo_combustivel_mes
                        save_user_data()
                        
                        st.metric(
                            "💰 Combustível por dia",
                            format_currency(custo_combustivel_dia),
                            f"{litros_necessarios:.1f}L necessários"
                        )
                        st.metric(
                            "💰 Combustível mensal",
                            format_currency(custo_combustivel_mes),
                            f"Para {dias_mes_combustivel} dias"
                        )
                        
                        # Adicionar ao custo total mensal
                        custo_total_com_combustivel = aluguel_mensal + custo_combustivel_mes
                        
                        # Mostrar detalhamento específico para frequência de trabalho
                        frequencia_texto = st.session_state.business_data.get('frequencia_trabalho', 'Apenas sábados (4 dias/mês)')
                        st.warning(f"**Custo total mensal: {format_currency(custo_total_com_combustivel)}**")
                        st.info(f"**Baseado em:** {frequencia_texto} + Combustível {format_currency(custo_combustivel_mes)}")
                    else:
                        custo_combustivel_mes = 0
                        st.session_state.business_data['custo_combustivel_mensal'] = 0
                        save_user_data()
            else:
                # Para aluguel mensal, zerar custos de combustível
                st.session_state.business_data['custo_combustivel_mensal'] = 0
                save_user_data()
            
            # Campo de salários CLT separado (pode ser zero no início)
            if folha_clt_total > 0:
                help_text_clt = f"✅ Valor integrado do DP: {format_currency(folha_clt_total)} - Funcionários CLT com encargos"
            else:
                help_text_clt = "💡 Pode deixar zero para começar apenas com comissionistas - contrate CLT quando tiver caixa"
            
            salarios_clt = st.number_input(
                "Folha CLT (salários + encargos) (R$)",
                min_value=0.0,
                value=float(salarios_clt_default),
                step=100.0,
                format="%.0f",
                help=help_text_clt,
                key="salarios_clt_input"
            )
            
            if salarios_clt != st.session_state.business_data.get('salarios_clt'):
                st.session_state.business_data['salarios_clt'] = salarios_clt
                save_user_data()
            
            # Seção de Despesas Operacionais - Serviços Profissionais por Diária
            st.markdown("**👩‍⚕️ Serviços Profissionais por Diária**")
            
            # Configuração do optometrista por diária
            col_opt1, col_opt2 = st.columns(2)
            
            with col_opt1:
                diaria_optometrista = st.number_input(
                    "Diária Optometrista (R$)",
                    min_value=0.0,
                    value=float(st.session_state.business_data.get('diaria_optometrista', 150.0)),
                    step=10.0,
                    format="%.0f",
                    help="Valor da diária do optometrista (despesa operacional)"
                )
                if diaria_optometrista != st.session_state.business_data.get('diaria_optometrista'):
                    st.session_state.business_data['diaria_optometrista'] = diaria_optometrista
                    save_user_data()
            
            with col_opt2:
                dias_optometrista_mes = st.number_input(
                    "Dias optometrista/mês",
                    min_value=0,
                    value=int(st.session_state.business_data.get('dias_optometrista_mes', 4)),
                    step=1,
                    help="Quantos dias por mês o optometrista trabalha"
                )
                if dias_optometrista_mes != st.session_state.business_data.get('dias_optometrista_mes'):
                    st.session_state.business_data['dias_optometrista_mes'] = dias_optometrista_mes
                    save_user_data()
            
            # Cálculo automático do custo mensal do optometrista
            custo_optometrista_mensal = diaria_optometrista * dias_optometrista_mes
            st.session_state.business_data['custo_optometrista_mensal'] = custo_optometrista_mensal
            save_user_data()
            
            if custo_optometrista_mensal > 0:
                st.info(f"💰 **Custo Optometrista:** {dias_optometrista_mes} dias × {format_currency(diaria_optometrista)} = **{format_currency(custo_optometrista_mensal)}/mês**")
            

            
            # Mostrar breakdown se há funcionários
            if folha_clt_total > 0 or servicos_prestadores_total > 0:
                funcionarios_clt = [f for f in st.session_state.funcionarios if f['tipo_contrato'] == 'CLT']
                funcionarios_prestadores = [f for f in st.session_state.funcionarios if f['tipo_contrato'] != 'CLT']
                
                if funcionarios_clt:
                    st.caption(f"👥 CLT: {len(funcionarios_clt)} funcionários = {format_currency(folha_clt_total)}")
                if funcionarios_prestadores:
                    st.caption(f"🤝 Prestadores: {len(funcionarios_prestadores)} pessoas = {format_currency(servicos_prestadores_total)}")
            
            # Calcular totais separados para clareza contábil
            total_folha_clt = salarios_clt
            total_optometrista = custo_optometrista_mensal
            
            # Salvar apenas optometrista para Sistema Integrado (campo 0)
            st.session_state.business_data['0'] = total_optometrista
            
            # Total geral de pessoal (CLT + Optometrista)
            total_pessoal = total_folha_clt + total_optometrista
            st.session_state.business_data['salarios_total'] = total_pessoal
            
            # Separar despesas operacionais
            st.session_state.business_data['despesas_servicos_profissionais'] = total_optometrista
            
            # Painel de Auditoria de Duplicidades
            st.markdown("---")
            st.markdown("### 🔍 Auditoria de Duplicidades de Custos")
            
            with st.expander("⚠️ Verificar possíveis duplicidades", expanded=False):
                st.markdown("**Análise de Sobreposições Detectadas:**")
                
                duplicidades_encontradas = []
                
                # Verificar se optometrista está em dois lugares
                if custo_optometrista_mensal > 0 and servicos_prestadores_total > 0:
                    # Verificar se há optometrista no DP também
                    funcionarios_dp = st.session_state.get('funcionarios', [])
                    optometrista_no_dp = any('optometrista' in str(f.get('cargo', '')).lower() for f in funcionarios_dp)
                    
                    if optometrista_no_dp:
                        duplicidades_encontradas.append({
                            'tipo': 'Optometrista duplicado',
                            'descricao': f'Optometrista aparece tanto em Serviços Profissionais (R$ {custo_optometrista_mensal:.0f}) quanto no DP',
                            'solucao': 'Remover optometrista do DP e manter apenas em Serviços Profissionais por diária'
                        })
                
                # Verificar duplicidade de aluguel
                aluguel_etapa10 = st.session_state.business_data.get('aluguel', 0)
                outros_fixos = st.session_state.business_data.get('outros_fixos', 0)
                if aluguel_etapa10 > 0 and outros_fixos > 2000:  # Se outros fixos muito alto, pode incluir aluguel
                    duplicidades_encontradas.append({
                        'tipo': 'Possível aluguel duplicado',
                        'descricao': f'Aluguel: R$ {aluguel_etapa10:.0f} + Outros fixos muito alto: R$ {outros_fixos:.0f}',
                        'solucao': 'Verificar se outros fixos não incluem aluguel novamente'
                    })
                

                
                # Verificar se marketing está duplicado
                orcamento_marketing = st.session_state.business_data.get('orcamento_marketing', 0)
                marketing_outros = st.session_state.business_data.get('marketing', 0)
                if orcamento_marketing > 0 and marketing_outros > 0:
                    duplicidades_encontradas.append({
                        'tipo': 'Marketing duplicado',
                        'descricao': f'Orçamento Marketing: R$ {orcamento_marketing:.0f} + Marketing outros: R$ {marketing_outros:.0f}',
                        'solucao': 'Usar apenas um campo para marketing total'
                    })
                
                # Exibir resultados
                if duplicidades_encontradas:
                    st.error(f"🚨 **{len(duplicidades_encontradas)} possíveis duplicidades encontradas:**")
                    
                    for i, dup in enumerate(duplicidades_encontradas, 1):
                        st.markdown(f"""
                        **{i}. {dup['tipo']}**
                        - **Problema:** {dup['descricao']}
                        - **Solução:** {dup['solucao']}
                        """)
                        
                        # Botão de correção automática para optometrista
                        if dup['tipo'] == 'Optometrista duplicado':
                            if st.button(f"🔧 Corrigir automaticamente - {dup['tipo']}", key=f"fix_dup_{i}"):
                                # Remover optometrista do DP
                                funcionarios_limpos = [f for f in st.session_state.funcionarios 
                                                     if 'optometrista' not in str(f.get('cargo', '')).lower()]
                                st.session_state.funcionarios = funcionarios_limpos
                                st.success("✅ Optometrista removido do DP - mantido apenas em Serviços Profissionais")
                                st.rerun()
                else:
                    st.success("✅ **Nenhuma duplicidade detectada na estrutura atual**")
                
                # Resumo consolidado dos custos
                st.markdown("---")
                st.markdown("**📊 Resumo Consolidado dos Custos (sem duplicidades):**")
                
                custo_consolidado = {
                    'Aluguel': aluguel_etapa10,
                    'Folha CLT': total_folha_clt,
                    'Optometrista (diárias)': total_optometrista,
                    'Outros Custos Fixos': st.session_state.business_data.get('outros_fixos', 0),
                    'Marketing': max(orcamento_marketing, marketing_outros),  # Pegar o maior, não somar
                }
                
                total_consolidado = sum(custo_consolidado.values())
                
                for categoria, valor in custo_consolidado.items():
                    if valor > 0:
                        percentual = (valor / total_consolidado * 100) if total_consolidado > 0 else 0
                        st.markdown(f"• **{categoria}:** {format_currency(valor)} ({percentual:.1f}%)")
                
                st.markdown(f"**📍 Total Mensal:** {format_currency(total_consolidado)}")
                st.markdown(f"**📍 Total Anual:** {format_currency(total_consolidado * 12)}")
            
            # Painel de integração de dados (apenas se houver dados integrados válidos)
            dados_integrados_validos = []
            
            if folha_clt_total > 0 or servicos_prestadores_total > 0:
                dados_integrados_validos.append("folha")
            if area_loja > 0 and aluguel_sugerido > 0:
                dados_integrados_validos.append("operacional")
            if st.session_state.business_data.get('investimento_total', 0) > 0:
                dados_integrados_validos.append("investimento")
            
            if dados_integrados_validos:
                with st.expander("📊 Dados Integrados do Plano", expanded=False):
                    if folha_clt_total > 0 or servicos_prestadores_total > 0:
                        total_funcionarios = folha_clt_total + servicos_prestadores_total
                        st.success(f"✅ Folha de pagamento integrada: {format_currency(total_funcionarios)}")
                        st.write(f"   {len(st.session_state.funcionarios)} funcionários do DP")
                        
                        if folha_clt_total > 0:
                            funcionarios_clt = [f for f in st.session_state.funcionarios if f['tipo_contrato'] == 'CLT']
                            st.write(f"   📋 CLT: {len(funcionarios_clt)} funcionários = {format_currency(folha_clt_total)}")
                            for func in funcionarios_clt:
                                custo_total = func['salario_base'] * 1.68
                                st.write(f"      • {func['nome']} ({func['cargo']}): {format_currency(custo_total)}")
                        
                        if servicos_prestadores_total > 0:
                            funcionarios_prestadores = [f for f in st.session_state.funcionarios if f['tipo_contrato'] != 'CLT']
                            st.write(f"   🤝 Prestadores: {len(funcionarios_prestadores)} pessoas = {format_currency(servicos_prestadores_total)}")
                            for func in funcionarios_prestadores:
                                st.write(f"      • {func['nome']} ({func['cargo']}): {format_currency(func['salario_base'])}")
                    
                    if area_loja > 0 and aluguel_sugerido > 0:
                        st.success(f"✅ Dados operacionais: {area_loja}m² em {cidade}")
                        st.write(f"   Aluguel sugerido: {format_currency(aluguel_sugerido)}")
                    
                    investimento_total = st.session_state.business_data.get('investimento_total', 0)
                    if investimento_total > 0:
                        st.success(f"✅ Investimento inicial: {format_currency(investimento_total)}")
                        depreciacao_calc = investimento_total * 0.3 / 120
                        st.write(f"   Depreciação mensal: {format_currency(depreciacao_calc)}")
            else:
                st.info("💡 Complete o DP, Investimento Inicial ou Plano Operacional para ver dados integrados aqui.")
            

            
            # Botão para forçar atualização
            if st.button("Atualizar Custos das Etapas Anteriores", help="Força atualização com dados do DP, Investimento e Operacional"):
                valores_atualizados = []
                
                # Forçar atualização da folha de salários
                if folha_clt_total > 0 or servicos_prestadores_total > 0:
                    total_folha = folha_clt_total + servicos_prestadores_total
                    st.session_state.business_data['salarios_total'] = total_folha
                    valores_atualizados.append(f"Folha de salários: {format_currency(total_folha)} (DP)")
                
                # Forçar atualização do aluguel
                if area_loja > 0 and cidade:
                    st.session_state.business_data['aluguel'] = aluguel_sugerido
                    valores_atualizados.append(f"Aluguel: {format_currency(aluguel_sugerido)} ({area_loja}m² em {cidade})")
                
                # Calcular depreciação do investimento
                investimento_total = st.session_state.business_data.get('investimento_total', 0)
                if investimento_total > 0:
                    depreciacao_mensal = investimento_total * 0.3 / 120
                    st.session_state.business_data['depreciacao_mensal'] = depreciacao_mensal
                    valores_atualizados.append(f"Depreciação: {format_currency(depreciacao_mensal)} (investimento)")
                
                if valores_atualizados:
                    save_user_data()
                    st.success("Custos atualizados: " + " | ".join(valores_atualizados))
                    st.rerun()
                else:
                    st.warning("Complete o DP, Investimento Inicial ou Plano Operacional primeiro.")
            

            
            # Calcular outros custos fixos incluindo combustível e captador
            custo_combustivel_mensal = st.session_state.business_data.get('custo_combustivel_mensal', 0)
            
            # Calcular custo do captador e forçar atualização
            custo_captador_calculado = calcular_custo_captador_mensal()
            if custo_captador_calculado > 0:
                st.session_state.business_data['custo_captador_mensal_calculado'] = custo_captador_calculado
            
            outros_fixos_base = st.session_state.business_data.get('outros_fixos_base', 0)
            
            # Botão para atualizar custos das etapas anteriores
            if st.button("🔄 Atualizar Custos das Etapas Anteriores", use_container_width=True):
                custo_captador_calculado = calcular_custo_captador_mensal()
                st.session_state.business_data['custo_captador_mensal_calculado'] = custo_captador_calculado
                save_user_data()
                st.success(f"Custo do captador atualizado: {format_currency(custo_captador_calculado)}")
                st.rerun()
            
            if custo_combustivel_mensal > 0 or custo_captador_calculado > 0:
                # Mostrar breakdown quando há custos adicionais
                num_cols = 2 + (1 if custo_combustivel_mensal > 0 else 0) + (1 if custo_captador_calculado > 0 else 0)
                cols = st.columns([2] + [1] * (num_cols - 1))
                
                with cols[0]:
                    outros_fixos_input = st.number_input(
                        "Outros custos fixos (R$)",
                        min_value=0.0,
                        value=float(outros_fixos_base),
                        step=100.0,
                        format="%.0f",
                        help="Energia, telefone, internet, seguros"
                    )
                    if outros_fixos_input != outros_fixos_base:
                        st.session_state.business_data['outros_fixos_base'] = outros_fixos_input
                        save_user_data()
                
                col_idx = 1
                if custo_combustivel_mensal > 0:
                    with cols[col_idx]:
                        st.metric(
                            "🚗 Combustível",
                            format_currency(custo_combustivel_mensal),
                            "Interior"
                        )
                    col_idx += 1
                
                if custo_captador_calculado > 0:
                    with cols[col_idx]:
                        st.metric(
                            "👥 Captador",
                            format_currency(custo_captador_calculado),
                            "Gestão de Pessoas"
                        )
                        
                        # Mostrar memória de cálculo
                        if st.button("🔍 Memória de Cálculo", key="memoria_captador"):
                            memoria = st.session_state.business_data.get('memoria_calculo_captador', 'Cálculo não disponível')
                            st.code(memoria)
                
                # Apenas outros custos base (não incluir combustível aqui pois será mostrado separado)
                outros_fixos = outros_fixos_input
                breakdown_parts = [f"Base {format_currency(outros_fixos_input)}"]
                if custo_combustivel_mensal > 0:
                    breakdown_parts.append(f"Combustível {format_currency(custo_combustivel_mensal)}")
                if custo_captador_calculado > 0:
                    breakdown_parts.append(f"Captador {format_currency(custo_captador_calculado)}")
                
                breakdown_text = f"**Total: {format_currency(outros_fixos)}** = " + " + ".join(breakdown_parts)
                st.info(breakdown_text)
            else:
                # Modo normal sem custos adicionais
                outros_fixos = st.number_input(
                    "Outros custos fixos (R$)",
                    min_value=0.0,
                    value=float(outros_fixos_base),
                    step=100.0,
                    format="%.0f",
                    help="Energia, telefone, internet, seguros"
                )
                if outros_fixos != outros_fixos_base:
                    st.session_state.business_data['outros_fixos_base'] = outros_fixos
                    save_user_data()
            
            # Salvar apenas o combustível como outros custos
            outros_fixos_final = custo_combustivel_mensal  # Apenas R$ 575,11
            
            if outros_fixos_final != st.session_state.business_data.get('outros_fixos'):
                st.session_state.business_data['outros_fixos'] = outros_fixos_final
                save_user_data()
            
            # Incluir custo do captador nos custos fixos
            custo_captador_mensal = calcular_custo_captador_mensal()
            
            custos_fixos_total = aluguel_mensal + salarios_clt + total_optometrista + custo_captador_mensal + outros_fixos_final
            st.metric("Total Custos Fixos", format_currency(custos_fixos_total))
            
            # Mostrar breakdown dos custos fixos incluindo captador
            if st.checkbox("📊 Mostrar detalhamento dos custos fixos"):
                st.markdown("**Detalhamento dos Custos Fixos:**")
                st.write(f"• Aluguel: {format_currency(aluguel_mensal)}")
                st.write(f"• Folha CLT: {format_currency(salarios_clt)}")
                st.write(f"• Optometrista: {format_currency(total_optometrista)}")
                st.write(f"• **Captador: {format_currency(custo_captador_mensal)}**")
                st.write(f"• Outros custos: {format_currency(outros_fixos_final)}")
                st.write(f"**Total: {format_currency(custos_fixos_total)}**")
        
        with col2:
            st.markdown("**Custos Variáveis (%)**")
            
            # Calcular CMV automaticamente baseado nos custos reais da precificação
            custo_materiais_fisicos = st.session_state.business_data.get('custo_materiais_fisicos', 89.80)
            ticket_medio = st.session_state.business_data.get('ticket_medio', 180)
            
            if ticket_medio > 0:
                cmv_percentual = (custo_materiais_fisicos / ticket_medio) * 100
            else:
                cmv_percentual = 45.0  # fallback
            
            st.session_state.business_data['cmv_percentual'] = cmv_percentual
            save_user_data()
            
            st.success(f"✅ **CMV calculado automaticamente**: {cmv_percentual:.1f}% baseado nos custos reais")
            st.caption(f"Baseado em: R$ {custo_materiais_fisicos:.2f} (custo) ÷ R$ {ticket_medio:.2f} (ticket médio)")
            
            # Validação crítica de impostos baseada no regime tributário
            tipo_empresa = st.session_state.business_data.get('tipo_empresa', 'MEI')
            objetivo_faturamento = st.session_state.business_data.get('objetivo_faturamento', 0)
            receita_anual = objetivo_faturamento * 12
            
            # Calcular alíquota correta baseada na legislação brasileira atual
            from tax_calculator import TaxCalculator
            calc = TaxCalculator()
            
            impostos_sugerido = 6.0  # Default fallback
            
            if tipo_empresa == 'MEI':
                impostos_sugerido = 0.3  # MEI paga valor fixo, não percentual sobre receita
                st.info("💡 **MEI**: Você paga R$ 76,90 fixo por mês conforme legislação 2025")
            elif tipo_empresa in ['Microempresa', 'Empresa de Pequeno Porte']:
                # Calcular conforme tabela oficial do Simples Nacional
                resultado_simples = calc.calculate_simples_nacional(receita_anual, "Anexo I - Comércio")
                impostos_sugerido = resultado_simples['aliquota_efetiva']
                
                st.info(f"💡 **{tipo_empresa}**: Conforme Simples Nacional Anexo I, você paga {impostos_sugerido:.1f}% (alíquota oficial para R$ {receita_anual:,.0f}/ano)")
                st.caption("📋 Base legal: Lei Complementar nº 123/2006 - Simples Nacional")
            elif tipo_empresa in ['Ltda', 'Outro']:
                impostos_sugerido = 13.33
                st.warning(f"💡 **Lucro Presumido**: Conforme legislação, empresas normais pagam cerca de {impostos_sugerido}% (confirme com contador)")
            
            # Usar automaticamente o valor correto da legislação
            impostos_percentual = impostos_sugerido
            st.session_state.business_data['impostos_percentual'] = impostos_percentual
            save_user_data()
            
            st.success(f"✅ **Impostos aplicados automaticamente**: {impostos_percentual:.1f}% conforme legislação brasileira")
            
            comissoes_percentual = st.slider(
                "Comissões (%)",
                min_value=0.0,
                max_value=15.0,
                value=float(st.session_state.business_data.get('comissoes_percentual', 3.0)),
                step=0.5
            )
            if comissoes_percentual != st.session_state.business_data.get('comissoes_percentual'):
                st.session_state.business_data['comissoes_percentual'] = comissoes_percentual
                save_user_data()
            
            outros_variaveis_percentual = st.slider(
                "Outros custos variáveis (%)",
                min_value=0.0,
                max_value=10.0,
                value=float(st.session_state.business_data.get('outros_variaveis_percentual', 2.0)),
                step=0.5
            )
            if outros_variaveis_percentual != st.session_state.business_data.get('outros_variaveis_percentual'):
                st.session_state.business_data['outros_variaveis_percentual'] = outros_variaveis_percentual
                save_user_data()
            
            total_variaveis_perc = cmv_percentual + impostos_percentual + comissoes_percentual + outros_variaveis_percentual
            st.metric("Total Custos Variáveis", f"{total_variaveis_perc:.1f}%")
        
        # Configuração detalhada de despesas operacionais
        st.markdown("### 🏢 Despesas Operacionais Detalhadas")
        st.markdown("Configure cada despesa individualmente para cálculos precisos")
        
        col_desp1, col_desp2, col_desp3 = st.columns(3)
        
        with col_desp1:
            st.markdown("**Utilidades e Infraestrutura**")
            
            energia_agua = st.number_input(
                "Energia + Água (R$/mês)",
                min_value=0.0,
                max_value=2000.0,
                value=float(st.session_state.business_data.get('energia_agua', 800)),
                step=50.0,
                help="Conta de luz + água + gás"
            )
            if energia_agua != st.session_state.business_data.get('energia_agua'):
                st.session_state.business_data['energia_agua'] = energia_agua
                save_user_data()
            
            telefone_internet = st.number_input(
                "Telefone + Internet (R$/mês)",
                min_value=0.0,
                max_value=800.0,
                value=float(st.session_state.business_data.get('telefone_internet', 350)),
                step=25.0,
                help="Telefone fixo + internet + celular"
            )
            if telefone_internet != st.session_state.business_data.get('telefone_internet'):
                st.session_state.business_data['telefone_internet'] = telefone_internet
                save_user_data()
            
            material_escritorio = st.number_input(
                "Material de Escritório (R$/mês)",
                min_value=0.0,
                max_value=500.0,
                value=float(st.session_state.business_data.get('material_escritorio', 200)),
                step=25.0,
                help="Papelaria, toner, material de limpeza"
            )
            if material_escritorio != st.session_state.business_data.get('material_escritorio'):
                st.session_state.business_data['material_escritorio'] = material_escritorio
                save_user_data()
        
        with col_desp2:
            st.markdown("**Serviços Profissionais**")
            
            contabilidade = st.number_input(
                "Contabilidade (R$/mês)",
                min_value=0.0,
                max_value=2000.0,
                value=float(st.session_state.business_data.get('contabilidade', 800)),
                step=50.0,
                help="Contador + assessoria fiscal"
            )
            if contabilidade != st.session_state.business_data.get('contabilidade'):
                st.session_state.business_data['contabilidade'] = contabilidade
                save_user_data()
            
            # Optometrista removido - agora está em Serviços Profissionais por Diária
            
            limpeza_seguranca = st.number_input(
                "Limpeza + Segurança (R$/mês)",
                min_value=0.0,
                max_value=1500.0,
                value=float(st.session_state.business_data.get('limpeza_seguranca', 600)),
                step=50.0,
                help="Empresa de limpeza + segurança"
            )
            if limpeza_seguranca != st.session_state.business_data.get('limpeza_seguranca'):
                st.session_state.business_data['limpeza_seguranca'] = limpeza_seguranca
                save_user_data()
        
        with col_desp3:
            st.markdown("**Seguros e Manutenção**")
            
            seguros = st.number_input(
                "Seguros (R$/mês)",
                min_value=0.0,
                max_value=1000.0,
                value=float(st.session_state.business_data.get('seguros', 400)),
                step=25.0,
                help="Seguro do estabelecimento + equipamentos"
            )
            if seguros != st.session_state.business_data.get('seguros'):
                st.session_state.business_data['seguros'] = seguros
                save_user_data()
            
            manutencao_equipamentos = st.number_input(
                "Manutenção Equipamentos (R$/mês)",
                min_value=0.0,
                max_value=800.0,
                value=float(st.session_state.business_data.get('manutencao_equipamentos', 300)),
                step=25.0,
                help="Manutenção de equipamentos ópticos"
            )
            if manutencao_equipamentos != st.session_state.business_data.get('manutencao_equipamentos'):
                st.session_state.business_data['manutencao_equipamentos'] = manutencao_equipamentos
                save_user_data()
            
            marketing_publicidade = st.number_input(
                "Marketing + Publicidade (R$/mês)",
                min_value=0.0,
                max_value=2000.0,
                value=float(st.session_state.business_data.get('marketing_publicidade', 500)),
                step=50.0,
                help="Redes sociais + anúncios + material gráfico"
            )
            if marketing_publicidade != st.session_state.business_data.get('marketing_publicidade'):
                st.session_state.business_data['marketing_publicidade'] = marketing_publicidade
                save_user_data()
        
        # Resumo das despesas operacionais (sem optometrista - agora está em Serviços Profissionais)
        total_despesas_detalhadas = (energia_agua + telefone_internet + material_escritorio + 
                                   contabilidade + limpeza_seguranca + 
                                   seguros + manutencao_equipamentos + marketing_publicidade)
        
        st.markdown("**📊 Resumo das Despesas Operacionais:**")
        col_res1, col_res2, col_res3 = st.columns(3)
        
        with col_res1:
            st.metric("Utilidades", format_currency(energia_agua + telefone_internet + material_escritorio))
        
        with col_res2:
            st.metric("Serviços Profissionais", format_currency(contabilidade + limpeza_seguranca))
        
        with col_res3:
            st.metric("Seguros + Manutenção + Marketing", format_currency(seguros + manutencao_equipamentos + marketing_publicidade))
        
        st.metric("**Total Despesas Operacionais**", format_currency(total_despesas_detalhadas))
        
        # Sistema de Rateio por Óculos Vendidos
        st.markdown("---")
        st.markdown("### 🎯 Rateio de Custos por Óculos Vendidos")
        st.markdown("Calcule quanto cada custo fixo representa por óculos vendido")
        
        # Pegar meta de óculos vendidos por mês
        ticket_medio = st.session_state.business_data.get('ticket_medio', 180)
        vendas_mes_1 = st.session_state.business_data.get('vendas_mes_1', 20831)
        oculos_por_mes = int(vendas_mes_1 / ticket_medio) if ticket_medio > 0 else 100
        
        col_rateio1, col_rateio2 = st.columns([1, 1])
        
        with col_rateio1:
            st.markdown("**Meta de Óculos por Mês**")
            oculos_meta = st.number_input(
                "Óculos vendidos por mês",
                min_value=10,
                max_value=1000,
                value=oculos_por_mes,
                step=5,
                help="Quantos óculos você pretende vender por mês"
            )
            if oculos_meta != st.session_state.business_data.get('oculos_meta_mes'):
                st.session_state.business_data['oculos_meta_mes'] = oculos_meta
                save_user_data()
            
            st.metric("Faturamento por óculos", format_currency(ticket_medio))
        
        with col_rateio2:
            st.markdown("**Custos Rateados por Óculos**")
            
            # Calcular custos totais fixos
            aluguel_valor = st.session_state.business_data.get('aluguel', 3500)
            folha_clt = st.session_state.business_data.get('salarios_clt', 0)
            
            # Obter dados do optometrista dos Serviços Profissionais por Diária
            custo_optometrista_mensal = st.session_state.business_data.get('custo_optometrista_mensal', 0)
            
            # Incluir combustível no cálculo de custos fixos totais
            custo_combustivel_mensal = st.session_state.business_data.get('custo_combustivel_mensal', 0)
            
            # Calcular custo do captador baseado nas configurações da Gestão de Pessoas
            custo_captador_mensal = calcular_custo_captador_mensal()
            
            custos_fixos_totais = (aluguel_valor + folha_clt + total_despesas_detalhadas + custo_optometrista_mensal + custo_combustivel_mensal + custo_captador_mensal)
            
            if oculos_meta > 0:
                # Rateio por óculos
                aluguel_por_oculos = aluguel_valor / oculos_meta
                optometrista_por_oculos = custo_optometrista_mensal / oculos_meta
                combustivel_por_oculos = custo_combustivel_mensal / oculos_meta
                captador_por_oculos = custo_captador_mensal / oculos_meta
                despesas_por_oculos = total_despesas_detalhadas / oculos_meta
                total_fixo_por_oculos = custos_fixos_totais / oculos_meta
                
                st.metric("Aluguel por óculos", format_currency(aluguel_por_oculos))
                st.metric("Optometrista por óculos", format_currency(optometrista_por_oculos))
                st.metric("Combustível por óculos", format_currency(combustivel_por_oculos))
                st.metric("Captador por óculos", format_currency(captador_por_oculos))
                st.metric("Despesas por óculos", format_currency(despesas_por_oculos))
                st.metric("**Total fixo por óculos**", format_currency(total_fixo_por_oculos))
                
                # Salvar para uso no sistema
                st.session_state.business_data['custo_fixo_por_oculos'] = total_fixo_por_oculos
                save_user_data()
            else:
                st.warning("Configure a meta de óculos para ver o rateio")
        
        # Card visual do rateio com custos diretos incluídos
        if oculos_meta > 0:
            # Obter custos diretos da precificação (Composição do Produto)
            custo_materiais_fisicos = st.session_state.business_data.get('custo_materiais_fisicos', 89.80)
            
            # Custos totais por óculos = Custos fixos (rateio) + Custos diretos (materiais)
            custo_total_por_oculos = total_fixo_por_oculos + custo_materiais_fisicos
            margem_real = ticket_medio - custo_total_por_oculos
            percentual_margem_real = (margem_real / ticket_medio) * 100 if ticket_medio > 0 else 0
            
            cor_margem = "green" if percentual_margem_real > 40 else "orange" if percentual_margem_real > 25 else "red"
            

        
        # Configuração de Termos de Pagamento aos Fornecedores
        st.markdown("### 💳 Termos de Pagamento aos Fornecedores")
        st.markdown("Configure como você paga seus fornecedores para cálculos precisos de fluxo de caixa")
        
        col_pag1, col_pag2, col_pag3 = st.columns(3)
        
        with col_pag1:
            forma_pagamento = st.selectbox(
                "Forma de Pagamento Principal",
                ["À Vista", "30 dias", "45 dias", "60 dias", "Parcelado (30/60)", "Parcelado (30/60/90)", "Personalizado"],
                index=["À Vista", "30 dias", "45 dias", "60 dias", "Parcelado (30/60)", "Parcelado (30/60/90)", "Personalizado"].index(
                    st.session_state.business_data.get('forma_pagamento_fornecedor', 'Parcelado (30/60)')
                ),
                help="Como você paga seus fornecedores (ATAK, Brasil Lentes, GOLD, DSMHD)"
            )
            if forma_pagamento != st.session_state.business_data.get('forma_pagamento_fornecedor'):
                st.session_state.business_data['forma_pagamento_fornecedor'] = forma_pagamento
                save_user_data()
        
        with col_pag2:
            # Configurar percentuais baseado na forma selecionada
            if forma_pagamento == "À Vista":
                percentual_mes_atual = 100.0
                percentual_mes_seguinte = 0.0
                percentual_terceiro_mes = 0.0
            elif forma_pagamento == "30 dias":
                percentual_mes_atual = 0.0
                percentual_mes_seguinte = 100.0
                percentual_terceiro_mes = 0.0
            elif forma_pagamento == "45 dias":
                percentual_mes_atual = 0.0
                percentual_mes_seguinte = 50.0
                percentual_terceiro_mes = 50.0
            elif forma_pagamento == "60 dias":
                percentual_mes_atual = 0.0
                percentual_mes_seguinte = 0.0
                percentual_terceiro_mes = 100.0
            elif forma_pagamento == "Parcelado (30/60)":
                percentual_mes_atual = 0.0
                percentual_mes_seguinte = 80.0
                percentual_terceiro_mes = 20.0
            elif forma_pagamento == "Parcelado (30/60/90)":
                percentual_mes_atual = 0.0
                percentual_mes_seguinte = 60.0
                percentual_terceiro_mes = 40.0
            else:  # Personalizado
                percentual_mes_atual = st.slider(
                    "% Pago no Mês Atual",
                    min_value=0.0,
                    max_value=100.0,
                    value=float(st.session_state.business_data.get('pct_pagamento_mes_atual', 20.0)),
                    step=5.0
                )
                if percentual_mes_atual != st.session_state.business_data.get('pct_pagamento_mes_atual'):
                    st.session_state.business_data['pct_pagamento_mes_atual'] = percentual_mes_atual
                    save_user_data()
            
            if forma_pagamento != "Personalizado":
                st.session_state.business_data['pct_pagamento_mes_atual'] = percentual_mes_atual
        
        with col_pag3:
            if forma_pagamento == "Personalizado":
                percentual_mes_seguinte = st.slider(
                    "% Pago no Mês Seguinte",
                    min_value=0.0,
                    max_value=100.0 - percentual_mes_atual,
                    value=min(float(st.session_state.business_data.get('pct_pagamento_mes_seguinte', 60.0)), 100.0 - percentual_mes_atual),
                    step=5.0
                )
                percentual_terceiro_mes = 100.0 - percentual_mes_atual - percentual_mes_seguinte
                
                st.session_state.business_data['pct_pagamento_mes_seguinte'] = percentual_mes_seguinte
                st.session_state.business_data['pct_pagamento_terceiro_mes'] = percentual_terceiro_mes
                save_user_data()
            else:
                # Para formas pré-definidas, salvar os valores calculados
                st.session_state.business_data['pct_pagamento_mes_seguinte'] = percentual_mes_seguinte
                st.session_state.business_data['pct_pagamento_terceiro_mes'] = percentual_terceiro_mes
            
            # Mostrar distribuição atual
            st.info(f"""
            **Distribuição de Pagamentos:**
            • Mês atual: {percentual_mes_atual:.0f}%
            • Mês seguinte: {percentual_mes_seguinte:.0f}%
            • Terceiro mês: {percentual_terceiro_mes:.0f}%
            """)
        
        # Desconto para pagamento à vista
        if forma_pagamento != "À Vista":
            desconto_avista = st.slider(
                "Desconto por Pagamento à Vista (%)",
                min_value=0.0,
                max_value=10.0,
                value=float(st.session_state.business_data.get('desconto_avista_fornecedor', 2.5)),
                step=0.5,
                help="Desconto oferecido pelo fornecedor para pagamento à vista"
            )
            if desconto_avista != st.session_state.business_data.get('desconto_avista_fornecedor'):
                st.session_state.business_data['desconto_avista_fornecedor'] = desconto_avista
                save_user_data()
        else:
            desconto_avista = float(st.session_state.business_data.get('desconto_avista_fornecedor', 2.5))
        
        # Impacto no fluxo de caixa
        st.markdown("**💡 Impacto no Fluxo de Caixa:**")
        exemplo_compra = 10000
        valor_mes_atual = exemplo_compra * (percentual_mes_atual / 100)
        valor_mes_seguinte = exemplo_compra * (percentual_mes_seguinte / 100)
        valor_terceiro_mes = exemplo_compra * (percentual_terceiro_mes / 100)
        
        if forma_pagamento == "À Vista" and desconto_avista > 0:
            valor_com_desconto = exemplo_compra * (1 - desconto_avista / 100)
            st.success(f"Exemplo: Compra de R$ {exemplo_compra:,.2f} → Paga R$ {valor_com_desconto:,.2f} (desconto de {desconto_avista}%)")
        else:
            st.info(f"""
            Exemplo: Compra de R$ {exemplo_compra:,.2f}
            • Mês atual: R$ {valor_mes_atual:,.2f}
            • Mês seguinte: R$ {valor_mes_seguinte:,.2f}
            • Terceiro mês: R$ {valor_terceiro_mes:,.2f}
            """)
            if desconto_avista > 0:
                economia_anual = exemplo_compra * 12 * (desconto_avista / 100)
                st.warning(f"Oportunidade perdida: R$ {economia_anual:,.2f}/ano se pagasse à vista")
        
        # Atualizar outros_fixos com o total calculado
        outros_fixos = total_despesas_detalhadas - 0  # Subtrair para não duplicar
        if outros_fixos < 0:
            outros_fixos = 0
        
        # Salvar percentuais para cálculos
        st.session_state.business_data.update({
            'cmv_percentual': cmv_percentual,
            'impostos_percentual': impostos_percentual,
            'comissoes_percentual': comissoes_percentual,
            'outros_variaveis_percentual': outros_variaveis_percentual,
            'aluguel': aluguel_mensal,
            'salarios_clt': salarios_clt,
            'total_optometrista': total_optometrista,
            'salarios_total': salarios_clt + total_optometrista,

            'outros_fixos': outros_fixos,
            'total_despesas_operacionais': total_despesas_detalhadas
        })
        
        # Análise de ponto de equilíbrio
        st.markdown("### ⚖️ Análise de Ponto de Equilíbrio")
        col_eq1, col_eq2, col_eq3 = st.columns(3)
        
        margem_contribuicao_perc = 100 - total_variaveis_perc
        ponto_equilibrio_valor = custos_fixos_total / (margem_contribuicao_perc / 100) if margem_contribuicao_perc > 0 else 0
        ponto_equilibrio_unidades = ponto_equilibrio_valor / ticket_medio if ticket_medio > 0 else 0
        
        with col_eq1:
            st.metric("Margem de Contribuição", f"{margem_contribuicao_perc:.1f}%")
        
        with col_eq2:
            st.metric("Ponto de Equilíbrio", format_currency(ponto_equilibrio_valor))
        
        with col_eq3:
            st.metric("Vendas Necessárias", f"{ponto_equilibrio_unidades:.0f} unidades/mês")
        
        # Botão para explicar a origem do cálculo
        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            if st.button("📖 De onde vem esse valor do ponto de equilíbrio?", key="explain_equilibrio_main"):
                st.info(f"""
                💡 **Você precisa vender {format_currency(ponto_equilibrio_valor)} por mês**
                
                **Fórmula:** Custos Fixos ÷ Margem de Contribuição = Vendas Necessárias
                
                **Custos Fixos Totais: {format_currency(custos_fixos_total)}**
                • Aluguel: {format_currency(aluguel_mensal)}
                • Folha CLT: {format_currency(salarios_clt)}
                • Serviços terceirizados: {format_currency(total_optometrista)}
                • Serviços terceiros: {format_currency(0)}
                • Outros custos: {format_currency(outros_fixos)}
                
                **Margem de Contribuição: {margem_contribuicao_perc:.1f}%**
                • Custos variáveis: {total_variaveis_perc:.1f}%
                • Sobra para custos fixos: {margem_contribuicao_perc:.1f}%
                
                **Cálculo:** {format_currency(custos_fixos_total)} ÷ {margem_contribuicao_perc:.1f}% = {format_currency(ponto_equilibrio_valor)}
                
                **Em resumo:** De cada R$ 100 vendidos, sobram R$ {margem_contribuicao_perc:.0f} para custos fixos. Como seus custos fixos são {format_currency(custos_fixos_total)}, você precisa vender {format_currency(ponto_equilibrio_valor)} para empatar.
                """)
        
        # Salvar dados calculados
        st.session_state.business_data.update({
            'margem_contribuicao_perc': margem_contribuicao_perc,
            'ponto_equilibrio_valor': ponto_equilibrio_valor,
            'ponto_equilibrio_unidades': ponto_equilibrio_unidades
        })
    
    with tab3:
        st.subheader("📊 DRE Projetado Mês a Mês")
        
        # Calcular DRE mês a mês
        dre_mensal = []
        
        for mes in range(1, 13):
            if mes == 1:
                receita_mes = vendas_mes_1
            else:
                receita_mes = dre_mensal[mes-2]['receita_bruta'] * (1 + crescimento_mensal/100)
            
            # Custos variáveis detalhados
            cmv_valor = receita_mes * (cmv_percentual / 100)
            impostos_valor = receita_mes * (impostos_percentual / 100)
            comissoes_valor = receita_mes * (comissoes_percentual / 100)
            
            # Taxas financeiras baseadas na configuração da Etapa 5
            usar_customizada = st.session_state.business_data.get('usar_taxa_customizada', False)
            if usar_customizada:
                taxa_financeira_percent = st.session_state.business_data.get('taxa_customizada', 4.3) / 100
            else:
                taxa_financeira_percent = st.session_state.business_data.get('taxa_mercado_pago', 4.3) / 100
            
            # Aplicar taxa financeira baseada no percentual de vendas a prazo
            percentual_prazo = (100 - st.session_state.business_data.get('percentual_avista', 70)) / 100
            taxas_financeiras_valor = receita_mes * percentual_prazo * taxa_financeira_percent
            
            # Calcular comissões do captador baseadas nas configurações
            comissoes_captador_valor = 0
            if st.session_state.business_data.get('usar_sistema_captacao', False):
                # Estimar número de vendas baseado no ticket médio
                ticket_medio_estimado = st.session_state.business_data.get('ticket_medio', 180)
                if ticket_medio_estimado > 0:
                    total_vendas_mes = receita_mes / ticket_medio_estimado
                    
                    # Vendas à vista e parceladas
                    percentual_avista = st.session_state.business_data.get('percentual_avista', 70) / 100
                    vendas_avista = total_vendas_mes * percentual_avista
                    vendas_parceladas = total_vendas_mes * (1 - percentual_avista)
                    
                    # Calcular comissões por modalidade
                    tipo_comissao_avista = st.session_state.business_data.get('tipo_comissao_avista', 'Valor fixo por venda')
                    tipo_comissao_parcelada = st.session_state.business_data.get('tipo_comissao_parcelada', 'Valor fixo por venda')
                    
                    # Comissão vendas à vista
                    if tipo_comissao_avista == "Valor fixo por venda":
                        comissao_avista_total = vendas_avista * st.session_state.business_data.get('comissao_avista', 30.0)
                    else:
                        receita_avista = receita_mes * percentual_avista
                        comissao_avista_total = receita_avista * (st.session_state.business_data.get('percentual_comissao_avista', 3.0) / 100)
                    
                    # Comissão vendas parceladas
                    if tipo_comissao_parcelada == "Valor fixo por venda":
                        comissao_parcelada_total = vendas_parceladas * st.session_state.business_data.get('comissao_parcelada', 20.0)
                    else:
                        receita_parcelada = receita_mes * (1 - percentual_avista)
                        comissao_parcelada_total = receita_parcelada * (st.session_state.business_data.get('percentual_comissao_parcelada', 2.0) / 100)
                    
                    # Comissões por produto (se habilitado)
                    comissao_produtos_total = 0
                    if st.session_state.business_data.get('usar_comissao_produto', False):
                        # Estimar 75% das vendas incluem lentes, 90% incluem armações
                        vendas_com_lentes = total_vendas_mes * 0.75
                        vendas_com_armacoes = total_vendas_mes * 0.90
                        
                        comissao_produtos_total = (
                            vendas_com_lentes * st.session_state.business_data.get('comissao_lentes', 10.0) +
                            vendas_com_armacoes * st.session_state.business_data.get('comissao_armacoes', 5.0)
                        )
                    
                    comissoes_captador_valor = comissao_avista_total + comissao_parcelada_total + comissao_produtos_total
            
            outros_var_valor = receita_mes * (outros_variaveis_percentual / 100)
            
            custos_variaveis_total = cmv_valor + impostos_valor + comissoes_valor + taxas_financeiras_valor + comissoes_captador_valor + outros_var_valor
            margem_contribuicao = receita_mes - custos_variaveis_total
            
            # Custos fixos detalhados
            aluguel_mes = aluguel_mensal
            salarios_mes = salarios_clt + total_optometrista
            servicos_mes = 0
            outros_fixos_mes = outros_fixos
            depreciacao_mes = (st.session_state.business_data.get('reforma_loja', 15000) + 
                             st.session_state.business_data.get('equipamentos_total', 12000)) * 0.05 / 12
            
            custos_fixos_total_mes = aluguel_mes + salarios_mes + servicos_mes + outros_fixos_mes + depreciacao_mes
            lucro_operacional_mes = margem_contribuicao - custos_fixos_total_mes
            
            dre_mensal.append({
                'mes': mes,
                'receita_bruta': receita_mes,
                'cmv': cmv_valor,
                'impostos': impostos_valor,
                'comissoes': comissoes_valor,
                'taxas_financeiras': taxas_financeiras_valor,
                'comissoes_captador': comissoes_captador_valor,
                'outros_variaveis': outros_var_valor,
                'custos_variaveis_total': custos_variaveis_total,
                'margem_contribuicao': margem_contribuicao,
                'aluguel': aluguel_mes,
                'salarios': salarios_mes,
                'servicos': servicos_mes,
                'outros_fixos': outros_fixos_mes,
                'depreciacao': depreciacao_mes,
                'custos_fixos_total': custos_fixos_total_mes,
                'lucro_operacional': lucro_operacional_mes
            })
        
        # Mostrar tabela DRE
        st.markdown("### DRE Detalhado Mês a Mês")
        
        df_dre = pd.DataFrame([
            {
                'Item': 'Receita Bruta',
                **{f'Mês {i+1}': f"R$ {dre['receita_bruta']:,.0f}" for i, dre in enumerate(dre_mensal)},
                'Total Anual': f"R$ {sum(dre['receita_bruta'] for dre in dre_mensal):,.0f}"
            },
            {
                'Item': '(-) CMV',
                **{f'Mês {i+1}': f"R$ {dre['cmv']:,.0f}" for i, dre in enumerate(dre_mensal)},
                'Total Anual': f"R$ {sum(dre['cmv'] for dre in dre_mensal):,.0f}"
            },
            {
                'Item': '(-) Impostos',
                **{f'Mês {i+1}': f"R$ {dre['impostos']:,.0f}" for i, dre in enumerate(dre_mensal)},
                'Total Anual': f"R$ {sum(dre['impostos'] for dre in dre_mensal):,.0f}"
            },
            {
                'Item': '(-) Taxas Financeiras',
                **{f'Mês {i+1}': f"R$ {dre['taxas_financeiras']:,.0f}" for i, dre in enumerate(dre_mensal)},
                'Total Anual': f"R$ {sum(dre['taxas_financeiras'] for dre in dre_mensal):,.0f}"
            },
            {
                'Item': '(-) Comissões',
                **{f'Mês {i+1}': f"R$ {dre['comissoes']:,.0f}" for i, dre in enumerate(dre_mensal)},
                'Total Anual': f"R$ {sum(dre['comissoes'] for dre in dre_mensal):,.0f}"
            },
            {
                'Item': '(-) Comissões Captador',
                **{f'Mês {i+1}': f"R$ {dre['comissoes_captador']:,.0f}" for i, dre in enumerate(dre_mensal)},
                'Total Anual': f"R$ {sum(dre['comissoes_captador'] for dre in dre_mensal):,.0f}"
            },
            {
                'Item': '= Margem de Contribuição',
                **{f'Mês {i+1}': f"R$ {dre['margem_contribuicao']:,.0f}" for i, dre in enumerate(dre_mensal)},
                'Total Anual': f"R$ {sum(dre['margem_contribuicao'] for dre in dre_mensal):,.0f}"
            },
            {
                'Item': '(-) Aluguel',
                **{f'Mês {i+1}': f"R$ {dre['aluguel']:,.0f}" for i, dre in enumerate(dre_mensal)},
                'Total Anual': f"R$ {sum(dre['aluguel'] for dre in dre_mensal):,.0f}"
            },
            {
                'Item': '(-) Salários',
                **{f'Mês {i+1}': f"R$ {dre['salarios']:,.0f}" for i, dre in enumerate(dre_mensal)},
                'Total Anual': f"R$ {sum(dre['salarios'] for dre in dre_mensal):,.0f}"
            },
            {
                'Item': '(-) Depreciação',
                **{f'Mês {i+1}': f"R$ {dre['depreciacao']:,.0f}" for i, dre in enumerate(dre_mensal)},
                'Total Anual': f"R$ {sum(dre['depreciacao'] for dre in dre_mensal):,.0f}"
            },
            {
                'Item': '= LUCRO OPERACIONAL',
                **{f'Mês {i+1}': f"R$ {dre['lucro_operacional']:,.0f}" for i, dre in enumerate(dre_mensal)},
                'Total Anual': f"R$ {sum(dre['lucro_operacional'] for dre in dre_mensal):,.0f}"
            }
        ])
        
        st.dataframe(df_dre, use_container_width=True)
        
        # Breakdown detalhado por linha
        st.markdown("### 🔍 Breakdown Detalhado")
        
        linha_selecionada = st.selectbox(
            "Selecione uma linha para ver a composição detalhada:",
            ["Receita Bruta", "CMV", "Impostos", "Taxas Financeiras", "Comissões", "Comissões Captador", "Salários", "Outros Custos Fixos"]
        )
        
        if linha_selecionada == "Receita Bruta":
            st.markdown("**Composição da Receita Bruta:**")
            st.write(f"• Vendas mês 1: R$ {vendas_mes_1:,.2f}")
            st.write(f"• Crescimento mensal: {crescimento_mensal}%")
            st.write(f"• Ticket médio: R$ {ticket_medio:,.2f}")
            st.write(f"• Vendas por mês: {vendas_mes_1/ticket_medio:.0f} unidades")
        
        elif linha_selecionada == "CMV":
            st.markdown("**Composição do CMV:**")
            st.write(f"• Percentual sobre receita: {cmv_percentual}%")
            st.write("• Inclui: Custo das lentes, armações, materiais")
            st.write("• Base: Preços de fornecedores (ATAK, Brasil Lentes, GOLD)")
        
        elif linha_selecionada == "Impostos":
            st.markdown("**Composição dos Impostos:**")
            regime_tributario = st.session_state.business_data.get('regime_tributario', 'Simples Nacional')
            st.write(f"• Regime tributário: {regime_tributario}")
            st.write(f"• Alíquota média: {impostos_percentual}%")
            if regime_tributario == "Simples Nacional":
                st.write("• Inclui: IRPJ, CSLL, PIS, COFINS, ICMS, CPP, ISS")
        
        elif linha_selecionada == "Taxas Financeiras":
            st.markdown("**Composição das Taxas Financeiras:**")
            usar_customizada = st.session_state.business_data.get('usar_taxa_customizada', False)
            if usar_customizada:
                taxa_percentual = st.session_state.business_data.get('taxa_customizada', 4.3)
                st.write(f"• Taxa customizada: {taxa_percentual}%")
            else:
                taxa_percentual = st.session_state.business_data.get('taxa_mercado_pago', 4.3)
                opcao_mp = st.session_state.business_data.get('opcao_recebimento_mp', 'Crédito à vista - 14 dias (3,79%)')
                st.write(f"• Mercado Pago: {opcao_mp}")
                st.write(f"• Taxa aplicada: {taxa_percentual}%")
            
            percentual_prazo = (100 - st.session_state.business_data.get('percentual_avista', 70))
            percentual_avista = st.session_state.business_data.get('percentual_avista', 70)
            st.write(f"• Vendas à vista: {percentual_avista}% (taxa 0%)")
            st.write(f"• Vendas a prazo: {percentual_prazo}% (com taxa)")
            valor_taxas_mensal = vendas_mes_1 * (percentual_prazo / 100) * (taxa_percentual / 100)
            st.write(f"• Valor médio mensal: R$ {valor_taxas_mensal:,.2f}")
            st.write(f"• Fórmula: Receita × {percentual_prazo}% × {taxa_percentual}%")
        
        elif linha_selecionada == "Comissões":
            st.markdown("**Composição das Comissões:**")
            st.write(f"• Percentual sobre vendas: {comissoes_percentual}%")
            st.write("• Comissões de vendedores sobre receita bruta")
            st.write("• Inclui: Comissão de vendas, prêmios por meta")
            st.write("• Base de cálculo: Receita bruta mensal")
            valor_comissao_mensal = vendas_mes_1 * (comissoes_percentual / 100)
            st.write(f"• Valor médio mensal: R$ {valor_comissao_mensal:,.2f}")
        
        elif linha_selecionada == "Comissões Captador":
            st.markdown("**Composição das Comissões do Captador:**")
            
            if st.session_state.business_data.get('usar_sistema_captacao', False):
                # Calcular exemplo com dados do primeiro mês
                ticket_medio_calc = st.session_state.business_data.get('ticket_medio', 180)
                percentual_avista = st.session_state.business_data.get('percentual_avista', 70)
                
                total_vendas_exemplo = vendas_mes_1 / ticket_medio_calc
                vendas_avista_exemplo = total_vendas_exemplo * (percentual_avista / 100)
                vendas_parcelada_exemplo = total_vendas_exemplo * ((100 - percentual_avista) / 100)
                
                # Comissões configuradas
                comissao_avista_config = st.session_state.business_data.get('comissao_avista', 30.0)
                comissao_parcelada_config = st.session_state.business_data.get('comissao_parcelada', 20.0)
                tipo_avista = st.session_state.business_data.get('tipo_comissao_avista', 'Valor fixo por venda')
                tipo_parcelada = st.session_state.business_data.get('tipo_comissao_parcelada', 'Valor fixo por venda')
                
                st.write(f"• Sistema de captação: **Ativo**")
                st.write(f"• Vendas estimadas/mês: {total_vendas_exemplo:.0f} unidades")
                st.write(f"• Vendas à vista ({percentual_avista}%): {vendas_avista_exemplo:.0f} unidades")
                st.write(f"• Vendas parceladas ({100-percentual_avista}%): {vendas_parcelada_exemplo:.0f} unidades")
                
                # Calcular comissões
                if tipo_avista == "Valor fixo por venda":
                    comissao_avista_total = vendas_avista_exemplo * comissao_avista_config
                    st.write(f"• Comissão à vista: {vendas_avista_exemplo:.0f} × R$ {comissao_avista_config:.2f} = R$ {comissao_avista_total:.2f}")
                else:
                    percentual_comissao_avista = st.session_state.business_data.get('percentual_comissao_avista', 3.0)
                    receita_avista = vendas_mes_1 * (percentual_avista / 100)
                    comissao_avista_total = receita_avista * (percentual_comissao_avista / 100)
                    st.write(f"• Comissão à vista: R$ {receita_avista:.2f} × {percentual_comissao_avista}% = R$ {comissao_avista_total:.2f}")
                
                if tipo_parcelada == "Valor fixo por venda":
                    comissao_parcelada_total = vendas_parcelada_exemplo * comissao_parcelada_config
                    st.write(f"• Comissão parcelada: {vendas_parcelada_exemplo:.0f} × R$ {comissao_parcelada_config:.2f} = R$ {comissao_parcelada_total:.2f}")
                else:
                    percentual_comissao_parcelada = st.session_state.business_data.get('percentual_comissao_parcelada', 2.0)
                    receita_parcelada = vendas_mes_1 * ((100 - percentual_avista) / 100)
                    comissao_parcelada_total = receita_parcelada * (percentual_comissao_parcelada / 100)
                    st.write(f"• Comissão parcelada: R$ {receita_parcelada:.2f} × {percentual_comissao_parcelada}% = R$ {comissao_parcelada_total:.2f}")
                
                # Comissões por produto
                if st.session_state.business_data.get('usar_comissao_produto', False):
                    comissao_lentes = st.session_state.business_data.get('comissao_lentes', 10.0)
                    comissao_armacoes = st.session_state.business_data.get('comissao_armacoes', 5.0)
                    vendas_com_lentes = total_vendas_exemplo * 0.75
                    vendas_com_armacoes = total_vendas_exemplo * 0.90
                    comissao_produtos_total = (vendas_com_lentes * comissao_lentes) + (vendas_com_armacoes * comissao_armacoes)
                    st.write(f"• Comissão produtos: R$ {comissao_produtos_total:.2f}")
                    total_comissoes_captador = comissao_avista_total + comissao_parcelada_total + comissao_produtos_total
                else:
                    total_comissoes_captador = comissao_avista_total + comissao_parcelada_total
                
                st.write(f"• **Total comissões captador: R$ {total_comissoes_captador:.2f}**")
                st.write("• Fonte: Configuração Etapa 8 - Sistema de Captação")
            else:
                st.write("• Sistema de captação: **Desativado**")
                st.write("• Configure na Etapa 8 para ativar comissões do captador")
                st.write("• Valor atual: R$ 0,00")
        
        elif linha_selecionada == "Salários":
            st.markdown("**Composição dos Salários:**")
            num_func = st.session_state.business_data.get('num_funcionarios', 2)
            st.write(f"• Número de funcionários: {num_func}")
            st.write(f"• Folha CLT: R$ {salarios_clt:,.2f}")
            st.write(f"• Serviços terceirizados: R$ {total_optometrista:,.2f}")
            st.write(f"• Total pessoal: R$ {salarios_clt + total_optometrista:,.2f}")
            st.write("• Inclui: Salários + encargos (68% sobre salário base)")
            if hasattr(st.session_state, 'funcionarios'):
                for func in st.session_state.funcionarios:
                    custo_func = func['salario_base'] * 1.68
                    st.write(f"  - {func['nome']} ({func['cargo']}): R$ {custo_func:,.2f}")
        
        elif linha_selecionada == "Outros Custos Fixos":
            st.markdown("**Composição dos Outros Custos Fixos:**")
            st.write(f"• Serviços de terceiros: R$ {0:,.2f}")
            st.write("  - Contabilidade, limpeza, segurança")
            st.write("  - Manutenção de equipamentos")
            st.write(f"• Outros custos fixos: R$ {outros_fixos:,.2f}")
            st.write("  - Telefone, internet, energia")
            st.write("  - Material de escritório, seguros")
            st.write("  - Taxas e licenças")
            total_outros = 0 + outros_fixos
            st.write(f"• **Total outros custos: R$ {total_outros:,.2f}**")
        
        # Indicadores de rentabilidade avançados
        st.markdown("### 📈 Indicadores de Rentabilidade e Viabilidade")
        
        receita_anual_total = sum(dre['receita_bruta'] for dre in dre_mensal)
        lucro_operacional_total = sum(dre['lucro_operacional'] for dre in dre_mensal)
        margem_contribuicao_total = sum(dre['margem_contribuicao'] for dre in dre_mensal)
        
        col_ind1, col_ind2, col_ind3, col_ind4 = st.columns(4)
        
        with col_ind1:
            margem_operacional = (lucro_operacional_total / receita_anual_total * 100) if receita_anual_total > 0 else 0
            st.metric("Margem Operacional", f"{margem_operacional:.1f}%", 
                     help="Lucro operacional / Receita anual")
        
        with col_ind2:
            investimento_total = st.session_state.business_data.get('investimento_total', 81500)
            roi_anual = (lucro_operacional_total / investimento_total * 100) if investimento_total > 0 else 0
            st.metric("ROI Anual", f"{roi_anual:.1f}%",
                     help="Retorno sobre investimento anual")
        
        with col_ind3:
            payback_anos = investimento_total / lucro_operacional_total if lucro_operacional_total > 0 else 0
            st.metric("Payback", f"{payback_anos:.1f} anos",
                     help="Tempo para recuperar investimento")
        
        with col_ind4:
            margem_contribuicao_perc_real = (margem_contribuicao_total / receita_anual_total * 100) if receita_anual_total > 0 else 0
            st.metric("Margem de Contribuição", f"{margem_contribuicao_perc_real:.1f}%",
                     help="Margem após custos variáveis")
        
        # Análise de cenários
        st.markdown("### 🎯 Análise de Cenários de Rentabilidade")
        
        cenarios_data = []
        cenarios = {
            "Pessimista (-20% receita, +10% custos)": {"receita": -20, "custos": +10},
            "Realista (projeção base)": {"receita": 0, "custos": 0},
            "Otimista (+30% receita, -5% custos)": {"receita": +30, "custos": -5}
        }
        
        for nome_cenario, ajustes in cenarios.items():
            receita_cenario = receita_anual_total * (1 + ajustes["receita"]/100)
            custos_variaveis_cenario = receita_cenario * (total_variaveis_perc/100) * (1 + ajustes["custos"]/100)
            custos_fixos_anuais = sum(dre['custos_fixos_total'] for dre in dre_mensal)
            custos_fixos_cenario = custos_fixos_anuais * (1 + ajustes["custos"]/100)
            lucro_cenario = receita_cenario - custos_variaveis_cenario - custos_fixos_cenario
            roi_cenario = (lucro_cenario / investimento_total * 100) if investimento_total > 0 else 0
            margem_cenario = (lucro_cenario / receita_cenario * 100) if receita_cenario > 0 else 0
            
            cenarios_data.append({
                'Cenário': nome_cenario,
                'Receita Anual': f"R$ {receita_cenario:,.0f}",
                'Lucro Operacional': f"R$ {lucro_cenario:,.0f}",
                'ROI': f"{roi_cenario:.1f}%",
                'Margem': f"{margem_cenario:.1f}%"
            })
        
        df_cenarios = pd.DataFrame(cenarios_data)
        st.dataframe(df_cenarios, use_container_width=True)
        
        # Ponto de equilíbrio detalhado
        st.markdown("### ⚖️ Análise de Ponto de Equilíbrio Detalhada")
        col_eq1, col_eq2 = st.columns(2)
        
        with col_eq1:
            st.write(f"**Custos Fixos Mensais:** R$ {custos_fixos_total:,.2f}")
            st.write(f"**Margem de Contribuição:** {margem_contribuicao_perc:.1f}%")
            st.write(f"**Ponto de Equilíbrio Mensal:** R$ {ponto_equilibrio_valor:,.2f}")
            st.write(f"**Vendas Necessárias:** {ponto_equilibrio_unidades:.0f} unidades/mês")
        
        with col_eq2:
            vendas_atual_mes = vendas_mes_1
            if vendas_atual_mes > ponto_equilibrio_valor:
                diferenca = vendas_atual_mes - ponto_equilibrio_valor
                st.success(f"✅ Acima do ponto de equilíbrio em R$ {diferenca:,.2f}")
                margem_seguranca = (diferenca / vendas_atual_mes * 100)
                st.write(f"**Margem de Segurança:** {margem_seguranca:.1f}%")
            else:
                diferenca = ponto_equilibrio_valor - vendas_atual_mes
                st.warning(f"⚠️ Abaixo do ponto de equilíbrio em R$ {diferenca:,.2f}")
                st.write("Necessário aumentar vendas ou reduzir custos")
        
        # Botão para explicar a origem do cálculo (logo abaixo da análise)
        if st.button("📖 De onde vem esse valor do ponto de equilíbrio?", key="explain_equilibrio_detalhado"):
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #fff8e1, #fffef7);
                padding: 1.5rem;
                border-radius: 12px;
                border-left: 4px solid #ff9800;
                margin: 1rem 0;
            ">
                <div style="font-size: 1.1rem; font-weight: bold; color: #e65100; margin-bottom: 0.5rem;">
                    Você precisa vender {format_currency(ponto_equilibrio_valor)} por mês
                </div>
                <div style="font-size: 1rem; font-weight: bold; color: #e65100; margin-bottom: 0.5rem;">
                    Porque?:
                </div>
                <div style="color: #e65100; line-height: 1.5;">
                    <strong>Fórmula do Ponto de Equilíbrio:</strong><br>
                    Custos Fixos ÷ Margem de Contribuição = Vendas Necessárias<br><br>
                    
                    <strong>Seus Custos Fixos Totais:</strong> {format_currency(custos_fixos_total)}<br>
                    • Aluguel: {format_currency(aluguel_mensal)}<br>
                    • Folha CLT: {format_currency(salarios_clt)}<br>
                    • Serviços terceirizados: {format_currency(total_optometrista)}<br>
                    • Serviços terceiros: {format_currency(0)}<br>
                    • Outros custos fixos: {format_currency(outros_fixos)}<br><br>
                    
                    <strong>Sua Margem de Contribuição:</strong> {margem_contribuicao_perc:.1f}%<br>
                    • Custos variáveis: {total_variaveis_perc:.1f}% (CMV + impostos + comissões)<br>
                    • Sobra para cobrir custos fixos: {margem_contribuicao_perc:.1f}%<br><br>
                    
                    <strong>Cálculo Final:</strong><br>
                    {format_currency(custos_fixos_total)} ÷ {margem_contribuicao_perc:.1f}% = {format_currency(ponto_equilibrio_valor)}<br><br>
                    
                    <strong>Traduzindo:</strong> De cada R$ 100 que você vende, sobram R$ {margem_contribuicao_perc:.0f} para pagar os custos fixos. Como seus custos fixos são {format_currency(custos_fixos_total)}, você precisa vender {format_currency(ponto_equilibrio_valor)} para "empatar" (não ter lucro nem prejuízo).
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Salvar todos os indicadores calculados
        st.session_state.business_data.update({
            'receita_anual': receita_anual_total,
            'lucro_operacional': lucro_operacional_total,
            'margem_operacional': margem_operacional,
            'roi_anual': roi_anual,
            'payback_anos': payback_anos,
            'margem_contribuicao_real': margem_contribuicao_perc_real,
            'ponto_equilibrio_status': 'acima' if vendas_atual_mes > ponto_equilibrio_valor else 'abaixo',
            'margem_seguranca': (vendas_atual_mes - ponto_equilibrio_valor) / vendas_atual_mes * 100 if vendas_atual_mes > 0 else 0,
            'projecoes_completas': True
        })
    
    with tab4:
        st.subheader("💸 Fluxo de Caixa Projetado")
        
        # Explicar origem do valor inicial
        st.markdown("### 💰 Origem do Saldo Inicial")
        
        capital_giro_default = st.session_state.business_data.get('capital_giro', 18000)
        reforma_loja = st.session_state.business_data.get('reforma_loja', 0)
        equipamentos_moveis = st.session_state.business_data.get('equipamentos_moveis', 
                                                                st.session_state.business_data.get('equipamentos_total', 
                                                                st.session_state.business_data.get('investimento_equipamentos', 1500)))
        estoque_inicial = st.session_state.business_data.get('estoque_inicial', 0)
        
        valor_total_investimento = reforma_loja + equipamentos_moveis + estoque_inicial + capital_giro_default
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Composição do Investimento Inicial:**")
            st.write(f"• Reforma da loja: R$ {reforma_loja:,.2f}")
            st.write(f"• Equipamentos e móveis: R$ {equipamentos_moveis:,.2f}")
            st.write(f"• Estoque inicial: R$ {estoque_inicial:,.2f}")
            st.write(f"• Capital de giro: R$ {capital_giro_default:,.2f}")
            st.markdown(f"**• TOTAL: R$ {valor_total_investimento:,.2f}**")
        
        with col2:
            st.markdown("**O que é Capital de Giro:**")
            st.write("• Dinheiro disponível para operação diária")
            st.write("• Pagamento de fornecedores")
            st.write("• Folha de pagamento dos primeiros meses")
            st.write("• Despesas operacionais iniciais")
            st.write("• Reserva para imprevistos")
        
        st.info(f"""
        💡 **Explicação do Saldo Inicial de R$ {capital_giro_default:,.2f}**
        
        Este valor representa o capital de giro necessário para iniciar as operações da ótica. 
        É calculado baseado nos custos fixos mensais estimados e representa aproximadamente 
        2-3 meses de operação para garantir fluxo de caixa positivo desde o início.
        """)
        
        # Calcular fluxo de caixa mês a mês
        fluxo_caixa = []
        saldo_acumulado = capital_giro_default  # Usar valor do capital de giro
        
        for mes in range(1, 13):
            if mes == 1:
                receita_mes = vendas_mes_1
            else:
                receita_mes = fluxo_caixa[mes-2]['receita_mes'] * (1 + crescimento_mensal/100)
            
            # Entradas baseadas nas configurações da Etapa 5
            percentual_avista = st.session_state.business_data.get('percentual_avista', 70) / 100
            percentual_prazo = 1 - percentual_avista
            prazo_medio_recebimento = st.session_state.business_data.get('prazo_medio_recebimento', 30)
            
            # Usar taxas do Mercado Pago configuradas na Etapa 5
            usar_customizada = st.session_state.business_data.get('usar_taxa_customizada', False)
            if usar_customizada:
                taxa_financeira = st.session_state.business_data.get('taxa_customizada', 4.3) / 100
            else:
                taxa_financeira = st.session_state.business_data.get('taxa_mercado_pago', 4.3) / 100
            
            # Vendas à vista (sem desconto da financeira)
            entradas_vendas = receita_mes * percentual_avista
            
            # Recebimentos a prazo (com desconto da financeira se aplicável)
            receita_prazo_bruta = receita_mes * percentual_prazo
            receita_prazo_liquida = receita_prazo_bruta * (1 - taxa_financeira)  # Descontar taxa
            
            # Calcular quando receber baseado no prazo configurado
            if prazo_medio_recebimento <= 30:
                # Antecipação: recebe tudo no mês seguinte, já descontada a taxa
                entradas_recebimentos = receita_prazo_liquida if mes > 1 else 0
            elif prazo_medio_recebimento <= 60:
                # Parcelado: recebe conforme cliente paga, com taxa menor
                entradas_recebimentos = receita_prazo_liquida if mes > 2 else 0
            else:
                # Direto: recebe quando cliente paga, sem taxa mas com risco
                entradas_recebimentos = receita_prazo_liquida if mes > 3 else 0
            
            entradas_total = entradas_vendas + entradas_recebimentos
            
            # Saídas detalhadas com todos os custos simulados
            # Usar configurações personalizadas de pagamento aos fornecedores
            pct_mes_atual = st.session_state.business_data.get('pct_pagamento_mes_atual', 20.0) / 100
            pct_mes_seguinte = st.session_state.business_data.get('pct_pagamento_mes_seguinte', 80.0) / 100
            forma_pag = st.session_state.business_data.get('forma_pagamento_fornecedor', 'Parcelado (30/60)')
            desconto_avista = st.session_state.business_data.get('desconto_avista_fornecedor', 2.5) / 100
            
            # Calcular pagamento de fornecedores baseado nos custos reais das tabelas
            # Buscar custos reais dos produtos configurados no sistema
            custo_lentes_real = st.session_state.business_data.get('custo_lentes_total', 0)
            custo_armacoes_real = st.session_state.business_data.get('custo_armacoes_total', 0)
            custo_servicos_real = st.session_state.business_data.get('custo_servicos_total', 0)
            
            # Total de custos baseado nas tabelas reais dos fornecedores
            cmv_real_total = custo_lentes_real + custo_armacoes_real + custo_servicos_real
            
            # Se não há dados reais, usar percentual como fallback
            if cmv_real_total <= 0:
                cmv_bruto = receita_mes * (cmv_percentual / 100)
            else:
                # Usar custos reais das tabelas dos fornecedores
                cmv_bruto = cmv_real_total
            
            # Aplicar termos de pagamento configurados
            if forma_pag == "À Vista":
                cmv_pagamento = cmv_bruto * (1 - desconto_avista)  # Aplicar desconto à vista
            else:
                cmv_pagamento = cmv_bruto * pct_mes_atual  # Pagar conforme configurado
            
            impostos_pagamento = receita_mes * (impostos_percentual / 100)
            
            # Folha de pagamento completa (incluindo todos os funcionários do DP)
            folha_completa = 0
            if hasattr(st.session_state, 'funcionarios') and st.session_state.funcionarios:
                for func in st.session_state.funcionarios:
                    if func['tipo_contrato'] == 'CLT':
                        folha_completa += func['salario_base'] * 1.68  # CLT com encargos
                    else:
                        folha_completa += func['salario_base']  # MEI/Prestador
            else:
                folha_completa = salarios_clt + total_optometrista
            
            # Custos operacionais específicos da ótica - valores exatos do usuário
            aluguel_pagamento = aluguel_mensal
            
            # Usar exatamente os valores configurados pelo usuário (podem ser zero)
            energia_agua = st.session_state.business_data.get('energia_agua', 0)
            telefone_internet = st.session_state.business_data.get('telefone_internet', 0)
            
            # Serviços profissionais - valores exatos do usuário
            contabilidade = st.session_state.business_data.get('contabilidade', 0)
            optometrista = st.session_state.business_data.get('custo_optometrista_mensal', 0)
            limpeza_seguranca = st.session_state.business_data.get('limpeza_seguranca', 0)
            
            # Custos de vendas e marketing - valores exatos do usuário
            comissoes_vendas = receita_mes * (comissoes_percentual / 100)
            
            # Comissões do captador baseadas na configuração
            comissoes_captador_pagamento = 0
            if st.session_state.business_data.get('usar_sistema_captacao', False):
                # Usar o mesmo cálculo da DRE para manter consistência
                ticket_medio_estimado = st.session_state.business_data.get('ticket_medio', 180)
                if ticket_medio_estimado > 0:
                    total_vendas_mes_fc = receita_mes / ticket_medio_estimado
                    percentual_avista_fc = st.session_state.business_data.get('percentual_avista', 70) / 100
                    vendas_avista_fc = total_vendas_mes_fc * percentual_avista_fc
                    vendas_parceladas_fc = total_vendas_mes_fc * (1 - percentual_avista_fc)
                    
                    # Calcular comissões por modalidade
                    tipo_comissao_avista = st.session_state.business_data.get('tipo_comissao_avista', 'Valor fixo por venda')
                    tipo_comissao_parcelada = st.session_state.business_data.get('tipo_comissao_parcelada', 'Valor fixo por venda')
                    
                    if tipo_comissao_avista == "Valor fixo por venda":
                        comissao_avista_fc = vendas_avista_fc * st.session_state.business_data.get('comissao_avista', 30.0)
                    else:
                        receita_avista_fc = receita_mes * percentual_avista_fc
                        comissao_avista_fc = receita_avista_fc * (st.session_state.business_data.get('percentual_comissao_avista', 3.0) / 100)
                    
                    if tipo_comissao_parcelada == "Valor fixo por venda":
                        comissao_parcelada_fc = vendas_parceladas_fc * st.session_state.business_data.get('comissao_parcelada', 20.0)
                    else:
                        receita_parcelada_fc = receita_mes * (1 - percentual_avista_fc)
                        comissao_parcelada_fc = receita_parcelada_fc * (st.session_state.business_data.get('percentual_comissao_parcelada', 2.0) / 100)
                    
                    # Comissões por produto
                    comissao_produtos_fc = 0
                    if st.session_state.business_data.get('usar_comissao_produto', False):
                        vendas_com_lentes_fc = total_vendas_mes_fc * 0.75
                        vendas_com_armacoes_fc = total_vendas_mes_fc * 0.90
                        comissao_produtos_fc = (
                            vendas_com_lentes_fc * st.session_state.business_data.get('comissao_lentes', 10.0) +
                            vendas_com_armacoes_fc * st.session_state.business_data.get('comissao_armacoes', 5.0)
                        )
                    
                    comissoes_captador_pagamento = comissao_avista_fc + comissao_parcelada_fc + comissao_produtos_fc
            
            marketing_publicidade = st.session_state.business_data.get('marketing_publicidade', 0)
            
            # Despesas administrativas - valores exatos do usuário  
            material_escritorio = st.session_state.business_data.get('material_escritorio', 0)
            seguros = st.session_state.business_data.get('seguros', 0)
            manutencao_equipamentos = st.session_state.business_data.get('manutencao_equipamentos', 0)
            
            # Taxas financeiras sobre vendas a prazo
            receita_prazo_valor = receita_mes * percentual_prazo
            taxas_financeiras_pagamento = receita_prazo_valor * taxa_financeira
            
            # Depreciação mensal
            depreciacao = st.session_state.business_data.get('depreciacao_mensal', 0)
            if depreciacao == 0:
                investimento_total = st.session_state.business_data.get('investimento_total', 0)
                if investimento_total > 0:
                    depreciacao = investimento_total * 0.3 / 120  # 30% do investimento em 10 anos
            
            # Total de saídas detalhado
            saidas_total = (cmv_pagamento + impostos_pagamento + taxas_financeiras_pagamento + 
                          folha_completa + aluguel_pagamento + energia_agua + telefone_internet + 
                          contabilidade + optometrista + limpeza_seguranca + 
                          comissoes_vendas + comissoes_captador_pagamento + marketing_publicidade + material_escritorio + 
                          seguros + manutencao_equipamentos + depreciacao)
            
            # Fluxo do mês
            fluxo_mes = entradas_total - saidas_total
            saldo_final = saldo_acumulado + fluxo_mes
            
            fluxo_caixa.append({
                'mes': mes,
                'receita_mes': receita_mes,
                'saldo_inicial': saldo_acumulado,
                'entradas_vendas': entradas_vendas,
                'entradas_recebimentos': entradas_recebimentos,
                'entradas_total': entradas_total,
                'cmv_pagamento': cmv_pagamento,
                'impostos_pagamento': impostos_pagamento,
                'taxas_financeiras_pagamento': taxas_financeiras_pagamento,
                'comissoes_captador_pagamento': comissoes_captador_pagamento,
                'folha_completa': folha_completa,
                'aluguel_pagamento': aluguel_pagamento,
                'energia_agua': energia_agua,
                'telefone_internet': telefone_internet,
                'contabilidade': contabilidade,
                'optometrista': optometrista,
                'limpeza_seguranca': limpeza_seguranca,
                'comissoes_vendas': comissoes_vendas,
                'marketing_publicidade': marketing_publicidade,
                'material_escritorio': material_escritorio,
                'seguros': seguros,
                'manutencao_equipamentos': manutencao_equipamentos,
                'depreciacao': depreciacao,
                'saidas_total': saidas_total,
                'fluxo_mes': fluxo_mes,
                'saldo_final': saldo_final
            })
            
            saldo_acumulado = saldo_final
        
        # Tabela do fluxo de caixa
        st.markdown("### 📊 Fluxo de Caixa Detalhado")
        
        df_fluxo = pd.DataFrame([
            {
                'Item': 'Saldo Inicial',
                **{f'Mês {i+1}': f"R$ {fc['saldo_inicial']:,.0f}" for i, fc in enumerate(fluxo_caixa)}
            },
            {
                'Item': f'(+) Vendas à Vista ({int(st.session_state.business_data.get("percentual_avista", 70))}%)',
                **{f'Mês {i+1}': f"R$ {fc['entradas_vendas']:,.0f}" for i, fc in enumerate(fluxo_caixa)}
            },
            {
                'Item': f'(+) Recebimentos ({100 - int(st.session_state.business_data.get("percentual_avista", 70))}%)',
                **{f'Mês {i+1}': f"R$ {fc['entradas_recebimentos']:,.0f}" for i, fc in enumerate(fluxo_caixa)}
            },
            {
                'Item': '= Total Entradas',
                **{f'Mês {i+1}': f"R$ {fc['entradas_total']:,.0f}" for i, fc in enumerate(fluxo_caixa)}
            },
            {
                'Item': '(-) Pagto. Fornecedores',
                **{f'Mês {i+1}': f"R$ {fc['cmv_pagamento']:,.0f}" for i, fc in enumerate(fluxo_caixa)}
            },
            {
                'Item': '(-) Impostos',
                **{f'Mês {i+1}': f"R$ {fc['impostos_pagamento']:,.0f}" for i, fc in enumerate(fluxo_caixa)}
            },
            {
                'Item': '(-) Taxas Financeiras',
                **{f'Mês {i+1}': f"R$ {fc['taxas_financeiras_pagamento']:,.0f}" for i, fc in enumerate(fluxo_caixa)}
            },
            {
                'Item': '(-) Folha de Pagamento',
                **{f'Mês {i+1}': f"R$ {fc['folha_completa']:,.0f}" for i, fc in enumerate(fluxo_caixa)}
            },
            {
                'Item': '(-) Aluguel',
                **{f'Mês {i+1}': f"R$ {fc['aluguel_pagamento']:,.0f}" for i, fc in enumerate(fluxo_caixa)}
            },
            {
                'Item': '(-) Energia/Água',
                **{f'Mês {i+1}': f"R$ {fc['energia_agua']:,.0f}" for i, fc in enumerate(fluxo_caixa)}
            },
            {
                'Item': '(-) Telefone/Internet',
                **{f'Mês {i+1}': f"R$ {fc['telefone_internet']:,.0f}" for i, fc in enumerate(fluxo_caixa)}
            },
            {
                'Item': '(-) Contabilidade',
                **{f'Mês {i+1}': f"R$ {fc['contabilidade']:,.0f}" for i, fc in enumerate(fluxo_caixa)}
            },
            {
                'Item': '(-) Optometrista',
                **{f'Mês {i+1}': f"R$ {fc['optometrista']:,.0f}" for i, fc in enumerate(fluxo_caixa)}
            },
            {
                'Item': '(-) Limpeza/Segurança',
                **{f'Mês {i+1}': f"R$ {fc['limpeza_seguranca']:,.0f}" for i, fc in enumerate(fluxo_caixa)}
            },
            {
                'Item': '(-) Comissões',
                **{f'Mês {i+1}': f"R$ {fc['comissoes_vendas']:,.0f}" for i, fc in enumerate(fluxo_caixa)}
            },
            {
                'Item': '(-) Comissões Captador',
                **{f'Mês {i+1}': f"R$ {fc['comissoes_captador_pagamento']:,.0f}" for i, fc in enumerate(fluxo_caixa)}
            },
            {
                'Item': '(-) Marketing',
                **{f'Mês {i+1}': f"R$ {fc['marketing_publicidade']:,.0f}" for i, fc in enumerate(fluxo_caixa)}
            },
            {
                'Item': '(-) Material Escritório',
                **{f'Mês {i+1}': f"R$ {fc['material_escritorio']:,.0f}" for i, fc in enumerate(fluxo_caixa)}
            },
            {
                'Item': '(-) Seguros',
                **{f'Mês {i+1}': f"R$ {fc['seguros']:,.0f}" for i, fc in enumerate(fluxo_caixa)}
            },
            {
                'Item': '(-) Manutenção',
                **{f'Mês {i+1}': f"R$ {fc['manutencao_equipamentos']:,.0f}" for i, fc in enumerate(fluxo_caixa)}
            },
            {
                'Item': '(-) Depreciação',
                **{f'Mês {i+1}': f"R$ {fc['depreciacao']:,.0f}" for i, fc in enumerate(fluxo_caixa)}
            },
            {
                'Item': '= Total Saídas',
                **{f'Mês {i+1}': f"R$ {fc['saidas_total']:,.0f}" for i, fc in enumerate(fluxo_caixa)}
            },
            {
                'Item': '= Fluxo do Mês',
                **{f'Mês {i+1}': f"R$ {fc['fluxo_mes']:,.0f}" for i, fc in enumerate(fluxo_caixa)}
            },
            {
                'Item': '= SALDO FINAL',
                **{f'Mês {i+1}': f"R$ {fc['saldo_final']:,.0f}" for i, fc in enumerate(fluxo_caixa)}
            }
        ])
        
        st.dataframe(df_fluxo, use_container_width=True)
        
        # Auditoria detalhada linha por linha
        st.markdown("### 🔍 Auditoria Detalhada - Fluxo de Caixa")
        st.markdown("*Clique em cada item para ver fórmulas, origem dos dados e memória de cálculo*")
        
        item_fluxo = st.selectbox(
            "Selecione um item para auditoria:",
            ["Saldo Inicial", "Vendas à Vista", "Recebimentos", "Pagamento Fornecedores", "Impostos", 
             "Taxas Financeiras", "Folha de Pagamento", "Aluguel", "Energia/Água", "Telefone/Internet", "Contabilidade",
             "Optometrista", "Limpeza/Segurança", "Comissões", "Marketing", "Material Escritório",
             "Seguros", "Manutenção", "Depreciação"]
        )
        
        if item_fluxo == "Saldo Inicial":
            st.markdown("**📊 AUDITORIA: Saldo Inicial (Capital de Giro)**")
            st.markdown("---")
            st.markdown("**🔢 Fórmula:**")
            st.code("Capital de Giro = Custos Fixos Mensais × 2,5 meses")
            st.markdown("**📍 Origem dos Dados:**")
            st.write(f"• Valor configurado: R$ {capital_giro_default:,.2f}")
            st.write("• Base: Custos operacionais estimados")
            st.write("• Multiplicador: 2,5 meses (padrão mercado)")
            st.markdown("**🎯 Memória de Cálculo:**")
            st.write("• Representa reserva para primeiros meses de operação")
            st.write("• Garante pagamento de fornecedores antes recebimento")
            st.write("• Cobre variações sazonais de faturamento")
            st.write("• Buffer de segurança para imprevistos")
            
        elif item_fluxo == "Vendas à Vista":
            percentual_config = st.session_state.business_data.get('percentual_avista', 70)
            st.markdown("**📊 AUDITORIA: Vendas à Vista**")
            st.markdown("---")
            st.markdown("**🔢 Fórmula:**")
            st.code(f"Vendas à Vista = Receita Mensal × {percentual_config}%")
            st.markdown("**📍 Origem dos Dados:**")
            st.write(f"• Percentual configurado: {percentual_config}% (Etapa 5 - Produtos e Serviços)")
            st.write("• Base de cálculo: Receita bruta mensal")
            st.write("• Formas de pagamento à vista: Dinheiro, PIX, Débito")
            st.markdown("**🎯 Memória de Cálculo:**")
            exemplo_mes1 = vendas_mes_1 * (percentual_config / 100)
            st.write(f"• Exemplo Mês 1: R$ {vendas_mes_1:,.2f} × {percentual_config}% = R$ {exemplo_mes1:,.2f}")
            st.write("• Recebimento: No mesmo mês da venda")
            st.write("• Impacto no fluxo: Positivo imediato")
        
        elif item_fluxo == "Recebimentos":
            percentual_config = st.session_state.business_data.get('percentual_avista', 70)
            percentual_prazo = 100 - percentual_config
            prazo_config = st.session_state.business_data.get('prazo_medio_recebimento', 30)
            
            # Usar taxas do Mercado Pago configuradas na Etapa 5
            usar_customizada = st.session_state.business_data.get('usar_taxa_customizada', False)
            if usar_customizada:
                taxa_financeira = st.session_state.business_data.get('taxa_customizada', 4.3)
                modalidade = "Customizada"
            else:
                taxa_mp = st.session_state.business_data.get('taxa_mercado_pago', 4.3)
                opcao_mp = st.session_state.business_data.get('opcao_recebimento_mp', 'Crédito à vista - 14 dias (3,79%)')
                taxa_financeira = taxa_mp
                if "PIX" in opcao_mp:
                    modalidade = "PIX"
                elif "Débito" in opcao_mp:
                    modalidade = "Débito"
                elif "Na hora" in opcao_mp:
                    modalidade = "Crédito na hora"
                elif "14 dias" in opcao_mp:
                    modalidade = "Crédito 14 dias"
                elif "30 dias" in opcao_mp:
                    modalidade = "Crédito 30 dias"
                else:
                    modalidade = "Crédito"
            
            st.markdown("**📊 AUDITORIA: Recebimentos a Prazo**")
            st.markdown("---")
            st.markdown("**🔢 Fórmula:**")
            st.code(f"Recebimentos = (Receita × {percentual_prazo}%) × (100% - {taxa_financeira}%)")
            st.markdown("**📍 Origem dos Dados:**")
            st.write(f"• Percentual a prazo: {percentual_prazo}% (Etapa 5 - Produtos e Serviços)")
            st.write(f"• Prazo médio: {prazo_config} dias")
            st.write(f"• Modalidade: {modalidade}")
            st.write(f"• Taxa da financeira: {taxa_financeira}%")
            st.markdown("**🎯 Memória de Cálculo:**")
            st.markdown("**Exemplo prático:**")
            st.write(f"• Cliente compra óculos de R$ 500 parcelado em 3x")
            st.write(f"• Valor bruto a prazo: R$ 500 × {percentual_prazo}% = R$ {500 * (percentual_prazo / 100):,.2f}")
            
            if taxa_financeira > 0:
                valor_liquido = 500 * (percentual_prazo / 100) * (1 - taxa_financeira / 100)
                st.write(f"• Taxa da financeira: R$ {500 * (percentual_prazo / 100):,.2f} × {taxa_financeira}% = R$ {500 * (percentual_prazo / 100) * (taxa_financeira / 100):,.2f}")
                st.write(f"• **Valor líquido recebido: R$ {valor_liquido:,.2f}**")
                st.write(f"• Prazo de recebimento: {prazo_config} dias")
            else:
                st.write(f"• **Valor recebido: R$ {500 * (percentual_prazo / 100):,.2f}** (sem taxa)")
                st.write("• Risco: Inadimplência assumida pela ótica")
            
            st.markdown("**💡 Entendimento:**")
            st.write("• Cliente pode parcelar em quantas vezes quiser")
            st.write("• Seu recebimento depende do contrato com a financeira")
            st.write(f"• {modalidade}: melhor fluxo de caixa vs menor taxa")
        
        elif item_fluxo == "Pagamento Fornecedores":
            st.markdown("**📊 AUDITORIA: Pagamento a Fornecedores (CMV)**")
            st.markdown("---")
            st.markdown("**🔢 Fórmula:**")
            st.code(f"CMV = Custos Reais dos Produtos ou {cmv_percentual}% da Receita")
            st.markdown("**📍 Origem dos Dados:**")
            custo_lentes_real = st.session_state.business_data.get('custo_lentes_total', 0)
            custo_armacoes_real = st.session_state.business_data.get('custo_armacoes_total', 0)
            custo_servicos_real = st.session_state.business_data.get('custo_servicos_total', 0)
            cmv_real_total = custo_lentes_real + custo_armacoes_real + custo_servicos_real
            
            if cmv_real_total > 0:
                st.write(f"• Custos reais da precificação: R$ {cmv_real_total:,.2f}")
                st.write(f"  - Lentes: R$ {custo_lentes_real:,.2f}")
                st.write(f"  - Armações: R$ {custo_armacoes_real:,.2f}")
                st.write(f"  - Serviços: R$ {custo_servicos_real:,.2f}")
            else:
                st.write(f"• Percentual estimado: {cmv_percentual}% da receita")
                st.write("• Configure produtos na Etapa 5 para custos reais")
            
            st.write("• Fornecedores: ATAK, Brasil Lentes, GOLD, DSMHD")
            st.markdown("**🎯 Memória de Cálculo:**")
            if cmv_real_total > 0:
                exemplo_cmv = cmv_real_total
                st.write(f"• Valor fixo mensal: R$ {exemplo_cmv:,.2f}")
            else:
                exemplo_cmv = vendas_mes_1 * (cmv_percentual / 100)
                st.write(f"• Exemplo Mês 1: R$ {vendas_mes_1:,.2f} × {cmv_percentual}% = R$ {exemplo_cmv:,.2f}")
            st.write("• Prazo pagamento: Conforme negociado com fornecedores")
            st.write("• Impacto: Maior custo do negócio após impostos")
        
        elif item_fluxo == "Impostos":
            regime = st.session_state.business_data.get('regime_tributario', 'Simples Nacional')
            st.markdown("**📊 AUDITORIA: Impostos**")
            st.markdown("---")
            st.markdown("**🔢 Fórmula:**")
            st.code(f"Impostos = Receita Mensal × {impostos_percentual}%")
            st.markdown("**📍 Origem dos Dados:**")
            st.write(f"• Regime tributário: {regime}")
            st.write(f"• Alíquota aplicada: {impostos_percentual}% (legislação brasileira)")
            if regime == "Simples Nacional":
                st.write("• Anexo I - Comércio (óticas)")
                st.write("• Impostos unificados: IRPJ, CSLL, PIS, COFINS, ICMS, CPP, ISS")
            st.markdown("**🎯 Memória de Cálculo:**")
            exemplo_imposto = vendas_mes_1 * (impostos_percentual / 100)
            st.write(f"• Exemplo Mês 1: R$ {vendas_mes_1:,.2f} × {impostos_percentual}% = R$ {exemplo_imposto:,.2f}")
            st.write("• Pagamento: DAS mensal até dia 20")
            st.write("• Base legal: Lei Complementar 123/2006 (Simples Nacional)")
            st.write("• Impacto: Obrigação fiscal automática sobre faturamento")
        
        elif item_fluxo == "Taxas Financeiras":
            st.markdown("**📊 AUDITORIA: Taxas Financeiras**")
            st.markdown("---")
            st.markdown("**🔢 Fórmula:**")
            st.code("Taxas = Receita × % Vendas a Prazo × Taxa da Financeira")
            st.markdown("**📍 Origem dos Dados:**")
            
            usar_customizada = st.session_state.business_data.get('usar_taxa_customizada', False)
            percentual_avista = st.session_state.business_data.get('percentual_avista', 70)
            percentual_prazo = 100 - percentual_avista
            
            if usar_customizada:
                taxa_config = st.session_state.business_data.get('taxa_customizada', 4.3)
                st.write(f"• Taxa customizada: {taxa_config}%")
                st.write("• Fonte: Configuração manual (Etapa 5)")
            else:
                taxa_config = st.session_state.business_data.get('taxa_mercado_pago', 4.3)
                opcao_mp = st.session_state.business_data.get('opcao_recebimento_mp', 'Crédito à vista - 14 dias (3,79%)')
                st.write(f"• Taxa Mercado Pago: {taxa_config}%")
                st.write(f"• Modalidade: {opcao_mp}")
                st.write("• Fonte: Configuração Etapa 5 - Produtos e Serviços")
            
            st.write(f"• Vendas à vista: {percentual_avista}% (taxa 0%)")
            st.write(f"• Vendas a prazo: {percentual_prazo}% (com taxa)")
            
            st.markdown("**🎯 Memória de Cálculo:**")
            exemplo_receita = vendas_mes_1
            exemplo_prazo = exemplo_receita * (percentual_prazo / 100)
            exemplo_taxa = exemplo_prazo * (taxa_config / 100)
            
            st.write(f"• Exemplo Mês 1:")
            st.write(f"  - Receita total: R$ {exemplo_receita:,.2f}")
            st.write(f"  - Vendas a prazo ({percentual_prazo}%): R$ {exemplo_prazo:,.2f}")
            st.write(f"  - Taxa financeira ({taxa_config}%): R$ {exemplo_taxa:,.2f}")
            st.write(f"• **Custo mensal das taxas: R$ {exemplo_taxa:,.2f}**")
            
            st.markdown("**💡 Entendimento:**")
            st.write("• Custo das vendas parceladas e cartão de crédito")
            st.write("• Reduz o valor líquido recebido das vendas a prazo")
            st.write("• Impacto direto no fluxo de caixa e margem")
        
        elif item_fluxo == "Folha de Pagamento":
            st.markdown("**📊 AUDITORIA: Folha de Pagamento**")
            st.markdown("---")
            st.markdown("**🔢 Fórmula:**")
            st.code("Folha Total = Σ(Salário Base × Encargos por Tipo)")
            st.markdown("**📍 Origem dos Dados:**")
            if hasattr(st.session_state, 'funcionarios') and st.session_state.funcionarios:
                st.write(f"• Funcionários cadastrados: {len(st.session_state.funcionarios)}")
                st.write("• Fonte: DP e Tributação (sistema integrado)")
                custo_total_folha = 0
                clt_count = 0
                terceirizado_count = 0
                for func in st.session_state.funcionarios:
                    if func['tipo_contrato'] == 'CLT':
                        custo_func = func['salario_base'] * 1.68
                        clt_count += 1
                    else:
                        custo_func = func['salario_base']
                        terceirizado_count += 1
                    custo_total_folha += custo_func
                st.markdown("**🎯 Memória de Cálculo:**")
                st.write(f"• Funcionários CLT: {clt_count} (com encargos 68%)")
                st.write(f"• Terceirizados/MEI: {terceirizado_count} (sem encargos)")
                for func in st.session_state.funcionarios:
                    if func['tipo_contrato'] == 'CLT':
                        custo_func = func['salario_base'] * 1.68
                        st.write(f"  - {func['nome']} ({func['cargo']}) CLT: R$ {func['salario_base']:,.2f} × 1.68 = R$ {custo_func:,.2f}")
                    else:
                        st.write(f"  - {func['nome']} ({func['cargo']}) {func['tipo_contrato']}: R$ {func['salario_base']:,.2f}")
                st.write(f"• **Total mensal: R$ {custo_total_folha:,.2f}**")
            else:
                st.write(f"• Folha CLT estimada: R$ {salarios_clt:,.2f}")
                st.write(f"• Serviços terceirizados: R$ {total_optometrista:,.2f}")
                st.write("• Configure funcionários no DP para cálculo detalhado")
                st.markdown("**🎯 Memória de Cálculo:**")
                st.write("• Encargos CLT incluem: INSS, FGTS, 13º, férias, rescisão")
                st.write("• Base legal: CLT e legislação trabalhista brasileira")
        
        elif item_fluxo == "Aluguel":
            aluguel_valor = st.session_state.business_data.get('aluguel_mensal', 0)
            st.markdown("**📊 AUDITORIA: Aluguel**")
            st.markdown("---")
            st.markdown("**🔢 Fórmula:**")
            st.code("Aluguel = Valor Fixo Mensal")
            st.markdown("**📍 Origem dos Dados:**")
            st.write(f"• Valor configurado: R$ {aluguel_valor:,.2f}")
            st.write("• Fonte: Etapa 9 - Investimento Inicial")
            st.write("• Tipo: Custo fixo mensal")
            st.markdown("**🎯 Memória de Cálculo:**")
            st.write("• Valor exato configurado pelo usuário")
            st.write("• Pago mensalmente, independente do faturamento")
            st.write("• Representa maior custo fixo da operação")
            if aluguel_valor == 0:
                st.warning("• Valor zerado - verifique se é propriedade própria")
        
        elif item_fluxo == "Energia/Água":
            energia_agua_valor = st.session_state.business_data.get('energia_agua', 0)
            st.markdown("**📊 AUDITORIA: Energia/Água**")
            st.markdown("---")
            st.markdown("**🔢 Fórmula:**")
            st.code("Energia/Água = Valor Fixo + Variável")
            st.markdown("**📍 Origem dos Dados:**")
            st.write(f"• Valor configurado: R$ {energia_agua_valor:,.2f}")
            st.write("• Tipo: Custo semi-variável")
            st.markdown("**🎯 Memória de Cálculo:**")
            st.write("• Inclui: Energia elétrica + Água + Esgoto")
            st.write("• Componentes: Taxa fixa + consumo variável")
            st.write("• Estimativa baseada no funcionamento da ótica")
            if energia_agua_valor == 0:
                st.warning("• Valor zerado - verifique configuração")
        
        elif item_fluxo == "Telefone/Internet":
            telefone_internet_valor = st.session_state.business_data.get('telefone_internet', 0)
            st.markdown("**📊 AUDITORIA: Telefone/Internet**")
            st.markdown("---")
            st.markdown("**🔢 Fórmula:**")
            st.code("Telefone/Internet = Planos Fixos Mensais")
            st.markdown("**📍 Origem dos Dados:**")
            st.write(f"• Valor configurado: R$ {telefone_internet_valor:,.2f}")
            st.write("• Tipo: Custo fixo operacional")
            st.markdown("**🎯 Memória de Cálculo:**")
            st.write("• Inclui: Internet banda larga + telefone fixo/móvel")
            st.write("• Essencial para: Sistema de vendas, comunicação")
            st.write("• Valor mensal fixo contratual")
            if telefone_internet_valor == 0:
                st.warning("• Valor zerado - verifique configuração")
        
        elif item_fluxo == "Contabilidade":
            contabilidade_valor = st.session_state.business_data.get('contabilidade', 0)
            st.markdown("**📊 AUDITORIA: Contabilidade**")
            st.markdown("---")
            st.markdown("**🔢 Fórmula:**")
            st.code("Contabilidade = Honorários Mensais")
            st.markdown("**📍 Origem dos Dados:**")
            st.write(f"• Valor configurado: R$ {contabilidade_valor:,.2f}")
            st.write("• Tipo: Serviço profissional obrigatório")
            st.markdown("**🎯 Memória de Cálculo:**")
            st.write("• Serviços: Escrituração contábil, impostos, folha")
            st.write("• Obrigatoriedade: Pessoa jurídica")
            st.write("• Frequência: Mensal")
            if contabilidade_valor == 0:
                st.warning("• Valor zerado - contabilidade é obrigatória para PJ")
        
        elif item_fluxo == "Optometrista":
            optometrista_valor = st.session_state.business_data.get('custo_optometrista_mensal', 0)
            st.markdown("**📊 AUDITORIA: Optometrista**")
            st.markdown("---")
            st.markdown("**🔢 Fórmula:**")
            st.code("Optometrista = Diária × Dias no Mês")
            st.markdown("**📍 Origem dos Dados:**")
            st.write(f"• Valor mensal: R$ {optometrista_valor:,.2f}")
            st.write("• Fonte: Serviços Profissionais por Diária")
            st.write("• Tipo: Prestador de serviços")
            st.markdown("**🎯 Memória de Cálculo:**")
            diaria = st.session_state.business_data.get('diaria_optometrista', 150)
            dias = st.session_state.business_data.get('dias_optometrista_mes', 4)
            st.write(f"• Diária: R$ {diaria:,.2f}")
            st.write(f"• Dias/mês: {dias}")
            st.write(f"• Total: R$ {diaria:,.2f} × {dias} = R$ {optometrista_valor:,.2f}")
            st.write("• Serviços: Exames de vista, prescrições")
            if optometrista_valor == 0:
                st.info("• Opcional - para ótica com exames completos")
        
        elif item_fluxo == "Limpeza/Segurança":
            limpeza_valor = st.session_state.business_data.get('limpeza_seguranca', 0)
            st.markdown("**📊 AUDITORIA: Limpeza/Segurança**")
            st.markdown("---")
            st.markdown("**🔢 Fórmula:**")
            st.code("Limpeza/Segurança = Serviços Terceirizados")
            st.markdown("**📍 Origem dos Dados:**")
            st.write(f"• Valor configurado: R$ {limpeza_valor:,.2f}")
            st.write("• Tipo: Serviço terceirizado")
            st.markdown("**🎯 Memória de Cálculo:**")
            st.write("• Inclui: Limpeza diária + monitoramento")
            st.write("• Frequência: Diária para limpeza")
            st.write("• Valor mensal fixo contratual")
            if limpeza_valor == 0:
                st.info("• Opcional - pode ser feito pelo próprio proprietário")
        
        elif item_fluxo == "Comissões":
            comissoes_percent = st.session_state.business_data.get('comissoes_percentual', 3)
            st.markdown("**📊 AUDITORIA: Comissões de Vendas**")
            st.markdown("---")
            st.markdown("**🔢 Fórmula:**")
            st.code(f"Comissões = Receita Mensal × {comissoes_percent}%")
            st.markdown("**📍 Origem dos Dados:**")
            st.write(f"• Percentual: {comissoes_percent}% sobre vendas")
            st.write("• Tipo: Custo variável sobre faturamento")
            st.markdown("**🎯 Memória de Cálculo:**")
            exemplo_comissao = vendas_mes_1 * (comissoes_percent / 100)
            st.write(f"• Exemplo Mês 1: R$ {vendas_mes_1:,.2f} × {comissoes_percent}% = R$ {exemplo_comissao:,.2f}")
            st.write("• Base: Faturamento bruto mensal")
            st.write("• Pagamento: Mensal conforme vendas realizadas")
        
        elif item_fluxo == "Marketing":
            marketing_valor = st.session_state.business_data.get('marketing_publicidade', 0)
            st.markdown("**📊 AUDITORIA: Marketing/Publicidade**")
            st.markdown("---")
            st.markdown("**🔢 Fórmula:**")
            st.code("Marketing = Investimento Mensal Fixo")
            st.markdown("**📍 Origem dos Dados:**")
            st.write(f"• Valor configurado: R$ {marketing_valor:,.2f}")
            st.write("• Tipo: Investimento em divulgação")
            st.markdown("**🎯 Memória de Cálculo:**")
            st.write("• Inclui: Publicidade online, impressos, promocões")
            st.write("• Estratégia: Atrair e reter clientes")
            st.write("• Valor mensal planejado")
            if marketing_valor == 0:
                st.warning("• Marketing é essencial para crescimento do negócio")
        
        elif item_fluxo == "Material Escritório":
            material_valor = st.session_state.business_data.get('material_escritorio', 0)
            st.markdown("**📊 AUDITORIA: Material de Escritório**")
            st.markdown("---")
            st.markdown("**🔢 Fórmula:**")
            st.code("Material Escritório = Consumo Mensal")
            st.markdown("**📍 Origem dos Dados:**")
            st.write(f"• Valor configurado: R$ {material_valor:,.2f}")
            st.write("• Tipo: Custo operacional variável")
            st.markdown("**🎯 Memória de Cálculo:**")
            st.write("• Inclui: Papel, canetas, formulários, impressões")
            st.write("• Consumo: Conforme operação da ótica")
            if material_valor == 0:
                st.info("• Valor baixo mas necessário para operação")
        
        elif item_fluxo == "Seguros":
            seguros_valor = st.session_state.business_data.get('seguros', 0)
            st.markdown("**📊 AUDITORIA: Seguros**")
            st.markdown("---")
            st.markdown("**🔢 Fórmula:**")
            st.code("Seguros = Prêmios Mensais")
            st.markdown("**📍 Origem dos Dados:**")
            st.write(f"• Valor configurado: R$ {seguros_valor:,.2f}")
            st.write("• Tipo: Proteção patrimonial")
            st.markdown("**🎯 Memória de Cálculo:**")
            st.write("• Inclui: Seguro contra incêndio, roubo, responsabilidade civil")
            st.write("• Proteção: Estoque, equipamentos, estabelecimento")
            if seguros_valor == 0:
                st.warning("• Seguros são importantes para proteção do negócio")
        
        elif item_fluxo == "Manutenção":
            manutencao_valor = st.session_state.business_data.get('manutencao_equipamentos', 0)
            st.markdown("**📊 AUDITORIA: Manutenção de Equipamentos**")
            st.markdown("---")
            st.markdown("**🔢 Fórmula:**")
            st.code("Manutenção = Custos Preventivos + Corretivos")
            st.markdown("**📍 Origem dos Dados:**")
            st.write(f"• Valor configurado: R$ {manutencao_valor:,.2f}")
            st.write("• Tipo: Conservação de ativos")
            st.markdown("**🎯 Memória de Cálculo:**")
            st.write("• Inclui: Equipamentos óticos, sistema, mobiliário")
            st.write("• Frequência: Preventiva + corretiva conforme necessário")
            if manutencao_valor == 0:
                st.info("• Importante para manter equipamentos funcionando")
        
        elif item_fluxo == "Depreciação":
            depreciacao_valor = st.session_state.business_data.get('depreciacao_mensal', 0)
            investimento_total = st.session_state.business_data.get('investimento_total', 0)
            st.markdown("**📊 AUDITORIA: Depreciação**")
            st.markdown("---")
            st.markdown("**🔢 Fórmula:**")
            st.code("Depreciação = (Investimento × 30%) ÷ 120 meses")
            st.markdown("**📍 Origem dos Dados:**")
            if depreciacao_valor == 0 and investimento_total > 0:
                depreciacao_calc = investimento_total * 0.3 / 120
                st.write(f"• Investimento total: R$ {investimento_total:,.2f}")
                st.write(f"• Depreciação calculada: R$ {depreciacao_calc:,.2f}/mês")
            else:
                st.write(f"• Valor configurado: R$ {depreciacao_valor:,.2f}")
            st.write("• Base: 30% do investimento em 10 anos")
            st.markdown("**🎯 Memória de Cálculo:**")
            st.write("• Representa desgaste dos equipamentos ao longo do tempo")
            st.write("• Contabilização do custo dos ativos fixos")
            st.write("• Método linear: valor igual todos os meses")
    
    # Store financial projections for other steps
    st.session_state.business_data.update({
        'vendas_mes_1': vendas_mes_1,
        'crescimento_mensal': crescimento_mensal,
        'cmv_percentual': cmv_percentual,
        'impostos_percentual': impostos_percentual,
        'comissoes_percentual': comissoes_percentual,
        'aluguel': aluguel_mensal,
        'salarios_clt': salarios_clt,
        'total_optometrista': total_optometrista,
        'salarios_total': salarios_clt + total_optometrista
    })
    save_user_data()
    
    # Navigation
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("⬅️ Etapa Anterior", key="prev_step10"):
            st.session_state.step = 9
            st.rerun()
    with col3:
        if st.button("Próxima Etapa ➡️", type="primary", key="next_step10"):
            st.session_state.step = 11
            st.rerun()

def show_step_11():
    """Etapa 11: Análise de Viabilidade"""
    st.header("1️⃣1️⃣ Análise de Viabilidade")
    st.markdown("**FASE 11: VIABILIDADE** - Análise matemática da viabilidade do negócio")
    
    # Recuperar dados das etapas anteriores
    investimento_total = st.session_state.business_data.get('investimento_total', 81500)
    receita_anual = st.session_state.business_data.get('receita_anual', 180000)
    lucro_operacional = st.session_state.business_data.get('lucro_operacional', 25000)
    ebitda = st.session_state.business_data.get('ebitda', 26350)
    margem_contribuicao_perc = st.session_state.business_data.get('margem_contribuicao_perc', 44.0)
    
    tab1, tab2, tab3 = st.tabs(["📊 Indicadores Chave", "💹 Análise de Sensibilidade", "🎯 Cenários"])
    
    with tab1:
        st.subheader("📊 Indicadores de Viabilidade")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Rentabilidade**")
            
            # ROI
            roi = (lucro_operacional / investimento_total) * 100 if investimento_total > 0 else 0
            st.metric("ROI Anual", f"{roi:.1f}%", 
                     delta="Acima de 20% = Excelente" if roi > 20 else "Abaixo de 15% = Atenção")
            
            # Botão explicação ROI
            if st.button("📖 De onde vem esse ROI?", key="explain_roi"):
                resultado = 'Excelente retorno!' if roi > 20 else 'Considere otimizar para melhorar o retorno.' if roi < 15 else 'Retorno adequado.'
                
                st.success(f"""
                💰 **ROI de {roi:.1f}% ao ano**
                
                **Fórmula:** (Lucro Operacional ÷ Investimento Total) × 100
                
                **Seus Números:**
                • Lucro Operacional: {format_currency(lucro_operacional)}
                • Investimento Total: {format_currency(investimento_total)}
                
                **Cálculo:** ({format_currency(lucro_operacional)} ÷ {format_currency(investimento_total)}) × 100 = {roi:.1f}%
                
                **Em resumo:** Para cada R$ 100 investidos, você ganha R$ {roi:.0f} por ano. {resultado}
                """)
            
            # Margem Operacional
            margem_operacional = (lucro_operacional / receita_anual) * 100 if receita_anual > 0 else 0
            st.metric("Margem Operacional", f"{margem_operacional:.1f}%",
                     delta="Acima de 10% = Boa" if margem_operacional > 10 else "Melhorar eficiência")
            
            # Botão explicação Margem Operacional
            if st.button("📖 De onde vem essa margem?", key="explain_margem"):
                resultado = 'Margem saudável!' if margem_operacional > 10 else 'Considere revisar custos para melhorar a margem.' if margem_operacional < 5 else 'Margem adequada.'
                st.info(f"""
                📈 **Margem Operacional de {margem_operacional:.1f}%**
                
                **Fórmula:** (Lucro Operacional ÷ Receita Anual) × 100
                
                **Seus Números:**
                • Lucro Operacional: {format_currency(lucro_operacional)}
                • Receita Anual: {format_currency(receita_anual)}
                
                **Cálculo:** ({format_currency(lucro_operacional)} ÷ {format_currency(receita_anual)}) × 100 = {margem_operacional:.1f}%
                
                **Em resumo:** De cada R$ 100 vendidos, sobram R$ {margem_operacional:.0f} como lucro líquido. {resultado}
                """)
            
            # EBITDA Margin
            ebitda_margin = (ebitda / receita_anual) * 100 if receita_anual > 0 else 0
            st.metric("Margem EBITDA", f"{ebitda_margin:.1f}%",
                     delta="Acima de 15% = Saudável" if ebitda_margin > 15 else "Revisar custos")
            
            # Botão explicação EBITDA
            if st.button("📖 De onde vem o EBITDA?", key="explain_ebitda"):
                resultado = 'Excelente geração de caixa!' if ebitda_margin > 15 else 'Considere otimizar a operação.' if ebitda_margin < 10 else 'Geração de caixa adequada.'
                st.info(f"""
                📊 **Margem EBITDA de {ebitda_margin:.1f}%**
                
                **O que é:** Lucro antes de Juros, Impostos, Depreciação e Amortização
                **Fórmula:** (EBITDA ÷ Receita Anual) × 100
                
                **Seus Números:**
                • EBITDA: {format_currency(ebitda)}
                • Receita Anual: {format_currency(receita_anual)}
                
                **Cálculo:** ({format_currency(ebitda)} ÷ {format_currency(receita_anual)}) × 100 = {ebitda_margin:.1f}%
                
                **Em resumo:** Sua operação gera {ebitda_margin:.1f}% de caixa sobre as vendas. {resultado}
                """)
            
            # Payback
            payback = investimento_total / lucro_operacional if lucro_operacional > 0 else float('inf')
            payback_text = f"{payback:.1f} anos" if payback != float('inf') else "Indefinido"
            st.metric("Payback", payback_text,
                     delta="Menos de 4 anos = Bom" if payback < 4 else "Muito longo")
            
            # Botão explicação Payback
            if st.button("📖 De onde vem esse tempo?", key="explain_payback"):
                resultado = 'Excelente tempo de retorno!' if payback < 3 else 'Tempo aceitável.' if payback < 5 else 'Considere otimizar para acelerar o retorno.'
                st.info(f"""
                ⏱️ **Payback de {payback:.1f} anos**
                
                **Fórmula:** Investimento Total ÷ Lucro Operacional Anual
                
                **Seus Números:**
                • Investimento Total: {format_currency(investimento_total)}
                • Lucro Operacional: {format_currency(lucro_operacional)}
                
                **Cálculo:** {format_currency(investimento_total)} ÷ {format_currency(lucro_operacional)} = {payback:.1f} anos
                
                **Em resumo:** Com lucro de {format_currency(lucro_operacional)} por ano, você recupera o investimento em {payback:.1f} anos. {resultado}
                """)
        
        with col2:
            st.markdown("**Análise de Risco**")
            
            # Ponto de Equilíbrio
            ponto_equilibrio = st.session_state.business_data.get('ponto_equilibrio_valor', 100000)
            margem_seguranca = ((receita_anual - ponto_equilibrio) / receita_anual) * 100 if receita_anual > 0 else 0
            st.metric("Margem de Segurança", f"{margem_seguranca:.1f}%",
                     delta="Acima de 30% = Seguro" if margem_seguranca > 30 else "Risco elevado")
            
            # Botão explicação Margem de Segurança
            if st.button("📖 De onde vem essa margem?", key="explain_margem_seg"):
                resultado = 'Margem segura!' if margem_seguranca > 30 else 'Risco elevado - considere reduzir custos ou aumentar vendas.' if margem_seguranca < 15 else 'Margem aceitável.'
                st.warning(f"""
                🛡️ **Margem de Segurança de {margem_seguranca:.1f}%**
                
                **Fórmula:** ((Receita Atual - Ponto Equilíbrio) ÷ Receita Atual) × 100
                
                **Seus Números:**
                • Receita Anual: {format_currency(receita_anual)}
                • Ponto de Equilíbrio: {format_currency(ponto_equilibrio)}
                • Diferença: {format_currency(receita_anual - ponto_equilibrio)}
                
                **Cálculo:** (({format_currency(receita_anual)} - {format_currency(ponto_equilibrio)}) ÷ {format_currency(receita_anual)}) × 100 = {margem_seguranca:.1f}%
                
                **Em resumo:** Suas vendas podem cair {margem_seguranca:.1f}% antes de ter prejuízo. {resultado}
                """)
            
            # Grau de Alavancagem Operacional
            custos_fixos_anual = (st.session_state.business_data.get('aluguel', 0) + 
                                 st.session_state.business_data.get('salarios_clt', 2550) +
                                 st.session_state.business_data.get('total_optometrista', 5000) +
                                 st.session_state.business_data.get('outros_fixos', 500)) * 12
            
            gao = (receita_anual * (margem_contribuicao_perc/100)) / lucro_operacional if lucro_operacional > 0 else 0
            st.metric("Alavancagem Operacional", f"{gao:.1f}x",
                     delta="Menor = Menos risco" if gao < 3 else "Alto risco operacional")
            
            # Botão explicação Alavancagem Operacional
            if st.button("📖 De onde vem essa alavancagem?", key="explain_alavancagem"):
                margem_contribuicao_valor = receita_anual * (margem_contribuicao_perc/100)
                resultado = 'Baixo risco operacional.' if gao < 3 else 'Alto risco - pequenas variações nas vendas impactam muito o lucro.' if gao > 5 else 'Risco moderado.'
                st.info(f"""
                ⚖️ **Alavancagem Operacional de {gao:.1f}x**
                
                **Fórmula:** Margem de Contribuição ÷ Lucro Operacional
                
                **Seus Números:**
                • Margem de Contribuição: {format_currency(margem_contribuicao_valor)}
                • Lucro Operacional: {format_currency(lucro_operacional)}
                
                **Cálculo:** {format_currency(margem_contribuicao_valor)} ÷ {format_currency(lucro_operacional)} = {gao:.1f}x
                
                **Em resumo:** Cada 1% de aumento nas vendas gera {gao:.1f}% de aumento no lucro. {resultado}
                """)
            
            # Cobertura de Custos Fixos
            margem_contribuicao_valor = receita_anual * (margem_contribuicao_perc/100)
            cobertura_fixos = margem_contribuicao_valor / custos_fixos_anual if custos_fixos_anual > 0 else 0
            st.metric("Cobertura Custos Fixos", f"{cobertura_fixos:.1f}x",
                     delta="Acima de 2x = Seguro" if cobertura_fixos > 2 else "Margem apertada")
            
            # Botão explicação Cobertura
            if st.button("📖 De onde vem essa cobertura?", key="explain_cobertura"):
                resultado = 'Excelente cobertura!' if cobertura_fixos > 3 else 'Cobertura segura.' if cobertura_fixos > 2 else 'Margem apertada - monitore de perto.'
                st.success(f"""
                🏛️ **Cobertura de {cobertura_fixos:.1f}x dos custos fixos**
                
                **Fórmula:** Margem de Contribuição ÷ Custos Fixos Anuais
                
                **Seus Números:**
                • Margem de Contribuição: {format_currency(margem_contribuicao_valor)}
                • Custos Fixos Anuais: {format_currency(custos_fixos_anual)}
                
                **Cálculo:** {format_currency(margem_contribuicao_valor)} ÷ {format_currency(custos_fixos_anual)} = {cobertura_fixos:.1f}x
                
                **Em resumo:** Você gera {cobertura_fixos:.1f}x o dinheiro necessário para pagar custos fixos. {resultado}
                """)
            
            # VPL (assumindo taxa de desconto de 12% a.a.)
            taxa_desconto = 0.12
            fluxos_5_anos = [lucro_operacional] * 5  # Simplificado
            vpl = sum([fluxo / ((1 + taxa_desconto) ** (ano + 1)) for ano, fluxo in enumerate(fluxos_5_anos)]) - investimento_total
            st.metric("VPL (5 anos)", format_currency(vpl),
                     delta="Positivo = Viável" if vpl > 0 else "Inviável")
            
            # Botão explicação VPL
            if st.button("📖 De onde vem esse VPL?", key="explain_vpl"):
                if vpl > 0:
                    st.success(f"""
                    💰 **VPL de {format_currency(vpl)} em 5 anos**
                    
                    **O que é:** Valor Presente Líquido - quanto vale hoje o dinheiro futuro
                    **Fórmula:** Soma dos lucros futuros descontados - Investimento inicial
                    
                    **Seus Números:**
                    • Lucro anual: {format_currency(lucro_operacional)}
                    • Taxa de desconto: {taxa_desconto:.0%}
                    • Investimento inicial: {format_currency(investimento_total)}
                    
                    **Cálculo:**
                    Valor presente dos lucros: {format_currency(vpl + investimento_total)}
                    Menos investimento: {format_currency(investimento_total)}
                    VPL = {format_currency(vpl)}
                    
                    **Em resumo:** Este negócio vale a pena - você ganha mais que investimentos seguros.
                    """)
                else:
                    st.error(f"""
                    📉 **VPL de {format_currency(vpl)} em 5 anos**
                    
                    **O que é:** Valor Presente Líquido - quanto vale hoje o dinheiro futuro
                    **Fórmula:** Soma dos lucros futuros descontados - Investimento inicial
                    
                    **Seus Números:**
                    • Lucro anual: {format_currency(lucro_operacional)}
                    • Taxa de desconto: {taxa_desconto:.0%}
                    • Investimento inicial: {format_currency(investimento_total)}
                    
                    **Cálculo:**
                    Valor presente dos lucros: {format_currency(vpl + investimento_total)}
                    Menos investimento: {format_currency(investimento_total)}
                    VPL = {format_currency(vpl)}
                    
                    **Em resumo:** Este negócio não compensa - você ganharia mais em outros investimentos.
                    """)
    
    with tab2:
        st.subheader("💹 Análise de Sensibilidade")
        
        st.markdown("**Impacto de Variações na Receita**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Variações na receita
            variacoes = [-30, -20, -10, 0, 10, 20, 30]
            resultados = []
            
            for var in variacoes:
                receita_ajustada = receita_anual * (1 + var/100)
                custos_variaveis_valor = receita_ajustada * (56/100)  # Assumindo 56% de custos variáveis
                margem_contribuicao = receita_ajustada - custos_variaveis_valor
                lucro_ajustado = margem_contribuicao - custos_fixos_anual - (investimento_total * 0.05)
                roi_ajustado = (lucro_ajustado / investimento_total) * 100 if investimento_total > 0 else 0
                resultados.append((var, receita_ajustada, lucro_ajustado, roi_ajustado))
            
            for var, receita, lucro, roi_calc in resultados:
                if var == 0:
                    st.markdown(f"**Base (0%): ROI {roi_calc:.1f}%**")
                else:
                    cor = "🟢" if var > 0 else "🔴"
                    st.write(f"{cor} {var:+d}%: ROI {roi_calc:.1f}%")
        
        with col2:
            st.markdown("**Análise Break-Even**")
            
            # Cálculo de quantas vendas precisa para break-even
            ticket_medio = st.session_state.business_data.get('ticket_medio', 250)
            vendas_break_even = ponto_equilibrio / ticket_medio if ticket_medio > 0 else 0
            vendas_por_dia = vendas_break_even / 365 if vendas_break_even > 0 else 0
            
            st.metric("Vendas/mês Break-Even", f"{vendas_break_even/12:.0f}")
            st.metric("Vendas/dia Break-Even", f"{vendas_por_dia:.1f}")
            st.metric("Receita Break-Even", format_currency(ponto_equilibrio))
            
            # Capacidade atual vs necessária
            capacidade_atendimento = st.session_state.business_data.get('capacidade_atendimento', 20)
            utilizacao_necessaria = (vendas_por_dia / capacidade_atendimento) * 100 if capacidade_atendimento > 0 else 0
            st.metric("Utilização Necessária", f"{utilizacao_necessaria:.1f}%",
                     delta="Viável" if utilizacao_necessaria < 80 else "Capacidade insuficiente")
    
    with tab3:
        st.subheader("🎯 Análise de Cenários")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**CENÁRIO PESSIMISTA**")
            st.caption("Receita -20%, Custos +10%")
            
            receita_pess = receita_anual * 0.8
            custos_fixos_pess = custos_fixos_anual * 1.1
            custos_var_pess = receita_pess * 0.61  # 61% ao invés de 56%
            lucro_pess = receita_pess - custos_var_pess - custos_fixos_pess - (investimento_total * 0.05)
            roi_pess = (lucro_pess / investimento_total) * 100 if investimento_total > 0 else 0
            
            st.metric("Receita", format_currency(receita_pess))
            st.metric("Lucro", format_currency(lucro_pess))
            st.metric("ROI", f"{roi_pess:.1f}%")
            
            if lucro_pess > 0:
                st.success("Ainda lucrativo")
            else:
                st.error("Prejuízo")
        
        with col2:
            st.markdown("**CENÁRIO REALISTA**")
            st.caption("Valores atuais")
            
            st.metric("Receita", format_currency(receita_anual))
            st.metric("Lucro", format_currency(lucro_operacional))
            st.metric("ROI", f"{roi:.1f}%")
            
            if roi > 15:
                st.success("Viável")
            elif roi > 10:
                st.warning("Marginal")
            else:
                st.error("Inviável")
        
        with col3:
            st.markdown("**CENÁRIO OTIMISTA**")
            st.caption("Receita +30%, Custos otimizados")
            
            receita_otim = receita_anual * 1.3
            custos_fixos_otim = custos_fixos_anual * 1.05  # Pequeno aumento
            custos_var_otim = receita_otim * 0.52  # Melhor eficiência
            lucro_otim = receita_otim - custos_var_otim - custos_fixos_otim - (investimento_total * 0.05)
            roi_otim = (lucro_otim / investimento_total) * 100 if investimento_total > 0 else 0
            
            st.metric("Receita", format_currency(receita_otim))
            st.metric("Lucro", format_currency(lucro_otim))
            st.metric("ROI", f"{roi_otim:.1f}%")
            
            if roi_otim > 25:
                st.success("Excelente retorno")
            else:
                st.info("Bom potencial")
        
        st.markdown("---")
        
        # Recomendação final baseada nos cálculos
        st.subheader("🎯 Recomendação de Viabilidade")
        
        score_viabilidade = 0
        if roi > 15: score_viabilidade += 2
        elif roi > 10: score_viabilidade += 1
        
        if margem_seguranca > 25: score_viabilidade += 2
        elif margem_seguranca > 15: score_viabilidade += 1
        
        if payback < 3: score_viabilidade += 2
        elif payback < 5: score_viabilidade += 1
        
        if vpl > 0: score_viabilidade += 2
        
        if lucro_pess > 0: score_viabilidade += 1  # Resistente ao cenário pessimista
        
        # Exibir recomendação
        if score_viabilidade >= 7:
            st.success("🟢 **ALTAMENTE VIÁVEL** - Negócio com forte potencial de retorno")
        elif score_viabilidade >= 5:
            st.warning("🟡 **VIÁVEL COM RESSALVAS** - Necessita ajustes para melhor performance")
        elif score_viabilidade >= 3:
            st.warning("🟠 **MARGINAL** - Viável mas com riscos significativos")
        else:
            st.error("🔴 **INVIÁVEL** - Recomenda-se revisão completa do modelo")
        
        st.caption(f"Score de viabilidade: {score_viabilidade}/9")
    
    # Navigation
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("⬅️ Etapa Anterior", key="prev_step11"):
            st.session_state.step = 10
            st.rerun()
    with col3:
        if st.button("Próxima Etapa ➡️", type="primary", key="next_step11"):
            st.session_state.step = 12
            st.rerun()

# Simulação Simples removed as requested by user

def show_step_12():
    """Etapa 12: Cenários e Riscos"""
    st.header("1️⃣2️⃣ Cenários e Riscos")
    st.markdown("**FASE 12: RISCOS** - Análise quantitativa de riscos e planos de contingência")
    
    # Recuperar dados das etapas anteriores
    receita_anual = st.session_state.business_data.get('receita_anual', 180000)
    investimento_total = st.session_state.business_data.get('investimento_total', 81500)
    lucro_operacional = st.session_state.business_data.get('lucro_operacional', 25000)
    
    tab1, tab2, tab3 = st.tabs(["⚠️ Matriz de Riscos", "📈 Simulação Monte Carlo", "🛡️ Planos de Contingência"])
    
    with tab1:
        st.subheader("⚠️ Análise Quantitativa de Riscos")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Riscos de Mercado**")
            
            # Concorrência
            impacto_concorrencia = st.slider(
                "Impacto da concorrência na receita (%)",
                min_value=0.0,
                max_value=50.0,
                value=float(st.session_state.business_data.get('impacto_concorrencia', 15.0)),
                step=5.0
            )
            if impacto_concorrencia != st.session_state.business_data.get('impacto_concorrencia'):
                st.session_state.business_data['impacto_concorrencia'] = impacto_concorrencia
                save_user_data()
            
            prob_concorrencia = st.slider(
                "Probabilidade de entrada de concorrentes (%)",
                min_value=0.0,
                max_value=100.0,
                value=float(st.session_state.business_data.get('prob_concorrencia', 30.0)),
                step=10.0
            )
            if prob_concorrencia != st.session_state.business_data.get('prob_concorrencia'):
                st.session_state.business_data['prob_concorrencia'] = prob_concorrencia
                save_user_data()
            
            # Cálculo do risco esperado
            risco_concorrencia = (impacto_concorrencia/100) * (prob_concorrencia/100) * receita_anual
            st.metric("Risco Concorrência", format_currency(risco_concorrencia))
            
            # Risco de demanda
            volatilidade_demanda = st.slider(
                "Volatilidade da demanda (%)",
                min_value=0.0,
                max_value=50.0,
                value=float(st.session_state.business_data.get('volatilidade_demanda', 20.0)),
                step=5.0
            )
            if volatilidade_demanda != st.session_state.business_data.get('volatilidade_demanda'):
                st.session_state.business_data['volatilidade_demanda'] = volatilidade_demanda
                save_user_data()
            
            # Value at Risk (VaR) simplificado - 5% pior cenário
            var_5_percent = receita_anual * (volatilidade_demanda/100) * 1.645  # Z-score para 95% confiança
            st.metric("VaR (5% pior caso)", format_currency(var_5_percent))
        
        with col2:
            st.markdown("**Riscos Operacionais**")
            
            # Risco de custos
            inflacao_custos = st.slider(
                "Inflação de custos anual (%)",
                min_value=0.0,
                max_value=20.0,
                value=float(st.session_state.business_data.get('inflacao_custos', 8.0)),
                step=1.0
            )
            if inflacao_custos != st.session_state.business_data.get('inflacao_custos'):
                st.session_state.business_data['inflacao_custos'] = inflacao_custos
                save_user_data()
            
            custos_fixos_anual = (st.session_state.business_data.get('aluguel', 3000) + 
                                 st.session_state.business_data.get('total_folha_salarios', 4500) +
                                 st.session_state.business_data.get('0', 800) +
                                 st.session_state.business_data.get('outros_fixos', 500)) * 12
            
            impacto_inflacao = custos_fixos_anual * (inflacao_custos/100)
            st.metric("Impacto Inflação", format_currency(impacto_inflacao))
            
            # Risco de inadimplência
            taxa_inadimplencia = st.slider(
                "Taxa de inadimplência (%)",
                min_value=0.0,
                max_value=15.0,
                value=float(st.session_state.business_data.get('taxa_inadimplencia', 3.0)),
                step=0.5
            )
            if taxa_inadimplencia != st.session_state.business_data.get('taxa_inadimplencia'):
                st.session_state.business_data['taxa_inadimplencia'] = taxa_inadimplencia
                save_user_data()
            
            perda_inadimplencia = receita_anual * (taxa_inadimplencia/100)
            st.metric("Perda Inadimplência", format_currency(perda_inadimplencia))
            
            # Risco total
            risco_total_anual = risco_concorrencia + impacto_inflacao + perda_inadimplencia
            st.metric("Risco Total Anual", format_currency(risco_total_anual))
            
            # Impacto no ROI
            lucro_com_riscos = lucro_operacional - risco_total_anual
            roi_com_riscos = (lucro_com_riscos / investimento_total) * 100 if investimento_total > 0 else 0
            st.metric("ROI Ajustado ao Risco", f"{roi_com_riscos:.1f}%")
    
    with tab2:
        st.subheader("📈 Simulação de Cenários")
        
        if st.button("Executar Simulação Monte Carlo"):
            import numpy as np
            import plotly.graph_objects as go
            
            # Parâmetros da simulação
            num_simulacoes = 1000
            
            # Distribuições das variáveis
            receitas_sim = np.random.normal(receita_anual, receita_anual * (volatilidade_demanda/100), num_simulacoes)
            receitas_sim = np.maximum(receitas_sim, receita_anual * 0.3)  # Mínimo 30% da receita base
            
            custos_variaveis_perc = np.random.normal(0.56, 0.05, num_simulacoes)  # 56% ± 5%
            custos_variaveis_perc = np.clip(custos_variaveis_perc, 0.4, 0.7)
            
            custos_fixos_sim = np.random.normal(custos_fixos_anual, custos_fixos_anual * 0.1, num_simulacoes)
            
            # Cálculo dos lucros simulados
            lucros_sim = []
            for i in range(num_simulacoes):
                receita = receitas_sim[i]
                custo_var = receita * custos_variaveis_perc[i]
                custo_fixo = custos_fixos_sim[i]
                lucro = receita - custo_var - custo_fixo - (investimento_total * 0.05)
                lucros_sim.append(lucro)
            
            lucros_sim = np.array(lucros_sim)
            
            # Estatísticas
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Lucro Médio", format_currency(np.mean(lucros_sim)))
                st.metric("Desvio Padrão", format_currency(np.std(lucros_sim)))
            
            with col2:
                st.metric("Percentil 5%", format_currency(np.percentile(lucros_sim, 5)))
                st.metric("Percentil 95%", format_currency(np.percentile(lucros_sim, 95)))
            
            with col3:
                prob_prejuizo = (lucros_sim < 0).sum() / num_simulacoes * 100
                st.metric("Prob. Prejuízo", f"{prob_prejuizo:.1f}%")
                
                prob_roi_15 = ((lucros_sim / investimento_total) > 0.15).sum() / num_simulacoes * 100
                st.metric("Prob. ROI > 15%", f"{prob_roi_15:.1f}%")
            
            # Histograma dos resultados
            fig = go.Figure(data=[go.Histogram(x=lucros_sim, nbinsx=50)])
            fig.update_layout(
                title="Distribuição de Lucros Simulados",
                xaxis_title="Lucro Anual (R$)",
                yaxis_title="Frequência",
                height=400
            )
            fig.add_vline(x=0, line_dash="dash", line_color="red", annotation_text="Break-even")
            fig.add_vline(x=np.mean(lucros_sim), line_dash="dash", line_color="green", annotation_text="Média")
            
            st.plotly_chart(fig, use_container_width=True)
        
        else:
            st.info("Clique no botão acima para executar simulação de 1000 cenários")
    
    with tab3:
        st.subheader("🛡️ Planos de Contingência Quantificados")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Cenário: Queda de 30% nas Vendas**")
            
            receita_crisis = receita_anual * 0.7
            custos_variaveis_crisis = receita_crisis * 0.56
            
            # Ações de contingência
            reducao_custos_fixos = st.slider(
                "Redução possível custos fixos (%)",
                min_value=0.0,
                max_value=50.0,
                value=20.0,
                step=5.0,
                key="reducao_custos"
            )
            
            custos_fixos_reduzidos = custos_fixos_anual * (1 - reducao_custos_fixos/100)
            lucro_crisis = receita_crisis - custos_variaveis_crisis - custos_fixos_reduzidos - (investimento_total * 0.05)
            
            st.write(f"Receita em crise: {format_currency(receita_crisis)}")
            st.write(f"Custos fixos reduzidos: {format_currency(custos_fixos_reduzidos)}")
            st.write(f"Lucro em crise: {format_currency(lucro_crisis)}")
            
            if lucro_crisis > 0:
                st.success("Ainda lucrativo com contingência")
            else:
                st.error("Necessita mais ajustes")
            
            # Tempo de sobrevivência
            if lucro_crisis < 0:
                capital_giro = st.session_state.business_data.get('capital_giro', 18000)
                meses_sobrevivencia = capital_giro / abs(lucro_crisis/12) if lucro_crisis < 0 else float('inf')
                st.metric("Meses de Sobrevivência", f"{meses_sobrevivencia:.1f}")
        
        with col2:
            st.markdown("**Ações de Contingência Planejadas**")
            
            acoes_contingencia = st.multiselect(
                "Ações implementáveis em crise",
                ["Reduzir jornada funcionários", "Renegociar aluguel", "Focar produtos alta margem", 
                 "Intensificar marketing digital", "Parcerias estratégicas", "Reduzir estoque",
                 "Buscar capital adicional", "Diversificar serviços"],
                default=st.session_state.business_data.get('acoes_contingencia', [])
            )
            if acoes_contingencia != st.session_state.business_data.get('acoes_contingencia'):
                st.session_state.business_data['acoes_contingencia'] = acoes_contingencia
                save_user_data()
            
            # Custos de implementação
            custo_contingencia = st.number_input(
                "Custo implementação contingência (R$)",
                min_value=0.0,
                value=float(st.session_state.business_data.get('custo_contingencia', 5000)),
                step=1000.0,
                format="%.0f"
            )
            if custo_contingencia != st.session_state.business_data.get('custo_contingencia'):
                st.session_state.business_data['custo_contingencia'] = custo_contingencia
                save_user_data()
            
            # Tempo para implementação
            tempo_implementacao = st.selectbox(
                "Tempo para implementar ações",
                ["1-2 semanas", "1 mês", "2-3 meses", "Mais de 3 meses"],
                index=["1-2 semanas", "1 mês", "2-3 meses", "Mais de 3 meses"].index(
                    st.session_state.business_data.get('tempo_implementacao', '1 mês')
                )
            )
            if tempo_implementacao != st.session_state.business_data.get('tempo_implementacao'):
                st.session_state.business_data['tempo_implementacao'] = tempo_implementacao
                save_user_data()
            
            # Eficácia esperada
            eficacia_contingencia = st.slider(
                "Eficácia esperada das ações (%)",
                min_value=0.0,
                max_value=100.0,
                value=float(st.session_state.business_data.get('eficacia_contingencia', 60.0)),
                step=10.0
            )
            if eficacia_contingencia != st.session_state.business_data.get('eficacia_contingencia'):
                st.session_state.business_data['eficacia_contingencia'] = eficacia_contingencia
                save_user_data()
    
    # Resumo final de riscos
    st.markdown("---")
    st.subheader("📊 Resumo Executivo de Riscos")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Risco Total", format_currency(risco_total_anual))
    
    with col2:
        impacto_percentual = (risco_total_anual / receita_anual) * 100
        st.metric("Impacto na Receita", f"{impacto_percentual:.1f}%")
    
    with col3:
        nivel_risco = "BAIXO" if impacto_percentual < 10 else "MÉDIO" if impacto_percentual < 20 else "ALTO"
        st.metric("Nível de Risco", nivel_risco)
    
    with col4:
        st.metric("ROI Ajustado", f"{roi_com_riscos:.1f}%")
    
    # Store risk data
    st.session_state.business_data.update({
        'risco_total_anual': risco_total_anual,
        'roi_com_riscos': roi_com_riscos,
        'nivel_risco': nivel_risco
    })
    save_user_data()
    
    # Navigation
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("⬅️ Etapa Anterior", key="prev_step12"):
            st.session_state.step = 11
            st.rerun()
    with col3:
        if st.button("🎯 Finalizar Plano", type="primary", key="finish_plan"):
            st.balloons()
            st.success("Plano de negócios concluído com análise completa!")
            st.info("Use o menu lateral para navegar entre etapas ou gerar relatórios.")
            st.rerun()

# All precificação functionality has been consolidated into Análise Integrada de Custos




def show_employee_manager():
    """Sistema Completo de DP e Tributação com Legislação Brasileira"""
    st.header("👥 DP e Tributação Completa")
    st.markdown("**Sistema integrado com cálculos tributários brasileiros (CLT, Simples Nacional, MEI)**")
    
    # Navegação

    
    st.markdown("---")
    
    # Abas do sistema de funcionários
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "👥 Funcionários", 
        "💰 Folha de Pagamento", 
        "📊 Análise Tributária", 
        "📋 Compliance CLT", 
        "🧮 Simulador de Custos"
    ])
    
    with tab1:
        st.subheader("👥 Cadastro de Funcionários")
        
        # Verificar se existem funcionários da Etapa 8 (Gestão de Pessoas)
        funcionarios_gestao = st.session_state.business_data.get('funcionarios_planejados', [])
        
        # Sistema de sincronização definitivo para DP
        def sync_funcionarios_dp():
            """Força sincronização bidirecional entre session_state e business_data"""
            funcionarios_salvos = st.session_state.business_data.get('funcionarios_dp', [])
            
            # Se não existe em session_state, carrega dos dados salvos
            if 'funcionarios' not in st.session_state:
                st.session_state.funcionarios = funcionarios_salvos.copy() if funcionarios_salvos else []
            
            # Se dados salvos são diferentes, sincroniza
            elif funcionarios_salvos != st.session_state.funcionarios:
                # Prioriza dados da session_state (mais recentes)
                st.session_state.business_data['funcionarios_dp'] = st.session_state.funcionarios.copy()
                save_user_data()
        
        # Executar sincronização no início da seção
        sync_funcionarios_dp()
        
        # Integração automática com Gestão de Pessoas (apenas se DP estiver vazio)
        if funcionarios_gestao and len(st.session_state.funcionarios) == 0:
            st.info("🔄 **Integração com Gestão de Pessoas**: Encontrados funcionários planejados na Etapa 8. Deseja importá-los automaticamente?")
            
            col_import1, col_import2 = st.columns(2)
            with col_import1:
                if st.button("✅ Importar Funcionários da Etapa 8", type="primary"):
                    # Converter dados da Etapa 8 para formato do DP
                    funcionarios_importados = []
                    for func in funcionarios_gestao:
                        funcionarios_importados.append({
                            'nome': func.get('nome', 'Funcionário'),
                            'cargo': func.get('cargo', 'Vendedor(a)'),
                            'salario_base': func.get('salario', 1518.00),
                            'tipo_contrato': func.get('tipo_contrato', 'CLT'),
                            'data_admissao': func.get('data_admissao', '2024-01-01'),
                            'vale_transporte': func.get('vale_transporte', True),
                            'vale_refeicao': func.get('vale_refeicao', 25.00),
                            'plano_saude': func.get('plano_saude', False),
                            'comissao_percentual': func.get('comissao', 0.0),
                            'horas_semanais': 44,
                            'tem_insalubridade': False,
                            'grau_instrucao': func.get('escolaridade', 'Ensino Médio'),
                            'dependentes': func.get('dependentes', 0)
                        })
                    
                    st.session_state.funcionarios = funcionarios_importados
                    # Sincronização forçada imediata
                    sync_funcionarios_dp()
                    st.success(f"✅ {len(funcionarios_importados)} funcionário(s) importado(s) da Gestão de Pessoas!")
                    st.rerun()
            
            with col_import2:
                if st.button("🔄 Manter Separado", type="secondary"):
                    st.session_state.funcionarios = []
                    st.info("Os dados ficaram separados. Você pode adicionar funcionários manualmente.")
                    st.rerun()
        
        # Botão para carregar dados de exemplo apenas se solicitado
        if len(st.session_state.funcionarios) == 0:
            if st.button("📝 Carregar Dados de Exemplo", type="secondary", help="Adiciona funcionários de exemplo para demonstração"):
                st.session_state.funcionarios = [
                    {
                        'nome': 'Maria Silva',
                        'cargo': 'Vendedora',
                        'salario_base': 1500.00,
                        'tipo_contrato': 'CLT',
                        'data_admissao': '2024-01-15',
                        'vale_transporte': True,
                        'vale_refeicao': 25.00,
                        'plano_saude': False,
                        'comissao_percentual': 2.0,
                        'horas_semanais': 44,
                        'tem_insalubridade': False,
                        'grau_instrucao': 'Ensino Médio',
                        'dependentes': 1
                    },
                    {
                        'nome': 'João Santos',
                        'cargo': 'Optometrista',
                        'salario_base': 3500.00,
                        'tipo_contrato': 'CLT',
                        'data_admissao': '2023-08-10',
                        'vale_transporte': True,
                        'vale_refeicao': 30.00,
                        'plano_saude': True,
                        'comissao_percentual': 1.5,
                        'horas_semanais': 44,
                        'tem_insalubridade': False,
                        'grau_instrucao': 'Superior',
                        'dependentes': 2
                    }
                ]
                st.success("Dados de exemplo carregados! Você pode editá-los ou removê-los conforme necessário.")
                st.rerun()
        
        # Adicionar novo funcionário
        with st.expander("➕ Adicionar Novo Funcionário"):
            col1, col2 = st.columns(2)
            
            with col1:
                novo_nome = st.text_input("Nome completo", key="novo_func_nome")
                novo_cargo = st.selectbox(
                    "Cargo",
                    ["Vendedor(a)", "Optometrista", "Gerente", "Recepcionista", "Técnico em Ótica", "Auxiliar Administrativo"],
                    key="novo_func_cargo"
                )
                # Validação de salário baseada no tipo de contrato
                if st.session_state.get("novo_func_tipo", "CLT") == "CLT":
                    novo_salario = st.number_input(
                        "Salário base (R$)",
                        min_value=1518.00,  # Salário mínimo 2025
                        value=1600.00,
                        step=100.00,
                        key="novo_func_salario",
                        help="⚠️ Valor mínimo R$ 1.518 (salário mínimo 2025)"
                    )
                else:
                    novo_salario = st.number_input(
                        "Valor de remuneração (R$)",
                        min_value=0.01,
                        value=1500.00,
                        step=100.00,
                        key="novo_func_salario",
                        help="Valor livre para MEI ou Prestador de Serviços"
                    )
                novo_tipo = st.selectbox(
                    "Tipo de contrato",
                    ["CLT", "MEI", "Prestador de Serviços"],
                    key="novo_func_tipo"
                )
            
            with col2:
                nova_data = st.date_input("Data de admissão", key="novo_func_data")
                novo_vt = st.checkbox("Vale transporte", key="novo_func_vt")
                novo_vr = st.number_input(
                    "Vale refeição diário (R$)",
                    min_value=0.00,
                    value=25.00,
                    step=5.00,
                    key="novo_func_vr"
                )
                novo_plano = st.checkbox("Plano de saúde", key="novo_func_plano")
                nova_comissao = st.number_input(
                    "Comissão (%)",
                    min_value=0.0,
                    max_value=10.0,
                    value=0.0,
                    step=0.5,
                    key="novo_func_comissao"
                )
                novos_dependentes = st.number_input(
                    "Dependentes",
                    min_value=0,
                    max_value=10,
                    value=0,
                    key="novo_func_dependentes"
                )
            
            if st.button("Adicionar Funcionário", type="primary"):
                if novo_nome:
                    novo_funcionario = {
                        'nome': novo_nome,
                        'cargo': novo_cargo,
                        'salario_base': novo_salario,
                        'tipo_contrato': novo_tipo,
                        'data_admissao': str(nova_data),
                        'vale_transporte': novo_vt,
                        'vale_refeicao': novo_vr,
                        'plano_saude': novo_plano,
                        'comissao_percentual': nova_comissao,
                        'horas_semanais': 44,
                        'tem_insalubridade': False,
                        'grau_instrucao': 'Ensino Médio',
                        'dependentes': novos_dependentes
                    }
                    st.session_state.funcionarios.append(novo_funcionario)
                    # Sincronização forçada imediata
                    sync_funcionarios_dp()
                    st.success(f"✅ Funcionário {novo_nome} adicionado com sucesso!")
                    st.rerun()
                else:
                    st.error("Digite o nome do funcionário")
        
        # Botão para sincronizar de volta para Gestão de Pessoas
        if st.session_state.funcionarios:
            col_sync_dp1, col_sync_dp2 = st.columns([1, 3])
            with col_sync_dp1:
                if st.button("🔄 Sincronizar → Gestão de Pessoas", type="secondary", help="Envia os funcionários cadastrados aqui para a Etapa 8"):
                    funcionarios_para_gestao = []
                    for func in st.session_state.funcionarios:
                        funcionarios_para_gestao.append({
                            'nome': func.get('nome', 'Funcionário'),
                            'cargo': func.get('cargo', 'Vendedor(a)'),
                            'salario': func.get('salario_base', 1518.00),
                            'tipo_contrato': func.get('tipo_contrato', 'CLT'),
                            'data_admissao': func.get('data_admissao', '2024-01-01'),
                            'vale_transporte': func.get('vale_transporte', True),
                            'vale_refeicao': func.get('vale_refeicao', 25.00),
                            'plano_saude': func.get('plano_saude', False),
                            'comissao': func.get('comissao_percentual', 0.0),
                            'escolaridade': func.get('grau_instrucao', 'Ensino Médio'),
                            'dependentes': func.get('dependentes', 0)
                        })
                    
                    st.session_state.business_data['funcionarios_planejados'] = funcionarios_para_gestao
                    save_user_data()
                    st.success(f"✅ {len(funcionarios_para_gestao)} funcionário(s) sincronizado(s) para Gestão de Pessoas!")
                    st.rerun()
            
            with col_sync_dp2:
                st.info("💡 Use este botão para manter os dados sincronizados entre DP e Gestão de Pessoas")
        
        # Lista de funcionários
        st.markdown("**Funcionários Cadastrados:**")
        
        for i, func in enumerate(st.session_state.funcionarios):
            with st.container():
                col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
                
                with col1:
                    st.markdown(f"**{func['nome']}**")
                    st.caption(f"{func['cargo']} • {func['tipo_contrato']}")
                
                with col2:
                    # Validação baseada no tipo de contrato do funcionário
                    if func['tipo_contrato'] == 'CLT':
                        novo_salario = st.number_input(
                            "Salário Base",
                            min_value=1518.00,  # Salário mínimo 2025
                            value=float(func['salario_base']),
                            step=100.00,
                            key=f"salario_clt_edit_{i}",
                            format="%.2f",
                            help="Mínimo R$ 1.518 (salário mínimo 2025)"
                        )
                    else:
                        novo_salario = st.number_input(
                            "Remuneração",
                            min_value=0.01,  # Valor livre para MEI/Prestador
                            value=float(func['salario_base']),
                            step=100.00,
                            key=f"salario_prest_edit_{i}",
                            format="%.2f",
                            help="Valor livre para MEI/Prestador"
                        )
                    
                    if novo_salario != func['salario_base']:
                        st.session_state.funcionarios[i]['salario_base'] = novo_salario
                        # Sincronização forçada imediata
                        sync_funcionarios_dp()
                
                with col3:
                    # Calcular custo total estimado
                    if func['tipo_contrato'] == 'CLT':
                        custo_estimado = func['salario_base'] * 1.68  # Encargos CLT
                    else:
                        custo_estimado = func['salario_base']
                    
                    st.metric("Custo Total", f"R$ {custo_estimado:.2f}")
                
                with col4:
                    if st.button("🗑️", key=f"del_func_{i}", help="Remover funcionário"):
                        st.session_state.funcionarios.pop(i)
                        # Sincronização forçada imediata
                        sync_funcionarios_dp()
                        st.rerun()
                
                st.markdown("---")
    
    with tab2:
        st.subheader("💰 Folha de Pagamento Detalhada")
        
        if not st.session_state.funcionarios:
            st.warning("Adicione funcionários na aba anterior para gerar a folha de pagamento")
        else:
            # Seletor de mês/ano para cálculo
            col_mes1, col_mes2, col_mes3 = st.columns(3)
            
            with col_mes1:
                mes_calculo = st.selectbox(
                    "Mês de referência",
                    list(range(1, 13)),
                    format_func=lambda x: [
                        "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
                        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
                    ][x-1],
                    index=5,  # Junho
                    key="mes_folha"
                )
            
            with col_mes2:
                ano_calculo = st.number_input(
                    "Ano",
                    min_value=2024,
                    max_value=2030,
                    value=2024,
                    key="ano_folha"
                )
            
            with col_mes3:
                # Buscar vendas automáticas das diferentes etapas
                # Etapa 10 - Receita anual / 12
                receita_anual = st.session_state.business_data.get('receita_anual', 0)
                faturamento_projetado = receita_anual / 12 if receita_anual > 0 else 0
                
                # Etapa 10 - Venda primeiro mês
                venda_primeiro_mes = st.session_state.business_data.get('vendas_mes_1', 0)
                
                # Simulação Simples
                vendas_simulacao = st.session_state.business_data.get('vendas_mes_simulacao', 0)
                
                # Resumo Empreendedor
                objetivo_faturamento = st.session_state.business_data.get('objetivo_faturamento', 0)
                
                # Ticket médio × clientes (Etapa 3)
                ticket_medio = st.session_state.business_data.get('ticket_medio_target', 0)
                clientes_mes = st.session_state.business_data.get('clientes_mes_objetivo', 0)
                vendas_calculadas = ticket_medio * clientes_mes if ticket_medio > 0 and clientes_mes > 0 else 0
                
                # Usar o maior valor disponível como sugestão
                vendas_sugeridas = max(
                    faturamento_projetado, 
                    venda_primeiro_mes,
                    vendas_simulacao, 
                    objetivo_faturamento,
                    vendas_calculadas,
                    30000.0
                )
                
                vendas_mes = st.number_input(
                    "Vendas do mês (R$)",
                    min_value=0.0,
                    value=float(vendas_sugeridas),
                    step=1000.0,
                    help=f"💡 Valor sugerido baseado nas projeções: {format_currency(vendas_sugeridas)}",
                    key="vendas_mes_folha"
                )
                
                # Mostrar origem dos dados
                if vendas_sugeridas > 30000:
                    fonte_dados = ""
                    if faturamento_projetado == vendas_sugeridas:
                        fonte_dados = "Etapa 10 - Receita Anual"
                    elif venda_primeiro_mes == vendas_sugeridas:
                        fonte_dados = "Etapa 10 - Primeiro Mês"
                    elif vendas_simulacao == vendas_sugeridas:
                        fonte_dados = "Simulação Simples"
                    elif objetivo_faturamento == vendas_sugeridas:
                        fonte_dados = "Resumo Empreendedor"
                    elif vendas_calculadas == vendas_sugeridas:
                        fonte_dados = "Ticket × Clientes"
                    
                    st.caption(f"📊 Dados de: {fonte_dados}")
                
                # Opção para buscar outros dados automaticamente
                if st.button("🔄 Atualizar com Dados das Etapas", help="Busca automaticamente os valores mais recentes"):
                    # Buscar valores de diferentes etapas
                    valores_encontrados = []
                    
                    # Buscar novamente os valores atualizados
                    receita_anual_atualizada = st.session_state.business_data.get('receita_anual', 0)
                    faturamento_atualizado = receita_anual_atualizada / 12 if receita_anual_atualizada > 0 else 0
                    venda_primeiro_mes_atualizada = st.session_state.business_data.get('vendas_mes_1', 0)
                    vendas_simulacao_atualizada = st.session_state.business_data.get('vendas_mes_simulacao', 0)
                    objetivo_faturamento_atualizado = st.session_state.business_data.get('objetivo_faturamento', 0)
                    ticket_medio_atualizado = st.session_state.business_data.get('ticket_medio_target', 0)
                    clientes_mes_atualizado = st.session_state.business_data.get('clientes_mes_objetivo', 0)
                    vendas_calculadas_atualizada = ticket_medio_atualizado * clientes_mes_atualizado if ticket_medio_atualizado > 0 and clientes_mes_atualizado > 0 else 0
                    
                    # Etapa 10 - Receita anual / 12
                    if faturamento_atualizado > 0:
                        valores_encontrados.append(f"• Receita Anual ÷ 12: {format_currency(faturamento_atualizado)}")
                    
                    # Etapa 10 - Primeiro mês
                    if venda_primeiro_mes_atualizada > 0:
                        valores_encontrados.append(f"• Primeiro Mês (Etapa 10): {format_currency(venda_primeiro_mes_atualizada)}")
                    
                    # Simulação Simples
                    if vendas_simulacao_atualizada > 0:
                        valores_encontrados.append(f"• Simulação Simples: {format_currency(vendas_simulacao_atualizada)}")
                    
                    # Resumo Empreendedor
                    if objetivo_faturamento_atualizado > 0:
                        valores_encontrados.append(f"• Resumo Empreendedor: {format_currency(objetivo_faturamento_atualizado)}")
                    
                    # Cálculo baseado em ticket médio e clientes
                    if vendas_calculadas_atualizada > 0:
                        valores_encontrados.append(f"• Calculado (Ticket {format_currency(ticket_medio_atualizado)} × {clientes_mes_atualizado} clientes): {format_currency(vendas_calculadas_atualizada)}")
                    
                    # Atualizar o valor automaticamente
                    novo_valor = max(
                        faturamento_atualizado, 
                        venda_primeiro_mes_atualizada,
                        vendas_simulacao_atualizada, 
                        objetivo_faturamento_atualizado,
                        vendas_calculadas_atualizada
                    )
                    
                    if novo_valor > 0:
                        st.success(f"""
                        **📈 Valores encontrados:**
                        
                        {chr(10).join(valores_encontrados)}
                        
                        💡 Maior valor encontrado: {format_currency(novo_valor)}
                        
                        ➡️ Use este valor no campo "Vendas do mês" acima.
                        """)
                    else:
                        st.warning("Nenhum valor de faturamento encontrado nas outras etapas. Verifique se preencheu as Projeções Financeiras ou Simulação Simples.")
            
            # Painel de integração de dados
            with st.expander("📊 Dados Integrados do Plano de Negócios", expanded=False):
                st.markdown("### 🔗 Fontes de Dados Conectadas")
                
                col_int1, col_int2 = st.columns(2)
                
                with col_int1:
                    st.markdown("**💰 Faturamento/Vendas:**")
                    
                    # Atualizar valores recalculados
                    receita_anual_atual = st.session_state.business_data.get('receita_anual', 0)
                    faturamento_atual = receita_anual_atual / 12 if receita_anual_atual > 0 else 0
                    venda_primeiro_mes_atual = st.session_state.business_data.get('vendas_mes_1', 0)
                    
                    # Listar todas as fontes de faturamento
                    if faturamento_atual > 0:
                        st.caption(f"✅ Receita Anual ÷ 12: {format_currency(faturamento_atual)}")
                    else:
                        st.caption("❌ Receita Anual ÷ 12: Não preenchido")
                    
                    if venda_primeiro_mes_atual > 0:
                        st.caption(f"✅ Primeiro Mês (Etapa 10): {format_currency(venda_primeiro_mes_atual)}")
                    else:
                        st.caption("❌ Primeiro Mês (Etapa 10): Não preenchido")
                    
                    if vendas_simulacao > 0:
                        st.caption(f"✅ Simulação Simples: {format_currency(vendas_simulacao)}")
                    else:
                        st.caption("❌ Simulação Simples: Não preenchido")
                    
                    if objetivo_faturamento > 0:
                        st.caption(f"✅ Resumo Empreendedor: {format_currency(objetivo_faturamento)}")
                    else:
                        st.caption("❌ Resumo Empreendedor: Não preenchido")
                
                with col_int2:
                    st.markdown("**📈 Dados Operacionais:**")
                    
                    # Ticket médio
                    ticket_medio = st.session_state.business_data.get('ticket_medio', 0)
                    if ticket_medio > 0:
                        st.caption(f"✅ Ticket Médio: {format_currency(ticket_medio)}")
                    else:
                        st.caption("❌ Ticket Médio: Não definido")
                    
                    # Clientes por mês
                    clientes_mes = st.session_state.business_data.get('clientes_mes', 0)
                    if clientes_mes > 0:
                        st.caption(f"✅ Clientes/Mês: {clientes_mes}")
                    else:
                        st.caption("❌ Clientes/Mês: Não definido")
                    
                    # Vendas calculadas
                    if ticket_medio > 0 and clientes_mes > 0:
                        vendas_calc = ticket_medio * clientes_mes
                        st.caption(f"💡 Faturamento Calculado: {format_currency(vendas_calc)}")
                    
                    # Funcionários planejados
                    funcionarios_planejados = st.session_state.business_data.get('funcionarios_planejados', [])
                    if funcionarios_planejados:
                        st.caption(f"✅ Funcionários Planejados: {len(funcionarios_planejados)}")
                    else:
                        st.caption("❌ Funcionários Planejados: Nenhum")
                
                st.info("""
                💡 **Como usar a integração:**
                - O valor de vendas é sugerido automaticamente baseado nos dados das etapas
                - Clique em "🔄 Atualizar com Dados das Etapas" para buscar os valores mais recentes
                - O sistema usa o maior valor encontrado como padrão
                - Comissões são calculadas automaticamente sobre o valor de vendas
                """)
            
            st.markdown("---")
            
            # Inicializar variáveis de controle
            total_salarios = 0
            total_encargos = 0
            total_liquido = 0
            
            for idx, func in enumerate(st.session_state.funcionarios):
                st.markdown(f"### 👤 {func['nome']} - {func['cargo']}")
                
                if func['tipo_contrato'] == 'CLT':
                    # Cálculos CLT detalhados
                    col_calc1, col_calc2, col_calc3 = st.columns(3)
                    
                    with col_calc1:
                        st.markdown("**💵 Proventos**")
                        
                        salario_base = func['salario_base']
                        st.write(f"• Salário base: R$ {salario_base:.2f}")
                        
                        # Comissões
                        comissao = (vendas_mes * func['comissao_percentual'] / 100) if func['comissao_percentual'] > 0 else 0
                        if comissao > 0:
                            st.write(f"• Comissão ({func['comissao_percentual']}%): R$ {comissao:.2f}")
                        
                        # Horas extras (simulação)
                        horas_extras = st.number_input(
                            f"Horas extras {func['nome'][:10]}",
                            min_value=0,
                            max_value=40,
                            value=0,
                            key=f"he_folha_{idx}_{func['nome'].replace(' ', '_')[:8]}"
                        )
                        valor_he = horas_extras * (salario_base / 220) * 1.5
                        if valor_he > 0:
                            st.write(f"• Horas extras (50%): R$ {valor_he:.2f}")
                        
                        salario_bruto = salario_base + comissao + valor_he
                        st.metric("**Total Bruto**", f"R$ {salario_bruto:.2f}")
                    
                    with col_calc2:
                        st.markdown("**📉 Descontos**")
                        
                        # INSS
                        inss = min(salario_bruto * 0.14, 877.24)  # Teto INSS 2024
                        st.write(f"• INSS (14%): R$ {inss:.2f}")
                        
                        # IRPF
                        base_irpf = salario_bruto - inss - (func['dependentes'] * 189.59)
                        if base_irpf <= 2112.00:
                            irpf = 0
                        elif base_irpf <= 2826.65:
                            irpf = base_irpf * 0.075 - 158.40
                        elif base_irpf <= 3751.05:
                            irpf = base_irpf * 0.15 - 370.40
                        elif base_irpf <= 4664.68:
                            irpf = base_irpf * 0.225 - 651.73
                        else:
                            irpf = base_irpf * 0.275 - 884.96
                        
                        irpf = max(0, irpf)
                        st.write(f"• IRPF: R$ {irpf:.2f}")
                        
                        # Vale transporte
                        vt_desconto = min(salario_bruto * 0.06, 220.00) if func['vale_transporte'] else 0
                        if vt_desconto > 0:
                            st.write(f"• Vale transporte (6%): R$ {vt_desconto:.2f}")
                        
                        # Plano de saúde
                        plano_desconto = 150.00 if func['plano_saude'] else 0
                        if plano_desconto > 0:
                            st.write(f"• Plano de saúde: R$ {plano_desconto:.2f}")
                        
                        total_descontos = inss + irpf + vt_desconto + plano_desconto
                        st.metric("**Total Descontos**", f"R$ {total_descontos:.2f}")
                    
                    with col_calc3:
                        st.markdown("**🏢 Encargos Patronais**")
                        
                        # INSS Patronal
                        inss_patronal = salario_bruto * 0.20
                        st.write(f"• INSS Patronal (20%): R$ {inss_patronal:.2f}")
                        
                        # FGTS
                        fgts = salario_bruto * 0.08
                        st.write(f"• FGTS (8%): R$ {fgts:.2f}")
                        
                        # Sistema S + Salário Educação
                        sistema_s = salario_bruto * 0.0358  # SESC + SENAC + SEBRAE + Sal.Educação
                        st.write(f"• Sistema S (3,58%): R$ {sistema_s:.2f}")
                        
                        # Seguro Acidente
                        seguro_acidente = salario_bruto * 0.01
                        st.write(f"• Seguro Acidente (1%): R$ {seguro_acidente:.2f}")
                        
                        total_encargos_func = inss_patronal + fgts + sistema_s + seguro_acidente
                        st.metric("**Total Encargos**", f"R$ {total_encargos_func:.2f}")
                    
                    # Valores finais
                    salario_liquido = salario_bruto - total_descontos
                    custo_total_funcionario = salario_bruto + total_encargos_func
                    
                    col_final1, col_final2, col_final3 = st.columns(3)
                    with col_final1:
                        st.success(f"**Líquido: R$ {salario_liquido:.2f}**")
                    with col_final2:
                        st.info(f"**Custo Total: R$ {custo_total_funcionario:.2f}**")
                    with col_final3:
                        percentual_encargos = (total_encargos_func / salario_bruto) * 100
                        st.warning(f"**Encargos: {percentual_encargos:.1f}%**")
                    
                    total_salarios += salario_bruto
                    total_encargos += total_encargos_func
                    total_liquido += salario_liquido
                
                else:
                    # Para MEI/Prestadores
                    st.info(f"Prestador de serviços - Pagamento: R$ {func['salario_base']:.2f}")
                    total_salarios += func['salario_base']
                
                st.markdown("---")
            
            # Resumo geral da folha
            st.markdown("## 📊 Resumo da Folha de Pagamento")
            
            col_resumo1, col_resumo2, col_resumo3, col_resumo4 = st.columns(4)
            
            with col_resumo1:
                st.metric("Total Salários Brutos", f"R$ {total_salarios:.2f}")
            
            with col_resumo2:
                st.metric("Total Encargos", f"R$ {total_encargos:.2f}")
            
            with col_resumo3:
                st.metric("Total a Pagar (Líquido)", f"R$ {total_liquido:.2f}")
            
            with col_resumo4:
                custo_total_folha = total_salarios + total_encargos
                st.metric("Custo Total da Folha", f"R$ {custo_total_folha:.2f}")
    
    with tab3:
        st.subheader("📊 Análise Tributária Detalhada")
        
        st.markdown("**Sistema de análise tributária baseado no faturamento do negócio**")
        
        # Análise por regime tributário (funciona independentemente de funcionários)
        regime_tributario = st.selectbox(
            "Regime tributário da empresa",
            ["Simples Nacional", "Lucro Presumido"],
            key="regime_analise"
        )
        
        faturamento_anual = st.number_input(
            "Faturamento anual estimado (R$)",
            min_value=0.0,
            value=360000.0,
            step=10000.0,
            key="fat_anual_tributario"
        )
        
        # Cálculo simplificado do Simples Nacional
        if regime_tributario == "Simples Nacional":
            st.markdown("### 📋 Simples Nacional - Anexo I (Comércio)")
            
            # Calcular alíquota baseada no faturamento
            if faturamento_anual <= 180000:
                aliquota = 4.0
                faixa = "1ª faixa"
            elif faturamento_anual <= 360000:
                aliquota = 7.3
                faixa = "2ª faixa"
            elif faturamento_anual <= 720000:
                aliquota = 9.5
                faixa = "3ª faixa"
            elif faturamento_anual <= 1800000:
                aliquota = 10.26
                faixa = "4ª faixa"
            else:
                aliquota = 11.31
                faixa = "5ª faixa"
            
            # Cálculos
            imposto_anual = faturamento_anual * (aliquota / 100)
            imposto_mensal = imposto_anual / 12
            
            # Exibir resultados
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    "Alíquota Simples",
                    f"{aliquota}%",
                    f"{faixa}"
                )
            
            with col2:
                st.metric(
                    "DAS Mensal",
                    f"R$ {imposto_mensal:,.2f}",
                    f"R$ {imposto_anual:,.2f}/ano"
                )
            
            with col3:
                percentual_fat = (imposto_mensal / (faturamento_anual/12)) * 100
                st.metric(
                    "% do Faturamento",
                    f"{percentual_fat:.1f}%",
                    "Carga tributária"
                )
            
            st.info("""
            **💡 Simples Nacional para Óticas:**
            - Anexo I (Comércio): Para venda de produtos ópticos
            - Pagamento único mensal através do DAS
            - Inclui todos os impostos federais, estaduais e municipais
            """)
        
        else:  # Lucro Presumido
            st.markdown("### 📋 Lucro Presumido")
            
            # Cálculos básicos Lucro Presumido
            base_calculo_irpj = faturamento_anual * 0.08  # 8% para comércio
            base_calculo_csll = faturamento_anual * 0.12  # 12% para comércio
            
            irpj = base_calculo_irpj * 0.15  # 15%
            csll = base_calculo_csll * 0.09  # 9%
            pis = faturamento_anual * 0.0065  # 0,65%
            cofins = faturamento_anual * 0.03  # 3%
            
            total_federal = irpj + csll + pis + cofins
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Impostos Federais Anuais:**")
                st.markdown(f"• IRPJ: R$ {irpj:,.2f}")
                st.markdown(f"• CSLL: R$ {csll:,.2f}")
                st.markdown(f"• PIS: R$ {pis:,.2f}")
                st.markdown(f"• COFINS: R$ {cofins:,.2f}")
                st.markdown(f"**Total: R$ {total_federal:,.2f}**")
            
            with col2:
                st.metric(
                    "Total Mensal",
                    f"R$ {total_federal/12:,.2f}",
                    f"{(total_federal/faturamento_anual)*100:.1f}% do faturamento"
                )
            
            st.warning("""
            **⚠️ Lucro Presumido:**
            - Não inclui ICMS (estadual) e ISS (municipal)
            - Requer maior controle contábil
            - Mais complexo que o Simples Nacional
            """)
        
        # Comparação final
        st.markdown("---")
        st.markdown("### 💰 Resumo da Tributação")
        
        # Usar valores configurados pelo usuário (não calcular automaticamente)
        impostos_configurado = st.session_state.business_data.get('impostos_percentual', 0) / 100
        custo_tributario_mensal_configurado = faturamento_anual * impostos_configurado / 12
        
        st.info(f"""
        **📊 Resumo baseado em suas configurações:**
        - Faturamento anual: R$ {faturamento_anual:,.2f}
        - Taxa de impostos configurada: {impostos_configurado*100:.1f}%
        - Custo tributário mensal configurado: R$ {custo_tributario_mensal_configurado:,.2f}
        
        💡 *Valores baseados no que você configurou na Etapa 10*
        """)
    
    with tab4:
        st.subheader("📋 Compliance CLT - Checklist de Obrigações")
        
        st.markdown("**Sistema de verificação de compliance trabalhista**")
        
        compliance_items = [
            {
                "categoria": "Admissão",
                "itens": [
                    "Registro do empregado no livro/sistema de registro",
                    "Anotação na CTPS (física ou digital)",
                    "Cadastro no PIS/PASEP",
                    "Exames médicos admissionais",
                    "Cadastro no eSocial",
                    "Termo de responsabilidade para vale-transporte"
                ]
            },
            {
                "categoria": "Mensal",
                "itens": [
                    "Folha de pagamento até o 5º dia útil",
                    "Guia de recolhimento do FGTS",
                    "GPS - Guia da Previdência Social",
                    "Declaração do IRPF retido",
                    "Controle de ponto (se aplicável)",
                    "Vale-refeição/alimentação"
                ]
            },
            {
                "categoria": "Anual",
                "itens": [
                    "13º salário (até 20/12 ou duas parcelas)",
                    "Férias + 1/3 constitucional",
                    "RAIS - Relação Anual de Informações Sociais",
                    "DIRF - Declaração do IR na Fonte",
                    "Exames médicos periódicos",
                    "PPP - Perfil Profissiográfico Previdenciário"
                ]
            },
            {
                "categoria": "Demissão",
                "itens": [
                    "Aviso prévio (trabalhado ou indenizado)",
                    "Exame médico demissional",
                    "Homologação (se aplicável)",
                    "Termo de rescisão",
                    "Guias para saque do FGTS",
                    "Baixa na CTPS e eSocial"
                ]
            }
        ]
        
        col_compliance1, col_compliance2 = st.columns(2)
        
        for i, categoria in enumerate(compliance_items):
            target_col = col_compliance1 if i % 2 == 0 else col_compliance2
            
            with target_col:
                st.markdown(f"### {categoria['categoria']}")
                
                for item in categoria['itens']:
                    compliant = st.checkbox(
                        item,
                        key=f"compliance_{categoria['categoria']}_{item[:20]}"
                    )
                    
                    if not compliant:
                        st.error(f"⚠️ Pendente: {item}")
                
                st.markdown("---")
        
        # Cálculo de compliance geral
        total_items = sum(len(cat['itens']) for cat in compliance_items)
        # Este seria calculado baseado nos checkboxes marcados
        st.markdown("### 📊 Score de Compliance")
        st.progress(0.75)  # Exemplo: 75% de compliance
        st.info("Score: 75% - Bom nível de compliance trabalhista")
    
    with tab5:
        st.subheader("🧮 Simulador de Custos de Contratação")
        
        st.markdown("**Simule diferentes cenários de contratação**")
        
        col_sim1, col_sim2 = st.columns(2)
        
        with col_sim1:
            st.markdown("**Configuração da Simulação**")
            
            cargo_simulacao = st.selectbox(
                "Cargo para simular",
                ["Vendedor(a)", "Optometrista", "Gerente", "Recepcionista", "Técnico em Ótica"],
                key="cargo_sim"
            )
            
            salario_simulacao = st.number_input(
                "Salário pretendido (R$)",
                min_value=1412.00,
                value=2000.00,
                step=100.00,
                key="salario_sim"
            )
            
            beneficios_sim = st.multiselect(
                "Benefícios oferecidos",
                ["Vale transporte", "Vale refeição", "Plano de saúde", "Plano odontológico", "Participação nos lucros"],
                default=["Vale transporte", "Vale refeição"],
                key="beneficios_sim"
            )
            
            comissao_sim = st.number_input(
                "Comissão sobre vendas (%)",
                min_value=0.0,
                max_value=10.0,
                value=2.0,
                step=0.5,
                key="comissao_sim"
            )
            
            vendas_esperadas = st.number_input(
                "Vendas mensais esperadas (R$)",
                min_value=0.0,
                value=15000.0,
                step=1000.0,
                key="vendas_sim"
            )
        
        with col_sim2:
            st.markdown("**Cálculo de Custo Total**")
            
            # Cálculos detalhados
            salario_base = salario_simulacao
            comissao_mensal = vendas_esperadas * (comissao_sim / 100)
            salario_bruto_mensal = salario_base + comissao_mensal
            
            # Encargos
            inss_patronal = salario_bruto_mensal * 0.20
            fgts = salario_bruto_mensal * 0.08
            sistema_s = salario_bruto_mensal * 0.0358
            seguro_acidente = salario_bruto_mensal * 0.01
            total_encargos_sim = inss_patronal + fgts + sistema_s + seguro_acidente
            
            # Benefícios
            custo_beneficios = 0
            if "Vale transporte" in beneficios_sim:
                custo_beneficios += 200  # Estimativa
            if "Vale refeição" in beneficios_sim:
                custo_beneficios += 550  # 22 dias x R$25
            if "Plano de saúde" in beneficios_sim:
                custo_beneficios += 300
            if "Plano odontológico" in beneficios_sim:
                custo_beneficios += 50
            
            # Custos anuais adicionais
            decimo_terceiro = salario_bruto_mensal
            ferias = salario_bruto_mensal * 1.33  # + 1/3
            custos_anuais_extras = (decimo_terceiro + ferias) / 12
            
            custo_total_mensal = salario_bruto_mensal + total_encargos_sim + custo_beneficios + custos_anuais_extras
            
            # Exibir resultados com explicação clara
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #f8f9fa, #e9ecef);
                padding: 1.5rem;
                border-radius: 12px;
                border-left: 4px solid #6c757d;
                margin: 1rem 0;
            ">
                <div style="font-size: 1.1rem; font-weight: bold; color: #495057; margin-bottom: 0.5rem;">
                    Custo total para contratar este funcionário
                </div>
                <div style="font-size: 2rem; font-weight: bold; color: #495057; margin-bottom: 1rem;">
                    R$ {custo_total_mensal:.2f}/mês
                </div>
                <div style="font-size: 1rem; font-weight: bold; color: #495057; margin-bottom: 0.5rem;">
                    Porque?:
                </div>
                <div style="color: #495057; line-height: 1.5;">
                    • <strong>Salário + comissão:</strong> R$ {salario_bruto_mensal:.2f} (base R$ {salario_base:.2f} + comissão R$ {comissao_mensal:.2f})<br>
                    • <strong>Encargos sociais:</strong> R$ {total_encargos_sim:.2f} (INSS, FGTS, Sistema S obrigatórios por lei)<br>
                    • <strong>Benefícios:</strong> R$ {custo_beneficios:.2f} (vale transporte, refeição, planos)<br>
                    • <strong>13º e férias:</strong> R$ {custos_anuais_extras:.2f} (custos anuais divididos por 12 meses)
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Análise de ROI
            st.markdown("**Análise de Retorno:**")
            if vendas_esperadas > 0:
                roi_contratacao = (vendas_esperadas - custo_total_mensal) / custo_total_mensal * 100
                st.metric("ROI da Contratação", f"{roi_contratacao:.1f}%")
                
                if roi_contratacao > 200:
                    st.success("✅ Contratação muito viável")
                elif roi_contratacao > 100:
                    st.info("✅ Contratação viável")
                elif roi_contratacao > 50:
                    st.warning("⚠️ Contratação questionável")
                else:
                    st.error("❌ Contratação não recomendada")
        
        # Comparação com diferentes regimes
        st.markdown("---")
        st.markdown("### 📊 Comparação por Regime Tributário")
        
        col_reg1, col_reg2, col_reg3 = st.columns(3)
        
        with col_reg1:
            st.markdown("**CLT + Simples Nacional**")
            custo_simples = custo_total_mensal - (salario_bruto_mensal * 0.20) + (salario_bruto_mensal * 0.08)
            st.metric("Custo Mensal", f"R$ {custo_simples:.2f}")
            st.caption("INSS patronal incluído no DAS")
        
        with col_reg2:
            st.markdown("**CLT + Lucro Presumido**")
            st.metric("Custo Mensal", f"R$ {custo_total_mensal:.2f}")
            st.caption("Todos os encargos aplicáveis")
        
        with col_reg3:
            st.markdown("**Prestador de Serviços/MEI**")
            custo_pj = salario_base * 1.3  # Acréscimo para compensar encargos
            st.metric("Custo Mensal", f"R$ {custo_pj:.2f}")
            st.caption("Sem encargos trabalhistas")

def show_plan_validator_tool():
    """Validador do Plano - Auditoria Completa do Plano de Negócios"""
    
    # Header with back button
    col1, col2 = st.columns([1, 6])
    with col1:
        if st.button("⬅️ Voltar", key="back_plan_validator"):
            st.session_state.show_plan_validator = False
            st.rerun()
    
    with col2:
        st.title("🔍 Validador do Plano de Negócios")
        st.markdown("**Auditoria completa - verifica se seu plano está consistente e completo**")
    
    # Contadores de status
    total_checks = 0
    passed_checks = 0
    warnings = 0
    errors = 0
    
    # Lista de validações
    validations = []
    
    # 1. VALIDAÇÃO BÁSICA DO NEGÓCIO
    st.subheader("📋 1. Informações Básicas do Negócio")
    
    # Verificar múltiplas possíveis chaves para nome da empresa
    nome_empresa = (st.session_state.business_data.get('nome_otica', '') or 
                   st.session_state.business_data.get('nome_negocio', '') or 
                   st.session_state.business_data.get('nome_empresa', ''))
    
    if nome_empresa and len(nome_empresa.strip()) > 3:
        validations.append({
            "status": "✅", 
            "item": "Nome da empresa definido", 
            "details": f"'{nome_empresa}'",
            "sugestao": "Nome adequado para identificação comercial"
        })
        passed_checks += 1
    elif nome_empresa and len(nome_empresa.strip()) > 0:
        validations.append({
            "status": "⚠️", 
            "item": "Nome da empresa muito curto", 
            "details": f"'{nome_empresa}' tem apenas {len(nome_empresa.strip())} caracteres",
            "sugestao": "AÇÃO: Vá para Etapa 1 → Campo 'Nome da Ótica' e digite um nome mais descritivo com pelo menos 4 caracteres. Ex: 'Ótica Vision', 'Ótica Central' ou 'Óptica do Bairro'"
        })
        warnings += 1
    else:
        validations.append({
            "status": "❌", 
            "item": "Nome da empresa não definido", 
            "details": "Campo obrigatório vazio",
            "sugestao": "AÇÃO CRÍTICA: Vá para Etapa 1 → Sumário Executivo → Campo 'Nome da Ótica' e defina o nome comercial. Este será o nome usado em contratos, notas fiscais e documentos oficiais."
        })
        errors += 1
    total_checks += 1
    
    missao = st.session_state.business_data.get('missao', '')
    if missao and len(missao) > 20:
        validations.append({"status": "✅", "item": "Missão da empresa definida", "details": f"{len(missao)} caracteres"})
        passed_checks += 1
    else:
        validations.append({"status": "⚠️", "item": "Missão muito curta ou não definida", "details": "Recomendado pelo menos 20 caracteres"})
        warnings += 1
    total_checks += 1
    
    # **VALIDAÇÃO TRIBUTÁRIA CRÍTICA** - Prioridade máxima
    st.subheader("🚨 Validação Tributária Crítica")
    
    tipo_empresa = st.session_state.business_data.get('tipo_empresa', 'MEI')
    objetivo_faturamento = st.session_state.business_data.get('objetivo_faturamento', 0)
    receita_anual = objetivo_faturamento * 12
    funcionarios_count = len(st.session_state.business_data.get('funcionarios_planejados', []))
    
    # Validações MEI
    if tipo_empresa == 'MEI':
        col_mei1, col_mei2 = st.columns(2)
        
        with col_mei1:
            st.markdown("**Limites MEI:**")
            if receita_anual > 81000:
                validations.append({
                    "status": "❌", 
                    "item": "ERRO CRÍTICO: Receita MEI excedida", 
                    "details": f"R$ {receita_anual:,.0f} > R$ 81.000 (limite MEI)",
                    "sugestao": "AÇÃO URGENTE: Vá para Etapa 1 → Altere 'Tipo de empresa' para 'Microempresa' OU reduza meta de faturamento para R$ 6.750/mês"
                })
                errors += 1
            else:
                validations.append({
                    "status": "✅", 
                    "item": "Receita MEI dentro do limite", 
                    "details": f"R$ {receita_anual:,.0f} ≤ R$ 81.000"
                })
                passed_checks += 1
            total_checks += 1
            
            if funcionarios_count > 1:
                validations.append({
                    "status": "❌", 
                    "item": "ERRO CRÍTICO: Funcionários MEI excedidos", 
                    "details": f"{funcionarios_count} funcionários > 1 (limite MEI)",
                    "sugestao": "AÇÃO URGENTE: Vá para Etapa 8 → Reduza para 1 funcionário OU altere regime para 'Microempresa'"
                })
                errors += 1
            else:
                validations.append({
                    "status": "✅", 
                    "item": "Funcionários MEI dentro do limite", 
                    "details": f"{funcionarios_count} ≤ 1 funcionário"
                })
                passed_checks += 1
            total_checks += 1
        
        with col_mei2:
            st.markdown("**Quanto você vai pagar de impostos no MEI:**")
            # Valores corretos MEI 2025: Óticas são comércio = R$ 76,90
            custo_mei_mes = 76.90  # R$ 75,90 INSS + R$ 1,00 ICMS (comércio)
            custo_mei_anual = custo_mei_mes * 12
            perc_sobre_receita = (custo_mei_anual / receita_anual * 100) if receita_anual > 0 else 0
            
            # Formato claro: valor + explicação detalhada
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #e8f5e8, #f0f8f0);
                padding: 1.5rem;
                border-radius: 12px;
                border-left: 4px solid #28a745;
                margin: 1rem 0;
            ">
                <div style="font-size: 1.1rem; font-weight: bold; color: #155724; margin-bottom: 0.5rem;">
                    Você paga por mês (MEI Comércio)
                </div>
                <div style="font-size: 2rem; font-weight: bold; color: #28a745; margin-bottom: 1rem;">
                    R$ {custo_mei_mes:.2f}
                </div>
                <div style="font-size: 1rem; font-weight: bold; color: #155724; margin-bottom: 0.5rem;">
                    Porque?:
                </div>
                <div style="color: #155724; line-height: 1.5;">
                    • <strong>É um valor fixo:</strong> Você paga sempre os mesmos R$ {custo_mei_mes:.2f}, mesmo que venda R$ 1.000 ou R$ 6.000 no mês<br>
                    • <strong>Composição do DAS:</strong> INSS R$ 75,90 + ICMS R$ 1,00 (ótica é comércio)<br>
                    • <strong>Sem surpresas:</strong> Não precisa calcular percentual sobre vendas, sempre o mesmo valor<br>
                    • <strong>Muito barato:</strong> Representa apenas {perc_sobre_receita:.2f}% do que você fatura
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Comparar com Simples Nacional
            if receita_anual > 0:
                custo_simples_anual = receita_anual * 0.04  # 4% primeira faixa
                custo_simples_mes = custo_simples_anual / 12
                diferenca_anual = custo_simples_anual - custo_mei_anual
                
                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, #fff3cd, #ffeaa7);
                    padding: 1.5rem;
                    border-radius: 12px;
                    border-left: 4px solid #ffc107;
                    margin: 1rem 0;
                ">
                    <div style="font-size: 1.1rem; font-weight: bold; color: #856404; margin-bottom: 0.5rem;">
                        Se fosse Microempresa (Simples Nacional)
                    </div>
                    <div style="font-size: 1.8rem; font-weight: bold; color: #ffc107; margin-bottom: 1rem;">
                        R$ {custo_simples_mes:.2f}/mês
                    </div>
                    <div style="font-size: 1rem; font-weight: bold; color: #856404; margin-bottom: 0.5rem;">
                        Porque?:
                    </div>
                    <div style="color: #856404; line-height: 1.5;">
                        • <strong>Baseado nas vendas:</strong> Você pagaria 4% de tudo que vender<br>
                        • <strong>Varia todo mês:</strong> Vendeu mais = paga mais impostos<br>
                        • <strong>Diferença anual:</strong> R$ {diferenca_anual:,.0f} {"a mais" if diferenca_anual > 0 else "a menos"} que o MEI<br>
                        • <strong>Conclusão:</strong> {"MEI é mais barato para seu faturamento" if diferenca_anual > 0 else "Microempresa seria mais cara"}
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    # Validações Simples Nacional
    elif tipo_empresa in ['Microempresa', 'Empresa de Pequeno Porte']:
        st.markdown("**Verificando se sua empresa pode usar Simples Nacional:**")
        
        if receita_anual > 4800000:
            validations.append({
                "status": "❌", 
                "item": "PROBLEMA: Sua empresa cresceu demais para o Simples Nacional", 
                "details": f"Você fatura R$ {receita_anual:,.0f} por ano, mas o limite é R$ 4.800.000",
                "sugestao": "O QUE FAZER: Procure um contador para mudar para Lucro Presumido. É mais caro, mas é obrigatório."
            })
            errors += 1
        else:
            # Calcular alíquota correta
            if receita_anual <= 180000:
                aliquota_correta = 4.0
                faixa_explicacao = "faturamento baixo"
            elif receita_anual <= 360000:
                aliquota_correta = 5.47
                faixa_explicacao = "faturamento médio-baixo"
            elif receita_anual <= 720000:
                aliquota_correta = 6.84
                faixa_explicacao = "faturamento médio"
            else:
                aliquota_correta = 8.0
                faixa_explicacao = "faturamento alto"
            
            impostos_atual = st.session_state.business_data.get('impostos_percentual', 6.0)
            
            col_sn1, col_sn2 = st.columns(2)
            with col_sn1:
                validations.append({
                    "status": "✅", 
                    "item": f"Você pode usar {tipo_empresa}", 
                    "details": f"Seu faturamento é considerado {faixa_explicacao} (taxa de {aliquota_correta}%)"
                })
                passed_checks += 1
                
            with col_sn2:
                # Cálculo do que vai pagar no Simples Nacional
                custo_mensal_simples = (receita_anual * aliquota_correta / 100) / 12
                
                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, #e3f2fd, #bbdefb);
                    padding: 1.5rem;
                    border-radius: 12px;
                    border-left: 4px solid #2196f3;
                    margin: 1rem 0;
                ">
                    <div style="font-size: 1.1rem; font-weight: bold; color: #0d47a1; margin-bottom: 0.5rem;">
                        Você paga por mês no Simples Nacional
                    </div>
                    <div style="font-size: 2rem; font-weight: bold; color: #2196f3; margin-bottom: 1rem;">
                        R$ {custo_mensal_simples:.2f}
                    </div>
                    <div style="font-size: 1rem; font-weight: bold; color: #0d47a1; margin-bottom: 0.5rem;">
                        Porque?:
                    </div>
                    <div style="color: #0d47a1; line-height: 1.5;">
                        • <strong>Taxa de {aliquota_correta}%:</strong> Você paga {aliquota_correta}% de tudo que vender<br>
                        • <strong>Seu faturamento é {faixa_explicacao}:</strong> R$ {receita_anual:,.0f}/ano = faixa de {aliquota_correta}%<br>
                        • <strong>Varia com as vendas:</strong> Vendeu R$ 10.000 = paga R$ {10000 * aliquota_correta / 100:.0f}<br>
                        • <strong>Inclui vários impostos:</strong> IRPJ, CSLL, PIS, COFINS, ICMS, ISS em uma guia só
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Validação da taxa configurada (mais flexível)
                diferenca_impostos = abs(impostos_atual - aliquota_correta)
                if diferenca_impostos > 3.0:
                    validations.append({
                        "status": "⚠️", 
                        "item": "Taxa de impostos muito diferente do padrão", 
                        "details": f"Você configurou {impostos_atual}%, padrão seria {aliquota_correta}% (diferença: {diferenca_impostos:.1f}%)",
                        "sugestao": f"INFORMATIVO: Se tem certeza do valor, mantenha. Se não, considere {aliquota_correta}% ou consulte contador"
                    })
                    warnings += 1
                else:
                    validations.append({
                        "status": "✅", 
                        "item": "Taxa de impostos configurada", 
                        "details": f"{impostos_atual}% (padrão seria {aliquota_correta}% - diferença aceitável)"
                    })
                    passed_checks += 1
                total_checks += 1
        total_checks += 1
    
    # Validações Lucro Presumido
    elif tipo_empresa in ['Ltda', 'Outro']:
        st.markdown("**Verificando impostos para empresa comum (Lucro Presumido):**")
        impostos_atual = st.session_state.business_data.get('impostos_percentual', 6.0)
        
        # Lucro Presumido típico: 13.33% (IR+CSLL+PIS+COFINS+ICMS/ISS)
        st.info("💡 Empresas normais (Ltda) pagam mais impostos que MEI ou Simples Nacional")
        
        if impostos_atual < 10.0:
            validations.append({
                "status": "⚠️", 
                "item": "Sua taxa de impostos parece muito baixa", 
                "details": f"Você configurou {impostos_atual}%, mas empresas normais pagam entre 13-15%",
                "sugestao": "O QUE FAZER: Vá na Etapa 10 → Mude 'Impostos' para 13-15%. Converse com um contador para confirmar."
            })
            warnings += 1
        else:
            validations.append({
                "status": "✅", 
                "item": "Sua taxa de impostos está dentro do esperado", 
                "details": f"{impostos_atual}% é uma taxa típica para empresas comuns"
            })
            passed_checks += 1
        total_checks += 1
    
    st.markdown("---")
    
    # 2. VALIDAÇÃO FINANCEIRA
    st.subheader("💰 2. Estrutura Financeira")
    
    vendas_mes_1 = st.session_state.business_data.get('vendas_mes_1', 0)
    if vendas_mes_1 > 5000:
        validations.append({"status": "✅", "item": "Meta de faturamento definida", "details": f"{format_currency(vendas_mes_1)}/mês"})
        passed_checks += 1
    else:
        validations.append({"status": "❌", "item": "Meta de faturamento muito baixa ou não definida", "details": "Defina na Etapa 10"})
        errors += 1
    total_checks += 1
    
    investimento_total = st.session_state.business_data.get('investimento_total', 0)
    capital_giro = st.session_state.business_data.get('capital_giro', 0)
    if investimento_total > 0 and capital_giro > 0:
        ratio_giro = (capital_giro / investimento_total) * 100
        if ratio_giro >= 15:
            validations.append({"status": "✅", "item": "Capital de giro adequado", "details": f"{ratio_giro:.1f}% do investimento total"})
            passed_checks += 1
        else:
            validations.append({"status": "⚠️", "item": "Capital de giro pode ser insuficiente", "details": f"Apenas {ratio_giro:.1f}% do investimento"})
            warnings += 1
    else:
        validations.append({"status": "❌", "item": "Investimento inicial não definido", "details": "Configure na Etapa 9"})
        errors += 1
    total_checks += 1
    
    # 3. VALIDAÇÕES MATEMÁTICAS AVANÇADAS
    st.subheader("🧮 3. Validações Matemáticas e Financeiras")
    
    # 3.1 VALIDAÇÃO DE FOLHA DE PAGAMENTO
    funcionarios_dp = st.session_state.business_data.get('funcionarios_dp', [])
    salarios_total = st.session_state.business_data.get('salarios_total', 0)
    folha_clt = st.session_state.business_data.get('folha_clt', 0)
    total_optometrista = st.session_state.business_data.get('total_optometrista', 0)
    
    if funcionarios_dp:
        # Calcular folha real baseada nos funcionários cadastrados
        folha_calculada_clt = 0
        folha_calculada_terceiros = 0
        
        for func in funcionarios_dp:
            salario_base = func.get('salario_base', 0)
            tipo_contrato = func.get('tipo_contrato', 'CLT')
            
            if tipo_contrato == 'CLT':
                # CLT com encargos de 68%
                custo_total = salario_base * 1.68
                folha_calculada_clt += custo_total
            else:
                # MEI/Prestador sem encargos
                folha_calculada_terceiros += salario_base
        
        # Comparar com valores informados nas projeções
        if abs(folha_clt - folha_calculada_clt) < 100:  # Tolerância de R$ 100
            validations.append({
                "status": "✅", 
                "item": "Folha CLT consistente", 
                "details": f"Calculado: {format_currency(folha_calculada_clt)} = Informado: {format_currency(folha_clt)}",
                "sugestao": "Valores de folha CLT estão corretos com encargos de 68%"
            })
            passed_checks += 1
        else:
            validations.append({
                "status": "❌", 
                "item": "Divergência na folha CLT", 
                "details": f"Calculado: {format_currency(folha_calculada_clt)} ≠ Informado: {format_currency(folha_clt)}",
                "sugestao": "AÇÃO: Vá para Etapa 10 → Folha CLT ou DP e Tributação para sincronizar os valores. A diferença pode indicar erro nos encargos (68%) ou funcionários não incluídos."
            })
            errors += 1
        total_checks += 1
        
        if abs(total_optometrista - folha_calculada_terceiros) < 50:
            validations.append({
                "status": "✅", 
                "item": "Serviços terceirizados consistentes", 
                "details": f"Calculado: {format_currency(folha_calculada_terceiros)} = Informado: {format_currency(total_optometrista)}"
            })
            passed_checks += 1
        else:
            validations.append({
                "status": "⚠️", 
                "item": "Divergência em serviços terceirizados", 
                "details": f"Calculado: {format_currency(folha_calculada_terceiros)} ≠ Informado: {format_currency(total_optometrista)}",
                "sugestao": "AÇÃO: Verifique na Etapa 10 se os valores de prestadores/MEI estão corretos (sem encargos)"
            })
            warnings += 1
        total_checks += 1
    else:
        validations.append({
            "status": "⚠️", 
            "item": "Nenhum funcionário cadastrado no DP", 
            "details": "Não é possível validar cálculos de folha",
            "sugestao": "AÇÃO: Acesse DP e Tributação para cadastrar funcionários ou Etapa 8 para planejar equipe"
        })
        warnings += 1
        total_checks += 1
    
    # 3.2 VALIDAÇÃO DE FATURAMENTO E TICKET MÉDIO
    ticket_medio = st.session_state.business_data.get('ticket_medio', 0)
    ticket_medio_esperado = st.session_state.business_data.get('ticket_medio_esperado', 0)
    clientes_mes = st.session_state.business_data.get('clientes_mes', 0)
    
    if ticket_medio > 0 and clientes_mes > 0:
        faturamento_calculado = ticket_medio * clientes_mes
        if vendas_mes_1 > 0:
            diferenca_faturamento = abs(faturamento_calculado - vendas_mes_1)
            tolerancia = vendas_mes_1 * 0.05  # 5% de tolerância
            
            if diferenca_faturamento <= tolerancia:
                validations.append({
                    "status": "✅", 
                    "item": "Faturamento matematicamente correto", 
                    "details": f"{format_currency(ticket_medio)} × {clientes_mes} clientes = {format_currency(faturamento_calculado)}",
                    "sugestao": "Cálculo: Ticket médio × Clientes/mês está consistente"
                })
                passed_checks += 1
            else:
                validations.append({
                    "status": "❌", 
                    "item": "Erro matemático no faturamento", 
                    "details": f"Calculado: {format_currency(faturamento_calculado)} ≠ Informado: {format_currency(vendas_mes_1)}",
                    "sugestao": "AÇÃO CRÍTICA: Vá para Etapa 10 → Corrija a fórmula: Faturamento = Ticket médio × Número de clientes. Valores devem ser consistentes."
                })
                errors += 1
        total_checks += 1
    
    # Verificar consistência entre tickets médios de diferentes etapas
    if ticket_medio > 0 and ticket_medio_esperado > 0:
        if abs(ticket_medio - ticket_medio_esperado) < 50:
            validations.append({
                "status": "✅", 
                "item": "Ticket médio sincronizado entre etapas", 
                "details": f"Etapa 3: {format_currency(ticket_medio_esperado)} = Etapa 10: {format_currency(ticket_medio)}"
            })
            passed_checks += 1
        else:
            validations.append({
                "status": "❌", 
                "item": "Tickets médios divergentes entre etapas", 
                "details": f"Etapa 3: {format_currency(ticket_medio_esperado)} ≠ Etapa 10: {format_currency(ticket_medio)}",
                "sugestao": "AÇÃO: Sincronize os valores na Etapa 3 (Ticket médio esperado) e Etapa 10 (Projeções). Devem ser iguais."
            })
            errors += 1
        total_checks += 1
    
    # 3.3 VALIDAÇÃO DE ENCARGOS E TRIBUTAÇÃO
    regime_tributario = st.session_state.business_data.get('regime_tributario', '')
    if regime_tributario and vendas_mes_1 > 0:
        if regime_tributario == 'Simples Nacional':
            # Simples Nacional - verificar alíquota
            anexo = st.session_state.business_data.get('anexo_simples', 'Anexo I')
            faturamento_anual = vendas_mes_1 * 12
            
            # Alíquotas aproximadas do Simples Nacional 2024
            if anexo == 'Anexo I' and faturamento_anual <= 180000:
                aliquota_esperada = 4.0  # Comércio
            elif anexo == 'Anexo III' and faturamento_anual <= 180000:
                aliquota_esperada = 6.0  # Serviços
            else:
                aliquota_esperada = 8.0  # Faixas superiores
            
            imposto_calculado = vendas_mes_1 * (aliquota_esperada / 100)
            imposto_informado = st.session_state.business_data.get('impostos', 0)
            
            if abs(imposto_calculado - imposto_informado) < 200:
                validations.append({
                    "status": "✅", 
                    "item": "Tributação Simples Nacional correta", 
                    "details": f"{anexo}: {aliquota_esperada}% = {format_currency(imposto_calculado)}",
                    "sugestao": f"Alíquota de {aliquota_esperada}% aplicada corretamente"
                })
                passed_checks += 1
            else:
                validations.append({
                    "status": "❌", 
                    "item": "Erro no cálculo tributário", 
                    "details": f"Esperado: {format_currency(imposto_calculado)} ({aliquota_esperada}%) ≠ Informado: {format_currency(imposto_informado)}",
                    "sugestao": "AÇÃO: Vá para DP e Tributação → Revise a alíquota do Simples Nacional. Para óticas, usar Anexo I (comércio) ou III (serviços)."
                })
                errors += 1
            total_checks += 1
    
    # 3.4 VALIDAÇÃO DE CUSTOS E MARGENS
    aluguel = st.session_state.business_data.get('aluguel', 0)
    if aluguel > 0 and vendas_mes_1 > 0:
        ratio_aluguel = (aluguel / vendas_mes_1) * 100
        if ratio_aluguel <= 15:
            validations.append({
                "status": "✅", 
                "item": "Aluguel proporcional à receita", 
                "details": f"{ratio_aluguel:.1f}% da receita (ideal: até 15%)",
                "sugestao": "Custo de aluguel dentro do recomendado para o setor óptico"
            })
            passed_checks += 1
        elif ratio_aluguel <= 25:
            validations.append({
                "status": "⚠️", 
                "item": "Aluguel elevado mas aceitável", 
                "details": f"{ratio_aluguel:.1f}% da receita (ideal: até 15%)",
                "sugestao": "ATENÇÃO: Aluguel alto pode pressionar margem. Considere negociar ou buscar localização alternativa."
            })
            warnings += 1
        else:
            validations.append({
                "status": "❌", 
                "item": "Aluguel muito alto - risco financeiro", 
                "details": f"{ratio_aluguel:.1f}% da receita (máximo recomendado: 15%)",
                "sugestao": "AÇÃO CRÍTICA: Renegocie aluguel ou busque novo ponto. Aluguel acima de 25% da receita compromete viabilidade."
            })
            errors += 1
        total_checks += 1
    
    # 3.5 ANÁLISE DE MARGEM DE PRODUTOS (EXEMPLO DETALHADO)
    produtos_cadastrados = st.session_state.business_data.get('produtos_servicos', [])
    if produtos_cadastrados:
        produto_exemplo = None
        for produto in produtos_cadastrados:
            if produto.get('preco_venda', 0) > 0 and produto.get('custo_unitario', 0) > 0:
                produto_exemplo = produto
                break
        
        if produto_exemplo:
            nome_produto = produto_exemplo.get('nome', 'Produto')
            preco_venda = produto_exemplo.get('preco_venda', 0)
            custo_unitario = produto_exemplo.get('custo_unitario', 0)
            
            margem_bruta = preco_venda - custo_unitario
            margem_percentual = (margem_bruta / preco_venda) * 100 if preco_venda > 0 else 0
            markup = (margem_bruta / custo_unitario) * 100 if custo_unitario > 0 else 0
            
            if margem_percentual >= 50:
                validations.append({
                    "status": "✅", 
                    "item": f"Margem adequada - {nome_produto}", 
                    "details": f"Custo: {format_currency(custo_unitario)} → Venda: {format_currency(preco_venda)} = {margem_percentual:.1f}% margem",
                    "sugestao": f"Markup: {markup:.1f}% - margem saudável para o setor óptico"
                })
                passed_checks += 1
            elif margem_percentual >= 30:
                validations.append({
                    "status": "⚠️", 
                    "item": f"Margem apertada - {nome_produto}", 
                    "details": f"Custo: {format_currency(custo_unitario)} → Venda: {format_currency(preco_venda)} = {margem_percentual:.1f}% margem",
                    "sugestao": "ATENÇÃO: Margem baixa. Para óticas, ideal é 50-60%. Revise preços ou fornecedores."
                })
                warnings += 1
            else:
                validations.append({
                    "status": "❌", 
                    "item": f"Margem insuficiente - {nome_produto}", 
                    "details": f"Custo: {format_currency(custo_unitario)} → Venda: {format_currency(preco_venda)} = {margem_percentual:.1f}% margem",
                    "sugestao": "AÇÃO CRÍTICA: Margem abaixo de 30% inviabiliza operação. Reavalie precificação na Etapa 5 ou Sistema de Precificação."
                })
                errors += 1
            total_checks += 1
        else:
            validations.append({
                "status": "⚠️", 
                "item": "Produtos sem custos/preços definidos", 
                "details": "Não é possível validar margens",
                "sugestao": "AÇÃO: Vá para Etapa 5 ou Sistema de Precificação para definir custos e preços de venda"
            })
            warnings += 1
            total_checks += 1
    
    # 3.6 VALIDAÇÃO DE CUSTOS FIXOS TOTAIS
    aluguel = st.session_state.business_data.get('aluguel', 0)
    salarios_total = st.session_state.business_data.get('salarios_total', 0)
    outros_custos = st.session_state.business_data.get('outros_custos_fixos', 0)
    
    if aluguel > 0 and salarios_total > 0:
        custo_fixo_total = aluguel + salarios_total + outros_custos
        if vendas_mes_1 > 0:
            ratio_custo = (custo_fixo_total / vendas_mes_1) * 100
            if ratio_custo <= 60:
                validations.append({
                    "status": "✅", 
                    "item": "Estrutura de custos equilibrada", 
                    "details": f"Custos fixos: {ratio_custo:.1f}% da receita (ideal: até 60%)",
                    "sugestao": f"Aluguel: {format_currency(aluguel)} + Folha: {format_currency(salarios_total)} + Outros: {format_currency(outros_custos)}"
                })
                passed_checks += 1
            elif ratio_custo <= 80:
                validations.append({
                    "status": "⚠️", 
                    "item": "Custos fixos elevados", 
                    "details": f"{ratio_custo:.1f}% da receita (ideal: até 60%)",
                    "sugestao": "ATENÇÃO: Estrutura de custos pesada. Considere otimizar folha ou renegociar aluguel."
                })
                warnings += 1
            else:
                validations.append({
                    "status": "❌", 
                    "item": "Custos fixos excessivos", 
                    "details": f"{ratio_custo:.1f}% da receita - risco alto de prejuízo",
                    "sugestao": "AÇÃO CRÍTICA: Custos fixos acima de 80% são insustentáveis. Reavalie toda estrutura de custos."
                })
                errors += 1
        else:
            validations.append({
                "status": "⚠️", 
                "item": "Custos definidos mas receita não", 
                "details": "Configure vendas na Etapa 10",
                "sugestao": "AÇÃO: Defina metas de faturamento para validar proporção de custos"
            })
            warnings += 1
    else:
        validations.append({"status": "❌", "item": "Custos fixos não definidos", "details": "Configure aluguel e folha na Etapa 10"})
        errors += 1
    total_checks += 1
    
    # 4. VALIDAÇÃO DE PESSOAL
    st.subheader("👥 4. Gestão de Pessoas")
    
    if hasattr(st.session_state, 'funcionarios') and st.session_state.funcionarios:
        num_funcionarios = len(st.session_state.funcionarios)
        funcionarios_clt = [f for f in st.session_state.funcionarios if f['tipo_contrato'] == 'CLT']
        
        if num_funcionarios >= 2:
            validations.append({"status": "✅", "item": "Equipe dimensionada", "details": f"{num_funcionarios} funcionários cadastrados"})
            passed_checks += 1
        else:
            validations.append({"status": "⚠️", "item": "Equipe pequena", "details": f"Apenas {num_funcionarios} funcionário(s)"})
            warnings += 1
        
        # Verificar se há optometrista
        tem_optometrista = any('optom' in f['cargo'].lower() for f in st.session_state.funcionarios)
        if tem_optometrista:
            validations.append({"status": "✅", "item": "Optometrista cadastrado", "details": "Essencial para ótica"})
            passed_checks += 1
        else:
            validations.append({"status": "❌", "item": "Optometrista não encontrado", "details": "Obrigatório para óticas"})
            errors += 1
        
        total_checks += 2
    else:
        validations.append({"status": "❌", "item": "Nenhum funcionário cadastrado", "details": "Configure no DP e Tributação"})
        errors += 1
        total_checks += 1
    
    # 5. VALIDAÇÃO DE MERCADO
    st.subheader("🎯 5. Análise de Mercado")
    
    cidade = st.session_state.business_data.get('cidade', '')
    estado = st.session_state.business_data.get('estado', '')
    if cidade and estado:
        validations.append({"status": "✅", "item": "Localização definida", "details": f"{cidade}, {estado}"})
        passed_checks += 1
    else:
        validations.append({"status": "❌", "item": "Localização não definida", "details": "Configure na Etapa 2"})
        errors += 1
    total_checks += 1
    
    # Verificar múltiplos campos do público-alvo
    faixa_etaria = st.session_state.business_data.get('faixa_etaria_principal', [])
    classe_social = st.session_state.business_data.get('classe_social', [])
    perfil_profissional = st.session_state.business_data.get('perfil_profissional', [])
    necessidades = st.session_state.business_data.get('necessidades_principais', [])
    
    if faixa_etaria or classe_social or perfil_profissional or necessidades:
        detalhes_publico = []
        if faixa_etaria:
            detalhes_publico.append(f"Idade: {', '.join(faixa_etaria[:2])}")
        if classe_social:
            detalhes_publico.append(f"Classe: {', '.join(classe_social[:2])}")
        if perfil_profissional:
            detalhes_publico.append(f"Perfil: {', '.join(perfil_profissional[:2])}")
        
        validations.append({"status": "✅", "item": "Público-alvo definido", "details": "; ".join(detalhes_publico)})
        passed_checks += 1
    else:
        validations.append({"status": "⚠️", "item": "Público-alvo não definido", "details": "Configure na Etapa 3"})
        warnings += 1
    total_checks += 1
    
    # 6. VALIDAÇÃO DE PRODUTOS
    st.subheader("🛍️ 6. Produtos e Serviços")
    
    ticket_medio = st.session_state.business_data.get('ticket_medio', 0)
    if ticket_medio > 0:
        if ticket_medio >= 150:
            validations.append({"status": "✅", "item": "Ticket médio competitivo", "details": f"{format_currency(ticket_medio)}"})
            passed_checks += 1
        else:
            validations.append({"status": "⚠️", "item": "Ticket médio baixo", "details": f"{format_currency(ticket_medio)} - considere aumentar"})
            warnings += 1
    else:
        validations.append({"status": "❌", "item": "Ticket médio não definido", "details": "Configure na Etapa 5"})
        errors += 1
    total_checks += 1
    
    # 7. VALIDAÇÃO MATEMÁTICA RIGOROSA
    st.subheader("🔍 7. Análise Matemática Crítica")
    
    objetivo_faturamento = st.session_state.business_data.get('objetivo_faturamento', 0)
    aluguel = st.session_state.business_data.get('aluguel', 0)
    salarios_total = st.session_state.business_data.get('salarios_total', 0)
    investimento_total = st.session_state.business_data.get('investimento_total', 0)
    area_loja = st.session_state.business_data.get('area_loja', 0)
    num_funcionarios = len(st.session_state.funcionarios) if hasattr(st.session_state, 'funcionarios') else 0
    
    # VALIDAÇÃO 1: Realismo do faturamento por vendas/dia
    if objetivo_faturamento > 0 and ticket_medio > 0:
        vendas_mes = objetivo_faturamento / ticket_medio
        vendas_dia_util = vendas_mes / 26  # 26 dias úteis
        vendas_sabado = vendas_dia_util * 1.5  # Sábados são mais movimentados
        
        if vendas_dia_util > 12:
            validations.append({
                "status": "❌", 
                "item": "CRÍTICO: Meta inviável operacionalmente", 
                "details": f"{vendas_dia_util:.1f} vendas/dia útil impossível para ótica",
                "sugestao": f"CORREÇÃO URGENTE: Vá para Etapa 1 → 'Meta de faturamento mensal' e reduza de {format_currency(objetivo_faturamento)} para no máximo {format_currency(12 * 26 * ticket_medio)}. OU vá para Etapa 5 → 'Faixa de preços' e aumente o ticket médio de {format_currency(ticket_medio)} para pelo menos {format_currency(objetivo_faturamento / (12 * 26))}."
            })
            errors += 1
        elif vendas_dia_util > 8:
            validations.append({
                "status": "⚠️", 
                "item": "Meta muito desafiadora", 
                "details": f"{vendas_dia_util:.1f} vendas/dia útil requer equipe experiente",
                "sugestao": f"OTIMIZAÇÃO: Para facilitar o alcance da meta, considere: 1) Aumentar ticket médio na Etapa 5 de {format_currency(ticket_medio)} para {format_currency(objetivo_faturamento / (6 * 26))}, OU 2) Contratar mais vendedores na Etapa 8, OU 3) Reduzir meta para {format_currency(6 * 26 * ticket_medio)} na Etapa 1."
            })
            warnings += 1
        else:
            validations.append({
                "status": "✅", 
                "item": "Meta operacionalmente viável", 
                "details": f"{vendas_dia_util:.1f} vendas/dia útil",
                "sugestao": "Meta realista para operação de ótica"
            })
            passed_checks += 1
        total_checks += 1
        
        # VALIDAÇÃO 2: Capacidade por funcionário
        if num_funcionarios > 0:
            vendas_por_funcionario_dia = vendas_dia_util / num_funcionarios
            if vendas_por_funcionario_dia > 4:
                validations.append({"status": "❌", "item": "CRÍTICO: Equipe insuficiente", "details": f"{vendas_por_funcionario_dia:.1f} vendas/funcionário/dia (máximo: 4)"})
                errors += 1
            elif vendas_por_funcionario_dia > 3:
                validations.append({"status": "⚠️", "item": "Equipe no limite", "details": f"{vendas_por_funcionario_dia:.1f} vendas/funcionário/dia"})
                warnings += 1
            else:
                validations.append({"status": "✅", "item": "Equipe adequada", "details": f"{vendas_por_funcionario_dia:.1f} vendas/funcionário/dia"})
                passed_checks += 1
            total_checks += 1
    
    # VALIDAÇÃO 3: Análise crítica do ticket médio
    if ticket_medio > 0:
        if ticket_medio < 100:
            validations.append({
                "status": "❌", 
                "item": "CRÍTICO: Ticket médio inviável", 
                "details": f"{format_currency(ticket_medio)} impossível cobrir custos",
                "sugestao": f"AÇÃO CRÍTICA: Vá para Etapa 5 → Produtos e Serviços → 'Faixa de preços mais vendida' e selecione pelo menos 'R$ 150 - R$ 299'. Com {format_currency(ticket_medio)}, nem conseguirá pagar um funcionário (salário mínimo + encargos = R$ 2.550/mês ÷ 100 vendas = R$ 25,50 só de mão de obra por venda)."
            })
            errors += 1
        elif ticket_medio < 200:
            validations.append({
                "status": "⚠️", 
                "item": "Ticket médio muito baixo", 
                "details": f"{format_currency(ticket_medio)} dificulta rentabilidade",
                "sugestao": f"MELHORIA: Vá para Etapa 5 → 'Faixa de preços mais vendida' e considere aumentar para 'R$ 200 - R$ 399'. Para referência: óticas bem-sucedidas têm ticket médio de R$ 250-400. Inclua mais serviços como consultas, tratamentos de lente ou acessórios."
            })
            warnings += 1
        elif ticket_medio > 1000:
            validations.append({
                "status": "⚠️", 
                "item": "Ticket médio muito alto", 
                "details": f"{format_currency(ticket_medio)} pode reduzir demanda drasticamente",
                "sugestao": f"CUIDADO: Ticket de {format_currency(ticket_medio)} é muito alto para maioria dos brasileiros. Vá para Etapa 5 → 'Faixa de preços' e considere oferecer opções mais acessíveis (R$ 300-600). OU vá para Etapa 3 → Público-Alvo e certifique-se de focar em classes A/B que podem pagar estes valores."
            })
            warnings += 1
        else:
            validations.append({
                "status": "✅", 
                "item": "Ticket médio realista", 
                "details": f"{format_currency(ticket_medio)} dentro da faixa viável",
                "sugestao": "Ticket médio adequado para o mercado brasileiro de óticas"
            })
            passed_checks += 1
        total_checks += 1
    
    # VALIDAÇÃO 4: Estrutura de custos vs faturamento
    if objetivo_faturamento > 0:
        custos_fixos_principais = aluguel + salarios_total
        if custos_fixos_principais > 0:
            percentual_custos_fixos = (custos_fixos_principais / objetivo_faturamento) * 100
            
            if percentual_custos_fixos > 75:
                validations.append({"status": "❌", "item": "CRÍTICO: Estrutura de custos insustentável", "details": f"{percentual_custos_fixos:.1f}% em custos fixos (máximo viável: 60%)"})
                errors += 1
            elif percentual_custos_fixos > 60:
                validations.append({"status": "⚠️", "item": "Custos fixos excessivos", "details": f"{percentual_custos_fixos:.1f}% do faturamento (ideal: <50%)"})
                warnings += 1
            else:
                validations.append({"status": "✅", "item": "Estrutura de custos saudável", "details": f"{percentual_custos_fixos:.1f}% em custos fixos"})
                passed_checks += 1
            total_checks += 1
        
        # VALIDAÇÃO 5: Aluguel específico
        if aluguel > 0:
            percentual_aluguel = (aluguel / objetivo_faturamento) * 100
            if percentual_aluguel > 20:
                validations.append({
                    "status": "❌", 
                    "item": "CRÍTICO: Aluguel proibitivo", 
                    "details": f"{percentual_aluguel:.1f}% do faturamento (máximo: 15%)",
                    "sugestao": f"CORREÇÃO: Vá para Etapa 10 → Projeções Financeiras → aba 'Estrutura de Custos' → campo 'Aluguel (R$)' e reduza de {format_currency(aluguel)} para no máximo {format_currency(objetivo_faturamento * 0.15)}. OU aumente a meta de faturamento na Etapa 1 para pelo menos {format_currency(aluguel / 0.15)}."
                })
                errors += 1
            elif percentual_aluguel > 12:
                validations.append({
                    "status": "⚠️", 
                    "item": "Aluguel elevado", 
                    "details": f"{percentual_aluguel:.1f}% do faturamento (ideal: <10%)",
                    "sugestao": f"OTIMIZAÇÃO: Vá para Etapa 10 → Projeções Financeiras → aba 'Estrutura de Custos' → reduza aluguel de {format_currency(aluguel)} para {format_currency(objetivo_faturamento * 0.10)} ou negocie um local mais barato."
                })
                warnings += 1
            else:
                validations.append({
                    "status": "✅", 
                    "item": "Aluguel proporcional", 
                    "details": f"{percentual_aluguel:.1f}% do faturamento",
                    "sugestao": "Proporção adequada entre aluguel e receita projetada"
                })
                passed_checks += 1
            total_checks += 1
    
    # VALIDAÇÃO 6: Análise de área vs faturamento
    if area_loja > 0 and objetivo_faturamento > 0:
        faturamento_por_m2 = objetivo_faturamento / area_loja
        if faturamento_por_m2 < 500:
            validations.append({"status": "❌", "item": "CRÍTICO: Produtividade por m² muito baixa", "details": f"{format_currency(faturamento_por_m2)}/m² (mínimo: R$ 800/m²)"})
            errors += 1
        elif faturamento_por_m2 < 800:
            validations.append({"status": "⚠️", "item": "Produtividade por m² baixa", "details": f"{format_currency(faturamento_por_m2)}/m² (ideal: >R$ 1.200/m²)"})
            warnings += 1
        else:
            validations.append({"status": "✅", "item": "Produtividade por m² adequada", "details": f"{format_currency(faturamento_por_m2)}/m²"})
            passed_checks += 1
        total_checks += 1
    
    # VALIDAÇÃO 7: Payback realista
    if investimento_total > 0 and objetivo_faturamento > 0:
        margem_liquida_conservadora = 0.15  # 15% margem líquida realista
        lucro_mensal = objetivo_faturamento * margem_liquida_conservadora
        payback_meses = investimento_total / lucro_mensal if lucro_mensal > 0 else 999
        
        if payback_meses > 48:
            validations.append({"status": "❌", "item": "CRÍTICO: Payback proibitivo", "details": f"{payback_meses:.0f} meses (máximo aceitável: 36 meses)"})
            errors += 1
        elif payback_meses > 30:
            validations.append({"status": "⚠️", "item": "Payback elevado", "details": f"{payback_meses:.0f} meses (ideal: <24 meses)"})
            warnings += 1
        else:
            validations.append({"status": "✅", "item": "Payback atrativo", "details": f"{payback_meses:.0f} meses"})
            passed_checks += 1
        total_checks += 1
    
    # VALIDAÇÃO 8: Capital de giro vs faturamento
    if investimento_total > 0 and objetivo_faturamento > 0:
        capital_giro_necessario = objetivo_faturamento * 2  # 2 meses de faturamento
        if investimento_total < capital_giro_necessario:
            deficit_capital = capital_giro_necessario - investimento_total
            validations.append({
                "status": "❌", 
                "item": "CRÍTICO: Capital de giro insuficiente", 
                "details": f"Faltam {format_currency(deficit_capital)} para 2 meses de operação",
                "sugestao": f"CORREÇÃO URGENTE: Vá para Etapa 9 → Investimento Inicial → role até o final → campo 'Investimento total' e aumente de {format_currency(investimento_total)} para pelo menos {format_currency(capital_giro_necessario)}. Você precisa de dinheiro suficiente para operar 2 meses sem faturar nada (período de adaptação inicial)."
            })
            errors += 1
        else:
            validations.append({
                "status": "✅", 
                "item": "Capital de giro adequado", 
                "details": f"Cobertura para {investimento_total/objetivo_faturamento:.1f} meses",
                "sugestao": "Capital suficiente para operação inicial segura"
            })
            passed_checks += 1
        total_checks += 1
    
    # VALIDAÇÃO 9: Viabilidade final integrada
    # Definir custo_fixo_total se não foi definido na validação anterior
    if 'custo_fixo_total' not in locals():
        custo_fixo_total = aluguel + salarios_total + outros_custos
    
    if vendas_mes_1 > 0 and custo_fixo_total > 0:
        # Ponto de equilíbrio com margem realista de 35%
        ponto_equilibrio = custo_fixo_total / 0.35
        
        if vendas_mes_1 >= ponto_equilibrio:
            margem_seguranca = ((vendas_mes_1 - ponto_equilibrio) / ponto_equilibrio) * 100
            if margem_seguranca > 30:
                validations.append({"status": "✅", "item": "Negócio matematicamente viável", "details": f"{margem_seguranca:.0f}% acima do ponto de equilíbrio"})
                passed_checks += 1
            else:
                validations.append({"status": "⚠️", "item": "Viabilidade limitada", "details": f"Apenas {margem_seguranca:.0f}% acima do equilíbrio"})
                warnings += 1
        else:
            deficit = ponto_equilibrio - vendas_mes_1
            percentual_deficit = (deficit / ponto_equilibrio) * 100
            validations.append({
                "status": "❌", 
                "item": "CRÍTICO: Negócio matematicamente inviável", 
                "details": f"{percentual_deficit:.0f}% abaixo do ponto de equilíbrio",
                "sugestao": f"CORREÇÃO CRÍTICA: Suas vendas previstas ({format_currency(vendas_mes_1)}) estão muito abaixo dos custos ({format_currency(ponto_equilibrio)}). Vá para Etapa 10 → Projeções Financeiras → aba 'DRE Mês a Mês' → linha 'Vendas mês 1' e verifique seus números. SOLUÇÕES: 1) Aumente ticket médio na Etapa 5, 2) Reduza custos fixos (aluguel/salários) na Etapa 10, ou 3) Aumente meta de faturamento na Etapa 1."
            })
            errors += 1
        total_checks += 1
    else:
        validations.append({"status": "❌", "item": "CRÍTICO: Dados insuficientes para análise", "details": "Impossível validar viabilidade matemática"})
        errors += 1
        total_checks += 1
    
    # RESUMO EXECUTIVO CRÍTICO
    st.markdown("---")
    st.subheader("📋 Resumo Executivo da Auditoria")
    
    # Calcular porcentagem de conclusão
    completion_percentage = (passed_checks / total_checks) * 100 if total_checks > 0 else 0
    
    # Determinar status geral e recomendação
    if errors > 3:
        status_geral = "🔴 CRÍTICO"
        recomendacao = "PARE: O plano apresenta problemas matemáticos graves que tornam o negócio inviável. Revise fundamentalmente a estrutura financeira antes de prosseguir."
        cor_status = "red"
    elif errors > 0:
        status_geral = "🟡 ALTO RISCO"
        recomendacao = "CUIDADO: Existem problemas críticos que podem comprometer a viabilidade. Ajuste os itens marcados como críticos antes de investir."
        cor_status = "orange"
    elif warnings > 4:
        status_geral = "🟡 MODERADO"
        recomendacao = "ATENÇÃO: O plano tem potencial, mas requer ajustes importantes para maximizar as chances de sucesso."
        cor_status = "orange"
    elif warnings > 0:
        status_geral = "🟢 VIÁVEL"
        recomendacao = "BOM: O negócio é matematicamente viável, mas algumas otimizações podem melhorar a performance."
        cor_status = "green"
    else:
        status_geral = "🟢 EXCELENTE"
        recomendacao = "ÓTIMO: O plano está bem estruturado matematicamente e apresenta alta probabilidade de sucesso."
        cor_status = "green"
    
    # Exibir status principal
    st.markdown(f"""
    <div style="background-color: {cor_status}; padding: 20px; border-radius: 10px; margin: 10px 0;">
        <h3 style="color: white; margin: 0;">{status_geral}</h3>
        <p style="color: white; margin: 10px 0 0 0; font-size: 16px;">{recomendacao}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Métricas detalhadas
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("✅ Aprovadas", passed_checks, f"{completion_percentage:.0f}%")
    
    with col2:
        st.metric("⚠️ Atenção", warnings)
    
    with col3:
        st.metric("❌ Críticas", errors)
    
    with col4:
        st.metric("📊 Total", total_checks)
    
    # Status geral
    if completion_percentage >= 80 and errors == 0:
        st.success("🎉 Excelente! Seu plano está bem estruturado e pronto para implementação.")
    elif completion_percentage >= 60 and errors <= 2:
        st.warning("⚡ Bom progresso! Algumas melhorias são necessárias antes de implementar.")
    else:
        st.error("🚨 Atenção! Várias questões críticas precisam ser resolvidas antes de prosseguir.")
    
    # Barra de progresso
    st.progress(completion_percentage / 100)
    st.caption(f"Plano {completion_percentage:.0f}% completo e validado")
    
    # Detalhes das validações
    st.markdown("### 📋 Detalhes da Auditoria")
    
    for validation in validations:
        with st.expander(f"{validation['status']} {validation['item']}", expanded=(validation['status'] == "❌")):
            st.write(f"**Detalhes:** {validation['details']}")
            if 'sugestao' in validation and validation['sugestao']:
                if validation['status'] == "❌":
                    st.error(f"**🎯 {validation['sugestao']}**")
                elif validation['status'] == "⚠️":
                    st.warning(f"**💡 {validation['sugestao']}**")
                else:
                    st.info(f"**✓ {validation['sugestao']}**")
    
    # SEÇÃO DE PRÓXIMOS PASSOS RECOMENDADOS
    if errors > 0 or warnings > 0:
        st.markdown("---")
        st.markdown("### 🎯 Próximos Passos Recomendados")
        
        # Priorizar ações por criticidade
        acoes_criticas = [v for v in validations if v['status'] == "❌" and 'sugestao' in v]
        acoes_melhorias = [v for v in validations if v['status'] == "⚠️" and 'sugestao' in v]
        
        if acoes_criticas:
            st.error("**🚨 QUESTÕES CRÍTICAS (resolver primeiro):**")
            for i, acao in enumerate(acoes_criticas[:3], 1):
                st.write(f"• {acao['item']}: {acao['sugestao']}")
        
        if acoes_melhorias:
            st.warning("**⚡ MELHORIAS RECOMENDADAS:**")
            for i, acao in enumerate(acoes_melhorias[:3], 1):
                st.write(f"• {acao['item']}: {acao['sugestao']}")
    else:
        st.success("🎉 **Parabéns!** Seu plano passou em todas as validações críticas!")
    
    # Recomendações antigas (manter por compatibilidade)
    st.markdown("### 💡 Outras Recomendações")
    
    if errors > 0:
        st.markdown("**🔴 Questões Críticas (resolver primeiro):**")
        for validation in validations:
            if validation['status'] == '❌':
                st.write(f"• {validation['item']}: {validation['details']}")
    
    if warnings > 0:
        st.markdown("**🟡 Melhorias Sugeridas:**")
        for validation in validations:
            if validation['status'] == '⚠️':
                st.write(f"• {validation['item']}: {validation['details']}")
    
    if completion_percentage >= 80:
        st.markdown("**🟢 Plano Aprovado - Próximas Ações:**")
        st.write("• Revisar cronograma de implementação")
        st.write("• Buscar financiamento se necessário")
        st.write("• Iniciar processo de abertura da empresa")
        st.write("• Começar negociações com fornecedores")


def show_fluxo_vital_tool():
    """Fluxo Vital - Guia Prático Passo a Passo para Abrir uma Ótica"""
    
    # Header with back button
    col1, col2 = st.columns([1, 6])
    with col1:
        if st.button("⬅️ Voltar", key="back_fluxo_vital"):
            st.session_state.show_fluxo_vital = False
            st.rerun()
    
    with col2:
        st.title("🚀 Fluxo Vital - Guia Prático para Sua Ótica")
        st.markdown("**Checklist operacional desde a ideia até o primeiro giro**")
    
    # Recuperar APENAS dados reais do sistema - sem valores fictícios
    investimento_total = st.session_state.business_data.get('investimento_total', 0)
    capital_giro = st.session_state.business_data.get('capital_giro', 0)
    receita_mes_1 = st.session_state.business_data.get('vendas_mes_1', 0) or st.session_state.business_data.get('receita_mensal', 0)
    
    # Investimento detalhado (dados reais dos campos do sistema)
    reforma_loja = st.session_state.business_data.get('reforma_loja', 0)
    equipamentos_moveis = st.session_state.business_data.get('equipamentos_moveis', 0)
    mobiliario_decoracao = st.session_state.business_data.get('mobiliario_decoracao', 0)
    sistema_eletrico = st.session_state.business_data.get('sistema_eletrico', 0)
    consultorio_exames = st.session_state.business_data.get('consultorio_exames', 0)
    area_vendas_estoque = st.session_state.business_data.get('area_vendas_estoque', 0)
    total_infraestrutura = reforma_loja + equipamentos_moveis + mobiliario_decoracao + sistema_eletrico + consultorio_exames + area_vendas_estoque
    
    # Custos mensais reais do sistema
    aluguel = st.session_state.business_data.get('aluguel', 0)
    agua_luz = st.session_state.business_data.get('agua_luz', 0)
    telefone_internet = st.session_state.business_data.get('telefone_internet', 0)  
    marketing = st.session_state.business_data.get('marketing', 0)
    outros_fixos = st.session_state.business_data.get('outros_fixos', 0)
    # Removed invalid assignment
    folha_mensal = st.session_state.business_data.get('salarios_total', 0)
    
    custos_operacionais = aluguel + agua_luz + telefone_internet + marketing + outros_fixos + 0
    custo_total_mensal = folha_mensal + custos_operacionais
    
    st.info(f"""
    💰 **Recursos Necessários (baseados no seu plano):**
    - Investimento inicial: R$ {investimento_total:,.0f}
    - Capital de giro: R$ {capital_giro:,.0f}
    - Infraestrutura total: R$ {total_infraestrutura:,.0f} (Reforma: R$ {reforma_loja:,.0f} + Equipamentos: R$ {equipamentos_moveis:,.0f} + Móveis: R$ {mobiliario_decoracao:,.0f})
    - Custo mensal: R$ {custo_total_mensal:,.0f}
    - Meta de receita: R$ {receita_mes_1:,.0f}/mês
    """)
    
    # Etapas do fluxo vital
    etapas = [
        {
            "fase": "💡 PLANEJAMENTO",
            "titulo": "1. Definição do Negócio",
            "saldo_inicial": capital_giro,
            "gastos": 0,
            "descricao": "Validar o conceito e definir estratégia",
            "acoes": [
                "✅ Pesquisar mercado local e concorrência",
                "✅ Definir público-alvo e posicionamento",
                "✅ Elaborar plano de negócios (você já fez!)",
                "✅ Projetar fluxo de caixa para 12 meses"
            ]
        },
        {
            "fase": "📋 LEGALIZAÇÃO",
            "titulo": "2. Abertura da Empresa",
            "saldo_inicial": capital_giro,
            "gastos": st.session_state.business_data.get('custos_abertura_empresa', 0),
            "descricao": "Formalizar o negócio e obter licenças",
            "acoes": [
                f"💰 Custos de abertura: {format_currency(st.session_state.business_data.get('custos_abertura_empresa', 0))}",
                f"📄 Regime tributário: {st.session_state.business_data.get('regime_tributario', 'Não definido')}",
                "📄 Obter CNPJ e inscrições estadual/municipal",
                "📄 Alvará de funcionamento e sanitário"
            ]
        },
        {
            "fase": "🏢 INFRAESTRUTURA",
            "titulo": "3. Montagem do Espaço",
            "saldo_inicial": capital_giro - st.session_state.business_data.get('custos_abertura_empresa', 0),
            "gastos": total_infraestrutura,
            "descricao": "Preparar o ponto comercial",
            "acoes": [
                f"💰 Reforma do espaço: {format_currency(reforma_loja)}" if reforma_loja > 0 else "• Reforma não planejada",
                f"💰 Equipamentos básicos: {format_currency(equipamentos_moveis)}" if equipamentos_moveis > 0 else "• Equipamentos não planejados",
                f"💰 Mobiliário e decoração: {format_currency(mobiliario_decoracao)}" if mobiliario_decoracao > 0 else "• Mobiliário não planejado",
                f"💰 Sistema elétrico: {format_currency(sistema_eletrico)}" if sistema_eletrico > 0 else "• Sistema elétrico não planejado",
                f"💰 Consultório exames: {format_currency(consultorio_exames)}" if consultorio_exames > 0 else "• Consultório não planejado",
                f"💰 Área vendas/estoque: {format_currency(area_vendas_estoque)}" if area_vendas_estoque > 0 else "• Área de vendas não planejada"
            ]
        },
        {
            "fase": "📦 ESTOQUE",
            "titulo": "4. Compra do Estoque Inicial",
            "saldo_inicial": capital_giro - st.session_state.business_data.get('custos_abertura_empresa', 0) - total_infraestrutura,
            "gastos": st.session_state.business_data.get('estoque_inicial', 0),
            "descricao": "Adquirir produtos para venda",
            "acoes": [
                f"💰 Estoque inicial: {format_currency(st.session_state.business_data.get('estoque_inicial', 0))}" if st.session_state.business_data.get('estoque_inicial', 0) > 0 else "• Estoque inicial não definido",
                f"📦 Fornecedores configurados: {', '.join(st.session_state.business_data.get('fornecedores_selecionados', ['Não definidos']))}",
                f"📦 Prazo pagamento: {st.session_state.business_data.get('forma_pagamento_fornecedor', 'Não definido')}",
                "📦 Organizar sistema de controle de estoque"
            ]
        },
        {
            "fase": "👥 EQUIPE",
            "titulo": "5. Contratação de Funcionários",
            "saldo_inicial": capital_giro - st.session_state.business_data.get('custos_abertura_empresa', 0) - total_infraestrutura - st.session_state.business_data.get('estoque_inicial', 0),
            "gastos": folha_mensal,
            "descricao": "Formar a equipe de trabalho",
            "acoes": [
                f"💰 Folha mensal: {format_currency(folha_mensal)}" if folha_mensal > 0 else "• Equipe não definida",
                "👥 Funcionários planejados no DP e Tributação",
                "📚 Treinamento da equipe em produtos",
                "📚 Capacitação em atendimento ao cliente"
            ]
        }
    ]
    
    # Exibir etapas em formato de timeline
    st.markdown("### 🛣️ Cronograma de Execução")
    
    saldo_atual = capital_giro
    
    for i, etapa in enumerate(etapas):
        # Card para cada etapa
        with st.expander(f"{etapa['fase']} - {etapa['titulo']}", expanded=i==0):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**{etapa['descricao']}**")
                
                for acao in etapa['acoes']:
                    if acao.startswith('💰'):
                        st.markdown(f"<span style='color: red'>{acao}</span>", unsafe_allow_html=True)
                    else:
                        st.markdown(acao)
            
            with col2:
                saldo_antes = saldo_atual
                saldo_atual -= etapa['gastos']
                
                st.metric("Saldo Inicial", f"R$ {saldo_antes:,.0f}")
                if etapa['gastos'] > 0:
                    st.metric("Gastos", f"R$ {etapa['gastos']:,.0f}", delta=f"-{etapa['gastos']:,.0f}")
                st.metric("Saldo Final", f"R$ {saldo_atual:,.0f}")
                
                if saldo_atual < 0:
                    st.error("⚠️ Saldo insuficiente!")
                elif saldo_atual < 5000:
                    st.warning("⚠️ Reserva baixa")
                else:
                    st.success("✅ Recursos OK")
    
    st.markdown("---")
    
    # Simulação do primeiro mês operacional
    st.markdown("### 💼 Primeiro Mês de Operação")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🔄 Ciclo Operacional Mensal**")
        
        # Entradas
        st.markdown("**ENTRADAS:**")
        vendas_vista = receita_mes_1 * 0.7
        st.write(f"• Vendas à vista (70%): R$ {vendas_vista:,.0f}")
        st.write(f"• Total de entrada: R$ {vendas_vista:,.0f}")
        
        # Saídas
        st.markdown("**SAÍDAS:**")
        
        # Calcular CMV real baseado nos custos de materiais da precificação
        custo_materiais_fisicos = st.session_state.business_data.get('custo_materiais_fisicos', 89.80)
        ticket_medio = st.session_state.business_data.get('ticket_medio', 180)
        vendas_quantidade = receita_mes_1 / ticket_medio if ticket_medio > 0 else 0
        cmv_real = custo_materiais_fisicos * vendas_quantidade
        percentual_cmv = (cmv_real / receita_mes_1 * 100) if receita_mes_1 > 0 else 0
        
        impostos = receita_mes_1 * 0.06
        st.write(f"• Fornecedores ({percentual_cmv:.1f}%): R$ {cmv_real:,.0f}")
        st.caption(f"   Baseado em: {vendas_quantidade:.0f} óculos × R$ {custo_materiais_fisicos:.2f} custo real")
        st.write(f"• Impostos (6%): R$ {impostos:,.0f}")
        st.write(f"• Folha de pagamento: R$ {folha_mensal:,.0f}")
        st.write(f"• Aluguel: R$ {aluguel:,.0f}")
        st.write(f"• Outros custos: R$ {custos_operacionais - aluguel:,.0f}")
        
        total_saidas = cmv_real + impostos + folha_mensal + custos_operacionais
        st.write(f"• **Total de saídas: R$ {total_saidas:,.0f}**")
    
    with col2:
        st.markdown("**📊 Resultado do Mês**")
        
        fluxo_mes = vendas_vista - total_saidas
        
        if fluxo_mes > 0:
            st.success(f"✅ Fluxo positivo: R$ {fluxo_mes:,.0f}")
            st.write("🎉 Parabéns! Seu primeiro mês será lucrativo")
        else:
            st.error(f"❌ Fluxo negativo: R$ {fluxo_mes:,.0f}")
            st.write("⚠️ Atenção: revisar estratégia de vendas")
        
        saldo_final_mes = saldo_atual + fluxo_mes
        st.metric("Saldo após 1º mês", f"R$ {saldo_final_mes:,.0f}")
        
        # Meta para equilíbrio
        if fluxo_mes < 0:
            vendas_necessarias = total_saidas / 0.7
            st.write(f"💡 **Vendas necessárias:** R$ {vendas_necessarias:,.0f}")
            diferenca = vendas_necessarias - receita_mes_1
            st.write(f"📈 **Aumentar vendas em:** R$ {diferenca:,.0f}")
    
    # Dicas práticas
    st.markdown("---")
    st.markdown("### 💡 Dicas para o Sucesso")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**🎯 Vendas**")
        st.write("• Foque em serviços completos")
        st.write("• Ofereça exames gratuitos")
        st.write("• Crie pacotes promocionais")
        st.write("• Invista em marketing digital")
    
    with col2:
        st.markdown("**💰 Financeiro**")
        st.write("• Monitore fluxo de caixa diário")
        st.write("• Negocie prazos com fornecedores")
        st.write("• Controle rigorosamente custos")
        st.write("• Mantenha reserva de emergência")
    
    with col3:
        st.markdown("**👥 Operacional**")
        st.write("• Treine equipe continuamente")
        st.write("• Mantenha estoque organizado")
        st.write("• Acompanhe satisfação clientes")
        st.write("• Invista em equipamentos qualidade")
    
    # Cronograma de 90 dias
    st.markdown("---")
    st.markdown("### 📅 Primeiros 90 Dias")
    
    meses_90_dias = [
        {
            "mes": "Mês 1",
            "foco": "Estabilização",
            "meta_vendas": receita_mes_1,
            "acoes": ["Inauguração", "Campanhas de lançamento", "Networking local"]
        },
        {
            "mes": "Mês 2", 
            "foco": "Crescimento",
            "meta_vendas": receita_mes_1 * 1.1,
            "acoes": ["Fidelização clientes", "Parcerias médicos", "Marketing digital"]
        },
        {
            "mes": "Mês 3",
            "foco": "Consolidação", 
            "meta_vendas": receita_mes_1 * 1.2,
            "acoes": ["Avaliar resultados", "Ajustar estratégias", "Planejar expansão"]
        }
    ]
    
    for mes_info in meses_90_dias:
        with st.expander(f"{mes_info['mes']}: {mes_info['foco']}"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.write("**Ações principais:**")
                for acao in mes_info['acoes']:
                    st.write(f"• {acao}")
            
            with col2:
                st.metric("Meta de Vendas", f"R$ {mes_info['meta_vendas']:,.0f}")


def show_entrepreneur_summary_tool():
    """Dashboard Empresarial Inteligente - Resumo Executivo para Tomada de Decisão"""
    st.header("📊 Dashboard Empresarial - Resumo Executivo")
    st.markdown("**Indicadores-chave para tomada de decisão estratégica**")
    
    st.markdown("---")
    
    # Recuperar dados principais do plano completo
    business_data = st.session_state.business_data
    nome_negocio = business_data.get('nome_otica', business_data.get('nome_negocio', 'Sua Ótica'))
    
    # Dados financeiros das Projeções Financeiras (Etapa 10)
    vendas_mes_1 = business_data.get('vendas_mes_1', 0)
    ticket_medio = business_data.get('ticket_medio', 0)
    investimento_total = business_data.get('investimento_total', 0)
    
    # Estrutura completa de custos
    aluguel_mensal = business_data.get('aluguel', 0)
    salarios_clt = business_data.get('salarios_clt', 0)
    servicos_terceiros = business_data.get('servicos_terceiros', 0)
    custo_combustivel = business_data.get('custo_combustivel_mensal', 0)
    energia_eletrica = business_data.get('energia_eletrica', 0)
    outros_custos = business_data.get('outros_custos_fixos', 0)
    custo_captador = business_data.get('custo_captador_mensal_calculado', 0)
    
    # CMV estimado (45% da receita bruta é padrão no setor ótico)
    cmv_estimado = vendas_mes_1 * 0.45 if vendas_mes_1 > 0 else 0
    
    # Calcular métricas operacionais
    oculos_meta_mes = int(vendas_mes_1 / ticket_medio) if ticket_medio > 0 else 0
    custos_fixos_totais = aluguel_mensal + salarios_clt + servicos_terceiros + custo_combustivel + energia_eletrica + outros_custos + custo_captador
    
    # Margem bruta (receita - CMV)
    margem_bruta_real = vendas_mes_1 - cmv_estimado if vendas_mes_1 > 0 else 0
    margem_bruta_percentual = (margem_bruta_real / vendas_mes_1 * 100) if vendas_mes_1 > 0 else 0
    
    # Lucro operacional (margem bruta - custos fixos)
    lucro_operacional = margem_bruta_real - custos_fixos_totais if margem_bruta_real > 0 else 0
    margem_operacional_percentual = (lucro_operacional / vendas_mes_1 * 100) if vendas_mes_1 > 0 else 0
    
    # Verificar se temos dados suficientes
    dados_suficientes = vendas_mes_1 > 0 and ticket_medio > 0 and investimento_total > 0
    
    if not dados_suficientes:
        st.warning("⚠️ Complete as Projeções Financeiras (Etapa 10) para ver o dashboard empresarial completo")
        st.info("Após completar, você terá acesso a todos os indicadores de performance e insights estratégicos")
        return
    
    # SEÇÃO 1: INDICADORES FINANCEIROS PRINCIPAIS
    st.markdown("## 💰 Indicadores Financeiros")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        with st.container():
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%); padding: 20px; border-radius: 15px; color: #2e7d32; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.08); border: 1px solid #a5d6a7;'>
                <h3 style='margin: 0; color: #1b5e20; font-size: 16px;'>💰 Faturamento Mensal</h3>
                <p style='font-size: 28px; margin: 10px 0; color: #1b5e20; font-weight: bold;'>{format_currency(vendas_mes_1)}</p>
                <p style='margin: 0; color: #388e3c; font-size: 12px;'>Meta de receita bruta</p>
            </div>
            """, unsafe_allow_html=True)
        
        with st.expander("🔍 Análise Detalhada"):
            st.write("**Como interpretar:**")
            st.write(f"• Este é seu objetivo de faturamento bruto mensal")
            st.write(f"• Equivale a {format_currency(vendas_mes_1 * 12)} por ano")
            st.write(f"• Representa {oculos_meta_mes} óculos vendidos por mês")
            if vendas_mes_1 > 50000:
                st.success("✅ Faturamento robusto para sustentabilidade")
            elif vendas_mes_1 > 25000:
                st.info("🔵 Faturamento adequado para início")
            else:
                st.warning("⚠️ Considere revisar estratégias de pricing")
    
    with col2:
        with st.container():
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); padding: 20px; border-radius: 15px; color: #0d47a1; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.08); border: 1px solid #90caf9;'>
                <h3 style='margin: 0; color: #0d47a1; font-size: 16px;'>📈 Margem Bruta</h3>
                <p style='font-size: 28px; margin: 10px 0; color: #0d47a1; font-weight: bold;'>{margem_bruta_percentual:.1f}%</p>
                <p style='margin: 0; color: #1565c0; font-size: 12px;'>{format_currency(margem_bruta_real)} líquido</p>
            </div>
            """, unsafe_allow_html=True)
        
        with st.expander("🔍 Análise Detalhada"):
            st.write("**Como interpretar:**")
            st.write(f"• Margem bruta após descontar CMV (custo dos produtos)")
            st.write(f"• CMV estimado: {format_currency(cmv_estimado)} (45% da receita)")
            st.write(f"• Sobra {format_currency(margem_bruta_real)} para custos fixos e lucro")
            st.write(f"• Benchmark setor ótico: 50-60%")
            if margem_bruta_percentual > 55:
                st.success("✅ Margem bruta excelente")
            elif margem_bruta_percentual > 45:
                st.info("🔵 Margem bruta adequada")
            else:
                st.warning("⚠️ Margem bruta baixa - revisar fornecedores")
    
    with col3:
        payback_meses = investimento_total / lucro_operacional if lucro_operacional > 0 else 0
        with st.container():
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%); padding: 20px; border-radius: 15px; color: #4a148c; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.08); border: 1px solid #ce93d8;'>
                <h3 style='margin: 0; color: #4a148c; font-size: 16px;'>⏱️ Tempo para Retorno</h3>
                <p style='font-size: 28px; margin: 10px 0; color: #4a148c; font-weight: bold;'>{payback_meses:.0f}</p>
                <p style='margin: 0; color: #6a1b9a; font-size: 12px;'>meses para payback</p>
            </div>
            """, unsafe_allow_html=True)
        
        with st.expander("🔍 Análise Detalhada"):
            st.write("**Como interpretar:**")
            st.write(f"• Tempo para recuperar investimento de {format_currency(investimento_total)}")
            st.write(f"• Com lucro operacional de {format_currency(lucro_operacional)}/mês")
            st.write(f"• Benchmark óticas: 12-24 meses")
            if payback_meses <= 18:
                st.success("✅ Payback excelente")
            elif payback_meses <= 30:
                st.info("🔵 Payback adequado")
            else:
                st.warning("⚠️ Payback longo - otimizar custos")
    
    with col4:
        roi_anual = (lucro_operacional * 12 / investimento_total * 100) if investimento_total > 0 else 0
        with st.container():
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #fff3e0 0%, #ffcc80 100%); padding: 20px; border-radius: 15px; color: #e65100; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.08); border: 1px solid #ffb74d;'>
                <h3 style='margin: 0; color: #e65100; font-size: 16px;'>🎯 ROI Anual</h3>
                <p style='font-size: 28px; margin: 10px 0; color: #e65100; font-weight: bold;'>{roi_anual:.0f}%</p>
                <p style='margin: 0; color: #f57c00; font-size: 12px;'>retorno sobre investimento</p>
            </div>
            """, unsafe_allow_html=True)
        
        with st.expander("🔍 Análise Detalhada"):
            st.write("**Como interpretar:**")
            st.write(f"• Retorno anual sobre capital investido")
            st.write(f"• CDI 2024: ~12% / Poupança: ~6%")
            st.write(f"• Benchmark negócios: 20-40%")
            if roi_anual > 30:
                st.success("✅ ROI excelente - negócio altamente atrativo")
            elif roi_anual > 15:
                st.info("🔵 ROI adequado - supera investimentos tradicionais")
            else:
                st.warning("⚠️ ROI baixo - avaliar viabilidade")
    
    st.markdown("---")
    
    # SEÇÃO 2: INDICADORES OPERACIONAIS
    st.markdown("## 🎯 Indicadores Operacionais")
    
    col1, col2, col3, col4 = st.columns(4)
    
    # Calcular vendas por dia útil (22 dias)
    vendas_por_dia = oculos_meta_mes / 22
    
    with col1:
        with st.container():
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%); padding: 20px; border-radius: 15px; color: #b71c1c; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.08); border: 1px solid #ef9a9a;'>
                <h3 style='margin: 0; color: #b71c1c; font-size: 16px;'>👥 Meta Diária</h3>
                <p style='font-size: 28px; margin: 10px 0; color: #b71c1c; font-weight: bold;'>{vendas_por_dia:.1f}</p>
                <p style='margin: 0; color: #c62828; font-size: 12px;'>óculos por dia útil</p>
            </div>
            """, unsafe_allow_html=True)
        
        with st.expander("🔍 Análise Detalhada"):
            st.write("**Como interpretar:**")
            st.write(f"• Meta: {vendas_por_dia:.1f} óculos por dia útil")
            st.write(f"• {oculos_meta_mes} óculos por mês")
            st.write(f"• Horário 9h-18h: {vendas_por_dia/9:.1f} por hora")
            if vendas_por_dia <= 3:
                st.success("✅ Meta muito alcançável")
            elif vendas_por_dia <= 5:
                st.info("🔵 Meta realista com bom atendimento")
            else:
                st.warning("⚠️ Meta ambiciosa - foque em conversão")
    
    with col2:
        with st.container():
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #388E3C 0%, #4CAF50 100%); padding: 20px; border-radius: 15px; color: white; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
                <h3 style='margin: 0; color: white; font-size: 16px;'>💳 Ticket Médio</h3>
                <p style='font-size: 28px; margin: 10px 0; color: white; font-weight: bold;'>{format_currency(ticket_medio)}</p>
                <p style='margin: 0; color: white; font-size: 12px;'>valor médio por venda</p>
            </div>
            """, unsafe_allow_html=True)
        
        with st.expander("🔍 Análise Detalhada"):
            st.write("**Como interpretar:**")
            st.write(f"• Valor médio de cada venda")
            st.write(f"• Benchmark óticas populares: R$ 350-500")
            st.write(f"• Benchmark óticas premium: R$ 600-1.200")
            if ticket_medio > 600:
                st.success("✅ Ticket alto - posicionamento premium")
            elif ticket_medio > 400:
                st.info("🔵 Ticket adequado - classe média")
            else:
                st.warning("⚠️ Ticket baixo - revisar mix de produtos")
    
    with col3:
        # Calcular ponto de equilíbrio
        ponto_equilibrio_oculos = custos_fixos_totais / ticket_medio if ticket_medio > 0 else 0
        with st.container():
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #455A64 0%, #607D8B 100%); padding: 20px; border-radius: 15px; color: white; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
                <h3 style='margin: 0; color: white; font-size: 16px;'>⚖️ Ponto de Equilíbrio</h3>
                <p style='font-size: 28px; margin: 10px 0; color: white; font-weight: bold;'>{ponto_equilibrio_oculos:.0f}</p>
                <p style='margin: 0; color: white; font-size: 12px;'>óculos para empatar</p>
            </div>
            """, unsafe_allow_html=True)
        
        with st.expander("🔍 Análise Detalhada"):
            st.write("**Como interpretar:**")
            st.write(f"• Vendas mínimas para cobrir custos fixos")
            st.write(f"• Custos fixos: {format_currency(custos_fixos_totais)}")
            st.write(f"• Margem de segurança: {oculos_meta_mes - ponto_equilibrio_oculos:.0f} óculos")
            margem_seguranca = ((oculos_meta_mes - ponto_equilibrio_oculos) / oculos_meta_mes * 100) if oculos_meta_mes > 0 else 0
            if margem_seguranca > 40:
                st.success(f"✅ Margem de segurança: {margem_seguranca:.0f}%")
            elif margem_seguranca > 20:
                st.info(f"🔵 Margem de segurança: {margem_seguranca:.0f}%")
            else:
                st.warning(f"⚠️ Margem baixa: {margem_seguranca:.0f}%")
    
    with col4:
        # Calcular eficiência de capital (vendas/investimento)
        eficiencia_capital = (vendas_mes_1 * 12) / investimento_total if investimento_total > 0 else 0
        with st.container():
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #6A1B9A 0%, #8E24AA 100%); padding: 20px; border-radius: 15px; color: white; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
                <h3 style='margin: 0; color: white; font-size: 16px;'>⚡ Eficiência Capital</h3>
                <p style='font-size: 28px; margin: 10px 0; color: white; font-weight: bold;'>{eficiencia_capital:.1f}x</p>
                <p style='margin: 0; color: white; font-size: 12px;'>receita por R$ investido</p>
            </div>
            """, unsafe_allow_html=True)
        
        with st.expander("🔍 Análise Detalhada"):
            st.write("**Como interpretar:**")
            st.write(f"• Cada R$ 1 investido gera R$ {eficiencia_capital:.1f} em receita anual")
            st.write(f"• Benchmark varejo: 2-4x")
            st.write(f"• Benchmark serviços: 1-3x")
            if eficiencia_capital > 3:
                st.success("✅ Eficiência excelente")
            elif eficiencia_capital > 1.5:
                st.info("🔵 Eficiência adequada")
            else:
                st.warning("⚠️ Baixa eficiência de capital")
    
    st.markdown("---")
    
    # SEÇÃO 3: ANÁLISE DE RISCOS E OPORTUNIDADES
    st.markdown("## ⚠️ Análise de Riscos e Cenários")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔻 Cenário Pessimista (-20%)")
        vendas_pessimista = vendas_mes_1 * 0.8
        margem_pessimista = vendas_pessimista - custos_fixos_totais
        roi_pessimista = (margem_pessimista * 12 / investimento_total * 100) if investimento_total > 0 else 0
        
        with st.container():
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%); padding: 15px; border-radius: 10px; color: #b71c1c; margin-bottom: 10px; border: 1px solid #ef9a9a;'>
                <h4 style='margin: 0; color: #b71c1c;'>Receita: {format_currency(vendas_pessimista)}</h4>
                <p style='margin: 5px 0; color: #c62828;'>Margem: {format_currency(margem_pessimista)} ({(margem_pessimista/vendas_pessimista*100):.1f}%)</p>
                <p style='margin: 0; color: #c62828;'>ROI: {roi_pessimista:.0f}%</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.write("**Principais riscos:**")
        st.write("• Concorrência agressiva")
        st.write("• Economia em recessão")
        st.write("• Dificuldade para encontrar clientes")
        st.write("• Problemas de fornecedores")
        
        if margem_pessimista > 0:
            st.info("🔵 Ainda viável no cenário pessimista")
        else:
            st.error("❌ Negócio inviável no cenário pessimista")
    
    with col2:
        st.markdown("### 🔺 Cenário Otimista (+30%)")
        vendas_otimista = vendas_mes_1 * 1.3
        margem_otimista = vendas_otimista - custos_fixos_totais
        roi_otimista = (margem_otimista * 12 / investimento_total * 100) if investimento_total > 0 else 0
        
        with st.container():
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%); padding: 15px; border-radius: 10px; color: #1b5e20; margin-bottom: 10px; border: 1px solid #a5d6a7;'>
                <h4 style='margin: 0; color: #1b5e20;'>Receita: {format_currency(vendas_otimista)}</h4>
                <p style='margin: 5px 0; color: #2e7d32;'>Margem: {format_currency(margem_otimista)} ({(margem_otimista/vendas_otimista*100):.1f}%)</p>
                <p style='margin: 0; color: #2e7d32;'>ROI: {roi_otimista:.0f}%</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.write("**Principais oportunidades:**")
        st.write("• Marketing digital eficaz")
        st.write("• Parcerias estratégicas")
        st.write("• Expansão de serviços")
        st.write("• Fidelização de clientes")
        
        st.success("✅ Grande potencial de crescimento")
    
    st.markdown("---")
    
    # SEÇÃO 4: ESTRATÉGIAS PARA O SUCESSO
    st.markdown("## 🚀 Estratégias para o Sucesso")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 💰 Aumentar Faturamento")
        st.write("**Estratégias de crescimento:**")
        if ticket_medio < 500:
            st.write("• **Upsell**: Oferecer lentes premium")
            st.write("• **Cross-sell**: Vender óculos de sol")
            st.write(f"• Meta: Elevar ticket para R$ 600 (+{((600/ticket_medio-1)*100):.0f}%)")
        else:
            st.write("• **Volume**: Aumentar fluxo de clientes")
            st.write("• **Recorrência**: Programa de fidelidade")
        st.write("• **Marketing**: Investir 5-8% do faturamento")
        st.write("• **Referências**: Programa de indicação")
        
        # Simular impacto do aumento de ticket
        if ticket_medio < 600:
            novo_ticket = 600
            novo_faturamento = oculos_meta_mes * novo_ticket
            impacto = novo_faturamento - vendas_mes_1
            st.info(f"💡 Aumentando ticket para R$ {novo_ticket}: +{format_currency(impacto)}/mês")
    
    with col2:
        st.markdown("### 📉 Reduzir Custos")
        st.write("**Otimizações possíveis:**")
        if aluguel_mensal / vendas_mes_1 > 0.15:
            st.write(f"• **Aluguel**: {(aluguel_mensal/vendas_mes_1*100):.1f}% da receita (alto)")
            st.write("• Negociar desconto ou buscar local menor")
        if (salarios_clt + outros_custos) / vendas_mes_1 > 0.25:
            st.write("• **Pessoal**: Otimizar estrutura")
            st.write("• Considerar comissionamento")
        st.write("• **Fornecedores**: Negociar melhores condições")
        st.write("• **Energia**: Equipamentos eficientes")
        st.write("• **Automação**: Reduzir tarefas manuais")
        
        # Simular redução de 10% nos custos
        reducao_custos = custos_fixos_totais * 0.1
        nova_margem = lucro_operacional + reducao_custos
        st.info(f"💡 Reduzindo custos 10%: +{format_currency(reducao_custos)}/mês")
    
    with col3:
        st.markdown("### 🎯 Aumentar Eficiência")
        st.write("**Melhorias operacionais:**")
        st.write("• **Atendimento**: Treinar equipe")
        st.write("• **Processo**: Reduzir tempo de venda")
        st.write("• **Estoque**: Otimizar giro")
        st.write("• **Tecnologia**: Sistema de gestão")
        st.write("• **Experiência**: Ambiente acolhedor")
        
        # Taxa de conversão atual e meta
        if vendas_por_dia <= 3:
            st.write(f"• **Meta**: {vendas_por_dia:.1f} → {vendas_por_dia*1.5:.1f} óculos/dia")
            st.info(f"💡 Melhorando conversão 50%: +{format_currency(vendas_mes_1*0.5)}/mês")
        else:
            st.write("• **Foco**: Manter qualidade do atendimento")
            st.info("💡 Priorizar margem sobre volume")
    
    st.markdown("---")
    
    # SEÇÃO 5: RESUMO EXECUTIVO FINAL
    st.markdown("## 📋 Resumo Executivo")
    
    # Calcular score geral do negócio
    score_faturamento = min(100, (vendas_mes_1 / 50000) * 25) if vendas_mes_1 > 0 else 0
    score_margem = min(100, (margem_operacional_percentual / 40) * 25) if margem_operacional_percentual > 0 else 0
    score_payback = min(100, max(0, (36 - payback_meses) / 36 * 25)) if payback_meses > 0 else 0
    score_roi = min(100, (roi_anual / 40) * 25) if roi_anual > 0 else 0
    score_total = score_faturamento + score_margem + score_payback + score_roi
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📊 Avaliação Geral do Negócio")
        
        # Barra de progresso para score
        if score_total >= 80:
            cor_score = "#4CAF50"
            status_negocio = "EXCELENTE"
            recomendacao = "Negócio altamente viável. Prossiga com confiança!"
        elif score_total >= 60:
            cor_score = "#FF9800"
            status_negocio = "BOM"
            recomendacao = "Negócio viável. Implemente melhorias sugeridas."
        elif score_total >= 40:
            cor_score = "#FF5722"
            status_negocio = "REGULAR"
            recomendacao = "Negócio arriscado. Revise custos e estratégias."
        else:
            cor_score = "#D32F2F"
            status_negocio = "CRÍTICO"
            recomendacao = "Negócio inviável. Reformule o plano completamente."
        
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, {cor_score} 0%, {cor_score}88 100%); padding: 20px; border-radius: 15px; color: white; text-align: center; margin-bottom: 20px;'>
            <h2 style='margin: 0; color: white;'>SCORE: {score_total:.0f}/100</h2>
            <h3 style='margin: 10px 0; color: white;'>{status_negocio}</h3>
            <p style='margin: 0; color: white; font-size: 16px;'>{recomendacao}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("**Componentes do Score:**")
        st.progress(score_faturamento/100, f"Faturamento: {score_faturamento:.0f}/25")
        st.progress(score_margem/100, f"Margem: {score_margem:.0f}/25") 
        st.progress(score_payback/100, f"Payback: {score_payback:.0f}/25")
        st.progress(score_roi/100, f"ROI: {score_roi:.0f}/25")
    
    with col2:
        st.markdown("### 🎯 Próximos Passos")
        
        if score_total >= 80:
            st.write("**Ações prioritárias:**")
            st.write("• Finalizar financiamento")
            st.write("• Definir fornecedores")
            st.write("• Contratar equipe")
            st.write("• Começar marketing")
        elif score_total >= 60:
            st.write("**Melhorias necessárias:**")
            st.write("• Otimizar custos fixos")
            st.write("• Revisar ticket médio")
            st.write("• Validar demanda")
            st.write("• Ajustar projeções")
        else:
            st.write("**Revisões críticas:**")
            st.write("• Rever modelo de negócio")
            st.write("• Reduzir investimento")
            st.write("• Buscar local mais barato")
            st.write("• Considerar sociedade")
        
        # Botão de ação principal
        if score_total >= 60:
            st.success("✅ Prosseguir com implementação")
        else:
            st.error("❌ Revisar plano antes de prosseguir")
    
    st.markdown("---")
    
    # Footer com resumo numérico
    st.markdown("### 📈 Resumo dos Números-Chave")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("💰 Faturamento", format_currency(vendas_mes_1), f"{format_currency(vendas_mes_1 * 12)}/ano")
    
    with col2:
        st.metric("📊 Margem", f"{margem_operacional_percentual:.1f}%", format_currency(lucro_operacional))
    
    with col3:
        st.metric("⏱️ Payback", f"{payback_meses:.0f} meses", f"{payback_meses/12:.1f} anos")
    
    with col4:
        st.metric("🎯 ROI", f"{roi_anual:.0f}%", "ao ano")
    
    with col5:
        st.metric("👥 Meta Diária", f"{vendas_por_dia:.1f}", "óculos/dia")

    
def show_investor_report_tool():
    """Relatório Completo para Investidores - Multilingual"""
    
    # Seletor de idioma no topo
    col_header1, col_header2 = st.columns([3, 1])
    
    with col_header1:
        st.header("📊 Relatório Completo para Investidores")
        st.markdown("**Documento profissional baseado no checklist completo para análise de investimento**")
    
    with col_header2:
        idioma = st.selectbox(
            "🌐 Idioma / Language / Idioma",
            ["Português", "English", "Español"],
            key="investor_report_language"
        )
    

    
    # Verificar se há dados suficientes
    if not st.session_state.business_data:
        if idioma == "English":
            st.warning("Complete all 12 steps of the business plan to generate the complete report")
        elif idioma == "Español":
            st.warning("Complete todas las 12 etapas del plan de negocios para generar el informe completo")
        else:
            st.warning("Complete todas as 12 etapas do plano de negócios para gerar o relatório completo")
        return
    
    # Traduções dos textos
    translations = {
        "Português": {
            "tabs": ["🎯 Propósito", "💡 Solução", "🏢 Mercado", "⚔️ Concorrência", "💰 Financeiro", "👥 Equipe", "📄 Download"],
            "purpose_title": "1. PROPÓSITO E PROBLEMA",
            "problem_identified": "Problema Identificado",
            "problem": "Problema",
            "validation": "Validação do Problema",
            "latent_pain": "Dor Latente no Mercado:",
            "evidence": "Evidências do Problema:",
            "target_audience": "Público-alvo",
            "relevance": "Relevância do Problema",
            "impact": "Impacto: Afeta diretamente a qualidade de vida e produtividade de milhões de brasileiros",
            "urgency": "Urgência: Necessidade crescente de correção visual e proteção ocular",
            "frequency": "Frequência: Problema recorrente que afeta pessoas por toda a vida",
            "solution_title": "2. SOLUÇÃO E PROPOSTA DE VALOR",
            "our_solution": "Nossa Solução",
            "value_proposition": "Proposta de Valor",
            "competitive_diff": "Diferencial Competitivo",
            "products_services": "Produtos e Serviços",
            "unique_advantages": "Vantagens Únicas",
            "solution_validation": "Validação da Solução",
            "entrepreneur_exp": "Experiência do Empreendedor",
            "business_status": "Status do Negócio: Pronto para operação",
            "validation_complete": "Validação: Análise completa de mercado e viabilidade realizada",
            "market_title": "3. MERCADO E OPORTUNIDADE",
            "market_size": "Tamanho do Mercado",
            "growth_analysis": "Análise de Crescimento",
            "sector_trends": "Tendências do Setor:",
            "strategic_location": "Localização Estratégica",
            "city": "Cidade",
            "pop_density": "Densidade Populacional",
            "location_advantages": "Vantagens da Localização:",
            "download_complete": "📄 Gerar Relatório Completo para Investidores",
            "download_success": "Relatório completo gerado com sucesso!",
            "download_preview": "📖 Prévia do Relatório Completo"
        },
        "English": {
            "tabs": ["🎯 Purpose", "💡 Solution", "🏢 Market", "⚔️ Competition", "💰 Financial", "👥 Team", "📄 Download"],
            "purpose_title": "1. PURPOSE AND PROBLEM",
            "problem_identified": "Identified Problem",
            "problem": "Problem",
            "validation": "Problem Validation",
            "latent_pain": "Latent Market Pain:",
            "evidence": "Problem Evidence:",
            "target_audience": "Target audience",
            "relevance": "Problem Relevance",
            "impact": "Impact: Directly affects the quality of life and productivity of millions of Brazilians",
            "urgency": "Urgency: Growing need for vision correction and eye protection",
            "frequency": "Frequency: Recurring problem that affects people throughout their lives",
            "solution_title": "2. SOLUTION AND VALUE PROPOSITION",
            "our_solution": "Our Solution",
            "value_proposition": "Value Proposition",
            "competitive_diff": "Competitive Differential",
            "products_services": "Products and Services",
            "unique_advantages": "Unique Advantages",
            "solution_validation": "Solution Validation",
            "entrepreneur_exp": "Entrepreneur Experience",
            "business_status": "Business Status: Ready for operation",
            "validation_complete": "Validation: Complete market and feasibility analysis conducted",
            "market_title": "3. MARKET AND OPPORTUNITY",
            "market_size": "Market Size",
            "growth_analysis": "Growth Analysis",
            "sector_trends": "Sector Trends:",
            "strategic_location": "Strategic Location",
            "city": "City",
            "pop_density": "Population Density",
            "location_advantages": "Location Advantages:",
            "download_complete": "📄 Generate Complete Investor Report",
            "download_success": "Complete report generated successfully!",
            "download_preview": "📖 Complete Report Preview"
        },
        "Español": {
            "tabs": ["🎯 Propósito", "💡 Solución", "🏢 Mercado", "⚔️ Competencia", "💰 Financiero", "👥 Equipo", "📄 Descarga"],
            "purpose_title": "1. PROPÓSITO Y PROBLEMA",
            "problem_identified": "Problema Identificado",
            "problem": "Problema",
            "validation": "Validación del Problema",
            "latent_pain": "Dolor Latente del Mercado:",
            "evidence": "Evidencias del Problema:",
            "target_audience": "Público objetivo",
            "relevance": "Relevancia del Problema",
            "impact": "Impacto: Afecta directamente la calidad de vida y productividad de millones de brasileños",
            "urgency": "Urgencia: Necesidad creciente de corrección visual y protección ocular",
            "frequency": "Frecuencia: Problema recurrente que afecta a las personas durante toda su vida",
            "solution_title": "2. SOLUCIÓN Y PROPUESTA DE VALOR",
            "our_solution": "Nuestra Solución",
            "value_proposition": "Propuesta de Valor",
            "competitive_diff": "Diferencial Competitivo",
            "products_services": "Productos y Servicios",
            "unique_advantages": "Ventajas Únicas",
            "solution_validation": "Validación de la Solución",
            "entrepreneur_exp": "Experiencia del Emprendedor",
            "business_status": "Estado del Negocio: Listo para operación",
            "validation_complete": "Validación: Análisis completo de mercado y viabilidad realizado",
            "market_title": "3. MERCADO Y OPORTUNIDAD",
            "market_size": "Tamaño del Mercado",
            "growth_analysis": "Análisis de Crecimiento",
            "sector_trends": "Tendencias del Sector:",
            "strategic_location": "Ubicación Estratégica",
            "city": "Ciudad",
            "pop_density": "Densidad Poblacional",
            "location_advantages": "Ventajas de la Ubicación:",
            "download_complete": "📄 Generar Informe Completo para Inversores",
            "download_success": "¡Informe completo generado exitosamente!",
            "download_preview": "📖 Vista Previa del Informe Completo"
        }
    }
    
    t = translations[idioma]
    
    # Dados do negócio
    nome_negocio = st.session_state.business_data.get('nome_negocio', 'Ótica não informada')
    cidade = st.session_state.business_data.get('cidade', 'Cidade não informada')
    estado = st.session_state.business_data.get('estado', 'Estado não informado')
    vendas_mes_1 = st.session_state.business_data.get('vendas_mes_1', 0)
    
    # Tabs para o relatório completo
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(t["tabs"])
    
    with tab1:
        st.subheader(t["purpose_title"])
        
        st.markdown(f"### {t['problem_identified']}")
        problema = st.session_state.business_data.get('problema_mercado', 'Não definido')
        st.write(f"**{t['problem']}:** {problema}")
        
        st.markdown(f"### {t['validation']}")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"**{t['latent_pain']}**")
            if idioma == "English":
                st.write("• Difficulty accessing quality optical products")
                st.write("• High prices in traditional market")
                st.write("• Limited personalized service")
                st.write("• Delays in specialized product delivery")
            elif idioma == "Español":
                st.write("• Dificultad para acceder a productos ópticos de calidad")
                st.write("• Precios elevados en el mercado tradicional")
                st.write("• Atención personalizada limitada")
                st.write("• Demoras en la entrega de productos especializados")
            else:
                st.write("• Dificuldade de acesso a produtos ópticos de qualidade")
                st.write("• Preços elevados no mercado tradicional")
                st.write("• Atendimento personalizado limitado")
                st.write("• Demora na entrega de produtos especializados")
        
        with col2:
            st.markdown(f"**{t['evidence']}**")
            publico_alvo = st.session_state.business_data.get('publico_alvo', 'Não definido')
            st.write(f"• {t['target_audience']}: {publico_alvo}")
            if idioma == "English":
                st.write("• Optical market growth: 8% annually")
                st.write("• Population aging increasing demand")
                st.write("• Intensive use of digital screens")
            elif idioma == "Español":
                st.write("• Crecimiento del mercado óptico: 8% anual")
                st.write("• Envejecimiento poblacional aumentando demanda")
                st.write("• Uso intensivo de pantallas digitales")
            else:
                st.write("• Crescimento do mercado óptico: 8% ao ano")
                st.write("• Envelhecimento populacional aumentando demanda")
                st.write("• Uso intensivo de telas digitais")
        
        st.markdown(f"### {t['relevance']}")
        st.write(f"**{t['impact']}**")
        st.write(f"**{t['urgency']}**")
        st.write(f"**{t['frequency']}**")
    
    with tab2:
        st.subheader("2. SOLUÇÃO E PROPOSTA DE VALOR")
        
        st.markdown("### Nossa Solução")
        proposta_valor = st.session_state.business_data.get('proposta_valor', 'Não definida')
        st.write(f"**Proposta de Valor:** {proposta_valor}")
        
        st.markdown("### Diferencial Competitivo")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Produtos e Serviços:**")
            produtos = st.session_state.business_data.get('produtos_servicos', 'Não definidos')
            st.write(f"• {produtos}")
            st.write("• Atendimento personalizado e consultorias")
            st.write("• Tecnologia de ponta em exames")
            st.write("• Parcerias com fornecedores premium")
        
        with col2:
            st.markdown("**Vantagens Únicas:**")
            st.write("• Localização estratégica privilegiada")
            st.write("• Equipe especializada e experiente")
            st.write("• Processo otimizado de atendimento")
            st.write("• Relacionamento próximo com clientes")
        
        st.markdown("### Validação da Solução")
        experiencia = st.session_state.business_data.get('experiencia_setor', 'Não informada')
        st.write(f"**Experiência do Empreendedor:** {experiencia}")
        st.write("**Status do Negócio:** Pronto para operação")
        st.write("**Validação:** Análise completa de mercado e viabilidade realizada")
    
    with tab3:
        st.subheader("3. MERCADO E OPORTUNIDADE")
        
        st.markdown("### Tamanho do Mercado")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**TAM - Total Addressable Market**")
            st.metric("Mercado Óptico Brasil", "R$ 4,2 bi")
            st.caption("Mercado total de produtos ópticos no Brasil")
        
        with col2:
            st.markdown("**SAM - Serviceable Available Market**")
            tam_regional = 4200000000 * 0.02  # 2% do mercado nacional estimado para região
            st.metric(f"Mercado Regional {estado}", format_currency(tam_regional))
            st.caption("Mercado acessível na região de atuação")
        
        with col3:
            st.markdown("**SOM - Serviceable Obtainable Market**")
            som_estimado = tam_regional * 0.01  # 1% do mercado regional
            st.metric("Mercado Obtível", format_currency(som_estimado))
            st.caption("Fatia de mercado realista nos primeiros anos")
        
        st.markdown("### Análise de Crescimento")
        st.write("**Tendências do Setor:**")
        st.write("• Crescimento médio anual: 8% (ABRAÃO - Associação Brasileira do Comércio Óptico)")
        st.write("• Envelhecimento populacional: +60 anos crescendo 4% ao ano")
        st.write("• Digitalização: aumento de 40% em problemas de visão relacionados a telas")
        st.write("• Renda per capita: melhoria do poder aquisitivo da classe média")
        
        st.markdown("### Localização Estratégica")
        st.write(f"**Cidade:** {cidade}, {estado}")
        densidade_pop = st.session_state.business_data.get('densidade_populacional', 'Não informada')
        st.write(f"**Densidade Populacional:** {densidade_pop}")
        st.write("**Vantagens da Localização:**")
        st.write("• Alto fluxo de pedestres e veículos")
        st.write("• Proximidade a centros médicos e clínicas")
        st.write("• Facilidade de acesso e estacionamento")
        st.write("• Visibilidade comercial privilegiada")
    
    with tab4:
        st.subheader("4. ANÁLISE DA CONCORRÊNCIA")
        
        st.markdown("### Concorrentes Identificados")
        concorrentes = st.session_state.business_data.get('principais_concorrentes', 'Não identificados')
        st.write(f"**Principais Concorrentes:** {concorrentes}")
        
        st.markdown("### Matriz de Posicionamento")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Concorrentes Diretos:**")
            st.write("• Óticas tradicionais da região")
            st.write("• Redes nacionais (Óticas Carol, Diniz)")
            st.write("• Franchises locais")
            
            st.markdown("**Pontos Fortes dos Concorrentes:**")
            st.write("• Marca estabelecida (redes)")
            st.write("• Volume de compras (preço)")
            st.write("• Marketing padronizado")
        
        with col2:
            st.markdown("**Concorrentes Indiretos:**")
            st.write("• E-commerce de produtos ópticos")
            st.write("• Óticas em shopping centers")
            st.write("• Clínicas oftalmológicas")
            
            st.markdown("**Nossos Diferenciais:**")
            st.write("• Atendimento personalizado e consultivo")
            st.write("• Agilidade na entrega")
            st.write("• Relacionamento próximo com clientes")
            st.write("• Flexibilidade para customização")
        
        st.markdown("### Estratégia Competitiva")
        estrategia_marketing = st.session_state.business_data.get('estrategia_marketing', 'Não definida')
        st.write(f"**Estratégia de Marketing:** {estrategia_marketing}")
        st.write("**Vantagem Competitiva Sustentável:**")
        st.write("• Especialização em atendimento consultivo")
        st.write("• Parcerias exclusivas com fornecedores premium")
        st.write("• Sistema de fidelização de clientes")
        st.write("• Localização estratégica privilegiada")
    
    with tab5:
        st.subheader("5. ANÁLISE FINANCEIRA DETALHADA")
        
        # Calcular métricas financeiras
        investimento_total = (
            st.session_state.business_data.get('reforma_loja', 0) +
            st.session_state.business_data.get('equipamentos_moveis', 0) +
            st.session_state.business_data.get('estoque_inicial', 0) +
            st.session_state.business_data.get('capital_giro', 0)
        )
        
        faturamento_anual = vendas_mes_1 * 12 if vendas_mes_1 else 0
        
        st.markdown("### Investimento Inicial")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            reforma = st.session_state.business_data.get('reforma_loja', 0)
            st.metric("Reforma", format_currency(reforma))
        
        with col2:
            equipamentos = st.session_state.business_data.get('equipamentos_moveis', 0)
            st.metric("Equipamentos", format_currency(equipamentos))
        
        with col3:
            estoque = st.session_state.business_data.get('estoque_inicial', 0)
            st.metric("Estoque Inicial", format_currency(estoque))
        
        with col4:
            capital_giro = st.session_state.business_data.get('capital_giro', 0)
            st.metric("Capital de Giro", format_currency(capital_giro))
        
        st.metric("**INVESTIMENTO TOTAL**", format_currency(investimento_total))
        
        st.markdown("### Projeções Financeiras")
        
        if vendas_mes_1 > 0:
            # Gerar DRE usando o gerador existente
            try:
                from dre_generator import DREGenerator
                dre_gen = DREGenerator()
                dre_data = dre_gen.generate_dre(st.session_state.business_data, {})
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**DRE Projetado (Mensal):**")
                    st.write(f"• Receita Bruta: {format_currency(dre_data['receita_bruta'])}")
                    st.write(f"• (-) Impostos: {format_currency(dre_data['impostos'])}")
                    st.write(f"• (-) CMV: {format_currency(dre_data['cmv'])}")
                    st.write(f"• Lucro Bruto: {format_currency(dre_data['lucro_bruto'])}")
                    st.write(f"• (-) Despesas Operacionais: {format_currency(dre_data['despesas_operacionais'])}")
                    st.markdown(f"**• Lucro Líquido: {format_currency(dre_data['lucro_liquido'])}**")
                
                with col2:
                    st.markdown("**Indicadores de Performance:**")
                    margem_bruta = (dre_data['lucro_bruto'] / dre_data['receita_bruta']) * 100 if dre_data['receita_bruta'] > 0 else 0
                    margem_liquida = (dre_data['lucro_liquido'] / dre_data['receita_bruta']) * 100 if dre_data['receita_bruta'] > 0 else 0
                    
                    st.metric("Margem Bruta", f"{margem_bruta:.1f}%")
                    st.metric("Margem Líquida", f"{margem_liquida:.1f}%")
                    
                    if investimento_total > 0 and dre_data['lucro_liquido'] > 0:
                        roi_anual = (dre_data['lucro_liquido'] * 12 / investimento_total) * 100
                        payback_anos = investimento_total / (dre_data['lucro_liquido'] * 12)
                        st.metric("ROI Anual", f"{roi_anual:.1f}%")
                        st.metric("Payback", f"{payback_anos:.1f} anos")
                
                st.markdown("### Análise de Viabilidade")
                st.write("**Pontos Fortes Financeiros:**")
                st.write(f"• Margem líquida atrativa: {margem_liquida:.1f}%")
                st.write(f"• Payback aceitável: {payback_anos:.1f} anos")
                st.write("• Baixo investimento inicial comparado ao potencial de retorno")
                st.write("• Fluxo de caixa positivo desde o primeiro ano")
                
            except Exception as e:
                st.warning("Complete as Projeções Financeiras (Etapa 10) para análise detalhada")
        else:
            st.warning("Complete as Projeções Financeiras (Etapa 10) para análise detalhada")
        
        st.markdown("### Cenários e Riscos")
        st.markdown("**Cenário Conservador:** Redução de 20% no faturamento")
        st.markdown("**Cenário Realista:** Projeções apresentadas")
        st.markdown("**Cenário Otimista:** Crescimento de 30% sobre as projeções")
        
        st.markdown("**Principais Riscos:**")
        st.write("• Concorrência de grandes redes")
        st.write("• Variações na economia local")
        st.write("• Mudanças na legislação do setor")
        st.write("• Dependência de fornecedores")
        
        st.markdown("**Mitigação de Riscos:**")
        st.write("• Diversificação de fornecedores")
        st.write("• Reserva de capital de giro")
        st.write("• Foco em fidelização de clientes")
        st.write("• Monitoramento constante do mercado")
    
    with tab6:
        st.subheader("6. EQUIPE E GESTÃO")
        
        st.markdown("### Perfil do Empreendedor")
        experiencia = st.session_state.business_data.get('experiencia_setor', 'Não informada')
        st.write(f"**Experiência no Setor:** {experiencia}")
        
        motivacao = st.session_state.business_data.get('motivacao', 'Não informada')
        st.write(f"**Motivação:** {motivacao}")
        
        st.markdown("### Estrutura Organizacional")
        num_funcionarios = st.session_state.business_data.get('num_funcionarios', 1)
        st.write(f"**Número de Funcionários:** {num_funcionarios}")
        
        # Mostrar estrutura de funcionários se disponível
        if hasattr(st.session_state, 'funcionarios') and st.session_state.funcionarios:
            st.markdown("**Equipe Planejada:**")
            for func in st.session_state.funcionarios:
                salario = func.get('salario_base', 0)
                cargo = func.get('cargo', 'Não definido')
                st.write(f"• {cargo}: R$ {salario:,.2f}")
        
        st.markdown("### Competências da Equipe")
        st.write("**Competências Técnicas:**")
        st.write("• Conhecimento em produtos ópticos")
        st.write("• Atendimento ao cliente especializado")
        st.write("• Gestão comercial e financeira")
        st.write("• Marketing digital e relacionamento")
        
        st.markdown("### Necessidades de Contratação")
        st.write("**Perfis Necessários:**")
        st.write("• Vendedor especializado em produtos ópticos")
        st.write("• Atendente com experiência em relacionamento")
        st.write("• Suporte administrativo")
        
        st.markdown("### Plano de Crescimento da Equipe")
        st.write("**Ano 1:** Equipe inicial para operação")
        st.write("**Ano 2:** Expansão com vendedor adicional")
        st.write("**Ano 3:** Supervisão e gestão especializada")
    
    with tab7:
        st.subheader(t["download_complete"].replace("📄 ", ""))
        
        # Mostrar duas opções de relatório
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📄 Relatório Padrão Multilíngue")
            if idioma == "English":
                st.info("Complete investor report with multilingual support and professional formatting")
            elif idioma == "Español":
                st.info("Informe completo para inversores con soporte multilingüe y formato profesional")
            else:
                st.info("Relatório completo para investidores com suporte multilíngue e formatação profissional")
        
        with col2:
            st.markdown("#### 📊 Relatório Estruturado Profissional")
            if idioma == "English":
                st.info("Industry-standard structured report with KPIs, financial analysis, and risk assessment")
            elif idioma == "Español":
                st.info("Informe estructurado estándar de la industria con KPIs, análisis financiero y evaluación de riesgos")
            else:
                st.info("Relatório estruturado padrão da indústria com KPIs, análise financeira e avaliação de riscos")
        
        # Botões lado a lado
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            if st.button(t["download_complete"], type="primary", key="standard_report"):
                try:
                    from multilingual_pdf_generator import MultilingualInvestorPDFGenerator
                    
                    # Gerar PDF profissional multilíngue
                    pdf_generator = MultilingualInvestorPDFGenerator()
                    pdf_buffer = pdf_generator.generate_investor_report_pdf(st.session_state.business_data, idioma)
                    
                    # Nome do arquivo baseado no idioma
                    if idioma == "English":
                        filename = f"complete_investor_report_{nome_negocio.replace(' ', '_')}.pdf"
                        label = "📥 Download Complete Investor Report (PDF)"
                    elif idioma == "Español":
                        filename = f"informe_completo_inversores_{nome_negocio.replace(' ', '_')}.pdf"
                        label = "📥 Descargar Informe Completo para Inversores (PDF)"
                    else:
                        filename = f"relatorio_completo_investidores_{nome_negocio.replace(' ', '_')}.pdf"
                        label = "📥 Download Relatório Completo para Investidores (PDF)"
                    
                    # Download do PDF multilíngue
                    st.download_button(
                        label=label,
                        data=pdf_buffer.getvalue(),
                        file_name=filename,
                        mime="application/pdf"
                    )
                    
                    st.success(t["download_success"])
                
                except Exception as e:
                    if idioma == "English":
                        st.error(f"Error generating report: {str(e)}")
                    elif idioma == "Español":
                        st.error(f"Error al generar informe: {str(e)}")
                    else:
                        st.error(f"Erro ao gerar relatório: {str(e)}")
        
        with col_btn2:
            # Botão para relatório estruturado profissional
            if idioma == "English":
                structured_label = "📊 Generate Professional Report"
                structured_filename = f"structured_investor_report_{nome_negocio.replace(' ', '_')}.pdf"
            elif idioma == "Español":
                structured_label = "📊 Generar Informe Estructurado"
                structured_filename = f"informe_estructurado_inversor_{nome_negocio.replace(' ', '_')}.pdf"
            else:
                structured_label = "📊 Gerar Relatório Estruturado"
                structured_filename = f"relatorio_estruturado_investidor_{nome_negocio.replace(' ', '_')}.pdf"
            
            if st.button(structured_label, type="secondary", key="structured_report"):
                try:
                    # Gerar relatório estruturado
                    structured_generator = StructuredInvestorReport()
                    structured_buffer = structured_generator.generate_structured_report(st.session_state.business_data, idioma)
                    
                    st.download_button(
                        label=f"📥 Download {structured_label.replace('📊 Gerar ', '').replace('📊 Generate ', '').replace('📊 Generar ', '')}",
                        data=structured_buffer.getvalue(),
                        file_name=structured_filename,
                        mime="application/pdf",
                        key="download_structured_report"
                    )
                    
                    if idioma == "English":
                        st.success("Professional structured report generated successfully!")
                    elif idioma == "Español":
                        st.success("¡Informe estructurado profesional generado exitosamente!")
                    else:
                        st.success("Relatório estruturado profissional gerado com sucesso!")
                
                except Exception as e:
                    if idioma == "English":
                        st.error(f"Error generating structured report: {str(e)}")
                    elif idioma == "Español":
                        st.error(f"Error al generar informe estructurado: {str(e)}")
                    else:
                        st.error(f"Erro ao gerar relatório estruturado: {str(e)}")
        
        # Versão texto para compatibilidade (opcional)
        if st.checkbox("Incluir versão texto", key="include_text_version"):
            # Gerar versão texto para compatibilidade
            if idioma == "English":
                    relatorio_expandido = f"""
COMPLETE INVESTOR REPORT
{nome_negocio}
Date: {datetime.now().strftime('%m/%d/%Y')}

═══════════════════════════════════════════════════════════════

1. PURPOSE AND PROBLEM

Identified Problem:
{st.session_state.business_data.get('problema_mercado', 'Difficulty accessing quality optical products with personalized service')}

Market Validation:
• Optical market growth: 8% annually
• Population aging increasing demand
• Intensive use of digital screens
• Target audience: {st.session_state.business_data.get('publico_alvo', 'Not defined')}

═══════════════════════════════════════════════════════════════

2. SOLUTION AND VALUE PROPOSITION

Value Proposition:
{st.session_state.business_data.get('proposta_valor', 'Not defined')}

Products and Services:
{st.session_state.business_data.get('produtos_servicos', 'Complete optical products with specialized service')}

Competitive Advantage:
• Personalized and consultative service
• Privileged strategic location
• Close customer relationships
• Delivery speed

═══════════════════════════════════════════════════════════════

3. MARKET AND OPPORTUNITY

Location: {cidade}, {estado}

Market Size:
• TAM (Brazil): R$ 4.2 billion
• SAM (Regional): R$ {(4200000000 * 0.02):,.0f}
• SOM (Obtainable): R$ {(4200000000 * 0.02 * 0.01):,.0f}

Sector Trends:
• Average annual growth: 8%
• Population aging: +60 years growing 4% annually
• Digitalization: 40% increase in vision problems

═══════════════════════════════════════════════════════════════

4. FINANCIAL ANALYSIS

Initial Investment:
• Renovation: R$ {st.session_state.business_data.get('reforma_loja', 0):,.2f}
• Equipment: R$ {st.session_state.business_data.get('equipamentos_moveis', 0):,.2f}
• Initial Stock: R$ {st.session_state.business_data.get('estoque_inicial', 0):,.2f}
• Working Capital: R$ {st.session_state.business_data.get('capital_giro', 0):,.2f}
TOTAL: R$ {investimento_total:,.2f}

Annual Projections:
• Revenue: R$ {faturamento_anual:,.2f}
• Average Ticket: R$ {st.session_state.business_data.get('ticket_medio', 0):,.2f}

═══════════════════════════════════════════════════════════════

5. TEAM AND MANAGEMENT

Entrepreneur Experience:
{st.session_state.business_data.get('experiencia_setor', 'Not informed')}

Organizational Structure:
• Employees: {num_funcionarios}
• Payroll: R$ {st.session_state.business_data.get('salarios_total', 0):,.2f}

═══════════════════════════════════════════════════════════════

6. CONCLUSION AND RECOMMENDATION

Investment Strengths:
• Constantly growing market
• Low initial investment
• Strategic location
• Entrepreneur experience
• Proven business model

Identified Risks:
• Competition from large chains
• Local economy dependence
• Market seasonality

Recommendation:
RECOMMENDED investment based on complete market analysis,
financial viability and entrepreneur profile.

═══════════════════════════════════════════════════════════════
                    """
            elif idioma == "Español":
                    relatorio_expandido = f"""
INFORME COMPLETO PARA INVERSORES
{nome_negocio}
Fecha: {datetime.now().strftime('%d/%m/%Y')}

═══════════════════════════════════════════════════════════════

1. PROPÓSITO Y PROBLEMA

Problema Identificado:
{st.session_state.business_data.get('problema_mercado', 'Dificultad para acceder a productos ópticos de calidad con atención personalizada')}

Validación del Mercado:
• Crecimiento del mercado óptico: 8% anual
• Envejecimiento poblacional aumentando demanda
• Uso intensivo de pantallas digitales
• Público objetivo: {st.session_state.business_data.get('publico_alvo', 'No definido')}

═══════════════════════════════════════════════════════════════

2. SOLUCIÓN Y PROPUESTA DE VALOR

Propuesta de Valor:
{st.session_state.business_data.get('proposta_valor', 'No definida')}

Productos y Servicios:
{st.session_state.business_data.get('produtos_servicos', 'Productos ópticos completos con atención especializada')}

Ventaja Competitiva:
• Atención personalizada y consultiva
• Ubicación estratégica privilegiada
• Relación cercana con clientes
• Rapidez en la entrega

═══════════════════════════════════════════════════════════════

3. MERCADO Y OPORTUNIDAD

Ubicación: {cidade}, {estado}

Tamaño del Mercado:
• TAM (Brasil): R$ 4,2 mil millones
• SAM (Regional): R$ {(4200000000 * 0.02):,.0f}
• SOM (Obtenible): R$ {(4200000000 * 0.02 * 0.01):,.0f}

Tendencias del Sector:
• Crecimiento promedio anual: 8%
• Envejecimiento poblacional: +60 años creciendo 4% anual
• Digitalización: aumento del 40% en problemas de visión

═══════════════════════════════════════════════════════════════

4. ANÁLISIS FINANCIERO

Inversión Inicial:
• Renovación: R$ {st.session_state.business_data.get('reforma_loja', 0):,.2f}
• Equipos: R$ {st.session_state.business_data.get('equipamentos_moveis', 0):,.2f}
• Stock Inicial: R$ {st.session_state.business_data.get('estoque_inicial', 0):,.2f}
• Capital de Trabajo: R$ {st.session_state.business_data.get('capital_giro', 0):,.2f}
TOTAL: R$ {investimento_total:,.2f}

Proyecciones Anuales:
• Facturación: R$ {faturamento_anual:,.2f}
• Ticket Promedio: R$ {st.session_state.business_data.get('ticket_medio', 0):,.2f}

═══════════════════════════════════════════════════════════════

5. EQUIPO Y GESTIÓN

Experiencia del Emprendedor:
{st.session_state.business_data.get('experiencia_setor', 'No informada')}

Estructura Organizacional:
• Empleados: {num_funcionarios}
• Nómina: R$ {st.session_state.business_data.get('salarios_total', 0):,.2f}

═══════════════════════════════════════════════════════════════

6. CONCLUSIÓN Y RECOMENDACIÓN

Fortalezas de la Inversión:
• Mercado en crecimiento constante
• Baja inversión inicial
• Ubicación estratégica
• Experiencia del emprendedor
• Modelo de negocio comprobado

Riesgos Identificados:
• Competencia de grandes cadenas
• Dependencia de la economía local
• Estacionalidad del mercado

Recomendación:
Inversión RECOMENDADA basada en análisis completo del mercado,
viabilidad financiera y perfil del emprendedor.

═══════════════════════════════════════════════════════════════
                    """
            else:  # Português
                    relatorio_expandido = f"""
RELATÓRIO COMPLETO PARA INVESTIDORES
{nome_negocio}
Data: {datetime.now().strftime('%d/%m/%Y')}

═══════════════════════════════════════════════════════════════

1. PROPÓSITO E PROBLEMA

Problema Identificado:
{st.session_state.business_data.get('problema_mercado', 'Dificuldade de acesso a produtos ópticos de qualidade com atendimento personalizado')}

Validação do Mercado:
• Crescimento do mercado óptico: 8% ao ano
• Envelhecimento populacional aumentando demanda
• Uso intensivo de telas digitais
• Público-alvo: {st.session_state.business_data.get('publico_alvo', 'Não definido')}

═══════════════════════════════════════════════════════════════

2. SOLUÇÃO E PROPOSTA DE VALOR

Proposta de Valor:
{st.session_state.business_data.get('proposta_valor', 'Não definida')}

Produtos e Serviços:
{st.session_state.business_data.get('produtos_servicos', 'Produtos ópticos completos com atendimento especializado')}

Diferencial Competitivo:
• Atendimento personalizado e consultivo
• Localização estratégica privilegiada
• Relacionamento próximo com clientes
• Agilidade na entrega

═══════════════════════════════════════════════════════════════

3. MERCADO E OPORTUNIDADE

Localização: {cidade}, {estado}

Tamanho de Mercado:
• TAM (Brasil): R$ 4,2 bilhões
• SAM (Regional): R$ {(4200000000 * 0.02):,.0f}
• SOM (Obtível): R$ {(4200000000 * 0.02 * 0.01):,.0f}

Tendências do Setor:
• Crescimento médio anual: 8%
• Envelhecimento populacional: +60 anos crescendo 4% ao ano
• Digitalização: aumento de 40% em problemas de visão

═══════════════════════════════════════════════════════════════

4. ANÁLISE FINANCEIRA

Investimento Inicial:
• Reforma: R$ {st.session_state.business_data.get('reforma_loja', 0):,.2f}
• Equipamentos: R$ {st.session_state.business_data.get('equipamentos_moveis', 0):,.2f}
• Estoque: R$ {st.session_state.business_data.get('estoque_inicial', 0):,.2f}
• Capital de Giro: R$ {st.session_state.business_data.get('capital_giro', 0):,.2f}
TOTAL: R$ {investimento_total:,.2f}

Projeções Anuais:
• Faturamento: R$ {faturamento_anual:,.2f}
• Ticket Médio: R$ {st.session_state.business_data.get('ticket_medio', 0):,.2f}

═══════════════════════════════════════════════════════════════

5. EQUIPE E GESTÃO

Experiência do Empreendedor:
{st.session_state.business_data.get('experiencia_setor', 'Não informada')}

Estrutura Organizacional:
• Funcionários: {num_funcionarios}
• Folha de Pagamento: R$ {st.session_state.business_data.get('salarios_total', 0):,.2f}

═══════════════════════════════════════════════════════════════

6. CONCLUSÃO E RECOMENDAÇÃO

Pontos Fortes do Investimento:
• Mercado em crescimento constante
• Baixo investimento inicial
• Localização estratégica
• Experiência do empreendedor
• Modelo de negócio comprovado

Riscos Identificados:
• Concorrência de grandes redes
• Dependência da economia local
• Sazonalidade do mercado

Recomendação:
Investimento RECOMENDADO com base na análise completa do mercado,
viabilidade financeira e perfil do empreendedor.

═══════════════════════════════════════════════════════════════
                    """
                
            # Botão adicional para versão texto (compatibilidade)
            st.markdown("---")
            
            if idioma == "English":
                filename_txt = f"complete_investor_report_{nome_negocio.replace(' ', '_')}.txt"
                label_txt = "📄 Download Text Version"
            elif idioma == "Español":
                filename_txt = f"informe_completo_inversores_{nome_negocio.replace(' ', '_')}.txt"
                label_txt = "📄 Descargar Versión Texto"
            else:
                filename_txt = f"relatorio_completo_investidores_{nome_negocio.replace(' ', '_')}.txt"
                label_txt = "📄 Download Versão Texto"
            
            st.download_button(
                label=label_txt,
                data=relatorio_expandido,
                file_name=filename_txt,
                mime="text/plain"
            )
            
            # Mostrar prévia do conteúdo
            with st.expander(t["download_preview"]):
                if idioma == "English":
                    st.info("PDF contains professional formatting with charts, tables, and executive layout")
                elif idioma == "Español":
                    st.info("El PDF contiene formato profesional con gráficos, tablas y diseño ejecutivo")
                else:
                    st.info("O PDF contém formatação profissional com gráficos, tabelas e layout executivo")
                
                st.text(relatorio_expandido[:2000] + "..." if len(relatorio_expandido) > 2000 else relatorio_expandido)
        
        st.markdown("---")
        if idioma == "English":
            st.markdown("**Important:** This report answers the complete investor checklist:")
            st.write("✓ Purpose and problem clearly defined")
            st.write("✓ Detailed solution and value proposition")
            st.write("✓ Complete market and opportunity analysis")
            st.write("✓ Competition study and positioning")
            st.write("✓ Realistic financial projections")
            st.write("✓ Team profile and competencies")
            st.write("✓ Risk analysis and mitigation")
            st.write("✓ Substantiated recommendation")
        elif idioma == "Español":
            st.markdown("**Importante:** Este informe responde al checklist completo para inversores:")
            st.write("✓ Propósito y problema claramente definidos")
            st.write("✓ Solución y propuesta de valor detalladas")
            st.write("✓ Análisis completo de mercado y oportunidad")
            st.write("✓ Estudio de competencia y posicionamiento")
            st.write("✓ Proyecciones financieras realistas")
            st.write("✓ Perfil del equipo y competencias")
            st.write("✓ Análisis de riesgos y mitigación")
            st.write("✓ Recomendación fundamentada")
        else:
            st.markdown("**Importante:** Este relatório responde ao checklist completo para investidores:")
            st.write("✓ Propósito e problema claramente definidos")
            st.write("✓ Solução e proposta de valor detalhadas")
            st.write("✓ Análise completa de mercado e oportunidade")
            st.write("✓ Estudo da concorrência e posicionamento")
            st.write("✓ Projeções financeiras realistas")
            st.write("✓ Perfil da equipe e competências")
            st.write("✓ Análise de riscos e mitigação")
            st.write("✓ Recomendação fundamentada")

def show_premissas():
    """Central de Controle das Premissas - Atualiza todo o sistema"""
    
    st.title("⚙️ Premissas do Negócio")
    st.markdown("**Central de controle para atualizar todas as variáveis do plano automaticamente**")
    
    # Card de status atual
    col1, col2, col3 = st.columns(3)
    
    with col1:
        vendas_atual = st.session_state.business_data.get('vendas_mes_1', 0)
        st.metric("Vendas Mensais", format_currency(vendas_atual))
    
    with col2:
        ticket_atual = st.session_state.business_data.get('ticket_medio', 0)
        st.metric("Ticket Médio", format_currency(ticket_atual))
    
    with col3:
        oculos_atual = int(vendas_atual / ticket_atual) if ticket_atual > 0 else 0
        st.metric("Óculos/Mês", f"{oculos_atual} unidades")
    
    st.markdown("---")
    
    # Seção 1: Premissas de Vendas
    st.markdown("### 📊 1. Premissas de Vendas")
    
    col_prem1, col_prem2 = st.columns(2)
    
    with col_prem1:
        # Meta de óculos vendidos
        nova_meta_oculos = st.number_input(
            "Meta de óculos vendidos por mês:",
            min_value=1,
            max_value=500,
            value=oculos_atual if oculos_atual > 0 else 30,
            step=1,
            help="Quantos óculos você planeja vender por mês",
            key="nova_meta_oculos"
        )
        
        # Ticket médio
        novo_ticket_medio = st.number_input(
            "Ticket médio por venda (R$):",
            min_value=100.0,
            max_value=5000.0,
            value=float(ticket_atual) if ticket_atual > 0 else 500.0,
            step=50.0,
            help="Valor médio de cada venda",
            key="novo_ticket_medio"
        )
    
    with col_prem2:
        # Faturamento calculado automaticamente
        novo_faturamento = nova_meta_oculos * novo_ticket_medio
        st.metric("Faturamento Mensal Calculado", format_currency(novo_faturamento))
        
        # Distribuição de vendas
        st.markdown("**Distribuição de Vendas:**")
        percentual_avista = st.slider(
            "% Vendas à Vista:",
            min_value=0,
            max_value=100,
            value=st.session_state.business_data.get('percentual_vendas_avista', 50),
            step=5,
            key="novo_percentual_avista"
        )
        
        vendas_avista = int(nova_meta_oculos * (percentual_avista / 100))
        vendas_parcelada = nova_meta_oculos - vendas_avista
        
        st.write(f"• À vista: {vendas_avista} óculos")
        st.write(f"• Parcelado: {vendas_parcelada} óculos")
    
    # Seção 2: Custos e Margens
    st.markdown("### 💰 2. Estrutura de Custos")
    
    col_custo1, col_custo2 = st.columns(2)
    
    with col_custo1:
        # Custo médio por óculos
        custo_medio_oculos = st.number_input(
            "Custo médio por óculos (R$):",
            min_value=50.0,
            max_value=1000.0,
            value=st.session_state.business_data.get('custo_medio_oculos', 180.0),
            step=10.0,
            help="Custo dos produtos (lente + armação + acessórios)",
            key="novo_custo_medio_oculos"
        )
        
        # Margem desejada
        margem_desejada = st.number_input(
            "Margem desejada (%):",
            min_value=50,
            max_value=500,
            value=st.session_state.business_data.get('margem_desejada', 180),
            step=10,
            help="Margem de lucro sobre o custo",
            key="nova_margem_desejada"
        )
    
    with col_custo2:
        # Preço sugerido
        preco_sugerido = custo_medio_oculos * (1 + margem_desejada / 100)
        st.metric("Preço Sugerido", format_currency(preco_sugerido))
        
        # Margem real vs ticket médio
        if novo_ticket_medio > 0:
            margem_real = ((novo_ticket_medio - custo_medio_oculos) / custo_medio_oculos) * 100
            st.metric("Margem Real do Ticket", f"{margem_real:.1f}%")
    
    # Seção 3: Captador
    st.markdown("### 👥 3. Sistema de Captação")
    
    usar_captador = st.checkbox(
        "Usar sistema de captação",
        value=st.session_state.business_data.get('usar_sistema_captacao', False),
        key="usar_captador_premissas"
    )
    
    if usar_captador:
        col_capt1, col_capt2 = st.columns(2)
        
        with col_capt1:
            comissao_avista = st.number_input(
                "Comissão por venda à vista (R$):",
                min_value=0.0,
                max_value=100.0,
                value=st.session_state.business_data.get('comissao_avista', 30.0),
                step=1.0,
                key="nova_comissao_avista"
            )
            
            comissao_parcelada = st.number_input(
                "Comissão por venda parcelada (R$):",
                min_value=0.0,
                max_value=50.0,
                value=st.session_state.business_data.get('comissao_parcelada', 5.0),
                step=1.0,
                key="nova_comissao_parcelada"
            )
        
        with col_capt2:
            # Cálculo do custo do captador
            custo_captador_avista = vendas_avista * comissao_avista
            custo_captador_parcelada = vendas_parcelada * comissao_parcelada
            custo_captador_total = custo_captador_avista + custo_captador_parcelada
            
            st.metric("Custo Captador/Mês", format_currency(custo_captador_total))
            
            # Memória de cálculo
            with st.expander("🔍 Memória de Cálculo Captador"):
                st.code(f"""
Cálculo do Captador:
• {vendas_avista} vendas à vista × R$ {comissao_avista:.2f} = R$ {custo_captador_avista:.2f}
• {vendas_parcelada} vendas parceladas × R$ {comissao_parcelada:.2f} = R$ {custo_captador_parcelada:.2f}
TOTAL: R$ {custo_captador_total:.2f}/mês
                """)
    
    # Botão para aplicar todas as mudanças
    st.markdown("---")
    
    col_botao1, col_botao2, col_botao3 = st.columns([1, 2, 1])
    
    with col_botao2:
        if st.button("🔄 APLICAR TODAS AS PREMISSAS", type="primary", use_container_width=True, key="aplicar_premissas"):
            
            # Atualizar todas as variáveis do sistema
            st.session_state.business_data.update({
                # Vendas
                'vendas_mes_1': novo_faturamento,
                'ticket_medio': novo_ticket_medio,
                'meta_oculos_mes': nova_meta_oculos,
                'percentual_vendas_avista': percentual_avista,
                
                # Custos
                'custo_medio_oculos': custo_medio_oculos,
                'margem_desejada': margem_desejada,
                
                # Captador
                'usar_sistema_captacao': usar_captador,
                'comissao_avista': comissao_avista if usar_captador else 0,
                'comissao_parcelada': comissao_parcelada if usar_captador else 0,
                'custo_captador_mensal_calculado': custo_captador_total if usar_captador else 0,
                

                
                # Sincronizar com outras etapas
                'ticket_medio_esperado': novo_ticket_medio,  # Etapa 3
                'meta_faturamento_mensal': novo_faturamento,  # Etapa 7
                'faturamento_mensal': novo_faturamento,  # Etapa 10
            })
            
            # Recalcular captador
            if usar_captador:
                custo_captador = calcular_custo_captador_mensal()
                st.session_state.business_data['custo_captador_mensal_calculado'] = custo_captador
            
            st.success("✅ **Todas as premissas foram aplicadas com sucesso!**")
            st.balloons()
            
            # Mostrar resumo das mudanças
            with st.expander("📋 Resumo das Atualizações"):
                st.markdown(f"""
                **Vendas Atualizadas:**
                • Meta: {nova_meta_oculos} óculos/mês
                • Ticket: {format_currency(novo_ticket_medio)}
                • Faturamento: {format_currency(novo_faturamento)}
                • Distribuição: {percentual_avista}% à vista, {100-percentual_avista}% parcelado
                
                **Custos Atualizados:**
                • Custo médio: {format_currency(custo_medio_oculos)}
                • Margem: {margem_desejada}%
                • Preço sugerido: {format_currency(preco_sugerido)}
                
                **Captador:** {'Ativo' if usar_captador else 'Inativo'}
                {f'• Custo mensal: {format_currency(custo_captador_total)}' if usar_captador else ''}
                
                **Etapas Sincronizadas:**
                • Etapa 3: Ticket médio esperado
                • Etapa 7: Meta de faturamento
                • Etapa 8: Sistema de captação  
                • Etapa 10: Projeções financeiras
                """)
    
    # Seção de auditoria
    st.markdown("---")
    st.markdown("### 🔍 Auditoria do Sistema")
    
    with st.expander("Ver dados atuais do sistema"):
        dados_relevantes = {
            'vendas_mes_1': st.session_state.business_data.get('vendas_mes_1', 0),
            'ticket_medio': st.session_state.business_data.get('ticket_medio', 0),
            'custo_captador_mensal_calculado': st.session_state.business_data.get('custo_captador_mensal_calculado', 0),
            'usar_sistema_captacao': st.session_state.business_data.get('usar_sistema_captacao', False),
            'comissao_avista': st.session_state.business_data.get('comissao_avista', 0),
            'comissao_parcelada': st.session_state.business_data.get('comissao_parcelada', 0)
        }
        st.json(dados_relevantes)

if __name__ == "__main__":
    main()