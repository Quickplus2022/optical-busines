"""
Sistema Integrado de Análise de Custos - VERSÃO CORRIGIDA
Integração completa com estrutura de custos das Projeções Financeiras
Inclui todos os custos: combustível, aluguel, folha CLT, etc.
"""

import streamlit as st
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple

class IntegratedCostAnalyzer:
    """Analisador integrado de custos com dados das Projeções Financeiras"""
    
    def __init__(self):
        self.load_product_database()
        self.load_market_prices()
    
    def load_product_database(self):
        """Base de produtos com custos reais"""
        self.lens_costs = {
            'Monofocal Nacional': 45.00,
            'Monofocal Premium': 75.00,
            'Multifocal Nacional': 120.00,
            'Multifocal Premium': 180.00,
            'Progressiva Nacional': 200.00,
            'Progressiva Premium': 320.00,
            'Progressiva Grife': 480.00
        }
        
        self.frame_costs = {
            'Nacional Básica': 35.00,
            'Nacional Premium': 65.00,
            'Premium Nacional': 95.00,
            'Premium Importada': 150.00,
            'Grife Nacional': 220.00,
            'Grife Importada': 350.00
        }
        
        self.service_costs = {
            'Exame de Vista': 25.00,
            'Ajuste de Óculos': 8.00,
            'Conserto Simples': 15.00,
            'Troca de Lente': 30.00,
            'Adaptação': 12.00
        }
    
    def load_market_prices(self):
        """Preços de mercado para comparação"""
        self.market_prices = {
            ('Monofocal Nacional', 'Nacional Básica'): 180,
            ('Monofocal Premium', 'Nacional Premium'): 280,
            ('Multifocal Nacional', 'Premium Nacional'): 420,
            ('Multifocal Premium', 'Premium Importada'): 650,
            ('Progressiva Nacional', 'Grife Nacional'): 850,
            ('Progressiva Premium', 'Grife Importada'): 1200,
            ('Progressiva Grife', 'Grife Importada'): 1800
        }
    
    def extract_financial_data(self) -> Dict:
        """Extrai dados das Projeções Financeiras (Etapa 10)"""
        if 'business_data' not in st.session_state:
            return {}
        
        business_data = st.session_state['business_data']
        
        # Dados básicos da Etapa 10
        oculos_meta = business_data.get('oculos_meta_mes', 30)
        ticket_medio = business_data.get('ticket_medio', 500)
        
        # Custos Fixos Principais (da estrutura da Etapa 10)
        aluguel = business_data.get('aluguel', 400)
        folha_clt = business_data.get('salarios_clt', 0)
        combustivel = business_data.get('combustivel', 0)
        energia_agua = business_data.get('energia_agua', 0)
        
        # Despesas Operacionais Detalhadas
        material_escritorio = business_data.get('material_escritorio', 200)
        telefone_internet = business_data.get('telefone_internet', 0)
        limpeza_seguranca = business_data.get('limpeza_seguranca', 0)
        manutencao_equipamentos = business_data.get('manutencao_equipamentos', 0)
        marketing_publicidade = business_data.get('marketing_publicidade', 0)
        contabilidade = business_data.get('contabilidade', 0)
        
        # Outros custos
        servicos_profissionais = business_data.get('custo_optometrista_mensal', 0)
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
    
    def calculate_fixed_cost_allocation(self, financial_data: Dict) -> Dict:
        """Calcula rateio de custos fixos por óculos vendido baseado na Etapa 10"""
        if financial_data.get('oculos_meta', 0) <= 0:
            return {'custo_fixo_por_oculos': 0, 'total_custos_fixos': 0}
        
        # Somar TODOS os custos fixos da estrutura da Etapa 10
        total_custos_fixos = (
            financial_data.get('aluguel', 0) +
            financial_data.get('folha_clt', 0) +
            financial_data.get('combustivel', 0) +  # Incluído conforme Etapa 10
            financial_data.get('energia_agua', 0) +
            financial_data.get('material_escritorio', 0) +
            financial_data.get('telefone_internet', 0) +
            financial_data.get('limpeza_seguranca', 0) +
            financial_data.get('manutencao_equipamentos', 0) +
            financial_data.get('marketing_publicidade', 0) +
            financial_data.get('contabilidade', 0) +
            financial_data.get('servicos_profissionais', 0) +
            financial_data.get('seguros_manutencao', 0)
        )
        
        custo_fixo_por_oculos = total_custos_fixos / financial_data['oculos_meta']
        
        return {
            'total_custos_fixos': total_custos_fixos,
            'custo_fixo_por_oculos': custo_fixo_por_oculos,
            'meta_oculos': financial_data['oculos_meta']
        }
    
    def generate_complete_analysis_with_financial_data(self, financial_data: Dict, custom_margins: Dict = None) -> pd.DataFrame:
        """Gera análise completa baseada nas Projeções Financeiras"""
        
        # Verificar se dados são válidos
        if not financial_data:
            st.error("Dados financeiros não encontrados na Etapa 10")
            return pd.DataFrame()
        
        # Calcular rateio
        rateio_data = self.calculate_fixed_cost_allocation(financial_data)
        custo_fixo_por_oculos = rateio_data['custo_fixo_por_oculos']
        
        produtos = []
        
        # Óculos completos (lente + armação)
        for lente_tipo, lente_custo in self.lens_costs.items():
            for armacao_tipo, armacao_custo in self.frame_costs.items():
                
                # Custo direto
                custo_direto = lente_custo + armacao_custo
                
                # Custo total (direto + rateio)
                custo_total = custo_direto + custo_fixo_por_oculos
                
                # Aplicar margens personalizadas
                if custom_margins:
                    if 'monofocal' in lente_tipo.lower():
                        margem = custom_margins.get('monofocal', 1.8)
                    elif 'multifocal' in lente_tipo.lower():
                        margem = custom_margins.get('multifocal', 2.2)
                    elif 'progressiva' in lente_tipo.lower():
                        margem = custom_margins.get('progressiva', 2.8)
                    else:
                        margem = 2.0
                else:
                    margem = 2.0
                
                # Preço calculado
                preco_calculado = custo_total * margem
                preco_calculado = round(preco_calculado / 10) * 10  # Arredondar para dezenas
                
                # Preço do sistema atual (buscar em dados existentes)
                preco_sistema = 0
                if 'business_data' in st.session_state:
                    business_data = st.session_state['business_data']
                    produtos_etapa5 = business_data.get('produtos', [])
                    for produto in produtos_etapa5:
                        if (lente_tipo.lower() in produto.get('nome', '').lower() and 
                            armacao_tipo.lower() in produto.get('nome', '').lower()):
                            preco_sistema = produto.get('preco', 0)
                            break
                
                # Margem em reais e percentual
                margem_reais = preco_calculado - custo_total
                margem_percentual = (margem_reais / custo_total * 100) if custo_total > 0 else 0
                
                produto = {
                    'PRODUTO': f"{lente_tipo} + {armacao_tipo}",
                    'LENTE': lente_tipo,
                    'ARMAÇÃO': armacao_tipo,
                    'CUSTO LENTE': lente_custo,
                    'CUSTO ARMAÇÃO': armacao_custo,
                    'TOTAL DIRETO': custo_direto,
                    'RATEIO FIXO': custo_fixo_por_oculos,
                    'CUSTO TOTAL': custo_total,
                    'PREÇO CALCULADO': preco_calculado,
                    'PREÇO SISTEMA': preco_sistema,
                    'DIFERENÇA': preco_calculado - preco_sistema if preco_sistema > 0 else 0,
                    'MARGEM R$': margem_reais,
                    'MARGEM %': margem_percentual
                }
                
                produtos.append(produto)
        
        # Serviços (sem custos diretos de materiais)
        for servico_nome, servico_custo in self.service_costs.items():
            custo_total = servico_custo + (custo_fixo_por_oculos * 0.3)  # Rateio reduzido para serviços
            preco_calculado = custo_total * 3.0  # Margem alta para serviços
            margem_reais = preco_calculado - custo_total
            margem_percentual = (margem_reais / custo_total * 100) if custo_total > 0 else 0
            
            produto = {
                'PRODUTO': servico_nome,
                'LENTE': 'Serviço',
                'ARMAÇÃO': 'N/A',
                'CUSTO LENTE': 0,
                'CUSTO ARMAÇÃO': 0,
                'TOTAL DIRETO': servico_custo,
                'RATEIO FIXO': custo_fixo_por_oculos * 0.3,
                'CUSTO TOTAL': custo_total,
                'PREÇO CALCULADO': preco_calculado,
                'PREÇO SISTEMA': 0,
                'DIFERENÇA': 0,
                'MARGEM R$': margem_reais,
                'MARGEM %': margem_percentual
            }
            
            produtos.append(produto)
        
        return pd.DataFrame(produtos)
    
    def format_currency(self, value: float) -> str:
        """Formata valor como moeda brasileira"""
        return f"R$ {value:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

def show_integrated_cost_analyzer():
    """Interface principal do analisador integrado de custos"""
    
    st.title("🏭 Sistema Integrado de Análise de Custos")
    st.markdown("**Fonte única de verdade baseada nas Projeções Financeiras**")
    
    analyzer = IntegratedCostAnalyzer()
    
    # Verificar dados das Projeções Financeiras
    financial_data = analyzer.extract_financial_data()
    
    if not financial_data or financial_data.get('oculos_meta', 0) <= 0:
        st.warning("⚠️ **Dados das Projeções Financeiras necessários**")
        st.info("Complete a **Etapa 10 → Projeções Financeiras** para usar dados reais incluindo combustível e todos os custos")
        
        with st.expander("📋 Dados Necessários"):
            st.markdown("- Meta de óculos vendidos por mês")
            st.markdown("- Estrutura completa de custos fixos")
            st.markdown("- **Combustível** (agora incluído)")
            st.markdown("- Aluguel, folha CLT, energia, marketing, etc.")
        return
    
    # Mostrar resumo dos dados extraídos
    col_info1, col_info2, col_info3 = st.columns(3)
    
    with col_info1:
        st.metric("Meta Óculos/Mês", f"{financial_data.get('oculos_meta', 0)} unidades")
    
    with col_info2:
        st.metric("Ticket Médio", analyzer.format_currency(financial_data.get('ticket_medio', 0)))
    
    with col_info3:
        faturamento = financial_data.get('oculos_meta', 0) * financial_data.get('ticket_medio', 0)
        st.metric("Faturamento Mensal", analyzer.format_currency(faturamento))
    
    # Estrutura de custos incluindo combustível
    with st.expander("📊 Estrutura de Custos das Projeções Financeiras"):
        rateio_data = analyzer.calculate_fixed_cost_allocation(financial_data)
        
        col_custos1, col_custos2 = st.columns(2)
        
        with col_custos1:
            st.markdown("**Custos Fixos Principais:**")
            st.write(f"• Aluguel: {analyzer.format_currency(financial_data.get('aluguel', 0))}")
            st.write(f"• Folha CLT: {analyzer.format_currency(financial_data.get('folha_clt', 0))}")
            st.write(f"• **Combustível: {analyzer.format_currency(financial_data.get('combustivel', 0))}**")
            st.write(f"• Energia/Água: {analyzer.format_currency(financial_data.get('energia_agua', 0))}")
            
        with col_custos2:
            st.markdown("**Outros Custos:**")
            st.write(f"• Marketing: {analyzer.format_currency(financial_data.get('marketing_publicidade', 0))}")
            st.write(f"• Telefone/Internet: {analyzer.format_currency(financial_data.get('telefone_internet', 0))}")
            st.write(f"• Material Limpeza: {analyzer.format_currency(financial_data.get('material_limpeza', 0))}")
            st.write(f"• Contabilidade: {analyzer.format_currency(financial_data.get('contabilidade', 0))}")
        
        st.markdown("**Resumo do Rateio:**")
        col_rateio1, col_rateio2 = st.columns(2)
        with col_rateio1:
            st.metric("Total Custos Fixos", analyzer.format_currency(rateio_data['total_custos_fixos']))
        with col_rateio2:
            st.metric("Rateio por Óculos", analyzer.format_currency(rateio_data['custo_fixo_por_oculos']))
    
    # Editor de margens
    st.markdown("## ⚙️ Editor de Margens")
    
    col_margin1, col_margin2, col_margin3 = st.columns(3)
    
    with col_margin1:
        st.markdown("**Margens por Tipo de Lente**")
        margem_monofocal = st.slider("Monofocal (%)", 50, 900, 180, 10, key="margem_monofocal")
        margem_multifocal = st.slider("Multifocal (%)", 50, 900, 220, 10, key="margem_multifocal")
        margem_progressiva = st.slider("Progressiva (%)", 50, 900, 280, 10, key="margem_progressiva")
    
    with col_margin2:
        st.markdown("**Margens por Tipo de Armação**")
        margem_nacional = st.slider("Nacional (%)", 50, 900, 200, 10, key="margem_nacional")
        margem_premium = st.slider("Premium (%)", 50, 900, 250, 10, key="margem_premium")
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
        'grife': margem_grife / 100
    }
    
    # Gerar análise
    if st.button("🔄 Gerar Análise com Dados Reais", type="primary"):
        with st.spinner("Gerando análise com dados das Projeções Financeiras..."):
            df_analysis = analyzer.generate_complete_analysis_with_financial_data(financial_data, margens_personalizadas)
            
            if df_analysis is not None and not df_analysis.empty:
                st.success(f"✅ Análise gerada com {len(df_analysis)} produtos")
                
                # Tabs para diferentes visualizações
                tab1, tab2, tab3 = st.tabs(["📋 Tabela Completa", "💰 Comparação Preços", "📊 Análise"])
                
                with tab1:
                    st.markdown("### Tabela Completa de Produtos")
                    
                    # Filtrar apenas os principais produtos
                    df_display = df_analysis.copy()
                    df_display['PREÇO CALCULADO'] = df_display['PREÇO CALCULADO'].round(0)
                    df_display['MARGEM %'] = df_display['MARGEM %'].round(1)
                    
                    # Colunas principais
                    colunas_principais = ['PRODUTO', 'CUSTO TOTAL', 'PREÇO CALCULADO', 'MARGEM %', 'MARGEM R$']
                    
                    # Mostrar top 20 produtos
                    st.dataframe(
                        df_display[colunas_principais].head(20),
                        use_container_width=True,
                        hide_index=True
                    )
                
                with tab2:
                    st.markdown("### Comparação: Calculado vs Sistema Atual")
                    
                    # Produtos com preços do sistema
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
                        
                        # Estatísticas
                        media_diferenca = df_comparacao['DIFERENÇA'].mean()
                        if media_diferenca > 0:
                            st.info(f"📈 Preços calculados são em média R$ {media_diferenca:.0f} maiores que o sistema atual")
                        else:
                            st.warning(f"📉 Preços calculados são em média R$ {abs(media_diferenca):.0f} menores que o sistema atual")
                    else:
                        st.info("💡 Configure preços na Etapa 5 para comparação")
                
                with tab3:
                    st.markdown("### Análise de Rentabilidade")
                    
                    # Top produtos mais rentáveis
                    df_oculos = df_analysis[df_analysis['LENTE'] != 'Serviço'].copy()
                    if len(df_oculos) > 0:
                        # Produtos mais rentáveis
                        top_rentaveis = df_oculos.head(8)
                        
                        st.markdown("**Produtos Mais Rentáveis:**")
                        for _, produto in top_rentaveis.iterrows():
                            st.write(f"• {produto['PRODUTO']}: R$ {produto['MARGEM R$']:.0f} ({produto['MARGEM %']:.1f}%)")
                        
                        # Margem média por categoria
                        st.markdown("**Margem Média por Categoria:**")
                        try:
                            # Listar tipos únicos de lente
                            tipos_lente = ['Monofocal Nacional', 'Monofocal Premium', 'Multifocal Nacional', 'Multifocal Premium', 'Progressiva Nacional', 'Progressiva Premium']
                            for lente_tipo in tipos_lente:
                                df_lente = df_oculos[df_oculos['LENTE'] == lente_tipo]
                                if len(df_lente) > 0:
                                    margem_media = df_lente['MARGEM %'].mean()
                                    st.write(f"• {lente_tipo}: {margem_media:.1f}%")
                        except Exception:
                            st.write("Dados de margem por categoria não disponíveis")
            else:
                st.error("❌ Erro ao gerar análise. Verifique os dados das Projeções Financeiras.")
    
    # Integração com Etapa 5
    st.markdown("## 📋 Integração com Estrutura de Custos (Etapa 5)")
    
    if 'business_data' in st.session_state:
        business_data = st.session_state['business_data']
        servicos_etapa5 = business_data.get('servicos', [])
        
        if servicos_etapa5:
            st.success(f"✅ Encontrados {len(servicos_etapa5)} serviços configurados na Etapa 5")
            
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

if __name__ == "__main__":
    show_integrated_cost_analyzer()