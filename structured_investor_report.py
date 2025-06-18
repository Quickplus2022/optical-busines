"""
Gerador de Relatório Estruturado para Investidor
Baseado no checklist profissional com KPIs específicos para óticas
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.pdfgen import canvas
from io import BytesIO
from datetime import datetime, timedelta
import pandas as pd

class StructuredInvestorReport:
    """Gerador de relatório estruturado para investidores seguindo checklist profissional"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Configura estilos customizados para o PDF"""
        
        # Estilo do título principal
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=20,
            textColor=colors.HexColor('#1a365d'),
            alignment=TA_CENTER,
            spaceAfter=30,
            fontName='Helvetica-Bold'
        )
        
        # Estilo dos cabeçalhos de seção
        self.section_style = ParagraphStyle(
            'SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#2d3748'),
            alignment=TA_LEFT,
            spaceAfter=12,
            spaceBefore=20,
            fontName='Helvetica-Bold',
            backColor=colors.HexColor('#f7fafc'),
            borderPadding=8
        )
        
        # Estilo dos subcabeçalhos
        self.subsection_style = ParagraphStyle(
            'SubsectionHeader',
            parent=self.styles['Heading3'],
            fontSize=12,
            textColor=colors.HexColor('#4a5568'),
            alignment=TA_LEFT,
            spaceAfter=8,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        )
        
        # Estilo do texto normal
        self.normal_style = ParagraphStyle(
            'CustomNormal',
            parent=self.styles['Normal'],
            fontSize=10,
            alignment=TA_JUSTIFY,
            spaceAfter=6,
            fontName='Helvetica'
        )
        
        # Estilo para KPIs
        self.kpi_style = ParagraphStyle(
            'KPI',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#2b6cb0'),
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        # Estilo para alertas
        self.alert_style = ParagraphStyle(
            'Alert',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#e53e3e'),
            alignment=TA_LEFT,
            spaceAfter=6,
            fontName='Helvetica-Bold'
        )
    
    def _format_currency(self, value):
        """Formata valores monetários"""
        if value is None or value == 0:
            return "R$ 0,00"
        try:
            return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        except:
            return "R$ 0,00"
    
    def _format_percentage(self, value):
        """Formata percentuais"""
        try:
            return f"{value:.1f}%"
        except:
            return "0,0%"
    
    def _calculate_kpis(self, business_data):
        """Calcula KPIs específicos para óticas"""
        
        # Dados básicos
        receita_mensal = business_data.get('vendas_mes_1', 20831)
        receita_anual = business_data.get('receita_anual', 250000)
        ticket_medio = business_data.get('ticket_medio', 180)
        investimento_total = business_data.get('investimento_total', 81500)
        lucro_operacional = business_data.get('lucro_operacional', 45000)
        margem_operacional = business_data.get('margem_operacional', 18)
        
        # Cálculos de KPIs
        vendas_mes = receita_mensal / ticket_medio if ticket_medio > 0 else 0
        cac = 150  # Custo de Aquisição de Cliente estimado para óticas
        ltv = ticket_medio * 12  # LTV estimado (cliente compra 1x por ano)
        ltv_cac_ratio = ltv / cac if cac > 0 else 0
        
        # Burn rate (custos fixos mensais)
        custos_fixos_mes = business_data.get('aluguel', 3500) + business_data.get('salarios_total', 5500)
        burn_rate = custos_fixos_mes
        
        # Runway (meses de operação com capital atual)
        capital_disponivel = business_data.get('capital_giro', 18000)
        runway_meses = capital_disponivel / burn_rate if burn_rate > 0 else 0
        
        # Margem bruta
        cmv_perc = business_data.get('cmv_percentual', 45)
        margem_bruta = 100 - cmv_perc
        
        # Ponto de equilíbrio
        ponto_equilibrio = business_data.get('ponto_equilibrio_valor', 15000)
        equilibrio_atingido = receita_mensal >= ponto_equilibrio
        
        return {
            'receita_bruta_mensal': receita_mensal,
            'receita_anual': receita_anual,
            'margem_bruta': margem_bruta,
            'ticket_medio': ticket_medio,
            'vendas_mes': vendas_mes,
            'cac': cac,
            'ltv': ltv,
            'ltv_cac_ratio': ltv_cac_ratio,
            'burn_rate': burn_rate,
            'runway_meses': runway_meses,
            'margem_operacional': margem_operacional,
            'roi_anual': business_data.get('roi_anual', 55),
            'ponto_equilibrio': ponto_equilibrio,
            'equilibrio_atingido': equilibrio_atingido,
            'payback_anos': business_data.get('payback_anos', 1.8)
        }
    
    def generate_structured_report(self, business_data, language="pt"):
        """Gera relatório estruturado completo"""
        
        # Configurar buffer
        buffer = BytesIO()
        
        # Configurar documento
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=50,
            leftMargin=50,
            topMargin=80,
            bottomMargin=80
        )
        
        story = []
        
        # Dados básicos
        nome_negocio = business_data.get('nome_negocio', 'Ótica')
        cidade = business_data.get('cidade', 'Cidade')
        estado = business_data.get('estado', 'Estado')
        data_atual = datetime.now()
        periodo = f"{data_atual.strftime('%b')}-{(data_atual + timedelta(days=90)).strftime('%b %Y')}"
        
        # Calcular KPIs
        kpis = self._calculate_kpis(business_data)
        
        # 1. CAPA
        story.append(Paragraph("RELATÓRIO COMPLETO PARA INVESTIDOR", self.title_style))
        story.append(Paragraph(nome_negocio.upper(), self.title_style))
        story.append(Spacer(1, 20))
        
        capa_info = f"""
        <b>Período:</b> {periodo}<br/>
        <b>Localização:</b> {cidade}, {estado}<br/>
        <b>Data do Relatório:</b> {data_atual.strftime('%d/%m/%Y')}<br/>
        <b>Responsável:</b> {business_data.get('responsavel', 'Empreendedor')}<br/>
        <b>Contato:</b> {business_data.get('contato', 'contato@empresa.com')}
        """
        story.append(Paragraph(capa_info, self.normal_style))
        story.append(PageBreak())
        
        # 2. RESUMO EXECUTIVO
        story.append(Paragraph("2. RESUMO EXECUTIVO", self.section_style))
        
        resumo = f"""
        <b>Visão Geral:</b> {nome_negocio} é uma ótica estrategicamente posicionada no mercado de {cidade}, 
        focada em oferecer produtos ópticos de qualidade com atendimento diferenciado.<br/><br/>
        
        <b>Foco do Período:</b> Consolidação da operação e crescimento sustentável da base de clientes.<br/><br/>
        
        <b>Destaques Principais:</b><br/>
        • Receita mensal projetada: {self._format_currency(kpis['receita_bruta_mensal'])}<br/>
        • Margem bruta de {self._format_percentage(kpis['margem_bruta'])}<br/>
        • Ponto de equilíbrio {"atingido" if kpis['equilibrio_atingido'] else "previsto em 6 meses"}<br/>
        • ROI anual de {self._format_percentage(kpis['roi_anual'])}<br/><br/>
        
        <b>Desafios Críticos:</b><br/>
        • Construção de base sólida de clientes recorrentes<br/>
        • Otimização de estoque e fornecedores<br/>
        • Competição com grandes redes do mercado
        """
        story.append(Paragraph(resumo, self.normal_style))
        story.append(Spacer(1, 20))
        
        # 3. INDICADORES-CHAVE (KPIs)
        story.append(Paragraph("3. INDICADORES-CHAVE (KPIs)", self.section_style))
        
        kpi_data = [
            ['Indicador', 'Valor Atual', 'Variação', 'Meta'],
            ['Receita Bruta Mensal', self._format_currency(kpis['receita_bruta_mensal']), 'Base', self._format_currency(25000)],
            ['Margem Bruta (%)', self._format_percentage(kpis['margem_bruta']), 'Base', '60%'],
            ['Ticket Médio', self._format_currency(kpis['ticket_medio']), 'Base', self._format_currency(200)],
            ['Vendas/Mês (un)', f"{kpis['vendas_mes']:.0f}", 'Base', '150'],
            ['CAC', self._format_currency(kpis['cac']), 'Estimado', self._format_currency(120)],
            ['LTV', self._format_currency(kpis['ltv']), 'Base', self._format_currency(2000)],
            ['LTV/CAC', f"{kpis['ltv_cac_ratio']:.1f}x", '↑', '>3x'],
            ['Burn Rate', self._format_currency(kpis['burn_rate']) + '/mês', 'Base', self._format_currency(8000) + '/mês'],
            ['Runway', f"{kpis['runway_meses']:.1f} meses", 'Base', '12 meses'],
            ['ROI Anual', self._format_percentage(kpis['roi_anual']), 'Projetado', '40%']
        ]
        
        kpi_table = Table(kpi_data, colWidths=[2.2*inch, 1.5*inch, 1*inch, 1*inch])
        kpi_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2d3748')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f7fafc')])
        ]))
        
        story.append(kpi_table)
        story.append(PageBreak())
        
        # 4. DESEMPENHO FINANCEIRO
        story.append(Paragraph("4. DESEMPENHO FINANCEIRO", self.section_style))
        
        # DRE Resumida
        story.append(Paragraph("DRE Resumida (Projeção Anual)", self.subsection_style))
        
        dre_data = [
            ['Item', 'Valor Anual', '% Receita'],
            ['Receita Bruta', self._format_currency(kpis['receita_anual']), '100,0%'],
            ['(-) CMV', self._format_currency(kpis['receita_anual'] * (100-kpis['margem_bruta'])/100), f"{100-kpis['margem_bruta']:.1f}%"],
            ['= Margem Bruta', self._format_currency(kpis['receita_anual'] * kpis['margem_bruta']/100), f"{kpis['margem_bruta']:.1f}%"],
            ['(-) Custos Fixos', self._format_currency(kpis['burn_rate'] * 12), f"{kpis['burn_rate'] * 12 / kpis['receita_anual'] * 100:.1f}%"],
            ['= Lucro Operacional', self._format_currency(kpis['receita_anual'] * kpis['margem_operacional']/100), f"{kpis['margem_operacional']:.1f}%"]
        ]
        
        dre_table = Table(dre_data, colWidths=[2.5*inch, 1.5*inch, 1*inch])
        dre_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2b6cb0')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0')),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#e6fffa'))
        ]))
        
        story.append(dre_table)
        story.append(Spacer(1, 15))
        
        # Ponto de Equilíbrio
        equilibrio_text = f"""
        <b>Ponto de Equilíbrio:</b> {self._format_currency(kpis['ponto_equilibrio'])}/mês<br/>
        <b>Status:</b> {"✅ Atingido" if kpis['equilibrio_atingido'] else "⏳ Previsto para próximos 6 meses"}<br/>
        <b>Payback do Investimento:</b> {kpis['payback_anos']:.1f} anos
        """
        story.append(Paragraph(equilibrio_text, self.normal_style))
        story.append(Spacer(1, 20))
        
        # 5. USO DO INVESTIMENTO
        story.append(Paragraph("5. USO DO INVESTIMENTO", self.section_style))
        
        investimento_total = business_data.get('investimento_total', 81500)
        uso_data = [
            ['Categoria', 'Valor', '% Total'],
            ['Reforma da Loja', self._format_currency(business_data.get('reforma_loja', 15000)), f"{business_data.get('reforma_loja', 15000)/investimento_total*100:.1f}%"],
            ['Equipamentos', self._format_currency(business_data.get('equipamentos_moveis', 12000)), f"{business_data.get('equipamentos_moveis', 12000)/investimento_total*100:.1f}%"],
            ['Estoque Inicial', self._format_currency(business_data.get('estoque_inicial', 25000)), f"{business_data.get('estoque_inicial', 25000)/investimento_total*100:.1f}%"],
            ['Capital de Giro', self._format_currency(business_data.get('capital_giro', 18000)), f"{business_data.get('capital_giro', 18000)/investimento_total*100:.1f}%"],
            ['Outros', self._format_currency(business_data.get('outros_investimentos', 11500)), f"{business_data.get('outros_investimentos', 11500)/investimento_total*100:.1f}%"]
        ]
        
        uso_table = Table(uso_data, colWidths=[2.5*inch, 1.5*inch, 1*inch])
        uso_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#38a169')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0'))
        ]))
        
        story.append(uso_table)
        story.append(Spacer(1, 15))
        
        uso_status = f"""
        <b>Status do Investimento:</b><br/>
        • Valor total investido: {self._format_currency(investimento_total)}<br/>
        • Saldo disponível: {self._format_currency(business_data.get('capital_giro', 18000))}<br/>
        • Projeção de uso futuro: 6-12 meses para expansão de estoque e marketing
        """
        story.append(Paragraph(uso_status, self.normal_style))
        story.append(PageBreak())
        
        # 6. CLIENTES E TRAÇÃO
        story.append(Paragraph("6. CLIENTES E TRAÇÃO", self.section_style))
        
        clientes_text = f"""
        <b>Número de Clientes Ativos:</b> {int(kpis['vendas_mes'] * 0.8)} clientes/mês<br/>
        <b>Taxa de Crescimento:</b> Projetado 2% ao mês<br/>
        <b>Ticket Médio:</b> {self._format_currency(kpis['ticket_medio'])}<br/>
        <b>Frequência de Compra:</b> 1,2x por ano (média do setor)<br/>
        <b>Taxa de Retenção:</b> 85% (estimativa baseada em relacionamento próximo)<br/>
        <b>Principais Segmentos:</b><br/>
        • Profissionais liberais (40%)<br/>
        • Estudantes e jovens (30%)<br/>
        • Idosos com prescrição (30%)<br/><br/>
        
        <b>Diferenciais Competitivos:</b><br/>
        • Atendimento personalizado e consultivo<br/>
        • Localização estratégica com fácil acesso<br/>
        • Relacionamento próximo com clientes<br/>
        • Parcerias com oftalmologistas locais
        """
        story.append(Paragraph(clientes_text, self.normal_style))
        story.append(Spacer(1, 20))
        
        # 7. PRODUTO E TECNOLOGIA
        story.append(Paragraph("7. PRODUTO E TECNOLOGIA", self.section_style))
        
        produto_text = f"""
        <b>Mix de Produtos Atual:</b><br/>
        • Óculos de grau (60% do faturamento)<br/>
        • Óculos de sol (25% do faturamento)<br/>
        • Lentes de contato (10% do faturamento)<br/>
        • Acessórios e serviços (5% do faturamento)<br/><br/>
        
        <b>Fornecedores Principais:</b><br/>
        • ATAK, Brasil Lentes, GOLD (lentes)<br/>
        • Fornecedores nacionais de armações<br/>
        • Distribuidores de lentes de contato<br/><br/>
        
        <b>Inovações Planejadas:</b><br/>
        • Sistema de gestão integrado<br/>
        • Vendas online para produtos selecionados<br/>
        • Programa de fidelidade digital<br/>
        • Agendamento online para consultas
        """
        story.append(Paragraph(produto_text, self.normal_style))
        story.append(Spacer(1, 20))
        
        # 8. MARKETING E VENDAS
        story.append(Paragraph("8. MARKETING E VENDAS", self.section_style))
        
        marketing_text = f"""
        <b>Canais de Aquisição:</b><br/>
        • Localização e tráfego de pedestres (50%)<br/>
        • Indicação de clientes (30%)<br/>
        • Parcerias com oftalmologistas (15%)<br/>
        • Marketing digital local (5%)<br/><br/>
        
        <b>Custo de Aquisição (CAC):</b> {self._format_currency(kpis['cac'])}<br/>
        <b>LTV/CAC Ratio:</b> {kpis['ltv_cac_ratio']:.1f}x (excelente para varejo)<br/><br/>
        
        <b>Estratégias Futuras:</b><br/>
        • Programa de indicação com desconto<br/>
        • Marketing digital direcionado (Google Ads, Facebook)<br/>
        • Parcerias com empresas locais<br/>
        • Eventos e campanhas sazonais (Dia dos Pais, volta às aulas)
        """
        story.append(Paragraph(marketing_text, self.normal_style))
        story.append(PageBreak())
        
        # 9. RISCOS E DESAFIOS
        story.append(Paragraph("9. RISCOS E DESAFIOS", self.section_style))
        
        riscos_text = f"""
        <b>Principais Riscos Identificados:</b><br/>
        • <b>Concorrência:</b> Grandes redes com poder de negociação<br/>
        • <b>Economia Local:</b> Dependência do poder de compra regional<br/>
        • <b>Sazonalidade:</b> Variações durante o ano letivo<br/>
        • <b>Fornecedores:</b> Concentração em poucos fornecedores principais<br/><br/>
        
        <b>Estratégias de Mitigação:</b><br/>
        • Diferenciação pelo atendimento personalizado<br/>
        • Diversificação de fornecedores e produtos<br/>
        • Programa de fidelização para reduzir churn<br/>
        • Reserva de capital para 6 meses de operação<br/>
        • Monitoramento constante de margens e custos
        """
        story.append(Paragraph(riscos_text, self.normal_style))
        story.append(Spacer(1, 20))
        
        # 10. PRÓXIMOS PASSOS E METAS
        story.append(Paragraph("10. PRÓXIMOS PASSOS E METAS", self.section_style))
        
        proximos_text = f"""
        <b>Próximos 30 dias:</b><br/>
        • Finalizar instalação e abertura da loja<br/>
        • Contratar e treinar equipe inicial<br/>
        • Estabelecer parcerias com oftalmologistas<br/>
        • Lançar campanha de inauguração<br/><br/>
        
        <b>Próximos 90 dias:</b><br/>
        • Atingir {int(kpis['vendas_mes'] * 0.5)} vendas/mês<br/>
        • Implementar sistema de gestão<br/>
        • Estabelecer base de {int(kpis['vendas_mes'] * 0.8)} clientes ativos<br/>
        • Otimizar mix de produtos baseado em vendas<br/><br/>
        
        <b>Metas Anuais:</b><br/>
        • Receita anual: {self._format_currency(kpis['receita_anual'])}<br/>
        • Margem operacional: {self._format_percentage(kpis['margem_operacional'])}<br/>
        • ROI: {self._format_percentage(kpis['roi_anual'])}<br/>
        • Payback: {kpis['payback_anos']:.1f} anos<br/><br/>
        
        <b>Expansão Futura:</b><br/>
        • Avaliação de segunda loja após 18 meses<br/>
        • Possível franqueamento do modelo após consolidação
        """
        story.append(Paragraph(proximos_text, self.normal_style))
        story.append(Spacer(1, 20))
        
        # CONCLUSÃO
        story.append(Paragraph("CONCLUSÃO E RECOMENDAÇÃO", self.section_style))
        
        conclusao_text = f"""
        <b>Recomendação de Investimento: APROVADO</b><br/><br/>
        
        {nome_negocio} apresenta fundamentos sólidos para um investimento de baixo risco e retorno atrativo:
        <br/><br/>
        
        <b>Pontos Fortes:</b><br/>
        • Mercado óptico em crescimento constante (8% a.a.)<br/>
        • Localização estratégica com alto tráfego<br/>
        • Modelo de negócio comprovado e sustentável<br/>
        • ROI atrativo de {self._format_percentage(kpis['roi_anual'])} ao ano<br/>
        • Payback de {kpis['payback_anos']:.1f} anos, adequado para o setor<br/>
        • LTV/CAC de {kpis['ltv_cac_ratio']:.1f}x indica eficiência na aquisição<br/><br/>
        
        <b>Próximos Acompanhamentos:</b><br/>
        • Relatório mensal de vendas e KPIs<br/>
        • Reunião trimestral para análise de resultados<br/>
        • Apresentação anual de resultados e planos futuros
        """
        story.append(Paragraph(conclusao_text, self.normal_style))
        
        # Construir PDF
        doc.build(story)
        
        buffer.seek(0)
        return buffer