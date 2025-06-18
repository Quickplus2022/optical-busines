"""
Sistema de Sugestão de Preços para Lentes Oftálmicas
Baseado em dados de mercado e estrutura de custos
"""

import pandas as pd

class LensPricingSuggestions:
    """Sistema de sugestão de preços para lentes com base no mercado"""
    
    def __init__(self):
        # Custos base dos fornecedores (médias de mercado)
        self.custos_base = {
            'simples': {
                'basico': 35.0,
                'intermediario': 50.0, 
                'premium': 75.0
            },
            'bifocal': {
                'basico': 65.0,
                'intermediario': 90.0,
                'premium': 130.0
            },
            'multifocal': {
                'basico': 180.0,
                'intermediario': 280.0,
                'premium': 450.0
            }
        }
        
        # Custos dos tratamentos
        self.custos_tratamentos = {
            'anti_reflexo': {
                'basico': 15.0,
                'intermediario': 25.0,
                'premium': 40.0
            },
            'blue_light': {
                'basico': 20.0,
                'intermediario': 35.0,
                'premium': 55.0
            },
            'fotosensivel': {
                'basico': 45.0,
                'intermediario': 75.0,
                'premium': 120.0
            }
        }
        
        # Preços de mercado de referência (pesquisa 2024)
        self.precos_mercado = {
            'simples': {
                'basico': {'min': 120, 'medio': 180, 'max': 250},
                'intermediario': {'min': 200, 'medio': 280, 'max': 380},
                'premium': {'min': 350, 'medio': 480, 'max': 650}
            },
            'bifocal': {
                'basico': {'min': 250, 'medio': 350, 'max': 450},
                'intermediario': {'min': 400, 'medio': 550, 'max': 700},
                'premium': {'min': 650, 'medio': 850, 'max': 1200}
            },
            'multifocal': {
                'basico': {'min': 600, 'medio': 800, 'max': 1000},
                'intermediario': {'min': 900, 'medio': 1200, 'max': 1500},
                'premium': {'min': 1400, 'medio': 1800, 'max': 2500}
            }
        }
        
        # Margens recomendadas por linha
        self.margens_recomendadas = {
            'basico': {'min': 55, 'recomendada': 65, 'max': 75},
            'intermediario': {'min': 60, 'recomendada': 70, 'max': 80},
            'premium': {'min': 65, 'recomendada': 75, 'max': 85}
        }
    
    def calcular_custo_total(self, tipo_lente, linha, tratamentos=[]):
        """Calcula custo total da lente com tratamentos"""
        custo_base = self.custos_base[tipo_lente][linha]
        custo_tratamentos = 0
        
        for tratamento in tratamentos:
            if tratamento in self.custos_tratamentos:
                custo_tratamentos += self.custos_tratamentos[tratamento][linha]
        
        return custo_base + custo_tratamentos
    
    def sugerir_precos(self, tipo_lente, linha, tratamentos=[], estrategia='competitiva'):
        """Sugere preços baseado na estratégia escolhida"""
        custo_total = self.calcular_custo_total(tipo_lente, linha, tratamentos)
        
        # Margem baseada na estratégia
        if estrategia == 'conservadora':
            margem_pct = self.margens_recomendadas[linha]['min']
        elif estrategia == 'competitiva':
            margem_pct = self.margens_recomendadas[linha]['recomendada']
        else:  # agressiva
            margem_pct = self.margens_recomendadas[linha]['max']
        
        # Preço calculado pela margem
        preco_margem = custo_total / (1 - margem_pct/100)
        
        # Preços de mercado de referência
        mercado = self.precos_mercado[tipo_lente][linha]
        preco_mercado_min = mercado['min']
        preco_mercado_medio = mercado['medio']
        preco_mercado_max = mercado['max']
        
        # Ajuste do preço conforme mercado
        if estrategia == 'conservadora':
            preco_sugerido = min(preco_margem, preco_mercado_medio)
        elif estrategia == 'competitiva':
            preco_sugerido = preco_margem
            if preco_sugerido < preco_mercado_min:
                preco_sugerido = preco_mercado_min
            elif preco_sugerido > preco_mercado_max:
                preco_sugerido = preco_mercado_max
        else:  # agressiva
            preco_sugerido = min(preco_margem, preco_mercado_max)
        
        # Cálculos finais
        margem_real = ((preco_sugerido - custo_total) / preco_sugerido) * 100
        markup = preco_sugerido / custo_total
        
        return {
            'custo_total': custo_total,
            'preco_sugerido': round(preco_sugerido, 2),
            'margem_percentual': round(margem_real, 1),
            'markup': round(markup, 2),
            'referencia_mercado': {
                'minimo': preco_mercado_min,
                'medio': preco_mercado_medio,
                'maximo': preco_mercado_max
            },
            'posicionamento': self._avaliar_posicionamento(preco_sugerido, mercado)
        }
    
    def _avaliar_posicionamento(self, preco, mercado):
        """Avalia posicionamento do preço no mercado"""
        if preco <= mercado['min']:
            return 'Entrada/Econômico'
        elif preco <= mercado['medio']:
            return 'Competitivo'
        elif preco <= mercado['max']:
            return 'Premium'
        else:
            return 'Super Premium'
    
    def gerar_tabela_completa(self, estrategia='competitiva'):
        """Gera tabela completa de preços para todas as combinações"""
        resultados = []
        
        tipos_lente = ['simples', 'bifocal', 'multifocal']
        linhas = ['basico', 'intermediario', 'premium']
        combinacoes_tratamentos = [
            [],
            ['anti_reflexo'],
            ['blue_light'],
            ['fotosensivel'],
            ['anti_reflexo', 'blue_light'],
            ['anti_reflexo', 'fotosensivel'],
            ['blue_light', 'fotosensivel'],
            ['anti_reflexo', 'blue_light', 'fotosensivel']
        ]
        
        for tipo in tipos_lente:
            for linha in linhas:
                for tratamentos in combinacoes_tratamentos:
                    resultado = self.sugerir_precos(tipo, linha, tratamentos, estrategia)
                    
                    tratamentos_str = ' + '.join([t.replace('_', ' ').title() for t in tratamentos]) if tratamentos else 'Sem tratamento'
                    
                    resultados.append({
                        'Tipo Lente': tipo.title(),
                        'Linha': linha.title(),
                        'Tratamentos': tratamentos_str,
                        'Custo Total': resultado['custo_total'],
                        'Preço Sugerido': resultado['preco_sugerido'],
                        'Margem (%)': resultado['margem_percentual'],
                        'Markup': resultado['markup'],
                        'Posicionamento': resultado['posicionamento'],
                        'Mercado Min': resultado['referencia_mercado']['minimo'],
                        'Mercado Médio': resultado['referencia_mercado']['medio'],
                        'Mercado Max': resultado['referencia_mercado']['maximo']
                    })
        
        return pd.DataFrame(resultados)
    
    def calcular_mix_otimo(self, vendas_mensais_esperadas=100):
        """Sugere mix de produtos otimizado para lucratividade"""
        # Mix recomendado baseado em lucratividade e demanda de mercado
        mix_recomendado = {
            'simples': {
                'basico': 0.25,      # 25% das vendas
                'intermediario': 0.15, # 15% das vendas  
                'premium': 0.05       # 5% das vendas
            },
            'bifocal': {
                'basico': 0.15,      # 15% das vendas
                'intermediario': 0.10, # 10% das vendas
                'premium': 0.05       # 5% das vendas
            },
            'multifocal': {
                'basico': 0.10,      # 10% das vendas
                'intermediario': 0.07, # 7% das vendas
                'premium': 0.03       # 3% das vendas
            }
        }
        
        mix_resultado = []
        receita_total = 0
        lucro_total = 0
        
        for tipo in mix_recomendado:
            for linha in mix_recomendado[tipo]:
                percentual = mix_recomendado[tipo][linha]
                qtd_vendas = int(vendas_mensais_esperadas * percentual)
                
                if qtd_vendas > 0:
                    # Calcular com tratamento médio (anti-reflexo)
                    resultado = self.sugerir_precos(tipo, linha, ['anti_reflexo'])
                    
                    receita_produto = qtd_vendas * resultado['preco_sugerido']
                    custo_produto = qtd_vendas * resultado['custo_total']
                    lucro_produto = receita_produto - custo_produto
                    
                    receita_total += receita_produto
                    lucro_total += lucro_produto
                    
                    mix_resultado.append({
                        'Produto': f"{tipo.title()} {linha.title()}",
                        'Participação (%)': percentual * 100,
                        'Qtd Vendas/Mês': qtd_vendas,
                        'Preço Unitário': resultado['preco_sugerido'],
                        'Custo Unitário': resultado['custo_total'],
                        'Receita Mensal': receita_produto,
                        'Lucro Mensal': lucro_produto,
                        'Margem (%)': resultado['margem_percentual']
                    })
        
        margem_total = (lucro_total / receita_total * 100) if receita_total > 0 else 0
        
        return {
            'mix_detalhado': pd.DataFrame(mix_resultado),
            'resumo': {
                'receita_total_mensal': receita_total,
                'lucro_total_mensal': lucro_total,
                'margem_total_percentual': margem_total,
                'ticket_medio': receita_total / vendas_mensais_esperadas if vendas_mensais_esperadas > 0 else 0
            }
        }