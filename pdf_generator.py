import io
import base64
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import numpy as np

class PDFGenerator:
    """Generator for PDF reports and business plan documents"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Title'],
            fontSize=16,
            spaceAfter=30,
            textColor=colors.darkblue
        )
    
    def generate_business_plan_report(self, business_data, dre_data):
        """Generate a comprehensive business plan report in text format"""
        
        report = f"""
===============================================
        PLANO DE NEGÓCIOS - ÓTICA
        {business_data.get('nome_otica', 'Ótica Não Definida')}
===============================================

Data de Geração: {datetime.now().strftime('%d/%m/%Y %H:%M')}

==== 1. RESUMO EXECUTIVO ====

Nome da Empresa: {business_data.get('nome_otica', 'Não definido')}
Localização: {business_data.get('cidade', 'Não definida')}
Tipo de Produto: {business_data.get('tipo_produto', 'Não definido')}

Investimento Inicial: R$ {business_data.get('valor_estimado', 0):,.2f}
Receita Mensal Projetada: R$ {dre_data.get('receita_bruta', 0):,.2f}
Lucro Líquido Mensal: R$ {dre_data.get('lucro_liquido', 0):,.2f}
Margem Líquida: {(dre_data.get('lucro_liquido', 0) / dre_data.get('receita_bruta', 1) * 100):.1f}%

==== 2. VISÃO GERAL DO NEGÓCIO ====

Sócios e Experiência:
{business_data.get('socios', 'Não informado')}

Exames Próprios: {business_data.get('exame_proprio', 'Não definido')}

Número de Lojas Inicial: {business_data.get('num_lojas_inicial', 1)}

==== 3. MERCADO E CLIENTE ====

Público-Alvo:
{business_data.get('publico_alvo', 'Não definido')}

Faixa Etária: {business_data.get('faixa_etaria', 'Não definida')}

Problema que Resolve:
{business_data.get('problema_resolve', 'Não informado')}

Principais Concorrentes:
{business_data.get('concorrentes', 'Não informado')}

Diferencial Competitivo:
{business_data.get('diferencial', 'Não informado')}

==== 4. ESTRUTURA OPERACIONAL ====

Modelo de Atendimento: {', '.join(business_data.get('modelo_atendimento', []))}

Equipe Mínima por Loja:
{business_data.get('equipe_minima', 'Não definido')}

Fornecedores:
{business_data.get('fornecedores', 'Não informado')}

Sistemas: {', '.join(business_data.get('sistema_informatizado', []))}

==== 5. PRODUTOS E PREÇOS ====

Combos Oferecidos:
{business_data.get('combos_oferecidos', 'Não informado')}

Ticket Médio: R$ {business_data.get('ticket_medio', 0):,.2f}
Margem Esperada: {business_data.get('margem_esperada', 0)}%
Formas de Pagamento: {', '.join(business_data.get('formas_pagamento', []))}
Desconto à Vista: {business_data.get('desconto_avista', 0)}%
Máximo de Parcelas: {business_data.get('max_parcelas', 1)}x

==== 6. PROJEÇÕES FINANCEIRAS ====

DEMONSTRATIVO DO RESULTADO (MENSAL)
------------------------------------------
(+) Receita Bruta               R$ {dre_data.get('receita_bruta', 0):>10,.2f}
(-) Impostos                    R$ {dre_data.get('impostos', 0):>10,.2f}
(=) Receita Líquida             R$ {dre_data.get('receita_liquida', 0):>10,.2f}
(-) CMV                         R$ {dre_data.get('cmv', 0):>10,.2f}
(=) Lucro Bruto                 R$ {dre_data.get('lucro_bruto', 0):>10,.2f}
(-) Custos Fixos                R$ {dre_data.get('custos_fixos', 0):>10,.2f}
(-) Custos com Pessoal          R$ {dre_data.get('custos_pessoal', 0):>10,.2f}
(=) Lucro Operacional           R$ {dre_data.get('lucro_operacional', 0):>10,.2f}
(=) Lucro Líquido               R$ {dre_data.get('lucro_liquido', 0):>10,.2f}

INDICADORES FINANCEIROS
------------------------------------------
Ponto de Equilíbrio:            {dre_data.get('ponto_equilibrio', 0):,.0f} vendas/mês
Margem Bruta:                   {(dre_data.get('lucro_bruto', 0) / dre_data.get('receita_bruta', 1) * 100):.1f}%
Margem Líquida:                 {(dre_data.get('lucro_liquido', 0) / dre_data.get('receita_bruta', 1) * 100):.1f}%
"""

        # Add investment details if available
        if business_data.get('valor_estimado', 0) > 0:
            payback = business_data.get('valor_estimado', 0) / max(dre_data.get('lucro_liquido', 1), 1)
            roi_anual = (dre_data.get('lucro_liquido', 0) * 12 / business_data.get('valor_estimado', 1)) * 100
            
            report += f"""
Payback:                        {payback:.1f} meses
ROI Anual:                      {roi_anual:.1f}%
"""

        # Add cost breakdown
        report += f"""

==== 7. CUSTOS OPERACIONAIS ====

CUSTOS FIXOS MENSAIS (por loja)
------------------------------------------
Aluguel:                        R$ {business_data.get('aluguel', 0):,.2f}
Água + Luz:                     R$ {business_data.get('agua_luz', 0):,.2f}
Telefone + Internet:            R$ {business_data.get('telefone_internet', 0):,.2f}
Marketing:                      R$ {business_data.get('marketing', 0):,.2f}
Outros:                         R$ {business_data.get('outros_fixos', 0):,.2f}
------------------------------------------
Total por loja:                 R$ {(business_data.get('aluguel', 0) + business_data.get('agua_luz', 0) + business_data.get('telefone_internet', 0) + business_data.get('marketing', 0) + business_data.get('outros_fixos', 0)):,.2f}

PROJEÇÃO DE VENDAS
------------------------------------------
Vendas por dia por loja:        {business_data.get('vendas_dia', 0)} unidades
Dias úteis por mês:             {business_data.get('dias_uteis', 0)}
Vendas mensais por loja:        {business_data.get('vendas_dia', 0) * business_data.get('dias_uteis', 0)} unidades
"""

        # Add tax compliance information
        if 'regime_tributario' in business_data:
            report += f"""

==== 8. COMPLIANCE TRIBUTÁRIO ====

Regime Tributário: {business_data.get('regime_tributario', 'Não definido')}
"""
            if business_data.get('regime_tributario') == 'Simples Nacional':
                report += f"Anexo: {business_data.get('anexo_simples', 'Não definido')}\n"
            
            if 'tax_details' in dre_data:
                tax_details = dre_data['tax_details']
                if 'aliquota_efetiva' in tax_details:
                    report += f"Alíquota Efetiva: {tax_details['aliquota_efetiva']:.2f}%\n"
                report += f"Tributos Mensais: R$ {tax_details.get('tributo_mensal', 0):,.2f}\n"
                report += f"Tributos Anuais: R$ {tax_details.get('tributo_anual', 0):,.2f}\n"

        # Add marketing strategy
        report += f"""

==== 9. ESTRATÉGIA DE MARKETING ====

Como Atrair Primeiros Clientes:
{business_data.get('primeiros_clientes', 'Não informado')}

Parcerias: {', '.join(business_data.get('parcerias', []))}
Canais de Marketing: {', '.join(business_data.get('canais_marketing', []))}
Orçamento Mensal Marketing: R$ {business_data.get('orcamento_marketing', 0):,.2f}

==== 10. GESTÃO DE RISCOS ====

Principais Riscos: {', '.join(business_data.get('principais_riscos', []))}

Plano de Mitigação:
{business_data.get('plano_mitigacao', 'Não informado')}

Reserva de Emergência: {business_data.get('reserva_financeira', 'Não definida')}

==== 11. INVESTIMENTO INICIAL ====

Valor Total Necessário: R$ {business_data.get('valor_estimado', 0):,.2f}
Origem do Capital: {business_data.get('capital_proprio', 'Não definido')}

Principais Itens:
{business_data.get('itens_investimento', 'Não informado')}

==== 12. RECOMENDAÇÕES ESTRATÉGICAS ====

"""

        # Add strategic recommendations
        margem_liquida = (dre_data.get('lucro_liquido', 0) / dre_data.get('receita_bruta', 1) * 100)
        
        if margem_liquida < 5:
            report += "⚠️  ATENÇÃO: Margem líquida muito baixa. Revisar custos ou estratégia de preços.\n"
        elif margem_liquida < 10:
            report += "⚠️  Margem líquida baixa. Monitorar custos e buscar otimizações.\n"
        else:
            report += "✅ Margem líquida adequada para o setor.\n"

        if dre_data.get('ponto_equilibrio', 0) > business_data.get('vendas_dia', 0) * business_data.get('dias_uteis', 0):
            report += "⚠️  Ponto de equilíbrio acima das vendas projetadas. Revisar projeções.\n"
        else:
            report += "✅ Ponto de equilíbrio atingível com as vendas projetadas.\n"

        if business_data.get('valor_estimado', 0) > 0:
            payback = business_data.get('valor_estimado', 0) / max(dre_data.get('lucro_liquido', 1), 1)
            if payback > 24:
                report += "⚠️  Payback muito longo. Considerar reduzir investimento inicial.\n"
            elif payback > 12:
                report += "⚠️  Payback moderado. Monitorar fluxo de caixa nos primeiros meses.\n"
            else:
                report += "✅ Payback atrativo para o investimento.\n"

        report += f"""

==== 13. PRÓXIMOS PASSOS ====

1. Validar projeções com pesquisa de mercado local
2. Definir fornecedores e negociar condições
3. Buscar ponto comercial adequado
4. Regularizar documentação (CNPJ, licenças)
5. Implementar sistema de gestão
6. Desenvolver estratégia de lançamento
7. Monitorar indicadores mensalmente

===============================================
RELATÓRIO GERADO EM {datetime.now().strftime('%d/%m/%Y às %H:%M')}
Sistema de Plano de Negócios - Ótica v1.0
===============================================
"""

        return report
    
    def generate_dre_csv(self, dre_data):
        """Generate DRE in CSV format"""
        csv_content = """Descrição,Valor (R$)
(+) Receita Bruta,{:.2f}
(-) Impostos,{:.2f}
(=) Receita Líquida,{:.2f}
(-) CMV,{:.2f}
(=) Lucro Bruto,{:.2f}
(-) Custos Fixos,{:.2f}
(-) Custos com Pessoal,{:.2f}
(=) Lucro Operacional,{:.2f}
(=) Lucro Líquido,{:.2f}""".format(
            dre_data.get('receita_bruta', 0),
            dre_data.get('impostos', 0),
            dre_data.get('receita_liquida', 0),
            dre_data.get('cmv', 0),
            dre_data.get('lucro_bruto', 0),
            dre_data.get('custos_fixos', 0),
            dre_data.get('custos_pessoal', 0),
            dre_data.get('lucro_operacional', 0),
            dre_data.get('lucro_liquido', 0)
        )
        return csv_content
    
    def generate_projection_csv(self, projections):
        """Generate monthly projections in CSV format"""
        csv_content = "Mês,Receita (R$),Lucro (R$),Margem (%)\n"
        
        for proj in projections:
            csv_content += f"{proj['mes']},{proj['receita']:.2f},{proj['lucro']:.2f},{proj['margem']:.2f}\n"
        
        return csv_content
    
    def generate_executive_summary(self, business_data, dre_data):
        """Generate executive summary for investors/partners"""
        
        summary = f"""
RESUMO EXECUTIVO - {business_data.get('nome_otica', 'ÓTICA')}

OPORTUNIDADE DE NEGÓCIO
• Mercado: {business_data.get('publico_alvo', 'Ótica geral')}
• Localização: {business_data.get('cidade', 'Não definida')}
• Diferencial: {business_data.get('diferencial', 'Não definido')[:100]}...

PROJEÇÕES FINANCEIRAS
• Investimento Inicial: R$ {business_data.get('valor_estimado', 0):,.2f}
• Receita Mensal: R$ {dre_data.get('receita_bruta', 0):,.2f}
• Lucro Mensal: R$ {dre_data.get('lucro_liquida', 0):,.2f}
• Margem Líquida: {(dre_data.get('lucro_liquido', 0) / dre_data.get('receita_bruta', 1) * 100):.1f}%
• Payback: {(business_data.get('valor_estimado', 0) / max(dre_data.get('lucro_liquido', 1), 1)):.1f} meses

REGIME TRIBUTÁRIO
• {business_data.get('regime_tributario', 'Simples Nacional')}
• Carga Tributária: {(dre_data.get('impostos', 0) / dre_data.get('receita_bruta', 1) * 100):.1f}%

EQUIPE E ESTRUTURA
• Número de Lojas: {business_data.get('num_lojas_inicial', 1)}
• {business_data.get('equipe_minima', 'Equipe não definida')[:100]}

RISCOS E MITIGAÇÃO
• {business_data.get('plano_mitigacao', 'Não informado')[:200]}

Data: {datetime.now().strftime('%d/%m/%Y')}
"""
        return summary
    
    def generate_pdf_with_charts(self, business_data, dre_data, charts_data=None):
        """Generate PDF report with charts and financial data"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72,
                               topMargin=72, bottomMargin=18)
        
        # Container for the 'Flowable' objects
        elements = []
        
        # Title
        title = Paragraph("PLANO DE NEGÓCIOS - ÓTICA", self.title_style)
        elements.append(title)
        elements.append(Spacer(1, 20))
        
        # Business summary
        business_name = business_data.get('nome_otica', 'Ótica Não Definida')
        city = business_data.get('cidade', 'Cidade não informada')
        
        summary_text = f"""
        <b>Nome da Empresa:</b> {business_name}<br/>
        <b>Localização:</b> {city}<br/>
        <b>Data do Relatório:</b> {datetime.now().strftime('%d/%m/%Y')}<br/>
        """
        
        summary = Paragraph(summary_text, self.styles['Normal'])
        elements.append(summary)
        elements.append(Spacer(1, 20))
        
        # Financial Summary Table
        financial_title = Paragraph("RESUMO FINANCEIRO", self.styles['Heading2'])
        elements.append(financial_title)
        elements.append(Spacer(1, 12))
        
        financial_data = [
            ['Descrição', 'Valor (R$)'],
            ['Receita Bruta Mensal', f"{dre_data.get('receita_bruta', 0):,.2f}"],
            ['Impostos', f"{dre_data.get('impostos', 0):,.2f}"],
            ['Receita Líquida', f"{dre_data.get('receita_liquida', 0):,.2f}"],
            ['CMV', f"{dre_data.get('cmv', 0):,.2f}"],
            ['Lucro Bruto', f"{dre_data.get('lucro_bruto', 0):,.2f}"],
            ['Custos Fixos', f"{dre_data.get('custos_fixos', 0):,.2f}"],
            ['Custos com Pessoal', f"{dre_data.get('custos_pessoal', 0):,.2f}"],
            ['Lucro Líquido', f"{dre_data.get('lucro_liquido', 0):,.2f}"]
        ]
        
        financial_table = Table(financial_data, colWidths=[3*inch, 2*inch])
        financial_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(financial_table)
        elements.append(Spacer(1, 20))
        
        # Key Indicators
        indicators_title = Paragraph("INDICADORES PRINCIPAIS", self.styles['Heading2'])
        elements.append(indicators_title)
        elements.append(Spacer(1, 12))
        
        receita_bruta = dre_data.get('receita_bruta', 1)
        margem_bruta = (dre_data.get('lucro_bruto', 0) / receita_bruta) * 100 if receita_bruta > 0 else 0
        margem_liquida = (dre_data.get('lucro_liquido', 0) / receita_bruta) * 100 if receita_bruta > 0 else 0
        
        indicators_data = [
            ['Indicador', 'Valor'],
            ['Margem Bruta', f"{margem_bruta:.1f}%"],
            ['Margem Líquida', f"{margem_liquida:.1f}%"],
            ['Ponto de Equilíbrio', f"{dre_data.get('ponto_equilibrio', 0):.0f} vendas/mês"]
        ]
        
        if 'valor_estimado' in business_data:
            investimento = business_data['valor_estimado']
            payback = investimento / max(dre_data.get('lucro_liquido', 1), 1)
            indicators_data.append(['Payback', f"{payback:.1f} meses"])
        
        indicators_table = Table(indicators_data, colWidths=[3*inch, 2*inch])
        indicators_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(indicators_table)
        elements.append(Spacer(1, 20))
        
        # Add DRE chart
        chart_title = Paragraph("GRÁFICO DRE - COMPOSIÇÃO DO RESULTADO", self.styles['Heading2'])
        elements.append(chart_title)
        elements.append(Spacer(1, 12))
        
        # Create DRE chart with matplotlib
        chart_buffer = self.create_dre_chart(dre_data)
        if chart_buffer:
            chart_image = Image(chart_buffer, width=6*inch, height=4*inch)
            elements.append(chart_image)
            elements.append(Spacer(1, 20))
        
        elements.append(PageBreak())
        
        # Business Details
        details_title = Paragraph("DETALHES DO NEGÓCIO", self.styles['Heading2'])
        elements.append(details_title)
        elements.append(Spacer(1, 12))
        
        # Market and customers
        market_text = f"""
        <b>Público-Alvo:</b> {business_data.get('publico_alvo', 'Não definido')}<br/>
        <b>Faixa Etária:</b> {business_data.get('faixa_etaria', 'Não definida')}<br/>
        <b>Diferencial Competitivo:</b> {business_data.get('diferencial', 'Não informado')}<br/>
        """
        
        market_para = Paragraph(market_text, self.styles['Normal'])
        elements.append(market_para)
        elements.append(Spacer(1, 15))
        
        # Operations
        operations_text = f"""
        <b>Número de Lojas Inicial:</b> {business_data.get('num_lojas_inicial', 1)}<br/>
        <b>Modelo de Atendimento:</b> {', '.join(business_data.get('modelo_atendimento', []))}<br/>
        <b>Ticket Médio:</b> R$ {business_data.get('ticket_medio', 0):,.2f}<br/>
        <b>Margem Esperada:</b> {business_data.get('margem_esperada', 0)}%<br/>
        """
        
        operations_para = Paragraph(operations_text, self.styles['Normal'])
        elements.append(operations_para)
        elements.append(Spacer(1, 15))
        
        # Investment
        if 'valor_estimado' in business_data:
            investment_text = f"""
            <b>INVESTIMENTO INICIAL</b><br/>
            <b>Valor Total:</b> R$ {business_data['valor_estimado']:,.2f}<br/>
            <b>Origem do Capital:</b> {business_data.get('capital_proprio', 'Não definido')}<br/>
            """
            
            investment_para = Paragraph(investment_text, self.styles['Normal'])
            elements.append(investment_para)
            elements.append(Spacer(1, 15))
        
        # Tax regime
        if 'regime_tributario' in business_data:
            tax_text = f"""
            <b>REGIME TRIBUTÁRIO</b><br/>
            <b>Regime:</b> {business_data.get('regime_tributario', 'Não definido')}<br/>
            """
            if business_data.get('regime_tributario') == 'Simples Nacional':
                tax_text += f"<b>Anexo:</b> {business_data.get('anexo_simples', 'Não definido')}<br/>"
            
            tax_para = Paragraph(tax_text, self.styles['Normal'])
            elements.append(tax_para)
        
        # Build PDF
        doc.build(elements)
        buffer.seek(0)
        return buffer.getvalue()
    
    def create_dre_chart(self, dre_data):
        """Create DRE waterfall chart using matplotlib"""
        try:
            plt.style.use('default')
            fig, ax = plt.subplots(figsize=(10, 6))
            
            # Data for waterfall chart
            labels = ['Receita\nBruta', 'Impostos', 'CMV', 'Custos\nFixos', 'Custos\nPessoal', 'Lucro\nLíquido']
            values = [
                dre_data.get('receita_bruta', 0),
                -dre_data.get('impostos', 0),
                -dre_data.get('cmv', 0),
                -dre_data.get('custos_fixos', 0),
                -dre_data.get('custos_pessoal', 0),
                dre_data.get('lucro_liquido', 0)
            ]
            
            # Create waterfall effect
            cumulative = np.cumsum([0] + values[:-1])
            colors = ['green', 'red', 'red', 'red', 'red', 'blue']
            
            # Plot bars
            for i, (label, value, cum, color) in enumerate(zip(labels, values, cumulative, colors)):
                if i == 0 or i == len(labels) - 1:  # First and last bars start from zero
                    ax.bar(i, abs(value), bottom=0 if value >= 0 else value, 
                          color=color, alpha=0.7, edgecolor='black')
                else:  # Intermediate bars stack
                    bottom = cum if value < 0 else cum + value
                    ax.bar(i, abs(value), bottom=bottom, 
                          color=color, alpha=0.7, edgecolor='black')
                
                # Add value labels
                label_y = cum + value/2 if i != 0 and i != len(labels)-1 else value/2
                ax.text(i, label_y, f'R$ {abs(value):,.0f}', ha='center', va='center', 
                       fontweight='bold', fontsize=9)
            
            # Connect bars with lines
            for i in range(len(labels) - 1):
                if i < len(cumulative) - 1:
                    start_y = cumulative[i] + values[i] if i > 0 else values[0]
                    end_y = cumulative[i + 1]
                    ax.plot([i + 0.4, i + 1 - 0.4], [start_y, end_y], 
                           'k--', alpha=0.5, linewidth=1)
            
            ax.set_xticks(range(len(labels)))
            ax.set_xticklabels(labels, rotation=0, ha='center')
            ax.set_ylabel('Valor (R$)')
            ax.set_title('Demonstrativo do Resultado do Exercício (DRE)', fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3)
            
            # Format y-axis
            ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'R$ {x:,.0f}'))
            
            plt.tight_layout()
            
            # Save to buffer
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight', 
                       facecolor='white', edgecolor='none')
            buffer.seek(0)
            plt.close()
            
            return buffer
            
        except Exception as e:
            # Fallback simple chart
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.text(0.5, 0.5, 'Gráfico DRE\nEm construção', ha='center', va='center', 
                   fontsize=16, fontweight='bold')
            ax.set_title('Demonstrativo do Resultado do Exercício')
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
            buffer.seek(0)
            plt.close()
            
            return buffer
    
    def create_projection_chart(self, business_data, dre_data):
        """Create monthly projection chart"""
        try:
            months = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 
                     'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
            
            receita_base = dre_data.get('receita_bruta', 0)
            lucro_base = dre_data.get('lucro_liquido', 0)
            
            receitas = []
            lucros = []
            
            for i, month in enumerate(months):
                growth_factor = 1 + (i * 0.02)  # 2% monthly growth
                seasonality = 1.3 if month in ['Dez', 'Jan', 'Jul'] else 1.0
                
                receita_mes = receita_base * growth_factor * seasonality
                lucro_mes = lucro_base * growth_factor * seasonality
                
                receitas.append(receita_mes)
                lucros.append(lucro_mes)
            
            fig, ax = plt.subplots(figsize=(10, 6))
            
            x = np.arange(len(months))
            ax.plot(x, receitas, marker='o', linewidth=2, label='Receita Bruta', color='blue')
            ax.plot(x, lucros, marker='s', linewidth=2, label='Lucro Líquido', color='green')
            
            ax.set_xlabel('Meses')
            ax.set_ylabel('Valor (R$)')
            ax.set_title('Projeção Anual - Receita e Lucro', fontsize=14, fontweight='bold')
            ax.set_xticks(x)
            ax.set_xticklabels(months)
            ax.legend()
            ax.grid(True, alpha=0.3)
            
            # Format y-axis
            ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'R$ {x:,.0f}'))
            
            plt.tight_layout()
            
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight',
                       facecolor='white', edgecolor='none')
            buffer.seek(0)
            plt.close()
            
            return buffer
            
        except Exception as e:
            return None
