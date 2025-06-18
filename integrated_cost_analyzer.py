"""
Sistema Integrado de Análise de Custos para Óculos
Baseado na estrutura real de custos do sistema de Projeções Financeiras
Implementa apuração única e precisa conforme exemplo do usuário
"""

import streamlit as st
import pandas as pd
from typing import Dict, List, Tuple
import json

class IntegratedCostAnalyzer:
    """Analisador integrado de custos - fonte única de verdade baseada nas Projeções Financeiras"""
    
    def __init__(self):
        self.load_product_database()
        self.load_market_prices()
        self.load_financial_fees()
    
    def load_product_database(self):
        """Base completa de produtos real do sistema com custos atuais"""
        
        # Lentes por tipo e categoria
        self.lenses_costs = {
            'Monofocal': {
                'Nacional Básica': 35.00,
                'Nacional Premium': 45.00,
                'Importada Básica': 55.00,
                'Importada Premium': 85.00,
                'Grife Nacional': 120.00,
                'Grife Importada': 180.00
            },
            'Multifocal': {
                'Nacional Básica': 65.00,
                'Nacional Premium': 85.00,
                'Importada Básica': 95.00,
                'Importada Premium': 120.00,
                'Grife Nacional': 150.00,
                'Grife Importada': 220.00
            },
            'Progressiva': {
                'Nacional Básica': 85.00,
                'Nacional Premium': 110.00,
                'Importada Básica': 120.00,
                'Importada Premium': 150.00,
                'Grife Nacional': 220.00,
                'Grife Importada': 350.00
            }
        }
        
        # Tratamentos para lentes
        self.treatments_costs = {
            'Anti-reflexo Básico': 15.00,
            'Anti-reflexo Premium': 25.00,
            'Antirisco': 12.00,
            'Transitions (Fotossensível)': 45.00,
            'Blue Control (Luz Azul)': 20.00,
            'Polarizada': 35.00,
            'Espelhada': 18.00,
            'Hidrofóbica': 8.00
        }
        
        # Armações por categoria
        self.frames_costs = {
            'Nacional Básica': 25.00,
            'Nacional Premium': 45.00,
            'Importada Básica': 35.00,
            'Importada Premium': 65.00,
            'Grife Nacional': 80.00,
            'Grife Importada': 120.00,
            'Infantil Nacional': 30.00,
            'Infantil Importada': 50.00,
            'Esportiva Nacional': 40.00,
            'Esportiva Importada': 70.00
        }
        
        # Serviços oferecidos
        self.services_costs = {
            'Exame de Vista Básico': 80.00,
            'Exame de Vista Completo': 120.00,
            'Teste de Lente de Contato': 50.00,
            'Adaptação Lente de Contato': 80.00,
            'Conserto de Óculos': 25.00,
            'Ajuste de Armação': 15.00,
            'Limpeza Ultrassônica': 10.00,
            'Troca de Parafusos': 8.00,
            'Solda de Armação': 35.00,
            'Cópia de Receita': 12.00
        }
        
        # Acessórios
        self.accessories_costs = {
            'Caixinha Básica': 1.20,
            'Caixinha Premium': 2.50,
            'Paninho Microfibra': 0.80,
            'Limpa Lente Spray': 2.50,
            'Sacolinha Papel': 0.30,
            'Sacolinha TNT': 0.60,
            'Cordinha Básica': 3.00,
            'Cordinha Premium': 8.00,
            'Estojo Rígido': 15.00,
            'Kit Limpeza': 12.00
        }
        
        # Lentes de contato (se oferecidas)
        self.contact_lenses_costs = {
            'Gelatinosa Mensal': 25.00,
            'Gelatinosa Quinzenal': 35.00,
            'Gelatinosa Diária': 45.00,
            'Rígida': 80.00,
            'Tórica (Astigmatismo)': 55.00,
            'Multifocal': 65.00,
            'Colorida': 40.00
        }
    
    def load_market_prices(self):
        """Preços de mercado baseados nas tabelas reais do sistema"""
        self.market_prices = {
            ('Monofocal Nacional', 'Nacional Básica'): {'min': 180, 'avg': 220, 'max': 280},
            ('Monofocal Nacional', 'Nacional Premium'): {'min': 240, 'avg': 290, 'max': 350},
            ('Monofocal Premium', 'Nacional Premium'): {'min': 290, 'avg': 340, 'max': 420},
            ('Multifocal Nacional', 'Nacional Básica'): {'min': 380, 'avg': 450, 'max': 520},
            ('Multifocal Premium', 'Nacional Premium'): {'min': 480, 'avg': 550, 'max': 650},
            ('Progressiva Nacional', 'Nacional Básica'): {'min': 450, 'avg': 520, 'max': 600},
            ('Progressiva Premium', 'Nacional Premium'): {'min': 580, 'avg': 680, 'max': 780},
            ('Progressiva Grife', 'Grife Nacional'): {'min': 850, 'avg': 1200, 'max': 1800},
            ('Progressiva Grife', 'Grife Importada'): {'min': 1200, 'avg': 1800, 'max': 2500}
        }
    
    def load_financial_fees(self):
        """Taxas financeiras das operadoras"""
        self.financial_fees = {
            'À Vista (0 dias)': 0.0,
            'Antecipação (até 30 dias)': 4.25,  # Média 3,99% - 4,5%
            'Parcelado (30-60 dias)': 2.425,   # Média 2,35% - 2,5%
            'Parcelado (60-90 dias)': 3.2,
            'Parcelado (90+ dias)': 4.8
        }
    
    def extract_financial_data(self) -> Dict:
        """Extrai dados das Projeções Financeiras (Etapa 10) do session_state"""
        if 'business_data' not in st.session_state:
            st.session_state.business_data = {}
        
        business_data = st.session_state.business_data
        
        # Calcular meta de óculos baseada nos dados reais das Projeções Financeiras
        vendas_mes_1 = business_data.get('vendas_mes_1', 0)
        ticket_medio = business_data.get('ticket_medio', 460)
        
        # Calcular meta de óculos baseada no faturamento e ticket médio
        meta_oculos_calculada = 0
        if vendas_mes_1 > 0 and ticket_medio > 0:
            meta_oculos_calculada = int(vendas_mes_1 / ticket_medio)
        
        # Usar o valor calculado ou o definido manualmente
        meta_oculos_final = business_data.get('oculos_meta_mes', meta_oculos_calculada)
        
        # Dados essenciais para análise de custos - TODOS vêm das Projeções Financeiras
        extracted_data = {
            # Meta de vendas baseada em dados reais
            'meta_oculos_mes': meta_oculos_final,
            'ticket_medio': ticket_medio,
            'faturamento_mensal': vendas_mes_1,
            
            # Custos fixos detalhados da Etapa 10 - TODOS OS CUSTOS INCLUÍDOS
            'aluguel': business_data.get('aluguel', 0),
            'folha_clt': business_data.get('salarios_clt', 0),
            'servicos_terceirizados': business_data.get('servicos_terceirizados', 0),
            'optometrista': business_data.get('custo_optometrista_mensal', 0),
            'combustivel': business_data.get('combustivel', 0),  # COMBUSTÍVEL INCLUÍDO
            'telefone_internet': business_data.get('telefone_internet', 0),
            'energia_agua': business_data.get('energia_agua', 0),
            'marketing_publicidade': business_data.get('marketing_publicidade', 0),
            'seguros': business_data.get('seguros', 0),
            'iptu_licencas': business_data.get('iptu_licencas', 0),
            'material_escritorio': business_data.get('material_escritorio', 0),
            'material_limpeza': business_data.get('material_limpeza', 0),
            'contabilidade': business_data.get('contabilidade', 0),
            'limpeza_seguranca': business_data.get('limpeza_seguranca', 0),
            'manutencao_equipamentos': business_data.get('manutencao_equipamentos', 0),
            'software_sistemas': business_data.get('software_sistemas', 0),
            'despesas_bancarias': business_data.get('despesas_bancarias', 0),
            'outras_despesas': business_data.get('outras_despesas', 0),
            
            # Custo fixo total por óculos já calculado na Etapa 10
            'custo_fixo_por_oculos': business_data.get('custo_fixo_por_oculos', 0),
            
            # Dados da empresa
            'nome_empresa': business_data.get('nome_empresa', 'Ótica Exemplo'),
            'cidade': business_data.get('cidade', 'São Paulo'),
            'estado': business_data.get('estado', 'SP')
        }
        
        return extracted_data
    
    def calculate_fixed_cost_allocation(self, financial_data: Dict) -> Dict:
        """Calcula rateio de custos fixos por óculos vendido"""
        meta_oculos = financial_data['meta_oculos_mes']
        
        if meta_oculos <= 0:
            meta_oculos = 115  # Fallback padrão
        
        # Custos fixos individuais exatamente como na Etapa 10
        custos_fixos = {
            'Aluguel': financial_data['aluguel'],
            'Folha CLT': financial_data['folha_clt'],
            'Optometrista': financial_data['optometrista'],
            'Despesas Operacionais': (
                financial_data['energia_agua'] + financial_data['telefone_internet'] + 
                financial_data['material_escritorio'] + financial_data['contabilidade'] + 
                financial_data['limpeza_seguranca'] + financial_data['seguros'] + 
                financial_data['manutencao_equipamentos'] + financial_data['marketing_publicidade']
            ),
            'Marketing': financial_data['marketing_publicidade'],
            'Combustível': financial_data['combustivel'],
            'Telefone/Internet': financial_data['telefone_internet'],
            'Energia/Água': financial_data['energia_agua'],
            'Seguros': financial_data['seguros'],
            'Outras Despesas': financial_data['outras_despesas']
        }
        
        # Rateio por óculos
        rateio_por_oculos = {}
        total_fixo_mensal = 0
        
        for item, valor in custos_fixos.items():
            valor_por_oculos = valor / meta_oculos
            rateio_por_oculos[item] = {
                'mensal': valor,
                'por_oculos': valor_por_oculos
            }
            total_fixo_mensal += valor
        
        total_fixo_por_oculos = total_fixo_mensal / meta_oculos
        
        return {
            'custos_individuais': rateio_por_oculos,
            'total_mensal': total_fixo_mensal,
            'total_por_oculos': total_fixo_por_oculos,
            'meta_oculos': meta_oculos
        }
    
    def calculate_direct_costs(self, lente_tipo: str, armacao_tipo: str, 
                             acessorios_custom: Dict = None) -> Dict:
        """Calcula custos diretos (materiais físicos)"""
        
        # Buscar custo da lente
        custo_lente = 45.00  # default
        for tipo, categorias in self.lenses_costs.items():
            if tipo in lente_tipo:
                for categoria, custo in categorias.items():
                    if categoria in armacao_tipo:
                        custo_lente = custo
                        break
        
        # Custo da armação
        custo_armacao = self.frames_costs.get(armacao_tipo, 25.00)
        
        # Custo dos acessórios
        if acessorios_custom:
            custo_acessorios = sum(acessorios_custom.values())
        else:
            custo_acessorios = 4.80  # padrão
        
        total_direto = custo_lente + custo_armacao + custo_acessorios
        
        return {
            'lente': custo_lente,
            'armacao': custo_armacao,
            'acessorios': custo_acessorios,
            'total': total_direto,
            'breakdown': {
                'Lente': custo_lente,
                'Armação': custo_armacao,
                'Acessórios': custo_acessorios
            }
        }
    
    def calculate_financial_impact(self, preco_venda: float, modalidade: str) -> Dict:
        """Calcula impacto das taxas financeiras"""
        taxa = self.financial_fees.get(modalidade, 0.0)
        taxa_valor = preco_venda * (taxa / 100)
        valor_liquido = preco_venda - taxa_valor
        
        return {
            'preco_bruto': preco_venda,
            'taxa_percentual': taxa,
            'taxa_valor': taxa_valor,
            'valor_liquido': valor_liquido
        }
    
    def generate_complete_analysis_with_financial_data(self, financial_data: Dict, custom_margins: Dict = None) -> pd.DataFrame:
        """Gera análise completa de custos baseada nas Projeções Financeiras"""
        
        try:
            # Calcular rateio de custos fixos usando dados reais
            meta_oculos = financial_data.get('meta_oculos_mes', 1)
            if meta_oculos <= 0:
                meta_oculos = 1
            
            # Calcular rateio por óculos com TODOS os custos incluídos
            custos_fixos_totais = (
                financial_data.get('aluguel', 0) +
                financial_data.get('folha_clt', 0) +
                financial_data.get('servicos_terceirizados', 0) +
                financial_data.get('optometrista', 0) +
                financial_data.get('combustivel', 0) +  # COMBUSTÍVEL INCLUÍDO
                financial_data.get('telefone_internet', 0) +
                financial_data.get('energia_agua', 0) +
                financial_data.get('marketing_publicidade', 0) +
                financial_data.get('seguros', 0) +
                financial_data.get('iptu_licencas', 0) +
                financial_data.get('material_escritorio', 0) +
                financial_data.get('material_limpeza', 0) +
                financial_data.get('contabilidade', 0) +
                financial_data.get('limpeza_seguranca', 0) +
                financial_data.get('manutencao_equipamentos', 0) +
                financial_data.get('software_sistemas', 0) +
                financial_data.get('despesas_bancarias', 0) +
                financial_data.get('outras_despesas', 0)
            )
            
            rateio_por_oculos = custos_fixos_totais / meta_oculos
            
            # Lista de produtos para análise
            produtos = []
            
            # Óculos completos (lente + armação) - usar dados da base de produtos
            lentes = {
                'Monofocal Nacional': 45.00,
                'Monofocal Premium': 75.00,
                'Multifocal Nacional': 120.00,
                'Multifocal Premium': 180.00,
                'Progressiva Nacional': 200.00,
                'Progressiva Premium': 320.00,
                'Progressiva Grife': 480.00
            }
            
            armacoes = {
                'Nacional Básica': 35.00,
                'Nacional Premium': 65.00,
                'Premium Nacional': 95.00,
                'Premium Importada': 150.00,
                'Grife Nacional': 220.00,
                'Grife Importada': 350.00
            }
            
            for lente_tipo, lente_custo in lentes.items():
                for armacao_tipo, armacao_custo in armacoes.items():
                    # Aplicar margens personalizadas se fornecidas
                    if custom_margins:
                        if 'monofocal' in lente_tipo.lower():
                            margem_lente = custom_margins.get('monofocal', 1.8)
                        elif 'multifocal' in lente_tipo.lower():
                            margem_lente = custom_margins.get('multifocal', 2.2)
                        elif 'progressiva' in lente_tipo.lower():
                            margem_lente = custom_margins.get('progressiva', 2.8)
                        else:
                            margem_lente = 2.0
                        
                        if 'nacional' in armacao_tipo.lower():
                            margem_armacao = custom_margins.get('nacional', 1.5)
                        elif 'premium' in armacao_tipo.lower():
                            margem_armacao = custom_margins.get('premium', 2.0)
                        elif 'grife' in armacao_tipo.lower():
                            margem_armacao = custom_margins.get('grife', 3.5)
                        else:
                            margem_armacao = 2.0
                    else:
                        margem_lente = 2.0
                        margem_armacao = 2.0
                    
                    custo_direto = lente_custo + armacao_custo
                    custo_total = custo_direto + rateio_por_oculos
                    
                    # Preço com margem personalizada
                    preco_venda = custo_total * ((margem_lente + margem_armacao) / 2)
                    
                    # Buscar preço do sistema existente (comparação)
                    preco_sistema = self.get_existing_system_price(lente_tipo, armacao_tipo, financial_data)
                    
                    produtos.append({
                        'PRODUTO': f"{lente_tipo} + {armacao_tipo}",
                        'LENTE': lente_tipo,
                        'ARMAÇÃO': armacao_tipo,
                        'CUSTO LENTE': lente_custo,
                        'CUSTO ARMAÇÃO': armacao_custo,
                        'TOTAL DIRETO': custo_direto,
                        'RATEIO FIXO': rateio_por_oculos,
                        'CUSTO TOTAL': custo_total,
                        'PREÇO CALCULADO': preco_venda,
                        'PREÇO SISTEMA': preco_sistema,
                        'DIFERENÇA': preco_venda - preco_sistema if preco_sistema > 0 else 0,
                        'MARGEM %': ((preco_venda - custo_total) / preco_venda * 100) if preco_venda > 0 else 0,
                        'MARGEM R$': preco_venda - custo_total
                    })
            
            # Adicionar serviços
            for servico, custo in self.services_costs.items():
                custo_total = custo + (rateio_por_oculos * 0.3)  # Rateio menor para serviços
                preco_venda = custo_total * 2.5  # Margem padrão para serviços
                
                produtos.append({
                    'PRODUTO': f"Serviço: {servico}",
                    'LENTE': 'Serviço',
                    'ARMAÇÃO': 'N/A',
                    'CUSTO LENTE': 0,
                    'CUSTO ARMAÇÃO': custo,
                    'TOTAL DIRETO': custo,
                    'RATEIO FIXO': rateio_por_oculos * 0.3,
                    'CUSTO TOTAL': custo_total,
                    'PREÇO CALCULADO': preco_venda,
                    'PREÇO SISTEMA': 0,
                    'DIFERENÇA': 0,
                    'MARGEM %': ((preco_venda - custo_total) / preco_venda * 100) if preco_venda > 0 else 0,
                    'MARGEM R$': preco_venda - custo_total
                })
            
            # Adicionar acessórios
            for acessorio, custo in self.accessories_costs.items():
                margem_acessorio = custom_margins.get('acessorios', {}).get('kit_limpeza', 3.0) if custom_margins else 3.0
                custo_total = custo + (rateio_por_oculos * 0.1)  # Rateio muito menor para acessórios
                preco_venda = custo_total * margem_acessorio
                
                produtos.append({
                    'PRODUTO': f"Acessório: {acessorio}",
                    'LENTE': 'Acessório',
                    'ARMAÇÃO': 'N/A',
                    'CUSTO LENTE': 0,
                    'CUSTO ARMAÇÃO': custo,
                    'TOTAL DIRETO': custo,
                    'RATEIO FIXO': rateio_por_oculos * 0.1,
                    'CUSTO TOTAL': custo_total,
                    'PREÇO CALCULADO': preco_venda,
                    'PREÇO SISTEMA': 0,
                    'DIFERENÇA': 0,
                    'MARGEM %': ((preco_venda - custo_total) / preco_venda * 100) if preco_venda > 0 else 0,
                    'MARGEM R$': preco_venda - custo_total
                })
            
            df = pd.DataFrame(produtos)
            return df
            
        except Exception as e:
            st.error(f"Erro ao gerar análise: {str(e)}")
            return pd.DataFrame()
    
    def get_existing_system_price(self, lente_tipo: str, armacao_tipo: str, financial_data: Dict) -> float:
        """Busca preço do sistema existente para comparação"""
        # Mapear tipos para campos do sistema
        if 'monofocal' in lente_tipo.lower() and 'nacional' in armacao_tipo.lower():
            return financial_data.get('preco_monofocal_nacional', 0)
        elif 'monofocal' in lente_tipo.lower() and 'premium' in armacao_tipo.lower():
            return financial_data.get('preco_monofocal_premium', 0)
        elif 'multifocal' in lente_tipo.lower() and 'nacional' in armacao_tipo.lower():
            return financial_data.get('preco_multifocal_nacional', 0)
        elif 'multifocal' in lente_tipo.lower() and 'premium' in armacao_tipo.lower():
            return financial_data.get('preco_multifocal_premium', 0)
        elif 'progressiva' in lente_tipo.lower() and 'nacional' in armacao_tipo.lower():
            return financial_data.get('preco_progressiva_nacional', 0)
        elif 'progressiva' in lente_tipo.lower() and 'premium' in armacao_tipo.lower():
            return financial_data.get('preco_progressiva_premium', 0)
        
        return 0
    
    def generate_complete_analysis(self, combinations: List[Tuple] = None) -> pd.DataFrame:
        
        # Combinações padrão se não especificadas
        if combinations is None:
            combinations = [
                ('Monofocal Nacional', 'Nacional Básica'),
                ('Monofocal Premium', 'Nacional Premium'),
                ('Multifocal Nacional', 'Nacional Básica'),
                ('Multifocal Premium', 'Nacional Premium'),
                ('Progressiva Nacional', 'Nacional Básica'),
                ('Progressiva Premium', 'Nacional Premium'),
                ('Progressiva Grife', 'Grife Nacional')
            ]
        
        # Lista para armazenar resultados
        results = []
        
        for lente_tipo, armacao_tipo in combinations:
            # Custos diretos
            custos_diretos = self.calculate_direct_costs(lente_tipo, armacao_tipo)
            
            # Custo total
            custo_total = custos_diretos['total'] + rateio_data['total_por_oculos']
            
            # Preço de mercado
            market_data = self.get_market_comparison(lente_tipo, armacao_tipo)
            preco_mercado = market_data['avg']
            
            # Análise financeira para diferentes modalidades
            modalidades_analysis = {}
            for modalidade in self.financial_fees.keys():
                impact = self.calculate_financial_impact(preco_mercado, modalidade)
                margem_liquida = impact['valor_liquido'] - custo_total
                percentual_margem = (margem_liquida / impact['valor_liquido'] * 100) if impact['valor_liquido'] > 0 else 0
                
                modalidades_analysis[modalidade] = {
                    'valor_liquido': impact['valor_liquido'],
                    'margem_liquida': margem_liquida,
                    'percentual_margem': percentual_margem
                }
            
            # Compilar resultado
            result = {
                'PRODUTO': f"{lente_tipo} + {armacao_tipo}",
                'LENTE': lente_tipo,
                'ARMAÇÃO': armacao_tipo,
                
                # Custos diretos
                'CUSTO LENTE': f"R$ {custos_diretos['lente']:.2f}".replace('.', ','),
                'CUSTO ARMAÇÃO': f"R$ {custos_diretos['armacao']:.2f}".replace('.', ','),
                'CUSTO ACESSÓRIOS': f"R$ {custos_diretos['acessorios']:.2f}".replace('.', ','),
                'TOTAL DIRETO': f"R$ {custos_diretos['total']:.2f}".replace('.', ','),
                
                # Custos fixos rateados
                'RATEIO FIXO': f"R$ {rateio_data['total_por_oculos']:.2f}".replace('.', ','),
                
                # Custo total
                'CUSTO TOTAL': f"R$ {custo_total:.2f}".replace('.', ','),
                
                # Preços de mercado
                'MERCADO MÍNIMO': f"R$ {market_data['min']:.2f}".replace('.', ','),
                'MERCADO MÉDIO': f"R$ {market_data['avg']:.2f}".replace('.', ','),
                'MERCADO MÁXIMO': f"R$ {market_data['max']:.2f}".replace('.', ','),
                
                # Análises por modalidade
                'À VISTA MARGEM': f"{modalidades_analysis['À Vista (0 dias)']['percentual_margem']:.1f}%",
                'ANTECIPAÇÃO MARGEM': f"{modalidades_analysis['Antecipação (até 30 dias)']['percentual_margem']:.1f}%",
                'PARCELADO MARGEM': f"{modalidades_analysis['Parcelado (30-60 dias)']['percentual_margem']:.1f}%",
                
                # Dados numéricos para cálculos
                '_custo_total_num': custo_total,
                '_preco_mercado_num': preco_mercado,
                '_custos_diretos_num': custos_diretos['total'],
                '_rateio_fixo_num': rateio_data['total_por_oculos'],
                '_modalidades_data': modalidades_analysis
            }
            
            results.append(result)
        
        return pd.DataFrame(results)
    
    def get_market_comparison(self, lente_tipo: str, armacao_tipo: str) -> Dict:
        """Obtém comparação com preços de mercado"""
        for key, values in self.market_prices.items():
            if key[0] == lente_tipo and key[1] == armacao_tipo:
                return values
        return {'min': 0, 'avg': 0, 'max': 0}
    
    def format_currency(self, value: float) -> str:
        """Formata valor como moeda brasileira"""
        return f"R$ {value:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    
    def generate_complete_price_table(self, financial_data: Dict) -> pd.DataFrame:
        """Gera tabela completa de preços similar à foto do usuário"""
        
        # Calcular rateio de custos fixos
        rateio_data = self.calculate_fixed_cost_allocation(financial_data)
        custo_fixo_por_oculos = rateio_data['total_por_oculos']
        
        # Lista para armazenar todos os produtos
        complete_products = []
        
        # 1. ÓCULOS COMPLETOS (Lente + Armação + Tratamentos)
        for lente_tipo, lente_categorias in self.lenses_costs.items():
            for lente_categoria, custo_lente in lente_categorias.items():
                for armacao_categoria, custo_armacao in self.frames_costs.items():
                    
                    # Produto básico (sem tratamentos)
                    custo_direto_basico = custo_lente + custo_armacao + 4.80  # acessórios padrão
                    custo_total_basico = custo_direto_basico + custo_fixo_por_oculos
                    
                    # Margem sugerida baseada na categoria
                    if 'Grife' in lente_categoria or 'Grife' in armacao_categoria:
                        margem_sugerida = 180  # 180% para grife
                    elif 'Premium' in lente_categoria or 'Premium' in armacao_categoria:
                        margem_sugerida = 150  # 150% para premium
                    elif 'Importada' in lente_categoria or 'Importada' in armacao_categoria:
                        margem_sugerida = 120  # 120% para importada
                    else:
                        margem_sugerida = 100  # 100% para nacional básica
                    
                    preco_venda_basico = custo_total_basico * (1 + margem_sugerida / 100)
                    
                    complete_products.append({
                        'CATEGORIA': 'ÓCULOS COMPLETOS',
                        'PRODUTO': f"{lente_tipo} {lente_categoria} + {armacao_categoria}",
                        'ESPECIFICAÇÃO': f"Lente {lente_tipo} + Armação {armacao_categoria}",
                        'CUSTO DIRETO': self.format_currency(custo_direto_basico),
                        'RATEIO FIXO': self.format_currency(custo_fixo_por_oculos),
                        'CUSTO TOTAL': self.format_currency(custo_total_basico),
                        'MARGEM %': f"{margem_sugerida}%",
                        'PREÇO SUGERIDO': self.format_currency(preco_venda_basico),
                        '_custo_total_num': custo_total_basico,
                        '_margem_num': margem_sugerida,
                        '_preco_num': preco_venda_basico
                    })
                    
                    # Versões com tratamentos populares
                    tratamentos_populares = [
                        ['Anti-reflexo Básico'],
                        ['Anti-reflexo Premium', 'Antirisco'],
                        ['Transitions (Fotossensível)'],
                        ['Blue Control (Luz Azul)', 'Anti-reflexo Básico'],
                        ['Polarizada'] if lente_tipo == 'Monofocal' else ['Anti-reflexo Premium']
                    ]
                    
                    for tratamentos in tratamentos_populares:
                        custo_tratamentos = sum(self.treatments_costs.get(t, 0) for t in tratamentos)
                        custo_direto_tratado = custo_direto_basico + custo_tratamentos
                        custo_total_tratado = custo_direto_tratado + custo_fixo_por_oculos
                        preco_venda_tratado = custo_total_tratado * (1 + margem_sugerida / 100)
                        
                        tratamentos_str = " + ".join(tratamentos)
                        
                        complete_products.append({
                            'CATEGORIA': 'ÓCULOS COM TRATAMENTOS',
                            'PRODUTO': f"{lente_tipo} {lente_categoria} + {armacao_categoria}",
                            'ESPECIFICAÇÃO': f"Com {tratamentos_str}",
                            'CUSTO DIRETO': self.format_currency(custo_direto_tratado),
                            'RATEIO FIXO': self.format_currency(custo_fixo_por_oculos),
                            'CUSTO TOTAL': self.format_currency(custo_total_tratado),
                            'MARGEM %': f"{margem_sugerida}%",
                            'PREÇO SUGERIDO': self.format_currency(preco_venda_tratado),
                            '_custo_total_num': custo_total_tratado,
                            '_margem_num': margem_sugerida,
                            '_preco_num': preco_venda_tratado
                        })
        
        # 2. SERVIÇOS
        for servico, custo_servico in self.services_costs.items():
            custo_total_servico = custo_servico + (custo_fixo_por_oculos * 0.3)  # Rateio reduzido para serviços
            margem_servico = 80  # 80% de margem para serviços
            preco_servico = custo_total_servico * (1 + margem_servico / 100)
            
            complete_products.append({
                'CATEGORIA': 'SERVIÇOS',
                'PRODUTO': servico,
                'ESPECIFICAÇÃO': 'Serviço avulso',
                'CUSTO DIRETO': self.format_currency(custo_servico),
                'RATEIO FIXO': self.format_currency(custo_fixo_por_oculos * 0.3),
                'CUSTO TOTAL': self.format_currency(custo_total_servico),
                'MARGEM %': f"{margem_servico}%",
                'PREÇO SUGERIDO': self.format_currency(preco_servico),
                '_custo_total_num': custo_total_servico,
                '_margem_num': margem_servico,
                '_preco_num': preco_servico
            })
        
        # 3. LENTES DE CONTATO
        for lc_tipo, custo_lc in self.contact_lenses_costs.items():
            custo_total_lc = custo_lc + (custo_fixo_por_oculos * 0.2)  # Rateio menor para LC
            margem_lc = 120  # 120% de margem para lentes de contato
            preco_lc = custo_total_lc * (1 + margem_lc / 100)
            
            complete_products.append({
                'CATEGORIA': 'LENTES DE CONTATO',
                'PRODUTO': f"Lente de Contato {lc_tipo}",
                'ESPECIFICAÇÃO': 'Par de lentes',
                'CUSTO DIRETO': self.format_currency(custo_lc),
                'RATEIO FIXO': self.format_currency(custo_fixo_por_oculos * 0.2),
                'CUSTO TOTAL': self.format_currency(custo_total_lc),
                'MARGEM %': f"{margem_lc}%",
                'PREÇO SUGERIDO': self.format_currency(preco_lc),
                '_custo_total_num': custo_total_lc,
                '_margem_num': margem_lc,
                '_preco_num': preco_lc
            })
        
        # 4. ACESSÓRIOS
        for acessorio, custo_acessorio in self.accessories_costs.items():
            custo_total_acessorio = custo_acessorio + (custo_fixo_por_oculos * 0.1)  # Rateio mínimo
            margem_acessorio = 200  # 200% de margem para acessórios
            preco_acessorio = custo_total_acessorio * (1 + margem_acessorio / 100)
            
            complete_products.append({
                'CATEGORIA': 'ACESSÓRIOS',
                'PRODUTO': acessorio,
                'ESPECIFICAÇÃO': 'Acessório avulso',
                'CUSTO DIRETO': self.format_currency(custo_acessorio),
                'RATEIO FIXO': self.format_currency(custo_fixo_por_oculos * 0.1),
                'CUSTO TOTAL': self.format_currency(custo_total_acessorio),
                'MARGEM %': f"{margem_acessorio}%",
                'PREÇO SUGERIDO': self.format_currency(preco_acessorio),
                '_custo_total_num': custo_total_acessorio,
                '_margem_num': margem_acessorio,
                '_preco_num': preco_acessorio
            })
        
        return pd.DataFrame(complete_products)


def show_integrated_cost_analyzer():
    """Interface principal do analisador integrado de custos"""
    
    st.title("🔬 Sistema Integrado de Análise de Custos")
    st.markdown("**Fonte única de verdade baseada nas Projeções Financeiras**")
    
    # Inicializar analisador
    analyzer = IntegratedCostAnalyzer()
    
    # Extrair dados das Projeções Financeiras
    financial_data = analyzer.extract_financial_data()
    
    # Verificar se existem dados reais
    has_real_data = financial_data['meta_oculos_mes'] > 0
    
    if not has_real_data:
        st.warning("⚠️ **Dados das Projeções Financeiras não encontrados!**")
        st.info("👉 Complete a **Etapa 10 - Projeções Financeiras** primeiro para uma análise precisa.")
        st.markdown("---")
    
    # Mostrar resumo dos dados extraídos
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Meta de Óculos/Mês", 
            f"{financial_data['meta_oculos_mes']} unidades",
            help="Extraído das Projeções Financeiras"
        )
    
    with col2:
        st.metric(
            "Ticket Médio", 
            analyzer.format_currency(financial_data['ticket_medio']),
            help="Extraído das Projeções Financeiras"
        )
    
    with col3:
        st.metric(
            "Faturamento Mensal", 
            analyzer.format_currency(financial_data['faturamento_mensal']),
            help="Calculado automaticamente"
        )
    
    # Calcular rateio de custos fixos
    rateio_data = analyzer.calculate_fixed_cost_allocation(financial_data)
    
    # Seção 1: Estrutura de Rateio de Custos Fixos
    st.markdown("## 🏗️ Estrutura de Rateio de Custos Fixos")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"**Base de Cálculo:** {rateio_data.get('meta_oculos_mes', 0)} óculos/mês")
        
        # Tabela de rateio
        if 'custos_individuais' in rateio_data and rateio_data['custos_individuais']:
            rateio_df = []
            meta_oculos = rateio_data.get('meta_oculos_mes', 1)
            
            for item, dados in rateio_data['custos_individuais'].items():
                if isinstance(dados, dict):
                    rateio_df.append({
                        'Item de Custo': item,
                        'Valor Mensal': analyzer.format_currency(dados.get('mensal', 0)),
                        'Por Óculos': analyzer.format_currency(dados.get('por_oculos', 0)),
                        'Fórmula': f"R$ {dados.get('mensal', 0):.2f} ÷ {meta_oculos} = R$ {dados.get('por_oculos', 0):.2f}".replace('.', ',')
                    })
            
            if rateio_df:
                st.dataframe(pd.DataFrame(rateio_df), use_container_width=True)
            else:
                st.info("Configure as Projeções Financeiras (Etapa 10) para ver o rateio detalhado")
        else:
            st.info("Configure as Projeções Financeiras (Etapa 10) para ver o rateio detalhado")
    
    with col2:
        st.metric(
            "Custo Fixo Total/Mês",
            analyzer.format_currency(rateio_data['total_mensal'])
        )
        st.metric(
            "Custo Fixo/Óculos",
            analyzer.format_currency(rateio_data.get('total_por_oculos', 0))
        )
    
    # Seção 2: Editor de Margens
    st.markdown("## ✏️ Editor de Margens")
    
    # Controles de margem editáveis
    col_margin1, col_margin2, col_margin3 = st.columns(3)
    
    with col_margin1:
        st.markdown("**Margens por Tipo de Lente**")
        margem_monofocal = st.slider("Monofocal (%)", 50, 900, 180, 10, key="margem_monofocal")
        margem_multifocal = st.slider("Multifocal (%)", 50, 900, 220, 10, key="margem_multifocal")
        margem_progressiva = st.slider("Progressiva (%)", 50, 900, 280, 10, key="margem_progressiva")
    
    with col_margin2:
        st.markdown("**Margens por Tipo de Armação**")
        margem_nacional = st.slider("Nacional (%)", 50, 900, 150, 10, key="margem_nacional")
        margem_premium = st.slider("Premium (%)", 50, 900, 200, 10, key="margem_premium")
        margem_grife = st.slider("Grife (%)", 50, 900, 350, 10, key="margem_grife")
    
    with col_margin3:
        st.markdown("**Margens por Acessórios**")
        margem_limpeza = st.slider("Kit Limpeza (%)", 50, 900, 300, 10, key="margem_limpeza")
        margem_estojo = st.slider("Estojo (%)", 50, 900, 250, 10, key="margem_estojo")
        margem_cordinha = st.slider("Cordinha (%)", 50, 900, 400, 10, key="margem_cordinha")
    
    # Margens personalizadas
    margens_personalizadas = {
        'monofocal': margem_monofocal / 100,
        'multifocal': margem_multifocal / 100,
        'progressiva': margem_progressiva / 100,
        'nacional': margem_nacional / 100,
        'premium': margem_premium / 100,
        'grife': margem_grife / 100,
        'acessorios': {
            'kit_limpeza': margem_limpeza / 100,
            'estojo': margem_estojo / 100,
            'cordinha': margem_cordinha / 100
        }
    }
    
    # Seção 3: Análise Completa baseada nas Projeções Financeiras
    st.markdown("## 📊 Análise Completa por Produto")
    
    # Verificar dados das Projeções Financeiras
    financial_data = analyzer.extract_financial_data()
    
    if not financial_data or financial_data.get('meta_oculos_mes', 0) <= 0:
        st.warning("⚠️ **Dados das Projeções Financeiras necessários**")
        st.info("Complete a **Etapa 10** para usar dados reais incluindo combustível e todos os custos")
        return
    
    # Mostrar breakdown dos custos incluindo combustível
    with st.expander("📊 Custos Extraídos das Projeções Financeiras"):
        custos_fixos_total = (
            financial_data.get('aluguel', 0) + financial_data.get('folha_clt', 0) +
            financial_data.get('combustivel', 0) + financial_data.get('energia_agua', 0) +
            financial_data.get('marketing_publicidade', 0) + financial_data.get('telefone_internet', 0) +
            financial_data.get('servicos_terceirizados', 0) + financial_data.get('outras_despesas', 0)
        )
        
        st.write(f"**Combustível:** {analyzer.format_currency(financial_data.get('combustivel', 0))}")
        st.write(f"**Total Custos Fixos:** {analyzer.format_currency(custos_fixos_total)}")
        st.write(f"**Rateio por Óculos:** {analyzer.format_currency(custos_fixos_total / financial_data.get('meta_oculos_mes', 1))}")
    
    if st.button("🔄 Gerar Análise com Dados Reais", type="primary"):
        with st.spinner("Gerando análise com dados das Projeções Financeiras..."):
            df_analysis = analyzer.generate_complete_analysis_with_financial_data(financial_data, margens_personalizadas)
            
            if df_analysis is not None and not df_analysis.empty:
                st.success(f"Análise gerada com {len(df_analysis)} produtos - Margens aplicadas")
                
                # Tabs para visualizações
                tab1, tab2, tab3 = st.tabs(["📋 Tabela Completa", "💰 Comparação Preços", "📊 Análise"])
                
                with tab1:
                    st.markdown("### Tabela Completa de Produtos")
                    
                    # Mostrar principais produtos com melhor formatação
                    df_display = df_analysis.copy()
                    
                    # Arredondar preços para valores inteiros
                    df_display['PREÇO CALCULADO'] = df_display['PREÇO CALCULADO'].round(0)
                    df_display['MARGEM %'] = df_display['MARGEM %'].round(1)
                    
                    # Exibir tabela formatada
                    colunas_principais = ['PRODUTO', 'CUSTO TOTAL', 'PREÇO CALCULADO', 'MARGEM %', 'MARGEM R$']
                    st.dataframe(
                        df_display[colunas_principais].head(15),
                        use_container_width=True,
                        hide_index=True
                    )
                
                with tab2:
                    st.markdown("### Comparação: Calculado vs Sistema Atual")
                    
                    # Filtrar produtos com preços do sistema
                    df_comparacao = df_analysis[df_analysis['PREÇO SISTEMA'] > 0].copy()
                    
                    if len(df_comparacao) > 0:
                        df_comparacao['PREÇO CALCULADO'] = df_comparacao['PREÇO CALCULADO'].round(0)
                        df_comparacao['PREÇO SISTEMA'] = df_comparacao['PREÇO SISTEMA'].round(0)
                        df_comparacao['DIFERENÇA'] = df_comparacao['DIFERENÇA'].round(0)
                        
                        cols_comparacao = ['PRODUTO', 'PREÇO CALCULADO', 'PREÇO SISTEMA', 'DIFERENÇA']
                        st.dataframe(
                            df_comparacao[cols_comparacao],
                            use_container_width=True,
                            hide_index=True
                        )
                        
                        # Estatísticas da comparação
                        media_diferenca = df_comparacao['DIFERENÇA'].mean()
                        if media_diferenca > 0:
                            st.info(f"Preços calculados são em média R$ {media_diferenca:.0f} maiores")
                        else:
                            st.warning(f"Preços calculados são em média R$ {abs(media_diferenca):.0f} menores")
                    else:
                        st.info("Configure preços na Etapa 5 para comparação")
                
                with tab3:
                    st.markdown("### Análise de Rentabilidade")
                    
                    # Top produtos mais rentáveis
                    df_oculos = df_analysis[df_analysis['LENTE'] != 'Serviço'].copy()
                    if len(df_oculos) > 0:
                        top_rentaveis = df_oculos.nlargest(8, 'MARGEM R$')
                        
                        st.markdown("**Produtos Mais Rentáveis:**")
                        for _, produto in top_rentaveis.iterrows():
                            st.write(f"• {produto['PRODUTO']}: R$ {produto['MARGEM R$']:.0f} ({produto['MARGEM %']:.1f}%)")
                        
                        # Margem média por categoria
                        st.markdown("**Margem Média por Categoria:**")
                        margem_categoria = df_oculos.groupby('LENTE')['MARGEM %'].mean().sort_values(ascending=False)
                        
                        for categoria, margem in margem_categoria.head(6).items():
                            st.write(f"• {categoria}: {margem:.1f}%")
            else:
                st.error("Erro ao gerar análise. Verifique os dados das Projeções Financeiras.")
    
    # Seção 4: Integração com Estrutura de Custos da Etapa 5
    st.markdown("## 📋 Integração com Estrutura de Custos (Etapa 5)")
    
    # Verificar se temos dados da Etapa 5
    if 'business_data' in st.session_state:
        business_data = st.session_state['business_data']
        
        # Extrair dados de serviços da Etapa 5
        servicos_etapa5 = business_data.get('servicos', [])
        
        if servicos_etapa5:
            st.success(f"✅ Encontrados {len(servicos_etapa5)} serviços configurados na Etapa 5")
            
            # Mostrar estrutura de custos da Etapa 5
            with st.expander("📊 Custos de Serviços da Etapa 5"):
                for servico in servicos_etapa5:
                    nome = servico.get('nome', 'Serviço sem nome')
                    custo = servico.get('custo', 0)
                    preco = servico.get('preco', 0)
                    margem = ((preco - custo) / custo * 100) if custo > 0 else 0
                    
                    st.write(f"**{nome}:**")
                    st.write(f"  • Custo: R$ {custo:.2f}")
                    st.write(f"  • Preço: R$ {preco:.2f}")
                    st.write(f"  • Margem: {margem:.1f}%")
                    st.write("---")
        else:
            st.info("💡 Configure serviços na Etapa 5 para integração completa")
    else:
        st.warning("⚠️ Dados da Etapa 5 não encontrados")
        produto_selecionado = st.selectbox(
            "Selecione um produto para análise detalhada:",
            df_filtered['PRODUTO'].tolist(),
            key="produto_detalhado"
        )
        
        if produto_selecionado:
            produto_data = df_filtered[df_filtered['PRODUTO'] == produto_selecionado].iloc[0]
            
            # Layout da análise detalhada
            st.markdown(f"### 📋 Estrutura Completa: {produto_selecionado}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 1️⃣ Custos Diretos (Materiais Físicos)")
                st.markdown(f"• **Lente:** {produto_data['CUSTO LENTE']}")
                st.markdown(f"• **Armação:** {produto_data['CUSTO ARMAÇÃO']}")
                st.markdown(f"• **Acessórios:** {produto_data['CUSTO ACESSÓRIOS']}")
                st.markdown(f"• **Total Direto:** {produto_data['TOTAL DIRETO']}")
                
                st.markdown("#### 2️⃣ Custos Fixos Rateados")
                st.markdown(f"• **Rateio por Óculos:** {produto_data['RATEIO FIXO']}")
                st.markdown(f"• **Base:** {rateio_data['meta_oculos']} óculos/mês")
                
                st.markdown("#### 3️⃣ Custo Total Real")
                st.markdown(f"• **Custo Final:** {produto_data['CUSTO TOTAL']}")
            
            with col2:
                st.markdown("#### 4️⃣ Análise de Mercado")
                st.markdown(f"• **Preço Mínimo:** {produto_data['MERCADO MÍNIMO']}")
                st.markdown(f"• **Preço Médio:** {produto_data['MERCADO MÉDIO']}")
                st.markdown(f"• **Preço Máximo:** {produto_data['MERCADO MÁXIMO']}")
                
                st.markdown("#### 5️⃣ Margens por Modalidade")
                st.markdown(f"• **À Vista:** {produto_data['À VISTA MARGEM']}")
                st.markdown(f"• **Antecipação:** {produto_data['ANTECIPAÇÃO MARGEM']}")
                st.markdown(f"• **Parcelado:** {produto_data['PARCELADO MARGEM']}")
            
            # Simulador de preços
            st.markdown("#### 🧮 Simulador de Preços")
            
            preco_teste = st.number_input(
                "Teste um preço de venda:",
                min_value=0.0,
                value=float(produto_data['_preco_mercado_num']),
                step=10.0,
                format="%.2f",
                key="preco_simulacao"
            )
            
            if preco_teste > 0:
                col1, col2, col3 = st.columns(3)
                
                # Análise para cada modalidade
                modalidades = ['À Vista (0 dias)', 'Antecipação (até 30 dias)', 'Parcelado (30-60 dias)']
                
                for i, modalidade in enumerate(modalidades):
                    with [col1, col2, col3][i]:
                        impact = analyzer.calculate_financial_impact(preco_teste, modalidade)
                        margem_liquida = impact['valor_liquido'] - produto_data['_custo_total_num']
                        percentual = (margem_liquida / impact['valor_liquido'] * 100) if impact['valor_liquido'] > 0 else 0
                        
                        st.metric(
                            modalidade.replace(' (', '\n('),
                            f"{percentual:.1f}%",
                            f"R$ {margem_liquida:.2f}".replace('.', ','),
                            help=f"Valor líquido: R$ {impact['valor_liquido']:.2f}"
                        )
    
    # Seção 4: Insights e Recomendações
    st.markdown("## 💡 Insights e Recomendações")
    
    if not df_filtered.empty:
        # Calcular estatísticas
        margem_media_avista = df_filtered['À VISTA MARGEM'].str.replace('%', '').astype(float).mean()
        margem_media_parcelado = df_filtered['PARCELADO MARGEM'].str.replace('%', '').astype(float).mean()
        
        produtos_lucrativos = len(df_filtered[df_filtered['À VISTA MARGEM'].str.replace('%', '').astype(float) > 15])
        total_produtos = len(df_filtered)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Margem Média À Vista",
                f"{margem_media_avista:.1f}%",
                help="Margem média dos produtos selecionados"
            )
        
        with col2:
            st.metric(
                "Margem Média Parcelado",
                f"{margem_media_parcelado:.1f}%",
                help="Considerando taxas financeiras"
            )
        
        with col3:
            st.metric(
                "Produtos Lucrativos",
                f"{produtos_lucrativos}/{total_produtos}",
                help="Com margem > 15% à vista"
            )
        
        # Recomendações automáticas
        st.markdown("### 🎯 Recomendações Automáticas")
        
        if margem_media_avista < 10:
            st.error("⚠️ **Margem baixa detectada!** Considere aumentar preços ou reduzir custos fixos.")
        elif margem_media_avista < 20:
            st.warning("⚡ **Margem moderada.** Há espaço para otimização de preços.")
        else:
            st.success("✅ **Margens saudáveis!** Continue monitorando a competitividade.")
        
        if margem_media_avista - margem_media_parcelado > 5:
            st.info("💳 **Impacto significativo das taxas financeiras.** Considere incentivar pagamentos à vista.")
        
        # Produtos com melhor e pior performance
        melhor_produto = df_filtered.loc[df_filtered['À VISTA MARGEM'].str.replace('%', '').astype(float).idxmax()]
        pior_produto = df_filtered.loc[df_filtered['À VISTA MARGEM'].str.replace('%', '').astype(float).idxmin()]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.success(f"🏆 **Melhor Performance:** {melhor_produto['PRODUTO']}")
            st.write(f"Margem: {melhor_produto['À VISTA MARGEM']}")
        
        with col2:
            st.error(f"⚠️ **Menor Performance:** {pior_produto['PRODUTO']}")
            st.write(f"Margem: {pior_produto['À VISTA MARGEM']}")
    
    # Seção 5: Tabela Completa de Preços
    st.markdown("## 📋 Tabela Completa de Preços - Todos os Produtos e Serviços")
    st.markdown("**Incluindo óculos completos, tratamentos, serviços, lentes de contato e acessórios**")
    
    # Gerar tabela completa
    df_complete = analyzer.generate_complete_price_table(financial_data)
    
    if not df_complete.empty:
        # Filtros para a tabela completa
        col1, col2, col3 = st.columns(3)
        
        with col1:
            categorias_disponiveis = df_complete['CATEGORIA'].unique().tolist()
            categorias_selecionadas = st.multiselect(
                "Filtrar por Categoria:",
                categorias_disponiveis,
                default=categorias_disponiveis,
                key="filter_categorias_complete"
            )
        
        with col2:
            min_preco = st.number_input(
                "Preço Mínimo (R$):",
                min_value=0.0,
                value=0.0,
                step=50.0,
                key="min_preco_filter"
            )
        
        with col3:
            max_preco = st.number_input(
                "Preço Máximo (R$):",
                min_value=0.0,
                value=5000.0,
                step=50.0,
                key="max_preco_filter"
            )
        
        # Aplicar filtros
        df_filtered_complete = df_complete[df_complete['CATEGORIA'].isin(categorias_selecionadas)]
        
        if min_preco > 0 or max_preco < 5000:
            df_filtered_complete = df_filtered_complete[
                (df_filtered_complete['_preco_num'] >= min_preco) & 
                (df_filtered_complete['_preco_num'] <= max_preco)
            ]
        
        # Controles de ordenação
        col1, col2 = st.columns(2)
        
        with col1:
            ordenar_por = st.selectbox(
                "Ordenar por:",
                ['CATEGORIA', 'PREÇO SUGERIDO', 'MARGEM %', 'CUSTO TOTAL'],
                key="ordenar_tabela_complete"
            )
        
        with col2:
            ordem_crescente = st.checkbox(
                "Ordem Crescente",
                value=True,
                key="ordem_crescente_complete"
            )
        
        # Aplicar ordenação
        if ordenar_por in ['PREÇO SUGERIDO', 'CUSTO TOTAL']:
            coluna_ordenacao = f"_{ordenar_por.lower().replace(' ', '_').replace('ç', 'c')}_num"
            if coluna_ordenacao == '_preço_sugerido_num':
                coluna_ordenacao = '_preco_num'
            elif coluna_ordenacao == '_custo_total_num':
                coluna_ordenacao = '_custo_total_num'
        elif ordenar_por == 'MARGEM %':
            coluna_ordenacao = '_margem_num'
        else:
            coluna_ordenacao = ordenar_por
        
        if coluna_ordenacao in df_filtered_complete.columns:
            df_filtered_complete = df_filtered_complete.sort_values(
                by=coluna_ordenacao, 
                ascending=ordem_crescente
            )
        
        # Mostrar métricas da tabela completa
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Total de Produtos",
                len(df_filtered_complete)
            )
        
        with col2:
            if len(df_filtered_complete) > 0:
                preco_medio = df_filtered_complete['_preco_num'].mean()
                st.metric(
                    "Preço Médio",
                    analyzer.format_currency(preco_medio)
                )
        
        with col3:
            if len(df_filtered_complete) > 0:
                margem_media_complete = df_filtered_complete['_margem_num'].mean()
                st.metric(
                    "Margem Média",
                    f"{margem_media_complete:.0f}%"
                )
        
        with col4:
            categorias_ativas = len(df_filtered_complete['CATEGORIA'].unique())
            st.metric(
                "Categorias Ativas",
                categorias_ativas
            )
        
        # Exibir tabela completa
        colunas_exibir = [
            'CATEGORIA', 'PRODUTO', 'ESPECIFICAÇÃO',
            'CUSTO TOTAL', 'MARGEM %', 'PREÇO SUGERIDO'
        ]
        
        st.dataframe(
            df_filtered_complete[colunas_exibir],
            use_container_width=True,
            height=600
        )
        
        # Opção de download da tabela completa
        st.markdown("### 📥 Download da Tabela")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📋 Copiar Tabela Completa", key="copy_complete_table"):
                # Preparar dados para cópia
                tabela_texto = df_filtered_complete[colunas_exibir].to_string(index=False)
                st.text_area(
                    "Tabela para Cópia:",
                    tabela_texto,
                    height=200,
                    key="tabela_copy_area"
                )
        
        with col2:
            # Converter para CSV para download
            csv_data = df_filtered_complete[colunas_exibir].to_csv(index=False, sep=';')
            st.download_button(
                label="💾 Download CSV",
                data=csv_data,
                file_name=f"tabela_precos_{financial_data['nome_empresa'].replace(' ', '_')}.csv",
                mime="text/csv",
                key="download_complete_csv"
            )
        
        # Análise por categoria
        st.markdown("### 📊 Análise por Categoria")
        
        if len(df_filtered_complete) > 0:
            analise_categoria = df_filtered_complete.groupby('CATEGORIA').agg({
                '_preco_num': ['count', 'mean', 'min', 'max'],
                '_margem_num': 'mean'
            }).round(2)
            
            analise_categoria.columns = ['Quantidade', 'Preço Médio', 'Preço Mín', 'Preço Máx', 'Margem Média']
            
            # Formatar preços
            for col in ['Preço Médio', 'Preço Mín', 'Preço Máx']:
                analise_categoria[col] = analise_categoria[col].apply(analyzer.format_currency)
            
            analise_categoria['Margem Média'] = analise_categoria['Margem Média'].apply(lambda x: f"{x:.0f}%")
            
            st.dataframe(analise_categoria, use_container_width=True)
    
    # Footer com informações do sistema
    st.markdown("---")
    st.caption(f"📊 Análise baseada em {financial_data['nome_empresa']} - {financial_data['cidade']}/{financial_data['estado']}")
    st.caption("🔄 Dados atualizados automaticamente das Projeções Financeiras (Etapa 10)")