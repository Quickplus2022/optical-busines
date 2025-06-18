import pandas as pd

class LaborCalculator:
    """Calculator for Brazilian labor law compliance (CLT)"""
    
    def __init__(self):
        # Brazilian labor law rates (2025)
        self.inss_empresa = 0.20  # 20% employer INSS
        self.fgts = 0.08  # 8% FGTS
        self.ferias_provisao = 1/12  # 1/12 vacation provision
        self.decimo_terceiro = 1/12  # 1/12 13th salary provision
        self.inss_funcionario_max = 0.11  # Maximum 11% employee INSS
        self.inss_teto = 8157.41  # INSS ceiling 2025
        self.salario_minimo = 1518.00  # Minimum wage 2025
        
        # Additional charges
        self.salario_educacao = 0.025  # 2.5% education salary
        self.sistema_s = 0.01  # 1% Sistema S (SENAC/SEBRAE)
        self.acidente_trabalho = 0.02  # 2% work accident insurance (average)
        self.sebrae = 0.006  # 0.6% SEBRAE
    
    def calculate_inss_employee(self, salario_base):
        """Calculate employee INSS contribution with 2025 brackets"""
        if salario_base <= 1518.00:
            return salario_base * 0.075
        elif salario_base <= 2771.55:
            return 1518.00 * 0.075 + (salario_base - 1518.00) * 0.09
        elif salario_base <= 4159.00:
            return 1518.00 * 0.075 + (2771.55 - 1518.00) * 0.09 + (salario_base - 2771.55) * 0.12
        elif salario_base <= self.inss_teto:
            return 1518.00 * 0.075 + (2771.55 - 1518.00) * 0.09 + (4159.00 - 2771.55) * 0.12 + (salario_base - 4159.00) * 0.14
        else:
            return 1518.00 * 0.075 + (2771.55 - 1518.00) * 0.09 + (4159.00 - 2771.55) * 0.12 + (self.inss_teto - 4159.00) * 0.14
    
    def calculate_employee_cost(self, salario_base, encargos_adicionais=0.0):
        """Calculate total cost of a single employee"""
        try:
            # Ensure salary is valid
            if salario_base <= 0:
                return {
                    "salario_base": 0,
                    "inss_empresa": 0,
                    "fgts": 0,
                    "salario_educacao": 0,
                    "sistema_s": 0,
                    "acidente_trabalho": 0,
                    "sebrae": 0,
                    "ferias": 0,
                    "decimo_terceiro": 0,
                    "outros_encargos": 0,
                    "custo_total_mensal": 0,
                    "percentual_encargos": 0,
                    "error": "Invalid salary"
                }
            
            # Base salary
            custo_base = float(salario_base)
            
            # Employer contributions - using the correct rates
            inss_empresa = custo_base * 0.20  # 20% employer INSS
            fgts = custo_base * 0.08  # 8% FGTS
            salario_educacao = custo_base * 0.025  # 2.5% education salary
            sistema_s = custo_base * 0.01  # 1% Sistema S
            acidente_trabalho = custo_base * 0.02  # 2% work accident
            sebrae = custo_base * 0.006  # 0.6% SEBRAE
            
            # Provisions (paid annually but provisioned monthly)
            ferias = custo_base * (1/12)  # 1/12 for vacation
            decimo_terceiro = custo_base * (1/12)  # 1/12 for 13th salary
            
            # Additional charges (if specified)
            outros_encargos = custo_base * (float(encargos_adicionais) / 100)
            
            # Total monthly cost
            custo_total = (
                custo_base +
                inss_empresa +
                fgts +
                salario_educacao +
                sistema_s +
                acidente_trabalho +
                sebrae +
                ferias +
                decimo_terceiro +
                outros_encargos
            )
            
            return {
                "salario_base": salario_base,
                "inss_empresa": inss_empresa,
                "fgts": fgts,
                "salario_educacao": salario_educacao,
                "sistema_s": sistema_s,
                "acidente_trabalho": acidente_trabalho,
                "sebrae": sebrae,
                "ferias": ferias,
                "decimo_terceiro": decimo_terceiro,
                "outros_encargos": outros_encargos,
                "custo_total_mensal": custo_total,
                "percentual_encargos": ((custo_total - salario_base) / salario_base) * 100
            }
            
        except Exception as e:
            return {
                "salario_base": salario_base,
                "inss_empresa": salario_base * 0.20,
                "fgts": salario_base * 0.08,
                "salario_educacao": salario_base * 0.025,
                "sistema_s": salario_base * 0.01,
                "acidente_trabalho": salario_base * 0.02,
                "sebrae": salario_base * 0.006,
                "ferias": salario_base * (1/12),
                "decimo_terceiro": salario_base * (1/12),
                "outros_encargos": 0.0,
                "custo_total_mensal": salario_base * 1.8,
                "percentual_encargos": 80.0,
                "error": str(e)
            }
    

    
    def calculate_total_labor_costs(self, df_funcionarios):
        """Calculate total labor costs from employee DataFrame"""
        try:
            total_salarios = 0
            total_custos = 0
            total_encargos_sociais = 0
            total_provisoes = 0
            funcionarios_detalhes = []
            
            for index, funcionario in df_funcionarios.iterrows():
                cargo = funcionario['Cargo']
                quantidade = int(funcionario['Quantidade'])
                salario_base = float(funcionario['Salário Base (R$)'])
                
                # Fix: Interpret "Encargos (%)" column correctly
                # The column should represent ADDITIONAL encargos only (beyond the standard CLT charges)
                encargos_valor = float(funcionario.get('Encargos (%)', 0))
                
                # Always treat as additional percentage, but cap at reasonable values
                if encargos_valor > 50:
                    # If someone put a high value like 95%, they probably meant 0% additional
                    # Show a warning and use 0% additional
                    encargos_adicionais = 0.0
                    print(f"Warning: High encargos value {encargos_valor}% for {cargo} interpreted as 0% additional")
                else:
                    # This is additional percentage on top of standard ~58% CLT charges
                    encargos_adicionais = encargos_valor
                
                # Calculate cost per employee with corrected encargos
                custo_individual = self.calculate_employee_cost(salario_base, encargos_adicionais)
                
                # Multiply by quantity
                custo_total_cargo = custo_individual['custo_total_mensal'] * quantidade
                salario_total_cargo = salario_base * quantidade
                
                # Accumulate totals
                total_salarios += salario_total_cargo
                total_custos += custo_total_cargo
                
                # Calculate component totals
                encargos_sociais_cargo = (
                    custo_individual['inss_empresa'] +
                    custo_individual['fgts'] +
                    custo_individual['salario_educacao'] +
                    custo_individual['sistema_s'] +
                    custo_individual['acidente_trabalho'] +
                    custo_individual['sebrae']
                ) * quantidade
                
                provisoes_cargo = (
                    custo_individual['ferias'] +
                    custo_individual['decimo_terceiro']
                ) * quantidade
                
                total_encargos_sociais += encargos_sociais_cargo
                total_provisoes += provisoes_cargo
                
                funcionarios_detalhes.append({
                    'cargo': cargo,
                    'quantidade': quantidade,
                    'salario_base': salario_base,
                    'custo_individual': custo_individual['custo_total_mensal'],
                    'custo_total_cargo': custo_total_cargo,
                    'percentual_encargos': custo_individual['percentual_encargos']
                })
            
            return {
                "total_salarios": total_salarios,
                "encargos_sociais": total_encargos_sociais,
                "provisoes": total_provisoes,
                "custo_total_mensal": total_custos,
                "percentual_medio_encargos": ((total_custos - total_salarios) / total_salarios * 100) if total_salarios > 0 else 0,
                "funcionarios_detalhes": funcionarios_detalhes,
                "total_funcionarios": sum([f['quantidade'] for f in funcionarios_detalhes])
            }
            
        except Exception as e:
            return {
                "total_salarios": 0,
                "encargos_sociais": 0,
                "provisoes": 0,
                "custo_total_mensal": 0,
                "percentual_medio_encargos": 0,
                "funcionarios_detalhes": [],
                "total_funcionarios": 0,
                "error": str(e)
            }
    
    def calculate_mei_costs(self, atividade="comercio"):
        """Calculate MEI (Microempreendedor Individual) costs"""
        # MEI values for 2025
        if atividade == "comercio":
            mei_mensal = 76.90  # R$ 75.90 INSS + R$ 1.00 ICMS
        elif atividade == "servicos":
            mei_mensal = 80.90  # R$ 75.90 INSS + R$ 5.00 ISS
        else:
            mei_mensal = 81.90  # R$ 75.90 INSS + R$ 1.00 ICMS + R$ 5.00 ISS
        
        return {
            "regime": "MEI",
            "valor_mensal": mei_mensal,
            "valor_anual": mei_mensal * 12,
            "limite_receita_anual": 81000.00,
            "limite_funcionarios": 1
        }
    
    def generate_labor_report(self, df_funcionarios):
        """Generate comprehensive labor cost report"""
        costs = self.calculate_total_labor_costs(df_funcionarios)
        
        report = f"""
RELATÓRIO DE CUSTOS TRABALHISTAS

==== RESUMO EXECUTIVO ====
Total de Funcionários: {costs['total_funcionarios']}
Custo Total com Salários: R$ {costs['total_salarios']:,.2f}
Encargos Sociais: R$ {costs['encargos_sociais']:,.2f}
Provisões: R$ {costs['provisoes']:,.2f}
Custo Total Mensal: R$ {costs['custo_total_mensal']:,.2f}
Percentual Médio de Encargos: {costs['percentual_medio_encargos']:.1f}%

==== DETALHAMENTO POR CARGO ====
"""
        
        for func in costs['funcionarios_detalhes']:
            report += f"""
{func['cargo']}:
- Quantidade: {func['quantidade']} funcionário(s)
- Salário Base: R$ {func['salario_base']:,.2f}
- Custo Individual: R$ {func['custo_individual']:,.2f}
- Custo Total do Cargo: R$ {func['custo_total_cargo']:,.2f}
- Percentual de Encargos: {func['percentual_encargos']:.1f}%
"""
        
        return report
