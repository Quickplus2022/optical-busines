"""
Gerador de PDF Multilíngue para Relatório de Investidores
Formato profissional e elegante com suporte a Português, Inglês e Espanhol
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.pdfgen import canvas
from io import BytesIO
from datetime import datetime
import locale

class MultilingualInvestorPDFGenerator:
    """Gerador de PDF para relatório de investidores em múltiplos idiomas"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
        
        # Configurações de idioma
        self.translations = {
            "pt": {
                "title": "RELATÓRIO COMPLETO PARA INVESTIDORES",
                "date": "Data:",
                "page": "Página",
                "executive_summary": "SUMÁRIO EXECUTIVO",
                "purpose_problem": "1. PROPÓSITO E PROBLEMA",
                "solution_value": "2. SOLUÇÃO E PROPOSTA DE VALOR",
                "market_opportunity": "3. MERCADO E OPORTUNIDADE", 
                "competition": "4. ANÁLISE DA CONCORRÊNCIA",
                "financial": "5. PROJEÇÕES FINANCEIRAS",
                "team": "6. EQUIPE E GESTÃO",
                "conclusion": "7. CONCLUSÃO E RECOMENDAÇÃO",
                "problem_identified": "Problema Identificado",
                "market_validation": "Validação do Mercado",
                "value_proposition": "Proposta de Valor",
                "products_services": "Produtos e Serviços",
                "competitive_advantage": "Diferencial Competitivo",
                "market_size": "Tamanho do Mercado",
                "location": "Localização",
                "sector_trends": "Tendências do Setor",
                "initial_investment": "Investimento Inicial",
                "annual_projections": "Projeções Anuais",
                "entrepreneur_experience": "Experiência do Empreendedor",
                "organizational_structure": "Estrutura Organizacional",
                "investment_strengths": "Pontos Fortes do Investimento",
                "identified_risks": "Riscos Identificados",
                "recommendation": "Recomendação",
                "recommended": "RECOMENDADO",
                "total": "TOTAL",
                "revenue": "Faturamento",
                "average_ticket": "Ticket Médio",
                "employees": "Funcionários",
                "payroll": "Folha de Pagamento",
                "renovation": "Reforma",
                "equipment": "Equipamentos",
                "initial_stock": "Estoque Inicial",
                "working_capital": "Capital de Giro"
            },
            "en": {
                "title": "COMPLETE INVESTOR REPORT",
                "date": "Date:",
                "page": "Page",
                "executive_summary": "EXECUTIVE SUMMARY",
                "purpose_problem": "1. PURPOSE AND PROBLEM",
                "solution_value": "2. SOLUTION AND VALUE PROPOSITION",
                "market_opportunity": "3. MARKET AND OPPORTUNITY",
                "competition": "4. COMPETITION ANALYSIS",
                "financial": "5. FINANCIAL PROJECTIONS",
                "team": "6. TEAM AND MANAGEMENT",
                "conclusion": "7. CONCLUSION AND RECOMMENDATION",
                "problem_identified": "Identified Problem",
                "market_validation": "Market Validation",
                "value_proposition": "Value Proposition",
                "products_services": "Products and Services",
                "competitive_advantage": "Competitive Advantage",
                "market_size": "Market Size",
                "location": "Location",
                "sector_trends": "Sector Trends",
                "initial_investment": "Initial Investment",
                "annual_projections": "Annual Projections",
                "entrepreneur_experience": "Entrepreneur Experience",
                "organizational_structure": "Organizational Structure",
                "investment_strengths": "Investment Strengths",
                "identified_risks": "Identified Risks",
                "recommendation": "Recommendation",
                "recommended": "RECOMMENDED",
                "total": "TOTAL",
                "revenue": "Revenue",
                "average_ticket": "Average Ticket",
                "employees": "Employees",
                "payroll": "Payroll",
                "renovation": "Renovation",
                "equipment": "Equipment",
                "initial_stock": "Initial Stock",
                "working_capital": "Working Capital"
            },
            "es": {
                "title": "INFORME COMPLETO PARA INVERSORES",
                "date": "Fecha:",
                "page": "Página",
                "executive_summary": "RESUMEN EJECUTIVO",
                "purpose_problem": "1. PROPÓSITO Y PROBLEMA",
                "solution_value": "2. SOLUCIÓN Y PROPUESTA DE VALOR",
                "market_opportunity": "3. MERCADO Y OPORTUNIDAD",
                "competition": "4. ANÁLISIS DE COMPETENCIA",
                "financial": "5. PROYECCIONES FINANCIERAS",
                "team": "6. EQUIPO Y GESTIÓN",
                "conclusion": "7. CONCLUSIÓN Y RECOMENDACIÓN",
                "problem_identified": "Problema Identificado",
                "market_validation": "Validación del Mercado",
                "value_proposition": "Propuesta de Valor",
                "products_services": "Productos y Servicios",
                "competitive_advantage": "Ventaja Competitiva",
                "market_size": "Tamaño del Mercado",
                "location": "Ubicación",
                "sector_trends": "Tendencias del Sector",
                "initial_investment": "Inversión Inicial",
                "annual_projections": "Proyecciones Anuales",
                "entrepreneur_experience": "Experiencia del Emprendedor",
                "organizational_structure": "Estructura Organizacional",
                "investment_strengths": "Fortalezas de la Inversión",
                "identified_risks": "Riesgos Identificados",
                "recommendation": "Recomendación",
                "recommended": "RECOMENDADO",
                "total": "TOTAL",
                "revenue": "Facturación",
                "average_ticket": "Ticket Promedio",
                "employees": "Empleados",
                "payroll": "Nómina",
                "renovation": "Renovación",
                "equipment": "Equipos",
                "initial_stock": "Stock Inicial",
                "working_capital": "Capital de Trabajo"
            }
        }
    
    def _setup_custom_styles(self):
        """Configura estilos customizados para o PDF"""
        
        # Estilo do título principal
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#1f4e79'),
            alignment=TA_CENTER,
            spaceAfter=30,
            fontName='Helvetica-Bold'
        )
        
        # Estilo dos cabeçalhos de seção
        self.section_style = ParagraphStyle(
            'SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#2f5f8f'),
            alignment=TA_LEFT,
            spaceAfter=12,
            spaceBefore=20,
            fontName='Helvetica-Bold'
        )
        
        # Estilo dos subcabeçalhos
        self.subsection_style = ParagraphStyle(
            'SubsectionHeader',
            parent=self.styles['Heading3'],
            fontSize=12,
            textColor=colors.HexColor('#4472a8'),
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
        
        # Estilo para texto em destaque
        self.highlight_style = ParagraphStyle(
            'Highlight',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#d32f2f'),
            alignment=TA_LEFT,
            spaceAfter=6,
            fontName='Helvetica-Bold'
        )
    
    def _header_footer(self, canvas, doc, business_name, language):
        """Adiciona cabeçalho e rodapé às páginas"""
        canvas.saveState()
        
        # Cabeçalho
        canvas.setFont('Helvetica-Bold', 10)
        canvas.setFillColor(colors.HexColor('#1f4e79'))
        canvas.drawString(50, A4[1] - 50, business_name.upper())
        
        # Linha decorativa no cabeçalho
        canvas.setStrokeColor(colors.HexColor('#1f4e79'))
        canvas.setLineWidth(2)
        canvas.line(50, A4[1] - 60, A4[0] - 50, A4[1] - 60)
        
        # Rodapé
        canvas.setFont('Helvetica', 8)
        canvas.setFillColor(colors.gray)
        page_text = f"{self.translations[language]['page']} {doc.page}"
        canvas.drawRightString(A4[0] - 50, 30, page_text)
        
        # Data no rodapé
        date_str = datetime.now().strftime('%d/%m/%Y' if language in ['pt', 'es'] else '%m/%d/%Y')
        canvas.drawString(50, 30, f"{self.translations[language]['date']} {date_str}")
        
        canvas.restoreState()
    
    def _format_currency(self, value, language="pt"):
        """Formata valores monetários de acordo com o idioma"""
        if value is None or value == 0:
            return "R$ 0,00"
        
        try:
            if language == "pt" or language == "es":
                return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            else:  # English
                return f"R$ {value:,.2f}"
        except:
            return "R$ 0,00"
    
    def generate_investor_report_pdf(self, business_data, language="pt"):
        """Gera o PDF completo do relatório para investidores"""
        
        # Configurar idioma
        lang_code = {"Português": "pt", "English": "en", "Español": "es"}.get(language, "pt")
        t = self.translations[lang_code]
        
        # Criar buffer para o PDF
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
        
        # Lista de elementos do documento
        story = []
        
        # Dados básicos
        business_name = business_data.get('nome_negocio', 'Ótica')
        cidade = business_data.get('cidade', 'Cidade')
        estado = business_data.get('estado', 'Estado')
        
        # Título principal
        story.append(Paragraph(t["title"], self.title_style))
        story.append(Paragraph(business_name.upper(), self.title_style))
        story.append(Spacer(1, 30))
        
        # Sumário Executivo
        story.append(Paragraph(t["executive_summary"], self.section_style))
        
        executive_summary = f"""
        {business_name} é um empreendimento no setor óptico localizado em {cidade}, {estado}, 
        posicionado para atender a crescente demanda por produtos e serviços ópticos de qualidade. 
        O negócio combina localização estratégica, atendimento personalizado e produtos de qualidade 
        para criar uma proposta de valor diferenciada no mercado local.
        """
        
        if lang_code == "en":
            executive_summary = f"""
            {business_name} is an optical sector venture located in {cidade}, {estado}, 
            positioned to serve the growing demand for quality optical products and services. 
            The business combines strategic location, personalized service and quality products 
            to create a differentiated value proposition in the local market.
            """
        elif lang_code == "es":
            executive_summary = f"""
            {business_name} es un emprendimiento del sector óptico ubicado en {cidade}, {estado}, 
            posicionado para atender la creciente demanda de productos y servicios ópticos de calidad. 
            El negocio combina ubicación estratégica, atención personalizada y productos de calidad 
            para crear una propuesta de valor diferenciada en el mercado local.
            """
        
        story.append(Paragraph(executive_summary, self.normal_style))
        story.append(Spacer(1, 20))
        
        # 1. Propósito e Problema
        story.append(Paragraph(t["purpose_problem"], self.section_style))
        
        story.append(Paragraph(t["problem_identified"], self.subsection_style))
        problema = business_data.get('problema_mercado', 'Dificuldade de acesso a produtos ópticos de qualidade')
        story.append(Paragraph(problema, self.normal_style))
        
        story.append(Paragraph(t["market_validation"], self.subsection_style))
        if lang_code == "en":
            validation_text = """
            • Optical market growth: 8% annually<br/>
            • Population aging increasing demand<br/>
            • Intensive use of digital screens<br/>
            • Growing awareness of eye health importance
            """
        elif lang_code == "es":
            validation_text = """
            • Crecimiento del mercado óptico: 8% anual<br/>
            • Envejecimiento poblacional aumentando demanda<br/>
            • Uso intensivo de pantallas digitales<br/>
            • Creciente conciencia sobre la importancia de la salud ocular
            """
        else:
            validation_text = """
            • Crescimento do mercado óptico: 8% ao ano<br/>
            • Envelhecimento populacional aumentando demanda<br/>
            • Uso intensivo de telas digitais<br/>
            • Crescente consciência sobre importância da saúde ocular
            """
        
        story.append(Paragraph(validation_text, self.normal_style))
        story.append(PageBreak())
        
        # 2. Solução e Proposta de Valor
        story.append(Paragraph(t["solution_value"], self.section_style))
        
        story.append(Paragraph(t["value_proposition"], self.subsection_style))
        proposta_valor = business_data.get('proposta_valor', 'Atendimento óptico completo e personalizado')
        story.append(Paragraph(proposta_valor, self.normal_style))
        
        story.append(Paragraph(t["products_services"], self.subsection_style))
        produtos_servicos = business_data.get('produtos_servicos', 'Óculos, lentes de contato e exames')
        story.append(Paragraph(produtos_servicos, self.normal_style))
        
        story.append(Paragraph(t["competitive_advantage"], self.subsection_style))
        if lang_code == "en":
            advantage_text = """
            • Personalized and consultative service<br/>
            • Privileged strategic location<br/>
            • Close customer relationships<br/>
            • Delivery speed and efficiency
            """
        elif lang_code == "es":
            advantage_text = """
            • Atención personalizada y consultiva<br/>
            • Ubicación estratégica privilegiada<br/>
            • Relación cercana con clientes<br/>
            • Rapidez y eficiencia en la entrega
            """
        else:
            advantage_text = """
            • Atendimento personalizado e consultivo<br/>
            • Localização estratégica privilegiada<br/>
            • Relacionamento próximo com clientes<br/>
            • Agilidade e eficiência na entrega
            """
        
        story.append(Paragraph(advantage_text, self.normal_style))
        story.append(Spacer(1, 20))
        
        # 3. Mercado e Oportunidade
        story.append(Paragraph(t["market_opportunity"], self.section_style))
        
        story.append(Paragraph(f"{t['location']}: {cidade}, {estado}", self.subsection_style))
        
        story.append(Paragraph(t["market_size"], self.subsection_style))
        market_data = [
            ['TAM (Brasil)', 'R$ 4,2 bilhões' if lang_code != 'en' else 'R$ 4.2 billion'],
            ['SAM (Regional)', self._format_currency(4200000000 * 0.02, lang_code)],
            ['SOM (Obtível)' if lang_code != 'en' else 'SOM (Obtainable)', self._format_currency(4200000000 * 0.02 * 0.01, lang_code)]
        ]
        
        market_table = Table(market_data, colWidths=[2*inch, 2*inch])
        market_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f5f5f5')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cccccc'))
        ]))
        
        story.append(market_table)
        story.append(Spacer(1, 15))
        
        # 4. Projeções Financeiras
        story.append(Paragraph(t["financial"], self.section_style))
        
        story.append(Paragraph(t["initial_investment"], self.subsection_style))
        
        # Tabela de investimentos
        investimento_data = [
            [t["renovation"], self._format_currency(business_data.get('reforma_loja', 0), lang_code)],
            [t["equipment"], self._format_currency(business_data.get('equipamentos_moveis', 0), lang_code)],
            [t["initial_stock"], self._format_currency(business_data.get('estoque_inicial', 0), lang_code)],
            [t["working_capital"], self._format_currency(business_data.get('capital_giro', 0), lang_code)],
            [t["total"], self._format_currency(business_data.get('investimento_total', 81500), lang_code)]
        ]
        
        invest_table = Table(investimento_data, colWidths=[2.5*inch, 1.5*inch])
        invest_table.setStyle(TableStyle([
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#e3f2fd')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cccccc'))
        ]))
        
        story.append(invest_table)
        story.append(Spacer(1, 15))
        
        story.append(Paragraph(t["annual_projections"], self.subsection_style))
        projection_data = [
            [t["revenue"], self._format_currency(business_data.get('receita_anual', 180000), lang_code)],
            [t["average_ticket"], self._format_currency(business_data.get('ticket_medio', 150), lang_code)]
        ]
        
        proj_table = Table(projection_data, colWidths=[2.5*inch, 1.5*inch])
        proj_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f5f5f5')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cccccc'))
        ]))
        
        story.append(proj_table)
        story.append(PageBreak())
        
        # 5. Equipe e Gestão
        story.append(Paragraph(t["team"], self.section_style))
        
        story.append(Paragraph(t["entrepreneur_experience"], self.subsection_style))
        experiencia = business_data.get('experiencia_setor', 'Experiência sólida no setor óptico')
        story.append(Paragraph(experiencia, self.normal_style))
        
        story.append(Paragraph(t["organizational_structure"], self.subsection_style))
        num_funcionarios = business_data.get('num_funcionarios', 2)
        folha_pagamento = business_data.get('salarios_total', 5000)
        
        team_text = f"• {t['employees']}: {num_funcionarios}<br/>• {t['payroll']}: {self._format_currency(folha_pagamento, lang_code)}"
        story.append(Paragraph(team_text, self.normal_style))
        story.append(Spacer(1, 20))
        
        # 6. Conclusão e Recomendação
        story.append(Paragraph(t["conclusion"], self.section_style))
        
        story.append(Paragraph(t["investment_strengths"], self.subsection_style))
        if lang_code == "en":
            strengths_text = """
            • Constantly growing market<br/>
            • Reasonable initial investment<br/>
            • Strategic location<br/>
            • Entrepreneur experience<br/>
            • Proven business model
            """
        elif lang_code == "es":
            strengths_text = """
            • Mercado en crecimiento constante<br/>
            • Inversión inicial razonable<br/>
            • Ubicación estratégica<br/>
            • Experiencia del emprendedor<br/>
            • Modelo de negocio comprobado
            """
        else:
            strengths_text = """
            • Mercado em crescimento constante<br/>
            • Investimento inicial razoável<br/>
            • Localização estratégica<br/>
            • Experiência do empreendedor<br/>
            • Modelo de negócio comprovado
            """
        
        story.append(Paragraph(strengths_text, self.normal_style))
        
        story.append(Paragraph(t["identified_risks"], self.subsection_style))
        if lang_code == "en":
            risks_text = """
            • Competition from large chains<br/>
            • Local economy dependence<br/>
            • Market seasonality
            """
        elif lang_code == "es":
            risks_text = """
            • Competencia de grandes cadenas<br/>
            • Dependencia de la economía local<br/>
            • Estacionalidad del mercado
            """
        else:
            risks_text = """
            • Concorrência de grandes redes<br/>
            • Dependência da economia local<br/>
            • Sazonalidade do mercado
            """
        
        story.append(Paragraph(risks_text, self.normal_style))
        story.append(Spacer(1, 15))
        
        story.append(Paragraph(t["recommendation"], self.subsection_style))
        
        if lang_code == "en":
            recommendation_text = f"""
            Investment <b>{t["recommended"]}</b> based on complete market analysis, 
            financial viability and entrepreneur profile. The optical business presents 
            solid fundamentals and growth potential in an expanding market.
            """
        elif lang_code == "es":
            recommendation_text = f"""
            Inversión <b>{t["recommended"]}</b> basada en análisis completo del mercado, 
            viabilidad financiera y perfil del emprendedor. El negocio óptico presenta 
            fundamentos sólidos y potencial de crecimiento en un mercado en expansión.
            """
        else:
            recommendation_text = f"""
            Investimento <b>{t["recommended"]}</b> com base na análise completa do mercado, 
            viabilidade financeira e perfil do empreendedor. O negócio óptico apresenta 
            fundamentos sólidos e potencial de crescimento em um mercado em expansão.
            """
        
        story.append(Paragraph(recommendation_text, self.highlight_style))
        
        # Construir PDF com cabeçalho e rodapé customizados
        def add_header_footer(canvas, doc):
            self._header_footer(canvas, doc, business_name, lang_code)
        
        doc.build(story, onFirstPage=add_header_footer, onLaterPages=add_header_footer)
        
        # Retornar o buffer
        buffer.seek(0)
        return buffer