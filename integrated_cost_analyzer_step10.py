"""
Sistema Integrado de Análise de Custos - VERSÃO AVANÇADA COM ANÁLISE VISUAL
Integração completa com estrutura de custos das Projeções Financeiras (Etapa 10)
Inclui análise visual avançada de custos, valuation, M&A e simuladores de crescimento
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from typing import Dict, List, Tuple

class IntegratedCostAnalyzerStep10:
    """Analisador integrado de custos com dados das Projeções Financeiras - Etapa 10"""
    
    def __init__(self):
        # Base de produtos com custos reais
        self.lens_costs = {
            'Monofocal Nacional': 35,
            'Monofocal Premium': 65,
            'Multifocal Nacional': 85,
            'Multifocal Premium': 125,
            'Progressiva Nacional': 145,
            'Progressiva Premium': 195,
            'Progressiva Grife': 285
        }
        
        self.frame_costs = {
            'Nacional Básica': 25,
            'Nacional Premium': 45,
            'Premium Nacional': 75,
            'Premium Importada': 95,
            'Grife Nacional': 135,
            'Grife Importada': 185
        }
        
        # Acessórios
        self.accessories = {
            'Limpa Lente': 2.5,
            'Paninho': 1.8,
            'Caixinha': 3.2,
            'Sacolinha': 0.5,
            'Cordinha': 4.5
        }
    
    def extract_financial_data_step10(self) -> Dict:
        """Extrai dados das Projeções Financeiras (Etapa 10)"""
        if 'business_data' not in st.session_state:
            return {}
        
        business_data = st.session_state['business_data']
        
        # Dados básicos da Etapa 10
        oculos_meta = business_data.get('oculos_meta_mes', 30)
        ticket_medio = business_data.get('ticket_medio', 500)
        
        # Custos Fixos Principais (conforme estrutura Etapa 10)
        aluguel = business_data.get('aluguel', 400)
        folha_clt = business_data.get('salarios_clt', 0)
        combustivel = business_data.get('custo_combustivel_mensal', 0)  # CORRIGIDO: chave da Etapa 10
        energia_agua = business_data.get('energia_agua', 0)
        
        # Despesas Operacionais Detalhadas (conforme Etapa 10)
        material_escritorio = business_data.get('material_escritorio', 0)
        telefone_internet = business_data.get('telefone_internet', 0)
        limpeza_seguranca = business_data.get('limpeza_seguranca', 0)
        manutencao_equipamentos = business_data.get('manutencao_equipamentos', 0)
        marketing_publicidade = business_data.get('orcamento_marketing', 0)  # CORRIGIDO: chave da Etapa 10
        contabilidade = business_data.get('contabilidade', 0)
        
        # Outros custos (conforme Etapa 10)
        servicos_profissionais = business_data.get('servicos_terceiros', 0)  # CORRIGIDO: chave da Etapa 10
        seguros_manutencao = business_data.get('seguros_manutencao', 0)
        
        return {
            'oculos_meta': oculos_meta,
            'ticket_medio': ticket_medio,
            'aluguel': aluguel,
            'folha_clt': folha_clt,
            'combustivel': combustivel,
            'energia_agua': energia_agua,
            'material_escritorio': material_escritorio,
            'telefone_internet': telefone_internet,
            'limpeza_seguranca': limpeza_seguranca,
            'manutencao_equipamentos': manutencao_equipamentos,
            'marketing_publicidade': marketing_publicidade,
            'contabilidade': contabilidade,
            'servicos_profissionais': servicos_profissionais,
            'seguros_manutencao': seguros_manutencao
        }
    
    def calculate_fixed_cost_allocation_step10(self, financial_data: Dict) -> Dict:
        """Calcula rateio de custos fixos por óculos vendido baseado na Etapa 10"""
        if financial_data.get('oculos_meta', 0) <= 0:
            return {'custo_fixo_por_oculos': 0, 'total_custos_fixos': 0}
        
        # Buscar dados da Etapa 10 usando as chaves corretas do session_state
        business_data = st.session_state.business_data
        
        # Extrair custos reais da Etapa 10 das Projeções Financeiras
        aluguel = business_data.get('aluguel', 0)
        salarios_clt = business_data.get('salarios_clt', 0) 
        total_optometrista = business_data.get('total_optometrista', 0)
        custo_combustivel = business_data.get('custo_combustivel_mensal', 0)
        outros_fixos = business_data.get('outros_fixos', 0)
        
        # Buscar custo do captador já calculado pelo sistema principal
        custo_captador = business_data.get('custo_captador_mensal_calculado', 0)
        if custo_captador == 0:
            # Fallback: calcular se não estiver disponível
            if business_data.get('usar_sistema_captacao', False):
                vendas_avista = business_data.get('vendas_avista_mes', 0)
                vendas_parceladas = business_data.get('vendas_parceladas_mes', 0)
                comissao_avista = business_data.get('comissao_avista', 30)
                comissao_parcelada = business_data.get('comissao_parcelada', 5)
                custo_captador = (vendas_avista * comissao_avista) + (vendas_parceladas * comissao_parcelada)
                if custo_captador < 150:  # Gatilho mínimo
                    custo_captador = 0
        
        # Total dos custos fixos reais da Etapa 10
        total_custos_fixos = aluguel + salarios_clt + total_optometrista + custo_combustivel + outros_fixos + custo_captador
        
        custo_fixo_por_oculos = total_custos_fixos / financial_data['oculos_meta']
        
        return {
            'total_custos_fixos': total_custos_fixos,
            'custo_fixo_por_oculos': custo_fixo_por_oculos,
            'meta_oculos': financial_data['oculos_meta']
        }
    
    def calculate_direct_costs_complete(self, lente_tipo: str, armacao_tipo: str, tratamentos: list, acessorios: list) -> Dict:
        """Calcula custos diretos completos baseado na seleção do usuário"""
        
        # Base de custos de lentes
        custos_lentes = {
            "Monofocal CR-39": 25.00,
            "Monofocal Policarbonato": 35.00,
            "Multifocal": 85.00,
            "Progressiva Digital": 120.00,
            "Progressiva Premium": 180.00
        }
        
        # Base de custos de armações
        custos_armacoes = {
            "Nacional Básica": 30.00,
            "Nacional Premium": 55.00,
            "Importada": 85.00,
            "Grife Nacional": 120.00,
            "Grife Importada": 200.00
        }
        
        # Base de custos de tratamentos
        custos_tratamentos = {
            "Antirreflexo": 15.00,
            "Fotossensível": 25.00,
            "Blue Light": 20.00,
            "Oleofóbico": 10.00,
            "Hidrofóbico": 12.00
        }
        
        # Base de custos de acessórios
        custos_acessorios = {
            "Limpa Lente": 2.50,
            "Paninho": 1.80,
            "Caixinha": 3.20,
            "Cordinha": 4.50,
            "Estojo Rígido": 8.00
        }
        
        # Calcular custos
        custo_lente = custos_lentes.get(lente_tipo, 25.00)
        custo_armacao = custos_armacoes.get(armacao_tipo, 30.00)
        custo_tratamentos_total = sum([custos_tratamentos.get(t, 0) for t in tratamentos])
        custo_acessorios_total = sum([custos_acessorios.get(a, 0) for a in acessorios])
        
        custo_total = custo_lente + custo_armacao + custo_tratamentos_total + custo_acessorios_total
        
        return {
            'lente': custo_lente,
            'armacao': custo_armacao,
            'tratamentos': custo_tratamentos_total,
            'acessorios': custo_acessorios_total,
            'total': custo_total
        }
    
    def get_market_price_complete(self, lente_tipo: str, armacao_tipo: str, tratamentos: list) -> float:
        """Obtém preço de mercado baseado na combinação de produtos"""
        
        # Base de preços de mercado por tipo de lente
        precos_lentes_mercado = {
            "Monofocal CR-39": 180.00,
            "Monofocal Policarbonato": 250.00,
            "Multifocal": 450.00,
            "Progressiva Digital": 650.00,
            "Progressiva Premium": 950.00
        }
        
        # Base de preços de mercado por tipo de armação
        precos_armacoes_mercado = {
            "Nacional Básica": 120.00,
            "Nacional Premium": 220.00,
            "Importada": 350.00,
            "Grife Nacional": 480.00,
            "Grife Importada": 750.00
        }
        
        # Adicional por tratamentos
        adicional_tratamentos = {
            "Antirreflexo": 80.00,
            "Fotossensível": 150.00,
            "Blue Light": 120.00,
            "Oleofóbico": 60.00,
            "Hidrofóbico": 70.00
        }
        
        preco_base_lente = precos_lentes_mercado.get(lente_tipo, 180.00)
        preco_base_armacao = precos_armacoes_mercado.get(armacao_tipo, 120.00)
        preco_tratamentos = sum([adicional_tratamentos.get(t, 0) for t in tratamentos])
        
        # Preço de mercado é menor que a soma individual (pacotes)
        preco_total = (preco_base_lente + preco_base_armacao + preco_tratamentos) * 0.85
        
        return round(preco_total / 10) * 10  # Arredondar para dezenas
    
    def generate_complete_analysis_step10(self, financial_data: Dict, custom_margins: Dict = None) -> pd.DataFrame:
        """Gera análise completa baseada nas Projeções Financeiras da Etapa 10"""
        
        # Verificar se dados são válidos
        if not financial_data:
            return pd.DataFrame()
        
        # Calcular rateio
        rateio_data = self.calculate_fixed_cost_allocation_step10(financial_data)
        custo_fixo_por_oculos = rateio_data['custo_fixo_por_oculos']
        ticket_medio_atual = financial_data.get('ticket_medio', 500)
        
        produtos = []
        
        # Preços de mercado para comparação
        precos_mercado_lentes = {
            "Monofocal Nacional": 280, "Monofocal Importada": 350, "Monofocal Premium": 420,
            "Multifocal Nacional": 580, "Multifocal Importada": 720, "Multifocal Premium": 850,
            "Progressiva Nacional": 680, "Progressiva Importada": 850, "Progressiva Premium": 1200
        }
        
        precos_mercado_armacoes = {
            "Nacional Básica": 150, "Nacional Premium": 280, "Importada Básica": 380,
            "Importada Premium": 550, "Grife Nacional": 680, "Grife Importada": 950
        }
        
        # Óculos completos (lente + armação) - ANÁLISE EXPANDIDA
        for lente_tipo, lente_custo in self.lens_costs.items():
            for armacao_tipo, armacao_custo in self.frame_costs.items():
                
                # Custos detalhados
                custo_lente = lente_custo
                custo_armacao = armacao_custo  
                custo_direto = custo_lente + custo_armacao
                custo_rateio = custo_fixo_por_oculos
                custo_total = custo_direto + custo_rateio
                
                # Margens personalizadas por tipo
                if 'monofocal' in lente_tipo.lower():
                    margem_base = 2.2 if custom_margins else 2.2
                elif 'multifocal' in lente_tipo.lower():
                    margem_base = 2.8 if custom_margins else 2.8
                elif 'progressiva' in lente_tipo.lower():
                    margem_base = 3.2 if custom_margins else 3.2
                else:
                    margem_base = 2.5
                
                # Preços calculados
                preco_calculado = custo_total * margem_base
                preco_calculado = round(preco_calculado / 10) * 10
                
                # Preço de mercado para comparação
                preco_mercado_lente = precos_mercado_lentes.get(lente_tipo, 350)
                preco_mercado_armacao = precos_mercado_armacoes.get(armacao_tipo, 250)
                preco_mercado_total = (preco_mercado_lente + preco_mercado_armacao) * 0.9  # Desconto pacote
                preco_mercado_total = round(preco_mercado_total / 10) * 10
                
                # Análises de rentabilidade
                lucro_unitario = preco_calculado - custo_total
                margem_percentual = ((lucro_unitario / preco_calculado) * 100) if preco_calculado > 0 else 0
                markup_percentual = ((lucro_unitario / custo_total) * 100) if custo_total > 0 else 0
                
                # Competitividade
                diferenca_mercado = preco_calculado - preco_mercado_total
                competitividade_perc = ((diferenca_mercado / preco_mercado_total) * 100) if preco_mercado_total > 0 else 0
                
                # Análise de breakeven
                if lucro_unitario > 0:
                    vendas_breakeven = rateio_data['total_custos_fixos'] / lucro_unitario
                else:
                    vendas_breakeven = 0
                
                # Ticket médio ideal e potencial de vendas
                ticket_medio_atual = financial_data.get('ticket_medio', 500)
                potencial_ticket = (preco_calculado / ticket_medio_atual) * 100 if ticket_medio_atual > 0 else 100
                
                # ROI por produto
                investimento_produto = custo_direto * 10  # Estoque típico
                roi_mensal = (lucro_unitario * 5) / investimento_produto * 100 if investimento_produto > 0 else 0  # 5 vendas/mês
                
                # Classificação de rentabilidade
                if margem_percentual >= 70:
                    classificacao = "PREMIUM"
                elif margem_percentual >= 50:
                    classificacao = "ALTA"
                elif margem_percentual >= 30:
                    classificacao = "MÉDIA"
                else:
                    classificacao = "BAIXA"
                
                produtos.append({
                    'PRODUTO': f"{lente_tipo} + {armacao_tipo}",
                    'LENTE': lente_tipo,
                    'ARMAÇÃO': armacao_tipo,
                    'CUSTO LENTE': custo_lente,
                    'CUSTO ARMAÇÃO': custo_armacao,
                    'CUSTO DIRETO': custo_direto,
                    'RATEIO FIXO': custo_rateio,
                    'CUSTO TOTAL': custo_total,
                    'PREÇO CALC.': preco_calculado,
                    'PREÇO MERCADO': preco_mercado_total,
                    'LUCRO R$': lucro_unitario,
                    'MARGEM %': margem_percentual,
                    'MARKUP %': markup_percentual,
                    'VS MERCADO %': competitividade_perc,
                    'BREAKEVEN UND': vendas_breakeven,
                    'POTENCIAL TICKET %': potencial_ticket,
                    'ROI MENSAL %': roi_mensal,
                    'CLASSIFICAÇÃO': classificacao,
                    'STATUS COMPETITIVO': 'COMPETITIVO' if abs(competitividade_perc) <= 10 else ('CARO' if competitividade_perc > 10 else 'BARATO')
                })
        
        # Lentes de Contato
        lentes_contato = [
            ('LC Diária Miopia', 25, 120, 180),
            ('LC Diária Astigmatismo', 35, 160, 240),
            ('LC Mensal Miopia', 45, 180, 280),
            ('LC Mensal Multifocal', 65, 280, 420),
            ('LC Colorida', 55, 240, 360),
            ('LC Terapêutica', 85, 350, 520)
        ]
        
        for lc_nome, custo_lc, preco_calc_lc, preco_mercado_lc in lentes_contato:
            lucro_lc = preco_calc_lc - custo_lc
            margem_lc = ((lucro_lc / preco_calc_lc) * 100) if preco_calc_lc > 0 else 0
            markup_lc = ((lucro_lc / custo_lc) * 100) if custo_lc > 0 else 0
            comp_lc = ((preco_calc_lc - preco_mercado_lc) / preco_mercado_lc * 100) if preco_mercado_lc > 0 else 0
            
            classificacao_lc = "PREMIUM" if margem_lc >= 70 else ("ALTA" if margem_lc >= 50 else ("MÉDIA" if margem_lc >= 30 else "BAIXA"))
            
            produtos.append({
                'PRODUTO': lc_nome,
                'LENTE': 'Lente de Contato',
                'ARMAÇÃO': 'N/A',
                'CUSTO LENTE': custo_lc,
                'CUSTO ARMAÇÃO': 0,
                'CUSTO DIRETO': custo_lc,
                'RATEIO FIXO': 0,  # LC não tem rateio significativo
                'CUSTO TOTAL': custo_lc,
                'PREÇO CALC.': preco_calc_lc,
                'PREÇO MERCADO': preco_mercado_lc,
                'LUCRO R$': lucro_lc,
                'MARGEM %': margem_lc,
                'MARKUP %': markup_lc,
                'VS MERCADO %': comp_lc,
                'BREAKEVEN UND': 0,
                'POTENCIAL TICKET %': (preco_calc_lc / ticket_medio_atual) * 100 if ticket_medio_atual > 0 else 100,
                'ROI MENSAL %': (lucro_lc * 8) / (custo_lc * 15) * 100,  # 8 vendas, estoque 15 unidades
                'CLASSIFICAÇÃO': classificacao_lc,
                'STATUS COMPETITIVO': 'COMPETITIVO' if abs(comp_lc) <= 10 else ('CARO' if comp_lc > 10 else 'BARATO')
            })

        # Serviços Profissionais
        servicos = [
            ('Exame de Vista Completo', 25, 120, 150),
            ('Exame de Fundo de Olho', 35, 180, 220),
            ('Adaptação LC Primeira Vez', 40, 160, 200),
            ('Adaptação LC Renovação', 25, 100, 120),
            ('Conserto Óculos Básico', 8, 35, 45),
            ('Conserto Óculos Complexo', 25, 80, 100),
            ('Troca de Parafuso', 2, 15, 20),
            ('Ajuste Completo', 5, 25, 30),
            ('Limpeza Profissional', 3, 20, 25),
            ('Certificado Oftalmológico', 10, 50, 60)
        ]
        
        for servico_nome, custo_servico, preco_servico, preco_mercado_serv in servicos:
            lucro_serv = preco_servico - custo_servico
            margem_serv = ((lucro_serv / preco_servico) * 100) if preco_servico > 0 else 0
            markup_serv = ((lucro_serv / custo_servico) * 100) if custo_servico > 0 else 0
            comp_serv = ((preco_servico - preco_mercado_serv) / preco_mercado_serv * 100) if preco_mercado_serv > 0 else 0
            
            # Serviços tem breakeven específico
            breakeven_serv = rateio_data['total_custos_fixos'] / lucro_serv if lucro_serv > 0 else 0
            
            classificacao_serv = "PREMIUM" if margem_serv >= 80 else ("ALTA" if margem_serv >= 60 else ("MÉDIA" if margem_serv >= 40 else "BAIXA"))
            
            produtos.append({
                'PRODUTO': servico_nome,
                'LENTE': 'Serviço',
                'ARMAÇÃO': 'N/A',
                'CUSTO LENTE': custo_servico,
                'CUSTO ARMAÇÃO': 0,
                'CUSTO DIRETO': custo_servico,
                'RATEIO FIXO': custo_fixo_por_oculos * 0.3,  # Serviços usam menos infraestrutura
                'CUSTO TOTAL': custo_servico + (custo_fixo_por_oculos * 0.3),
                'PREÇO CALC.': preco_servico,
                'PREÇO MERCADO': preco_mercado_serv,
                'LUCRO R$': lucro_serv,
                'MARGEM %': margem_serv,
                'MARKUP %': markup_serv,
                'VS MERCADO %': comp_serv,
                'BREAKEVEN UND': breakeven_serv,
                'POTENCIAL TICKET %': (preco_servico / ticket_medio_atual) * 100 if ticket_medio_atual > 0 else 100,
                'ROI MENSAL %': (lucro_serv * 12) / custo_servico * 100,  # 12 atendimentos/mês
                'CLASSIFICAÇÃO': classificacao_serv,
                'STATUS COMPETITIVO': 'COMPETITIVO' if abs(comp_serv) <= 10 else ('CARO' if comp_serv > 10 else 'BARATO')
            })

        # Acessórios e Produtos Complementares
        acessorios = [
            ('Limpa Lente Premium', 3.5, 25, 30),
            ('Paninho Microfibra', 2.8, 18, 22),
            ('Caixinha Rígida', 4.2, 28, 35),
            ('Cordinha Silicone', 5.5, 35, 42),
            ('Estojo Couro', 12, 65, 80),
            ('Spray Antifog', 8, 45, 55),
            ('Kit Limpeza Completo', 15, 85, 100),
            ('Óculos de Sol Básico', 35, 180, 220),
            ('Óculos de Sol Premium', 85, 420, 500),
            ('Protetor Solar Ocular', 25, 120, 150)
        ]
        
        for acess_nome, custo_acess, preco_acess, preco_mercado_acess in acessorios:
            lucro_acess = preco_acess - custo_acess
            margem_acess = ((lucro_acess / preco_acess) * 100) if preco_acess > 0 else 0
            markup_acess = ((lucro_acess / custo_acess) * 100) if custo_acess > 0 else 0
            comp_acess = ((preco_acess - preco_mercado_acess) / preco_mercado_acess * 100) if preco_mercado_acess > 0 else 0
            
            # Acessórios tem baixo rateio
            rateio_acess = custo_fixo_por_oculos * 0.1  # Apenas 10% do rateio
            custo_total_acess = custo_acess + rateio_acess
            
            classificacao_acess = "PREMIUM" if margem_acess >= 75 else ("ALTA" if margem_acess >= 55 else ("MÉDIA" if margem_acess >= 35 else "BAIXA"))
            
            produtos.append({
                'PRODUTO': acess_nome,
                'LENTE': 'Acessório',
                'ARMAÇÃO': 'N/A',
                'CUSTO LENTE': custo_acess,
                'CUSTO ARMAÇÃO': 0,
                'CUSTO DIRETO': custo_acess,
                'RATEIO FIXO': rateio_acess,
                'CUSTO TOTAL': custo_total_acess,
                'PREÇO CALC.': preco_acess,
                'PREÇO MERCADO': preco_mercado_acess,
                'LUCRO R$': lucro_acess,
                'MARGEM %': margem_acess,
                'MARKUP %': markup_acess,
                'VS MERCADO %': comp_acess,
                'BREAKEVEN UND': rateio_data['total_custos_fixos'] / lucro_acess if lucro_acess > 0 else 0,
                'POTENCIAL TICKET %': (preco_acess / ticket_medio_atual) * 100 if ticket_medio_atual > 0 else 100,
                'ROI MENSAL %': (lucro_acess * 25) / (custo_acess * 30) * 100,  # 25 vendas, estoque 30 unidades
                'CLASSIFICAÇÃO': classificacao_acess,
                'STATUS COMPETITIVO': 'COMPETITIVO' if abs(comp_acess) <= 10 else ('CARO' if comp_acess > 10 else 'BARATO')
            })

        # Pacotes e Combos (produtos premium)
        pacotes = [
            ('Óculos Completo Básico', 150, 450, 520),
            ('Óculos Completo Premium', 280, 850, 980),
            ('Óculos + LC Combo', 220, 720, 850),
            ('Exame + Óculos', 180, 580, 680),
            ('Kit Família (2 Óculos)', 320, 980, 1150),
            ('Pacote Anual LC', 180, 580, 700)
        ]
        
        for pacote_nome, custo_pacote, preco_pacote, preco_mercado_pacote in pacotes:
            lucro_pacote = preco_pacote - custo_pacote
            margem_pacote = ((lucro_pacote / preco_pacote) * 100) if preco_pacote > 0 else 0
            markup_pacote = ((lucro_pacote / custo_pacote) * 100) if custo_pacote > 0 else 0
            comp_pacote = ((preco_pacote - preco_mercado_pacote) / preco_mercado_pacote * 100) if preco_mercado_pacote > 0 else 0
            
            # Pacotes tem rateio reduzido (economia de escala)
            rateio_pacote = custo_fixo_por_oculos * 0.7
            custo_total_pacote = custo_pacote + rateio_pacote
            
            classificacao_pacote = "PREMIUM" if margem_pacote >= 65 else ("ALTA" if margem_pacote >= 45 else ("MÉDIA" if margem_pacote >= 25 else "BAIXA"))
            
            produtos.append({
                'PRODUTO': pacote_nome,
                'LENTE': 'Pacote',
                'ARMAÇÃO': 'Combo',
                'CUSTO LENTE': custo_pacote * 0.6,  # Estimativa 60% lentes
                'CUSTO ARMAÇÃO': custo_pacote * 0.4,  # Estimativa 40% armação
                'CUSTO DIRETO': custo_pacote,
                'RATEIO FIXO': rateio_pacote,
                'CUSTO TOTAL': custo_total_pacote,
                'PREÇO CALC.': preco_pacote,
                'PREÇO MERCADO': preco_mercado_pacote,
                'LUCRO R$': lucro_pacote,
                'MARGEM %': margem_pacote,
                'MARKUP %': markup_pacote,
                'VS MERCADO %': comp_pacote,
                'BREAKEVEN UND': rateio_data['total_custos_fixos'] / lucro_pacote if lucro_pacote > 0 else 0,
                'POTENCIAL TICKET %': (preco_pacote / ticket_medio_atual) * 100 if ticket_medio_atual > 0 else 100,
                'ROI MENSAL %': (lucro_pacote * 3) / (custo_pacote * 5) * 100,  # 3 vendas, estoque 5 unidades
                'CLASSIFICAÇÃO': classificacao_pacote,
                'STATUS COMPETITIVO': 'COMPETITIVO' if abs(comp_pacote) <= 10 else ('CARO' if comp_pacote > 10 else 'BARATO')
            })
        
        return pd.DataFrame(produtos)
    
    def format_currency(self, value: float) -> str:
        """Formata valor como moeda brasileira"""
        return f"R$ {value:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    
    def create_cost_breakdown_chart(self, custos_diretos: Dict, custo_indireto: float) -> go.Figure:
        """Cria gráfico de breakdown de custos por percentual"""
        total_custo = custos_diretos['total'] + custo_indireto
        
        categories = ['Lente', 'Armação', 'Tratamentos', 'Acessórios', 'Custos Fixos']
        values = [
            custos_diretos['lente'],
            custos_diretos['armacao'], 
            custos_diretos['tratamentos'],
            custos_diretos['acessorios'],
            custo_indireto
        ]
        percentages = [(v/total_custo)*100 for v in values]
        
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
        
        fig = go.Figure(data=[go.Pie(
            labels=categories,
            values=percentages,
            hole=0.4,
            marker_colors=colors,
            textinfo='label+percent',
            textfont_size=12,
            hovertemplate='<b>%{label}</b><br>' +
                         'Valor: R$ %{customdata:,.2f}<br>' +
                         'Percentual: %{percent}<br>' +
                         '<extra></extra>',
            customdata=values
        )])
        
        fig.update_layout(
            title={
                'text': 'Composição de Custos por Categoria',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 18, 'color': '#2F3349'}
            },
            showlegend=True,
            legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.05),
            height=400,
            margin=dict(t=60, b=20, l=20, r=120)
        )
        
        return fig
    
    def create_margin_waterfall_chart(self, custo_total: float, preco_final: float, componentes: Dict) -> go.Figure:
        """Cria gráfico waterfall mostrando evolução do custo ao preço final"""
        
        fig = go.Figure(go.Waterfall(
            name="Análise de Margem",
            orientation="v",
            measure=["absolute", "relative", "relative", "relative", "relative", "relative", "total"],
            x=["Custo Base", "Lente", "Armação", "Tratamentos", "Acessórios", "Custos Fixos", "Preço Final"],
            textposition="outside",
            text=[
                f"R$ {componentes['lente']:.0f}",
                f"R$ {componentes['armacao']:.0f}", 
                f"R$ {componentes['tratamentos']:.0f}",
                f"R$ {componentes['acessorios']:.0f}",
                f"R$ {componentes['custos_fixos']:.0f}",
                f"R$ {preco_final:.0f}"
            ],
            y=[
                componentes['lente'],
                componentes['armacao'],
                componentes['tratamentos'], 
                componentes['acessorios'],
                componentes['custos_fixos'],
                preco_final - custo_total
            ],
            connector={"line":{"color":"rgb(63, 63, 63)"}},
        ))
        
        fig.update_layout(
            title="Evolução do Custo ao Preço Final",
            showlegend=False,
            height=400,
            xaxis_title="Componentes",
            yaxis_title="Valor (R$)"
        )
        
        return fig
    
    def create_sensitivity_analysis(self, custos_base: Dict, margem_base: float) -> go.Figure:
        """Cria análise de sensibilidade para variações de custo e margem"""
        
        # Variações de custo (-20% a +20%)
        cost_variations = np.arange(-20, 25, 5)
        # Variações de margem (100% a 400%)
        margin_variations = [100, 150, 200, 250, 300, 350, 400]
        
        base_cost = sum(custos_base.values())
        
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Sensibilidade ao Custo', 'Sensibilidade à Margem'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Gráfico 1: Sensibilidade ao custo
        prices_cost = []
        for var in cost_variations:
            new_cost = base_cost * (1 + var/100)
            new_price = new_cost * (1 + margem_base/100)
            prices_cost.append(new_price)
        
        fig.add_trace(
            go.Scatter(x=cost_variations, y=prices_cost, mode='lines+markers',
                      name='Preço Final', line=dict(color='#FF6B6B', width=3)),
            row=1, col=1
        )
        
        # Gráfico 2: Sensibilidade à margem
        prices_margin = []
        for margin in margin_variations:
            new_price = base_cost * (1 + margin/100)
            prices_margin.append(new_price)
        
        fig.add_trace(
            go.Scatter(x=margin_variations, y=prices_margin, mode='lines+markers',
                      name='Preço Final', line=dict(color='#4ECDC4', width=3)),
            row=1, col=2
        )
        
        fig.update_xaxes(title_text="Variação do Custo (%)", row=1, col=1)
        fig.update_xaxes(title_text="Margem (%)", row=1, col=2)
        fig.update_yaxes(title_text="Preço Final (R$)", row=1, col=1)
        fig.update_yaxes(title_text="Preço Final (R$)", row=1, col=2)
        
        fig.update_layout(height=400, showlegend=False)
        
        return fig

def show_integrated_cost_analyzer_step10():
    """Interface principal do analisador integrado de custos - Etapa 10"""
    
    st.title("🏭 Sistema Integrado de Análise de Custos")
    st.markdown("**Integração 100% com Estrutura de Custos da Etapa 10**")
    
    analyzer = IntegratedCostAnalyzerStep10()
    
    # Extrair dados das Projeções Financeiras (Etapa 10)
    financial_data = analyzer.extract_financial_data_step10()
    
    if not financial_data or financial_data.get('oculos_meta', 0) <= 0:
        st.warning("⚠️ **Dados da Etapa 10 necessários**")
        st.info("Complete a **Etapa 10 → Projeções Financeiras** para usar dados reais incluindo combustível e todos os custos")
        
        with st.expander("📋 Dados Necessários na Etapa 10"):
            st.markdown("- Meta de óculos vendidos por mês")
            st.markdown("- Estrutura completa de custos fixos")
            st.markdown("- **Combustível** (conforme mostrado nas imagens)")
            st.markdown("- Aluguel, folha CLT, energia, marketing, etc.")
        return
    
    # Mostrar resumo dos dados extraídos da Etapa 10
    col_info1, col_info2, col_info3 = st.columns(3)
    
    with col_info1:
        st.metric("Meta Óculos/Mês", f"{financial_data.get('oculos_meta', 0)} unidades")
    
    with col_info2:
        st.metric("Ticket Médio", analyzer.format_currency(financial_data.get('ticket_medio', 0)))
    
    with col_info3:
        faturamento = financial_data.get('oculos_meta', 0) * financial_data.get('ticket_medio', 0)
        st.metric("Faturamento Mensal", analyzer.format_currency(faturamento))
    
    # Auditoria: Mostrar dados brutos extraídos
    with st.expander("🔍 Auditoria: Dados Brutos da Session State"):
        st.write("**Verificando chaves na session_state.business_data:**")
        if 'business_data' in st.session_state:
            business_data = st.session_state['business_data']
            combustivel_keys = [k for k in business_data.keys() if 'combustivel' in k.lower()]
            st.write(f"Chaves com 'combustivel': {combustivel_keys}")
            for key in combustivel_keys:
                st.write(f"- {key}: {business_data.get(key)}")
                
            energia_keys = [k for k in business_data.keys() if 'energia' in k.lower()]
            st.write(f"Chaves com 'energia': {energia_keys}")
            for key in energia_keys:
                st.write(f"- {key}: {business_data.get(key)}")
                
            terceiros_keys = [k for k in business_data.keys() if 'terceiros' in k.lower()]
            st.write(f"Chaves com 'terceiros': {terceiros_keys}")
            for key in terceiros_keys:
                st.write(f"- {key}: {business_data.get(key)}")
                
            optometrista_keys = [k for k in business_data.keys() if 'optometrista' in k.lower()]
            st.write(f"Chaves com 'optometrista': {optometrista_keys}")
            for key in optometrista_keys:
                st.write(f"- {key}: {business_data.get(key)}")
    

    # Estrutura de custos incluindo combustível da Etapa 10
    with st.expander("📊 Estrutura de Custos da Etapa 10 (Projeções Financeiras)", expanded=True):
        rateio_data = analyzer.calculate_fixed_cost_allocation_step10(financial_data)
        
        col_custos1, col_custos2 = st.columns(2)
        
        # Buscar dados corretos da Etapa 10
        business_data = st.session_state.business_data
        
        with col_custos1:
            st.markdown("**Custos Principais:**")
            st.write(f"• Aluguel: {analyzer.format_currency(business_data.get('aluguel', 0))}")
            st.write(f"• Folha CLT: {analyzer.format_currency(business_data.get('salarios_clt', 0))}")
            st.write(f"• Optometrista: {analyzer.format_currency(business_data.get('total_optometrista', 0))}")
            
            # Calcular e mostrar custo do captador
            custo_captador_display = 0
            if business_data.get('usar_sistema_captacao', False):
                vendas_avista = business_data.get('vendas_avista_mes', 0)
                vendas_parceladas = business_data.get('vendas_parceladas_mes', 0)
                comissao_avista = business_data.get('comissao_avista', 30)
                comissao_parcelada = business_data.get('comissao_parcelada', 5)
                custo_captador_display = (vendas_avista * comissao_avista) + (vendas_parceladas * comissao_parcelada)
                if custo_captador_display < 150:
                    custo_captador_display = 0
            
            st.write(f"• **Captador: {analyzer.format_currency(custo_captador_display)}**")
        
        with col_custos2:
            st.markdown("**Outros Custos:**")
            st.write(f"• **Combustível: {analyzer.format_currency(business_data.get('custo_combustivel_mensal', 0))}**")
            st.write(f"• Outros custos: {analyzer.format_currency(business_data.get('outros_fixos', 0))}")
            st.write("  (inclui energia, telefone, marketing, etc.)")
        
        st.markdown("**Resumo do Rateio:**")
        col_rateio1, col_rateio2 = st.columns(2)
        with col_rateio1:
            st.metric("Total Custos Operacionais", analyzer.format_currency(rateio_data['total_custos_fixos']))
        with col_rateio2:
            st.metric("Rateio por Óculos", analyzer.format_currency(rateio_data['custo_fixo_por_oculos']))
    
    # Seletor de produto para análise de custo completo
    st.markdown("## 🔧 Análise de Custo Completo por Produto")
    
    col_produto1, col_produto2, col_produto3, col_produto4 = st.columns(4)
    
    with col_produto1:
        st.markdown("**Lente**")
        lente_selecionada = st.selectbox(
            "Tipo de Lente", 
            ["Monofocal CR-39", "Monofocal Policarbonato", "Multifocal", "Progressiva Digital", "Progressiva Premium"],
            key="lente_analise_step10"
        )
    
    with col_produto2:
        st.markdown("**Armação**")
        armacao_selecionada = st.selectbox(
            "Tipo de Armação",
            ["Nacional Básica", "Nacional Premium", "Importada", "Grife Nacional", "Grife Importada"],
            key="armacao_analise_step10"
        )
    
    with col_produto3:
        st.markdown("**Tratamentos**")
        tratamentos = st.multiselect(
            "Tratamentos",
            ["Antirreflexo", "Fotossensível", "Blue Light", "Oleofóbico", "Hidrofóbico"],
            default=["Antirreflexo"],
            key="tratamentos_analise_step10"
        )
    
    with col_produto4:
        st.markdown("**Acessórios**")
        acessorios = st.multiselect(
            "Acessórios",
            ["Limpa Lente", "Paninho", "Caixinha", "Cordinha", "Estojo Rígido"],
            default=["Limpa Lente", "Paninho", "Caixinha"],
            key="acessorios_analise_step10"
        )
    
    # Calcular custos diretos do produto selecionado
    custos_diretos = analyzer.calculate_direct_costs_complete(
        lente_selecionada, armacao_selecionada, tratamentos, acessorios
    )
    
    # Calcular rateio de custos indiretos
    custo_indireto_por_oculos = rateio_data['custo_fixo_por_oculos']
    
    # Custo total
    custo_total = custos_diretos['total'] + custo_indireto_por_oculos
    
    # Tabs principais para análise visual
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Análise Visual de Custos", 
        "💎 Composição do Produto", 
        "📈 Análise Avançada",
        "🎯 Simulador de Cenários",
        "💼 Valuation & M&A"
    ])
    
    with tab1:
        st.markdown("## 📊 Análise Visual de Custos")
        
        # Slider de margem personalizada DENTRO da tab
        margem_personalizada = st.slider(
            "💰 Margem de Lucro Desejada (%)",
            min_value=10,
            max_value=900,
            value=200,
            step=10,
            key="margem_visual_custos_step10"
        ) / 100
        
        # Calcular preço final para os gráficos
        preco_final = custo_total * (1 + margem_personalizada)
        preco_final = round(preco_final / 10) * 10
        
        # Preparar dados para gráficos
        componentes_grafico = {
            'lente': custos_diretos['lente'],
            'armacao': custos_diretos['armacao'],
            'tratamentos': custos_diretos['tratamentos'],
            'acessorios': custos_diretos['acessorios'],
            'custos_fixos': custo_indireto_por_oculos
        }
        
        # Gráfico 1: Breakdown por percentual (Pizza)
        st.markdown("### 🥧 Composição de Custos por Categoria")
        fig_pie = analyzer.create_cost_breakdown_chart(custos_diretos, custo_indireto_por_oculos)
        st.plotly_chart(fig_pie, use_container_width=True)
        
        # Resumo visual melhorado sem gráficos desnecessários
        st.markdown("### 💰 Resumo Financeiro do Produto")
        
        col_visual1, col_visual2, col_visual3 = st.columns(3)
        
        with col_visual1:
            st.metric("Custo Total", analyzer.format_currency(custo_total))
        
        with col_visual2:
            st.metric("Preço Final", analyzer.format_currency(preco_final))
        
        with col_visual3:
            margem_real = ((preco_final - custo_total) / preco_final * 100) if preco_final > 0 else 0
            st.metric("Margem Real", f"{margem_real:.1f}%")
        
        # Resumo numérico com EBITDA
        col_visual1, col_visual2, col_visual3, col_visual4, col_visual5 = st.columns(5)
        
        with col_visual1:
            percentual_direto = (custos_diretos['total'] / custo_total) * 100 if custo_total > 0 else 0
            st.metric("Custos Diretos", f"{percentual_direto:.1f}%", f"{analyzer.format_currency(custos_diretos['total'])}")
        
        with col_visual2:
            percentual_fixo = (custo_indireto_por_oculos / custo_total) * 100 if custo_total > 0 else 0
            st.metric("Custos Fixos", f"{percentual_fixo:.1f}%", f"{analyzer.format_currency(custo_indireto_por_oculos)}")
        
        with col_visual3:
            st.metric("Custo Total", analyzer.format_currency(custo_total))
        
        with col_visual4:
            margem_real = ((preco_final - custo_total) / custo_total) * 100 if custo_total > 0 else 0
            st.metric("Margem Real", f"{margem_real:.1f}%", f"{analyzer.format_currency(preco_final - custo_total)}")
        
        with col_visual5:
            # EBITDA baseado na margem líquida + estimativa de depreciação
            margem_liquida = ((preco_final - custo_total) / preco_final) * 100 if preco_final > 0 else 0
            ebitda_estimado = margem_liquida * 1.05  # +5% para depreciação
            st.metric("EBITDA %", f"{ebitda_estimado:.1f}%", "Margem EBITDA")
    
    with tab2:
        st.markdown("## 💎 Composição Final do Produto")
        
        col_custo1, col_custo2, col_custo3, col_custo4 = st.columns(4)
        
        with col_custo1:
            st.markdown("**💎 Custo Direto**")
            st.metric("Materiais", analyzer.format_currency(custos_diretos['total']))
        with st.expander("Breakdown"):
            st.write(f"• Lente: {analyzer.format_currency(custos_diretos['lente'])}")
            st.write(f"• Armação: {analyzer.format_currency(custos_diretos['armacao'])}")
            st.write(f"• Tratamentos: {analyzer.format_currency(custos_diretos['tratamentos'])}")
            st.write(f"• Acessórios: {analyzer.format_currency(custos_diretos['acessorios'])}")
    
    with col_custo2:
        st.markdown("**🏢 Custo Indireto**")
        st.metric("Rateio Operacional", analyzer.format_currency(custo_indireto_por_oculos))
        with st.expander("Breakdown"):
            st.write(f"• Total mensal: {analyzer.format_currency(rateio_data['total_custos_fixos'])}")
            st.write(f"• Meta óculos: {rateio_data['meta_oculos']}")
            st.write(f"• Por óculos: {analyzer.format_currency(custo_indireto_por_oculos)}")
    
    with col_custo3:
        st.markdown("**📊 Custo Total**")
        st.metric("Custo Completo", analyzer.format_currency(custo_total))
        margem_aplicada = st.slider("Margem (%)", 0, 900, 250, 10, key="margem_total_step10")
        preco_sugerido = custo_total * (1 + margem_aplicada / 100)
        preco_sugerido = round(preco_sugerido / 10) * 10  # Arredondar para dezenas
    
    with col_custo4:
        st.markdown("**💲 Preço Final**")
        st.metric("Preço Sugerido", analyzer.format_currency(preco_sugerido))
        margem_real = ((preco_sugerido - custo_total) / custo_total) * 100 if custo_total > 0 else 0
        st.write(f"Margem Real: {margem_real:.1f}%")
    
    # Comparação com preço de mercado
    preco_mercado = analyzer.get_market_price_complete(lente_selecionada, armacao_selecionada, tratamentos)
    
    col_comp1, col_comp2, col_comp3 = st.columns(3)
    
    with col_comp1:
        st.markdown("**🏪 Preço de Mercado**")
        st.metric("Referência", analyzer.format_currency(preco_mercado))
        competitividade = ((preco_sugerido - preco_mercado) / preco_mercado) * 100 if preco_mercado > 0 else 0
        if competitividade > 0:
            st.warning(f"↗️ {competitividade:.1f}% acima do mercado")
        else:
            st.success(f"↙️ {abs(competitividade):.1f}% abaixo do mercado")
    
    with col_comp2:
        st.markdown("**📈 Análise de Viabilidade**")
        lucro_unitario = preco_sugerido - custo_total
        st.metric("Lucro por Unidade", analyzer.format_currency(lucro_unitario))
        if lucro_unitario > 0:
            vendas_para_breakeven = rateio_data['total_custos_fixos'] / lucro_unitario
            st.write(f"Breakeven: {vendas_para_breakeven:.0f} unidades/mês")
    
    with col_comp3:
        st.markdown("**⚡ Simulação Rápida**")
        vendas_simuladas = st.number_input("Vendas/mês", 1, 200, 30, key="vendas_sim_step10")
        receita_simulada = vendas_simuladas * preco_sugerido
        custo_simulado = vendas_simuladas * custo_total
        lucro_simulado = receita_simulada - custo_simulado
        st.metric("Lucro Mensal", analyzer.format_currency(lucro_simulado))
    
    # Gerar análise completa
    custom_margins = st.session_state.get('custom_margins_step10', None)
    df_analysis = analyzer.generate_complete_analysis_step10(financial_data, custom_margins)
    
    if not df_analysis.empty:
        # Tabs organizadas
        tab1, tab2, tab3 = st.tabs(["📊 Tabela Completa", "📈 Análise de Rentabilidade", "🔍 Comparação de Preços"])
        
        with tab1:
            st.markdown("### 📊 Tabela Completa de Preços")
            st.markdown("**Baseada na estrutura de custos da Etapa 10 incluindo combustível**")
            
            # Filtros
            col_filter1, col_filter2 = st.columns(2)
            with col_filter1:
                tipos_lente = ['Todos'] + list(df_analysis[df_analysis['LENTE'] != 'Serviço']['LENTE'].unique())
                filtro_lente = st.selectbox("Filtrar por Lente", tipos_lente, key="filtro_lente_step10")
            
            with col_filter2:
                incluir_servicos = st.checkbox("Incluir Serviços", value=True, key="incluir_servicos_step10")
            
            # Aplicar filtros
            df_filtered = df_analysis.copy()
            if filtro_lente != 'Todos':
                df_filtered = df_filtered[df_filtered['LENTE'] == filtro_lente]
            if not incluir_servicos:
                df_filtered = df_filtered[df_filtered['LENTE'] != 'Serviço']
            
            # Mostrar tabela
            st.dataframe(
                df_filtered,
                use_container_width=True,
                hide_index=True
            )
    
    with tab3:
        st.markdown("## 📈 Análise Avançada de Performance")
        
        # Análise de rentabilidade por categoria
        col_perf1, col_perf2 = st.columns(2)
        
        with col_perf1:
            st.markdown("### 💰 Top 5 Produtos por Margem")
            if not df_analysis.empty and 'MARGEM R$' in df_analysis.columns:
                top_margin = df_analysis.nlargest(5, 'MARGEM R$')[['PRODUTO', 'MARGEM R$', 'MARGEM %']]
                for _, row in top_margin.iterrows():
                    st.write(f"• {row['PRODUTO']}: {analyzer.format_currency(row['MARGEM R$'])} ({row['MARGEM %']:.1f}%)")
        
        with col_perf2:
            st.markdown("### 🎯 Recomendações Estratégicas")
            if not df_analysis.empty:
                media_margem = df_analysis['MARGEM %'].mean()
                st.write(f"• Margem média: {media_margem:.1f}%")
                
                produtos_alta_margem = len(df_analysis[df_analysis['MARGEM %'] > 200])
                total_produtos = len(df_analysis)
                percentual_alta_margem = (produtos_alta_margem / total_produtos) * 100
                st.write(f"• Produtos com margem >200%: {produtos_alta_margem}/{total_produtos} ({percentual_alta_margem:.1f}%)")
                
                if percentual_alta_margem < 30:
                    st.warning("⚠️ Considere aumentar margens em produtos de baixo giro")
                else:
                    st.success("✅ Portfolio bem equilibrado em margens")
    
    with tab4:
        st.markdown("## 🎯 Simulador de Cenários Avançado")
        
        col_sim1, col_sim2 = st.columns(2)
        
        with col_sim1:
            st.markdown("### 📊 Parâmetros de Simulação")
            
            # Cenários de volume
            cenario_volume = st.selectbox(
                "Cenário de Volume",
                ["Conservador (-20%)", "Realista (Base)", "Otimista (+30%)", "Agressivo (+50%)"],
                index=1
            )
            
            # Fatores de ajuste de volume
            volume_factors = {
                "Conservador (-20%)": 0.8,
                "Realista (Base)": 1.0,
                "Otimista (+30%)": 1.3,
                "Agressivo (+50%)": 1.5
            }
            
            volume_factor = volume_factors[cenario_volume]
            meta_ajustada = int(financial_data.get('oculos_meta', 50) * volume_factor)
            
            # Cenários de margem
            margem_cenario = st.selectbox(
                "Estratégia de Margem",
                ["Competitiva (150%)", "Padrão (200%)", "Premium (300%)", "Luxo (400%)"],
                index=1
            )
            
            margin_values = {
                "Competitiva (150%)": 1.5,
                "Padrão (200%)": 2.0,
                "Premium (300%)": 3.0,
                "Luxo (400%)": 4.0
            }
            
            margem_valor = margin_values[margem_cenario]
            
            # Cenários de custo
            custo_cenario = st.selectbox(
                "Cenário de Custos",
                ["Otimizado (-10%)", "Atual (Base)", "Inflacionado (+15%)", "Crise (+25%)"],
                index=1
            )
            
            cost_factors = {
                "Otimizado (-10%)": 0.9,
                "Atual (Base)": 1.0,
                "Inflacionado (+15%)": 1.15,
                "Crise (+25%)": 1.25
            }
            
            cost_factor = cost_factors[custo_cenario]
        
        with col_sim2:
            st.markdown("### 💼 Resultados da Simulação")
            
            # Calcular métricas do cenário
            custo_ajustado = custo_total * cost_factor
            preco_cenario = custo_ajustado * margem_valor
            preco_cenario = round(preco_cenario / 10) * 10
            
            # Receita e lucro mensal
            receita_mensal = meta_ajustada * preco_cenario
            custo_mensal_produtos = meta_ajustada * custo_ajustado
            custos_fixos_totais = rateio_data['total_custos_fixos']
            lucro_bruto = receita_mensal - custo_mensal_produtos
            lucro_liquido = lucro_bruto - custos_fixos_totais
            
            # EBITDA do cenário
            ebitda_cenario = lucro_liquido * 1.05  # +5% para depreciação
            ebitda_margem = (ebitda_cenario / receita_mensal * 100) if receita_mensal > 0 else 0
            
            # Exibir métricas
            st.metric("Meta Óculos Ajustada", f"{meta_ajustada} unid/mês")
            st.metric("Preço Médio", analyzer.format_currency(preco_cenario))
            st.metric("Receita Mensal", analyzer.format_currency(receita_mensal))
            st.metric("Lucro Líquido", analyzer.format_currency(lucro_liquido))
            st.metric("EBITDA", f"{analyzer.format_currency(ebitda_cenario)} ({ebitda_margem:.1f}%)")
            
            # Margem líquida
            margem_liquida = (lucro_liquido / receita_mensal * 100) if receita_mensal > 0 else 0
            
            if margem_liquida > 15:
                st.success(f"✅ Margem líquida excelente: {margem_liquida:.1f}%")
            elif margem_liquida > 8:
                st.info(f"🔵 Margem líquida adequada: {margem_liquida:.1f}%")
            else:
                st.warning(f"⚠️ Margem líquida baixa: {margem_liquida:.1f}%")
            
            # ROI anualizado
            investimento_inicial = st.session_state.business_data.get('investimento_total', 100000)
            roi_anual = (lucro_liquido * 12 / investimento_inicial * 100) if investimento_inicial > 0 else 0
            
            st.markdown("### 📈 Indicadores Anualizados")
            st.metric("ROI Anual", f"{roi_anual:.1f}%")
            
            # Payback
            if lucro_liquido > 0:
                payback_meses = investimento_inicial / lucro_liquido
                st.metric("Payback", f"{payback_meses:.1f} meses")
            else:
                st.error("Cenário inviável - Payback indefinido")
    
    with tab5:
        st.markdown("## 💼 Valuation & Análise M&A")
        
        col_val1, col_val2 = st.columns(2)
        
        with col_val1:
            st.markdown("### 💰 Valuation Múltiplos de Mercado")
            
            # Receita anual baseada no cenário atual
            receita_anual = (financial_data.get('oculos_meta', 50) * 
                           financial_data.get('ticket_medio', 500) * 12)
            
            # EBITDA estimado (lucro líquido + depreciação estimada)
            lucro_mensal_base = (financial_data.get('oculos_meta', 50) * preco_final) - rateio_data['total_custos_fixos']
            ebitda_anual = lucro_mensal_base * 12 * 1.05  # +5% para depreciação
            ebitda_percentual = (ebitda_anual / receita_anual * 100) if receita_anual > 0 else 0
            
            st.write(f"**Receita Anual Estimada:** {analyzer.format_currency(receita_anual)}")
            st.write(f"**EBITDA Anual Estimado:** {analyzer.format_currency(ebitda_anual)}")
            st.write(f"**EBITDA Margem:** {ebitda_percentual:.1f}%")
            
            # Múltiplos típicos do setor ótico
            st.markdown("**Múltiplos de Mercado - Setor Ótico:**")
            
            # Valuation por receita
            multiplo_receita_baixo = 0.8
            multiplo_receita_alto = 1.5
            
            valor_receita_baixo = receita_anual * multiplo_receita_baixo
            valor_receita_alto = receita_anual * multiplo_receita_alto
            
            st.write(f"• P/Receita (0.8-1.5x): {analyzer.format_currency(valor_receita_baixo)} - {analyzer.format_currency(valor_receita_alto)}")
            
            # Valuation por EBITDA
            if ebitda_anual > 0:
                multiplo_ebitda_baixo = 3.5
                multiplo_ebitda_alto = 6.0
                
                valor_ebitda_baixo = ebitda_anual * multiplo_ebitda_baixo
                valor_ebitda_alto = ebitda_anual * multiplo_ebitda_alto
                
                st.write(f"• EV/EBITDA (3.5-6.0x): {analyzer.format_currency(valor_ebitda_baixo)} - {analyzer.format_currency(valor_ebitda_alto)}")
            
            # Valuation médio
            if ebitda_anual > 0:
                valor_medio = (valor_receita_baixo + valor_receita_alto + valor_ebitda_baixo + valor_ebitda_alto) / 4
                st.success(f"**Valuation Médio Estimado: {analyzer.format_currency(valor_medio)}**")
        
        with col_val2:
            st.markdown("### 🚀 Análise de Crescimento e Expansão")
            
            # Simulador de crescimento
            crescimento_anual = st.slider("Taxa de Crescimento Anual (%)", 5, 50, 15, 5)
            anos_projecao = st.slider("Anos de Projeção", 3, 10, 5)
            
            # Projeção de crescimento
            projecoes = []
            receita_atual = receita_anual
            ebitda_atual = ebitda_anual
            
            for ano in range(1, anos_projecao + 1):
                receita_projetada = receita_atual * ((1 + crescimento_anual/100) ** ano)
                ebitda_projetado = ebitda_atual * ((1 + crescimento_anual/100) ** ano)
                
                projecoes.append({
                    'Ano': f"Ano {ano}",
                    'Receita': receita_projetada,
                    'EBITDA': ebitda_projetado
                })
            
            df_projecoes = pd.DataFrame(projecoes)
            
            st.markdown("**Projeções de Crescimento:**")
            for _, row in df_projecoes.iterrows():
                st.write(f"• {row['Ano']}: Receita {analyzer.format_currency(row['Receita'])}, EBITDA {analyzer.format_currency(row['EBITDA'])}")
            
            # Cenários de expansão
            st.markdown("### 🏪 Cenários de Expansão")
            
            num_lojas = st.selectbox("Número de Lojas", [1, 2, 3, 5, 10], index=0)
            
            if num_lojas > 1:
                receita_multi_lojas = receita_anual * num_lojas * 0.85  # 15% desconto por economia de escala
                investimento_expansao = investimento_inicial * (num_lojas - 1) * 0.8  # 20% desconto por experiência
                
                st.write(f"**Receita Anual ({num_lojas} lojas):** {analyzer.format_currency(receita_multi_lojas)}")
                st.write(f"**Investimento Adicional:** {analyzer.format_currency(investimento_expansao)}")
                
                # ROI da expansão
                lucro_adicional = receita_multi_lojas - receita_anual
                roi_expansao = (lucro_adicional / investimento_expansao * 100) if investimento_expansao > 0 else 0
                
                if roi_expansao > 25:
                    st.success(f"🚀 Expansão muito atrativa: ROI {roi_expansao:.1f}%")
                elif roi_expansao > 15:
                    st.info(f"💼 Expansão viável: ROI {roi_expansao:.1f}%")
                else:
                    st.warning(f"⚠️ Expansão arriscada: ROI {roi_expansao:.1f}%")
            
            # Estratégias de saída
            st.markdown("### 🎯 Estratégias de Saída (Exit)")
            
            exit_strategy = st.selectbox(
                "Estratégia de Saída",
                ["Venda Estratégica", "Aquisição por Rede", "IPO (Expansão)", "Gestão Familiar"]
            )
            
            if exit_strategy == "Venda Estratégica":
                st.info("💼 Múltiplo típico: 4-7x EBITDA. Foco em rentabilidade e sistemas.")
            elif exit_strategy == "Aquisição por Rede":
                st.info("🏪 Múltiplo típico: 1-2x Receita. Foco em localização e customer base.")
            elif exit_strategy == "IPO (Expansão)":
                st.info("🚀 Múltiplo típico: 8-15x EBITDA. Necessário >20 lojas e crescimento >30%.")
            else:
                st.info("👨‍👩‍👧‍👦 Foco em sustentabilidade e passagem geracional.")
    
    # Adicionar download da análise completa
    st.markdown("---")
    col_download1, col_download2 = st.columns(2)
    
    with col_download1:
        if st.button("📊 Download Análise Completa", use_container_width=True):
            if not df_analysis.empty:
                csv = df_analysis.to_csv(index=False, encoding='utf-8-sig')
                st.download_button(
                    label="💾 Baixar CSV",
                    data=csv,
                    file_name=f"analise_custos_{financial_data.get('nome_empresa', 'otica')}.csv",
                    mime="text/csv"
                )
    
    with col_download2:
        if st.button("📈 Gerar Relatório Executivo", use_container_width=True):
            st.info("Funcionalidade em desenvolvimento - Relatório com gráficos e insights executivos")
    
    # Adicionar seção de análise expandida
    if not df_analysis.empty:
        st.markdown("---")
        st.markdown("## 🎯 Análise Expandida")
        
        # Top produtos mais rentáveis
        df_oculos = df_analysis[df_analysis['LENTE'] != 'Serviço'].copy()
        if len(df_oculos) > 0:
            col_exp1, col_exp2 = st.columns(2)
            
            with col_exp1:
                st.markdown("### 💰 Produtos Mais Rentáveis")
                top_rentaveis = df_oculos.head(5)
                for _, produto in top_rentaveis.iterrows():
                    lucro = produto.get('LUCRO R$', 0)
                    margem = produto.get('MARGEM %', 0)
                    st.write(f"• {produto['PRODUTO']}: {analyzer.format_currency(float(lucro))} ({margem:.1f}%)")
            
            with col_exp2:
                st.markdown("### 📊 Estrutura de Custo (Etapa 10)")
                st.write(f"• Rateio por óculos: {analyzer.format_currency(rateio_data['custo_fixo_por_oculos'])}")
                st.write(f"• Total custos fixos: {analyzer.format_currency(rateio_data['total_custos_fixos'])}")
                st.write(f"• Meta óculos/mês: {rateio_data['meta_oculos']}")
    else:
        st.error("❌ Erro ao gerar análise. Verifique os dados da Etapa 10.")