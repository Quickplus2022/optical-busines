import pandas as pd
from tax_calculator import TaxCalculator
from labor_calculator import LaborCalculator

class DREGenerator:
    """Generator for DRE (Demonstrativo do Resultado do Exercício)"""
    
    def __init__(self):
        self.tax_calc = TaxCalculator()
        self.labor_calc = LaborCalculator()
    
    def generate_dre(self, business_data, uploaded_files, num_lojas=1):
        """Generate complete DRE based on business data"""
        try:
            # Get revenue data from Step 3.5 product costing system
            receita_mensal_produtos = business_data.get('receita_mensal_estimada', 0)
            
            if receita_mensal_produtos > 0:
                # Use calculated revenue from product costing system
                receita_bruta_por_loja = receita_mensal_produtos
                receita_bruta = receita_bruta_por_loja * num_lojas
                receita_anual = receita_bruta * 12
                
                # Get calculated costs from product costing
                custo_produtos_mensal = business_data.get('custo_total_mensal_produtos', 0)
                margem_bruta_calculada = business_data.get('margem_bruta_mensal', 0)
                percentual_margem = business_data.get('percentual_margem_produtos', 50)
                
                # Use actual ticket médio from product mix
                ticket_medio = business_data.get('ticket_medio', 350)
                
                # Calculate sales volume
                total_vendas_mes = (
                    business_data.get('qtd_lentes', 0) +
                    business_data.get('qtd_armacoes', 0) +
                    business_data.get('qtd_exames', 0) +
                    business_data.get('qtd_servicos', 0)
                )
                vendas_mes_por_loja = total_vendas_mes
                
            else:
                # Fallback to traditional calculation if Step 3.5 not configured
                ticket_medio = business_data.get('ticket_medio', 350)
                vendas_dia = business_data.get('vendas_dia', 8)
                dias_uteis = business_data.get('dias_uteis', 26)
                
                # Revenue calculation
                vendas_mes_por_loja = vendas_dia * dias_uteis
                receita_bruta_por_loja = vendas_mes_por_loja * ticket_medio
                receita_bruta = receita_bruta_por_loja * num_lojas
                receita_anual = receita_bruta * 12
                
                # Use estimated margin
                percentual_margem = business_data.get('margem_esperada', 50)
                custo_produtos_mensal = receita_bruta_por_loja * ((100 - percentual_margem) / 100)
            
            # Tax calculation
            regime_tributario = business_data.get('regime_tributario', 'Simples Nacional')
            anexo_simples = business_data.get('anexo_simples', 'Anexo I - Comércio')
            
            if regime_tributario == "Simples Nacional":
                tax_result = self.tax_calc.calculate_simples_nacional(receita_anual, anexo_simples)
                impostos = tax_result['tributo_mensal']
            elif regime_tributario == "Lucro Presumido":
                tax_result = self.tax_calc.calculate_lucro_presumido(receita_anual)
                impostos = tax_result['tributo_mensal']
            else:
                # Default to Simples Nacional
                tax_result = self.tax_calc.calculate_simples_nacional(receita_anual, anexo_simples)
                impostos = tax_result['tributo_mensal']
            
            receita_liquida = receita_bruta - impostos
            
            # Cost of goods sold (CMV) - use calculated costs from Step 3.5
            if receita_mensal_produtos > 0:
                # Use actual calculated costs from product costing system
                cmv = custo_produtos_mensal * num_lojas
            else:
                # Fallback calculation
                cmv = receita_bruta * ((100 - percentual_margem) / 100)
            
            lucro_bruto = receita_liquida - cmv
            
            # Fixed costs
            custos_fixos_por_loja = (
                business_data.get('aluguel', 3500) +
                business_data.get('agua_luz', 400) +
                business_data.get('telefone_internet', 200) +
                business_data.get('marketing', 800) +
                business_data.get('outros_fixos', 500)
            )
            custos_fixos = custos_fixos_por_loja * num_lojas
            
            # Labor costs (folha CLT + serviços terceirizados - sem optometrista)
            custos_folha_clt = business_data.get('salarios_clt', 0) * num_lojas
            custos_servicos_terceirizados = business_data.get('servicos_terceirizados', 0) * num_lojas
            custos_pessoal = custos_folha_clt + custos_servicos_terceirizados
            
            # Despesas operacionais - serviços profissionais por diária
            despesas_servicos_profissionais = business_data.get('despesas_servicos_profissionais', 0) * num_lojas
            
            # Se não há dados do novo sistema, usar estimativa antiga
            if custos_pessoal == 0 and 'funcionarios' in uploaded_files:
                labor_costs = self.labor_calc.calculate_total_labor_costs(uploaded_files['funcionarios'])
                custos_pessoal = labor_costs['custo_total_mensal'] * num_lojas
            elif custos_pessoal == 0:
                # Estimate based on typical optical shop structure
                custos_pessoal = self._estimate_labor_costs(num_lojas)
            
            # Operational result
            lucro_operacional = lucro_bruto - custos_fixos - custos_pessoal - despesas_servicos_profissionais
            lucro_liquido = lucro_operacional  # Simplified (no financial costs)
            
            # Break-even point
            custo_total_mensal = custos_fixos + custos_pessoal + despesas_servicos_profissionais
            margem_contribuicao_unitaria = ticket_medio * (percentual_margem / 100)
            ponto_equilibrio = custo_total_mensal / margem_contribuicao_unitaria if margem_contribuicao_unitaria > 0 else 0
            
            return {
                "receita_bruta": receita_bruta,
                "impostos": impostos,
                "receita_liquida": receita_liquida,
                "cmv": cmv,
                "lucro_bruto": lucro_bruto,
                "custos_fixos": custos_fixos,
                "custos_pessoal": custos_pessoal,
                "despesas_servicos_profissionais": despesas_servicos_profissionais,
                "custos_folha_clt": custos_folha_clt,
                "custos_servicos_terceirizados": custos_servicos_terceirizados,
                "lucro_operacional": lucro_operacional,
                "lucro_liquido": lucro_liquido,
                "ponto_equilibrio": ponto_equilibrio,
                "vendas_mes": vendas_mes_por_loja * num_lojas,
                "tax_regime": regime_tributario,
                "tax_details": tax_result,
                "num_lojas": num_lojas
            }
            
        except Exception as e:
            return self._generate_default_dre(num_lojas, str(e))
    
    def _estimate_labor_costs(self, num_lojas):
        """Estimate labor costs for typical optical shop"""
        # Typical structure: 1 manager + 2 sales + 1 optometrist per store
        custo_por_loja = (
            4500 +  # Manager
            2800 * 2 +  # 2 Sales people
            5500  # Optometrist
        )
        # Apply labor charges (approximately 80%)
        custo_com_encargos = custo_por_loja * 1.8
        return custo_com_encargos * num_lojas
    
    def _generate_default_dre(self, num_lojas, error_msg=""):
        """Generate default DRE with basic estimates"""
        receita_bruta = 30000 * num_lojas  # Default R$ 30k per store
        impostos = receita_bruta * 0.08  # 8% default tax
        receita_liquida = receita_bruta - impostos
        cmv = receita_bruta * 0.5  # 50% CMV
        lucro_bruto = receita_liquida - cmv
        custos_fixos = 5400 * num_lojas  # Default fixed costs
        custos_pessoal = 15600 * num_lojas  # Default labor costs
        lucro_operacional = lucro_bruto - custos_fixos - custos_pessoal
        lucro_liquido = lucro_operacional
        
        return {
            "receita_bruta": receita_bruta,
            "impostos": impostos,
            "receita_liquida": receita_liquida,
            "cmv": cmv,
            "lucro_bruto": lucro_bruto,
            "custos_fixos": custos_fixos,
            "custos_pessoal": custos_pessoal,
            "lucro_operacional": lucro_operacional,
            "lucro_liquido": lucro_liquido,
            "ponto_equilibrio": 100 * num_lojas,
            "vendas_mes": 200 * num_lojas,
            "tax_regime": "Estimado",
            "num_lojas": num_lojas,
            "error": error_msg
        }
    
    def generate_annual_projection(self, dre_monthly, growth_rate=0, seasonal_months=None, seasonal_increase=30):
        """Generate 12-month projection based on monthly DRE"""
        months = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
                 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
        
        if seasonal_months is None:
            seasonal_months = ['Dezembro', 'Janeiro', 'Julho']
        
        projections = []
        base_receita = dre_monthly['receita_bruta']
        base_lucro = dre_monthly['lucro_liquido']
        
        for i, month in enumerate(months):
            # Apply growth
            growth_factor = (1 + growth_rate/100) ** i
            
            # Apply seasonality
            seasonality = 1 + (seasonal_increase/100) if month in seasonal_months else 1.0
            
            receita_mes = base_receita * growth_factor * seasonality
            lucro_mes = base_lucro * growth_factor * seasonality
            
            projections.append({
                'mes': month,
                'receita': receita_mes,
                'lucro': lucro_mes,
                'margem': (lucro_mes / receita_mes * 100) if receita_mes > 0 else 0
            })
        
        return projections
    
    def calculate_financial_indicators(self, dre_data, investimento_inicial=0):
        """Calculate financial performance indicators"""
        receita_bruta = dre_data['receita_bruta']
        lucro_liquido = dre_data['lucro_liquido']
        custos_totais = dre_data['custos_fixos'] + dre_data['custos_pessoal']
        
        indicators = {
            'margem_bruta': (dre_data['lucro_bruto'] / receita_bruta * 100) if receita_bruta > 0 else 0,
            'margem_operacional': (dre_data['lucro_operacional'] / receita_bruta * 100) if receita_bruta > 0 else 0,
            'margem_liquida': (lucro_liquido / receita_bruta * 100) if receita_bruta > 0 else 0,
            'ponto_equilibrio_vendas': dre_data['ponto_equilibrio'],
            'ponto_equilibrio_receita': dre_data['ponto_equilibrio'] * (receita_bruta / dre_data['vendas_mes']) if dre_data['vendas_mes'] > 0 else 0
        }
        
        if investimento_inicial > 0 and lucro_liquido > 0:
            indicators['payback_meses'] = investimento_inicial / lucro_liquido
            indicators['roi_anual'] = (lucro_liquido * 12 / investimento_inicial * 100)
        
        return indicators
    
    def generate_comparative_dre(self, business_data, uploaded_files, scenarios):
        """Generate comparative DRE for multiple scenarios"""
        comparative_results = []
        
        for scenario in scenarios:
            num_lojas = scenario.get('num_lojas', 1)
            modified_data = business_data.copy()
            
            # Apply scenario modifications
            if 'ticket_medio' in scenario:
                modified_data['ticket_medio'] = scenario['ticket_medio']
            if 'vendas_dia' in scenario:
                modified_data['vendas_dia'] = scenario['vendas_dia']
            if 'margem_esperada' in scenario:
                modified_data['margem_esperada'] = scenario['margem_esperada']
            
            dre = self.generate_dre(modified_data, uploaded_files, num_lojas)
            dre['scenario_name'] = scenario.get('name', f"Cenário {num_lojas} lojas")
            comparative_results.append(dre)
        
        return comparative_results
