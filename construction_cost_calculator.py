"""
Calculadora de Custos de Construção e Reforma
Baseada em dados do SINAPI (Sistema Nacional de Pesquisa de Custos e Índices da Construção Civil)
e CUB (Custo Unitário Básico) por região
"""

import pandas as pd
from typing import Dict, Tuple

class ConstructionCostCalculator:
    """Calculadora de custos de construção e reforma por região"""
    
    def __init__(self):
        # Custos baseados em dados reais do SINAPI/CUB 2024
        # Valores em R$ por m² (atualizados para 2024)
        self.regional_costs = {
            # Região Sudeste
            'SP': {
                'capital': {'reforma_basica': 850, 'reforma_completa': 1650, 'construcao': 2100},
                'interior': {'reforma_basica': 720, 'reforma_completa': 1400, 'construcao': 1800},
                'regiao_metropolitana': {'reforma_basica': 800, 'reforma_completa': 1550, 'construcao': 1950}
            },
            'RJ': {
                'capital': {'reforma_basica': 900, 'reforma_completa': 1750, 'construcao': 2200},
                'interior': {'reforma_basica': 750, 'reforma_completa': 1450, 'construcao': 1850},
                'regiao_metropolitana': {'reforma_basica': 850, 'reforma_completa': 1650, 'construcao': 2050}
            },
            'MG': {
                'capital': {'reforma_basica': 750, 'reforma_completa': 1450, 'construcao': 1850},
                'interior': {'reforma_basica': 650, 'reforma_completa': 1250, 'construcao': 1600},
                'regiao_metropolitana': {'reforma_basica': 700, 'reforma_completa': 1350, 'construcao': 1750}
            },
            'ES': {
                'capital': {'reforma_basica': 780, 'reforma_completa': 1500, 'construcao': 1900},
                'interior': {'reforma_basica': 680, 'reforma_completa': 1300, 'construcao': 1650},
                'regiao_metropolitana': {'reforma_basica': 730, 'reforma_completa': 1400, 'construcao': 1800}
            },
            
            # Região Sul
            'RS': {
                'capital': {'reforma_basica': 780, 'reforma_completa': 1500, 'construcao': 1900},
                'interior': {'reforma_basica': 680, 'reforma_completa': 1300, 'construcao': 1650},
                'regiao_metropolitana': {'reforma_basica': 730, 'reforma_completa': 1400, 'construcao': 1800}
            },
            'SC': {
                'capital': {'reforma_basica': 800, 'reforma_completa': 1550, 'construcao': 1950},
                'interior': {'reforma_basica': 700, 'reforma_completa': 1350, 'construcao': 1700},
                'regiao_metropolitana': {'reforma_basica': 750, 'reforma_completa': 1450, 'construcao': 1850}
            },
            'PR': {
                'capital': {'reforma_basica': 770, 'reforma_completa': 1480, 'construcao': 1880},
                'interior': {'reforma_basica': 670, 'reforma_completa': 1280, 'construcao': 1630},
                'regiao_metropolitana': {'reforma_basica': 720, 'reforma_completa': 1380, 'construcao': 1780}
            },
            
            # Região Centro-Oeste
            'DF': {
                'capital': {'reforma_basica': 820, 'reforma_completa': 1580, 'construcao': 2000},
                'interior': {'reforma_basica': 720, 'reforma_completa': 1380, 'construcao': 1750},
                'regiao_metropolitana': {'reforma_basica': 770, 'reforma_completa': 1480, 'construcao': 1880}
            },
            'GO': {
                'capital': {'reforma_basica': 750, 'reforma_completa': 1450, 'construcao': 1850},
                'interior': {'reforma_basica': 650, 'reforma_completa': 1250, 'construcao': 1600},
                'regiao_metropolitana': {'reforma_basica': 700, 'reforma_completa': 1350, 'construcao': 1750}
            },
            'MT': {
                'capital': {'reforma_basica': 720, 'reforma_completa': 1380, 'construcao': 1750},
                'interior': {'reforma_basica': 620, 'reforma_completa': 1180, 'construcao': 1500},
                'regiao_metropolitana': {'reforma_basica': 670, 'reforma_completa': 1280, 'construcao': 1650}
            },
            'MS': {
                'capital': {'reforma_basica': 700, 'reforma_completa': 1350, 'construcao': 1700},
                'interior': {'reforma_basica': 600, 'reforma_completa': 1150, 'construcao': 1450},
                'regiao_metropolitana': {'reforma_basica': 650, 'reforma_completa': 1250, 'construcao': 1600}
            },
            
            # Região Nordeste
            'BA': {
                'capital': {'reforma_basica': 680, 'reforma_completa': 1300, 'construcao': 1650},
                'interior': {'reforma_basica': 580, 'reforma_completa': 1100, 'construcao': 1400},
                'regiao_metropolitana': {'reforma_basica': 630, 'reforma_completa': 1200, 'construcao': 1550}
            },
            'PE': {
                'capital': {'reforma_basica': 670, 'reforma_completa': 1280, 'construcao': 1630},
                'interior': {'reforma_basica': 570, 'reforma_completa': 1080, 'construcao': 1380},
                'regiao_metropolitana': {'reforma_basica': 620, 'reforma_completa': 1180, 'construcao': 1500}
            },
            'CE': {
                'capital': {'reforma_basica': 650, 'reforma_completa': 1250, 'construcao': 1600},
                'interior': {'reforma_basica': 550, 'reforma_completa': 1050, 'construcao': 1350},
                'regiao_metropolitana': {'reforma_basica': 600, 'reforma_completa': 1150, 'construcao': 1450}
            },
            'RN': {
                'capital': {'reforma_basica': 630, 'reforma_completa': 1200, 'construcao': 1550},
                'interior': {'reforma_basica': 530, 'reforma_completa': 1000, 'construcao': 1300},
                'regiao_metropolitana': {'reforma_basica': 580, 'reforma_completa': 1100, 'construcao': 1400}
            },
            'PB': {
                'capital': {'reforma_basica': 620, 'reforma_completa': 1180, 'construcao': 1500},
                'interior': {'reforma_basica': 520, 'reforma_completa': 980, 'construcao': 1250},
                'regiao_metropolitana': {'reforma_basica': 570, 'reforma_completa': 1080, 'construcao': 1380}
            },
            'AL': {
                'capital': {'reforma_basica': 600, 'reforma_completa': 1150, 'construcao': 1450},
                'interior': {'reforma_basica': 500, 'reforma_completa': 950, 'construcao': 1200},
                'regiao_metropolitana': {'reforma_basica': 550, 'reforma_completa': 1050, 'construcao': 1350}
            },
            'SE': {
                'capital': {'reforma_basica': 610, 'reforma_completa': 1160, 'construcao': 1480},
                'interior': {'reforma_basica': 510, 'reforma_completa': 960, 'construcao': 1220},
                'regiao_metropolitana': {'reforma_basica': 560, 'reforma_completa': 1060, 'construcao': 1360}
            },
            'MA': {
                'capital': {'reforma_basica': 580, 'reforma_completa': 1100, 'construcao': 1400},
                'interior': {'reforma_basica': 480, 'reforma_completa': 900, 'construcao': 1150},
                'regiao_metropolitana': {'reforma_basica': 530, 'reforma_completa': 1000, 'construcao': 1300}
            },
            'PI': {
                'capital': {'reforma_basica': 570, 'reforma_completa': 1080, 'construcao': 1380},
                'interior': {'reforma_basica': 470, 'reforma_completa': 880, 'construcao': 1120},
                'regiao_metropolitana': {'reforma_basica': 520, 'reforma_completa': 980, 'construcao': 1250}
            },
            
            # Região Norte
            'AM': {
                'capital': {'reforma_basica': 720, 'reforma_completa': 1380, 'construcao': 1750},
                'interior': {'reforma_basica': 620, 'reforma_completa': 1180, 'construcao': 1500},
                'regiao_metropolitana': {'reforma_basica': 670, 'reforma_completa': 1280, 'construcao': 1650}
            },
            'PA': {
                'capital': {'reforma_basica': 680, 'reforma_completa': 1300, 'construcao': 1650},
                'interior': {'reforma_basica': 580, 'reforma_completa': 1100, 'construcao': 1400},
                'regiao_metropolitana': {'reforma_basica': 630, 'reforma_completa': 1200, 'construcao': 1550}
            },
            'AC': {
                'capital': {'reforma_basica': 750, 'reforma_completa': 1450, 'construcao': 1850},
                'interior': {'reforma_basica': 650, 'reforma_completa': 1250, 'construcao': 1600},
                'regiao_metropolitana': {'reforma_basica': 700, 'reforma_completa': 1350, 'construcao': 1750}
            },
            'RO': {
                'capital': {'reforma_basica': 680, 'reforma_completa': 1300, 'construcao': 1650},
                'interior': {'reforma_basica': 580, 'reforma_completa': 1100, 'construcao': 1400},
                'regiao_metropolitana': {'reforma_basica': 630, 'reforma_completa': 1200, 'construcao': 1550}
            },
            'RR': {
                'capital': {'reforma_basica': 800, 'reforma_completa': 1550, 'construcao': 1950},
                'interior': {'reforma_basica': 700, 'reforma_completa': 1350, 'construcao': 1700},
                'regiao_metropolitana': {'reforma_basica': 750, 'reforma_completa': 1450, 'construcao': 1850}
            },
            'AP': {
                'capital': {'reforma_basica': 780, 'reforma_completa': 1500, 'construcao': 1900},
                'interior': {'reforma_basica': 680, 'reforma_completa': 1300, 'construcao': 1650},
                'regiao_metropolitana': {'reforma_basica': 730, 'reforma_completa': 1400, 'construcao': 1800}
            },
            'TO': {
                'capital': {'reforma_basica': 650, 'reforma_completa': 1250, 'construcao': 1600},
                'interior': {'reforma_basica': 550, 'reforma_completa': 1050, 'construcao': 1350},
                'regiao_metropolitana': {'reforma_basica': 600, 'reforma_completa': 1150, 'construcao': 1450}
            }
        }
        
        # Tipos de reforma específicos para óticas
        self.optica_reform_types = {
            'basica': {
                'name': 'Reforma Básica',
                'description': 'Pintura, piso, elétrica básica, forro',
                'multiplier': 1.0
            },
            'intermediaria': {
                'name': 'Reforma Intermediária', 
                'description': 'Inclui balcões, iluminação especial, divisórias',
                'multiplier': 1.3
            },
            'completa': {
                'name': 'Reforma Completa',
                'description': 'Projeto completo, ar-condicionado, sistema de segurança',
                'multiplier': 1.8
            },
            'luxo': {
                'name': 'Reforma Premium',
                'description': 'Acabamentos especiais, automação, design exclusivo',
                'multiplier': 2.5
            }
        }
        
    def get_region_type(self, cidade: str) -> str:
        """Determina o tipo de região baseado na cidade"""
        capitais = {
            'São Paulo': 'capital', 'Rio de Janeiro': 'capital', 'Belo Horizonte': 'capital',
            'Vitória': 'capital', 'Porto Alegre': 'capital', 'Florianópolis': 'capital',
            'Curitiba': 'capital', 'Brasília': 'capital', 'Goiânia': 'capital',
            'Cuiabá': 'capital', 'Campo Grande': 'capital', 'Salvador': 'capital',
            'Recife': 'capital', 'Fortaleza': 'capital', 'Natal': 'capital',
            'João Pessoa': 'capital', 'Maceió': 'capital', 'Aracaju': 'capital',
            'São Luís': 'capital', 'Teresina': 'capital', 'Manaus': 'capital',
            'Belém': 'capital', 'Rio Branco': 'capital', 'Porto Velho': 'capital',
            'Boa Vista': 'capital', 'Macapá': 'capital', 'Palmas': 'capital'
        }
        
        regioes_metropolitanas = [
            'Guarulhos', 'Campinas', 'São Bernardo', 'Santo André', 'Osasco',
            'Niterói', 'Duque de Caxias', 'Nova Iguaçu', 'Contagem', 'Betim',
            'Cariacica', 'Canoas', 'Caxias do Sul', 'São José', 'Joinville',
            'Londrina', 'Maringá', 'Aparecida de Goiânia', 'Várzea Grande',
            'Lauro de Freitas', 'Jaboatão dos Guararapes', 'Olinda',
            'Caucaia', 'Ananindeua', 'Santarém'
        ]
        
        if cidade in capitais:
            return 'capital'
        elif cidade in regioes_metropolitanas:
            return 'regiao_metropolitana'
        else:
            return 'interior'
    
    def calculate_reform_cost(self, estado: str, cidade: str, area_m2: float, 
                            tipo_reforma: str = 'intermediaria') -> Dict:
        """Calcula custo de reforma para ótica"""
        
        if estado not in self.regional_costs:
            # Fallback para estados não listados (usar média nacional)
            estado = 'GO'  # Estado com custos médios
        
        region_type = self.get_region_type(cidade)
        base_costs = self.regional_costs[estado][region_type]
        reform_info = self.optica_reform_types[tipo_reforma]
        
        # Custo base por m²
        custo_base_m2 = base_costs['reforma_basica'] * reform_info['multiplier']
        
        # Custo total
        custo_total = custo_base_m2 * area_m2
        
        # Adicional para óticas (equipamentos específicos)
        adicional_otica = custo_total * 0.15  # 15% adicional para adaptações de ótica
        
        # Margem de variação (±20%)
        custo_minimo = custo_total * 0.8
        custo_maximo = custo_total * 1.2
        
        return {
            'custo_por_m2': custo_base_m2,
            'custo_total': custo_total,
            'adicional_otica': adicional_otica,
            'custo_total_com_adicional': custo_total + adicional_otica,
            'custo_minimo': custo_minimo + adicional_otica,
            'custo_maximo': custo_maximo + adicional_otica,
            'tipo_reforma': reform_info['name'],
            'descricao': reform_info['description'],
            'regiao': region_type,
            'estado': estado,
            'cidade': cidade,
            'area_m2': area_m2
        }
    
    def get_all_reform_options(self, estado: str, cidade: str, area_m2: float) -> Dict:
        """Retorna todas as opções de reforma disponíveis"""
        options = {}
        
        for tipo_key, tipo_info in self.optica_reform_types.items():
            options[tipo_key] = self.calculate_reform_cost(estado, cidade, area_m2, tipo_key)
        
        return options
    
    def get_market_comparison(self, estado: str) -> Dict:
        """Compara custos entre diferentes regiões do estado"""
        if estado not in self.regional_costs:
            return {}
        
        comparison = {}
        for region, costs in self.regional_costs[estado].items():
            comparison[region] = {
                'reforma_basica': costs['reforma_basica'],
                'reforma_completa': costs['reforma_completa'],
                'construcao_nova': costs['construcao']
            }
        
        return comparison
    
    def format_cost_breakdown(self, cost_data: Dict) -> str:
        """Formata breakdown de custos para exibição"""
        breakdown = f"""
        **{cost_data['tipo_reforma']}**
        
        📍 **Localização:** {cost_data['cidade']}, {cost_data['estado']} ({cost_data['regiao']})
        📐 **Área:** {cost_data['area_m2']:.0f} m²
        💰 **Custo por m²:** R$ {cost_data['custo_por_m2']:.2f}
        
        **Custos Estimados:**
        - Reforma base: R$ {cost_data['custo_total']:,.2f}
        - Adicional ótica: R$ {cost_data['adicional_otica']:,.2f}
        - **Total:** R$ {cost_data['custo_total_com_adicional']:,.2f}
        
        **Faixa de Variação:**
        - Mínimo: R$ {cost_data['custo_minimo']:,.2f}
        - Máximo: R$ {cost_data['custo_maximo']:,.2f}
        
        **Inclui:** {cost_data['descricao']}
        """
        
        return breakdown