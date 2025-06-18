import streamlit as st
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional

class ProductCostCalculator:
    """Calculator for optical products pricing and cost management"""
    
    def __init__(self):
        self.fornecedores_lentes = {
            "ATAK": self._load_atak_prices(),
            "BRASIL LENTES": self._load_brasil_lentes_prices(),
            "GOLD": self._load_gold_prices(),
            "DSMHD": self._load_dsmhd_prices()
        }
        
        # Default frame cost
        self.custo_armacao_padrao = 70.00
        
        # Markup padrões
        self.markup_padrao = {
            "lentes": 2.5,  # 150% markup
            "armacoes": 3.0,  # 200% markup
            "servicos": 4.0   # 300% markup
        }
    
    def _load_atak_prices(self) -> Dict:
        """Load ATAK supplier lens prices"""
        return {
            "LT CR-39 INCOLOR 1.49": {
                "base": "Esf. -6,00 a +6,00",
                "custo": 12.00,
                "tipo": "visao_simples"
            },
            "LT CR-39 INCOLOR CIL 1.49": {
                "base": "Esf. -4,00 a +4,00 / Cil. -0,25 a -2,00",
                "custo": 15.00,
                "tipo": "visao_simples"
            },
            "LT CR-39 ANTIRREFLEXO 1.56": {
                "base": "Esf. -6,00 a +4,00 / Cil. -0,25 a -2,00",
                "custo": 12.00,
                "tipo": "visao_simples"
            },
            "LT CR-39 FOTO ANTIRREFLEXO 1.56": {
                "base": "Esf. -4,00 a +4,00 / Cil. -0,25 a -2,00",
                "custo": 30.00,
                "tipo": "visao_simples"
            },
            "LT CR-39 BLUE CUT ANTIRREFLEXO 1.56": {
                "base": "Esf. -6,00 a +4,00 / Cil. -0,25 a -2,00",
                "custo": 35.00,
                "tipo": "visao_simples"
            },
            "LT POLI INCOLOR 1.59": {
                "base": "Esf. -4,00 a +4,00 / Cil. -0,25 a -2,00",
                "custo": 23.00,
                "tipo": "visao_simples"
            },
            "LT POLI ANTIRREFLEXO 1.59": {
                "base": "Esf. -5,00 a +4,00 / Cil. -0,25 a -2,00",
                "custo": 30.00,
                "tipo": "visao_simples"
            },
            "LT POLI BLUE CUT ANTIRREFLEXO 1.59": {
                "base": "Esf. -6,00 a +4,00 / Cil. -0,25 a -2,00",
                "custo": 110.00,
                "tipo": "visao_simples"
            },
            "LT ALTO ÍNDICE ANTIRREFLEXO 1.61": {
                "base": "Esf. -6,25 a -10,00 / Cil. -2,00",
                "custo": 70.00,
                "tipo": "visao_simples"
            },
            "LT ALTO ÍNDICE ANTIRREFLEXO 1.67": {
                "base": "Esf. -10,25 a -12,00 / Cil. -2,00",
                "custo": 150.00,
                "tipo": "visao_simples"
            },
            "LT TRANSITIONS ANTIRREFLEXO 1.50": {
                "base": "Esf. -2,00 a +2,00 / Cil. -0,25 a -2,00",
                "custo": 185.00,
                "tipo": "visao_simples"
            }
        }
    
    def _load_brasil_lentes_prices(self) -> Dict:
        """Load BRASIL LENTES supplier prices"""
        return {
            "LP RESINA INCOLOR A.R 1.56": {
                "base": "Esf. +4,00 a -6,00 / Cil. -2,00",
                "custo": 12.00,
                "tipo": "visao_simples"
            },
            "LP RESINA ANTI BLUE A.R 1.56": {
                "base": "Esf. +6,00 a -8,00 / Cil. -2,00",
                "custo": 30.00,
                "tipo": "visao_simples"
            },
            "LP RESINA FOTO A.R 1.56": {
                "base": "Esf. +4,00 a -6,00 / Cil. -2,00",
                "custo": 25.00,
                "tipo": "visao_simples"
            },
            "LP RESINA FOTO AR ANTI-BLUE 1.56": {
                "base": "Esf. +6,00 a -6,00 / Cil. -2,00",
                "custo": 85.00,
                "tipo": "visao_simples"
            },
            "LP POLY INCOLOR A.R 1.59": {
                "base": "Esf. +6,00 a -6,00 / Cil. -2,00",
                "custo": 30.00,
                "tipo": "visao_simples"
            },
            "LP POLY ANTI-BLUE A.R 1.59": {
                "base": "Esf. +6,00 a -6,00 / Cil. -2,00",
                "custo": 90.00,
                "tipo": "visao_simples"
            },
            "LP POLY FOTO A.R 1.59": {
                "base": "Esf. +4,00 a -4,00 / Cil. -2,00",
                "custo": 140.00,
                "tipo": "visao_simples"
            },
            "LP RESINA ALTO ÍNDICE A.R 1.61": {
                "base": "Esf. +4,00 a -10,00 / Cil. -2,00",
                "custo": 60.00,
                "tipo": "visao_simples"
            },
            "LP RESINA ALTO ÍNDICE A.R 1.67": {
                "base": "Esf. -3,00 a -10,00 / Cil. -2,00",
                "custo": 280.00,
                "tipo": "visao_simples"
            },
            "LP MULTIFOCAL RESINA A.R 1.56": {
                "base": "Esf. -2,00 a +3,00 / Add. +1,00 a +3,00",
                "custo": 45.00,
                "tipo": "multifocal"
            },
            "LP MULTIFOCAL POLY ANTI-BLUE 1.59": {
                "base": "Esf. -2,00 a +3,00 / Add. +1,00 a +3,00",
                "custo": 150.00,
                "tipo": "multifocal"
            }
        }
    
    def _load_gold_prices(self) -> Dict:
        """Load GOLD supplier prices"""
        return {
            "GOLD INCOLOR 1.49": {
                "base": "Esf. -6,00 a +6,00 / Cil. -0,00 a -2,00",
                "custo": 10.00,
                "tipo": "visao_simples"
            },
            "GOLD AR 1.56": {
                "base": "Esf. -6,00 a +6,00 / Cil. -0,00 a -2,00",
                "custo": 12.00,
                "tipo": "visao_simples"
            },
            "GOLD PRO SENSE FOTO 1.56": {
                "base": "Esf. -6,00 a +6,00 / Cil. -0,00 a -2,00",
                "custo": 30.00,
                "tipo": "visao_simples"
            },
            "GOLD POLI AR 1.59": {
                "base": "Esf. -6,00 a +6,00 / Cil. -0,00 a -2,00",
                "custo": 28.00,
                "tipo": "visao_simples"
            },
            "GOLD ALTO ÍNDICE AR 1.67": {
                "base": "Esf. -6,00 a -15,00 / Cil. -0,00 a -0,00",
                "custo": 120.00,
                "tipo": "visao_simples"
            },
            "GOLD FOTO AR 1.67": {
                "base": "Esf. -6,00 a -15,00 / Cil. -0,00 a -0,00",
                "custo": 200.00,
                "tipo": "visao_simples"
            },
            "GOLD BLUE 1.56": {
                "base": "Base 0.50/2.00/4.00/6.00/8.00",
                "custo": 80.00,
                "tipo": "bloco"
            },
            "GOLD PROGRESSIVO AR 1.56": {
                "base": "Esf. -2,00 a +3,00 / Add. 1,00 a 3,00",
                "custo": 45.00,
                "tipo": "multifocal"
            },
            "GOLD PROGRESSIVO FOTO AR 1.56": {
                "base": "Esf. -2,00 a +3,00 / Add. 1,00 a 3,00",
                "custo": 55.00,
                "tipo": "multifocal"
            }
        }
    
    def _load_dsmhd_prices(self) -> Dict:
        """Load DSMHD supplier prices (estimated based on market)"""
        return {
            "DSMHD RESINA INCOLOR 1.56": {
                "base": "Esf. -6,00 a +6,00 / Cil. -2,00",
                "custo": 15.00,
                "tipo": "visao_simples"
            },
            "DSMHD RESINA AR 1.56": {
                "base": "Esf. -6,00 a +6,00 / Cil. -2,00",
                "custo": 18.00,
                "tipo": "visao_simples"
            },
            "DSMHD FOTO AR 1.56": {
                "base": "Esf. -4,00 a +4,00 / Cil. -2,00",
                "custo": 35.00,
                "tipo": "visao_simples"
            },
            "DSMHD POLI AR 1.59": {
                "base": "Esf. -6,00 a +6,00 / Cil. -2,00",
                "custo": 32.00,
                "tipo": "visao_simples"
            }
        }
    
    def get_fornecedor_lentes(self, fornecedor: str) -> Dict:
        """Get lens prices for specific supplier"""
        return self.fornecedores_lentes.get(fornecedor, {})
    
    def calculate_lens_cost(self, fornecedor: str, tipo_lente: str, quantidade: int = 1) -> Dict:
        """Calculate lens cost from supplier"""
        fornecedor_data = self.get_fornecedor_lentes(fornecedor)
        
        if tipo_lente not in fornecedor_data:
            return {
                "custo_unitario": 0.0,
                "custo_total": 0.0,
                "fornecedor": fornecedor,
                "tipo_lente": tipo_lente,
                "erro": f"Lente não encontrada no fornecedor {fornecedor}"
            }
        
        lente_data = fornecedor_data[tipo_lente]
        custo_unitario = lente_data["custo"]
        custo_total = custo_unitario * quantidade
        
        return {
            "custo_unitario": custo_unitario,
            "custo_total": custo_total,
            "fornecedor": fornecedor,
            "tipo_lente": tipo_lente,
            "base_grau": lente_data["base"],
            "tipo": lente_data["tipo"],
            "quantidade": quantidade
        }
    
    def calculate_frame_cost(self, custo_armacao: float = None, quantidade: int = 1) -> Dict:
        """Calculate frame cost"""
        if custo_armacao is None:
            custo_armacao = self.custo_armacao_padrao
        
        custo_total = custo_armacao * quantidade
        
        return {
            "custo_unitario": custo_armacao,
            "custo_total": custo_total,
            "quantidade": quantidade,
            "descricao": "Armação média"
        }
    
    def calculate_service_cost(self, tipo_servico: str, valor_servico: float, quantidade: int = 1) -> Dict:
        """Calculate service cost"""
        custo_total = valor_servico * quantidade
        
        return {
            "custo_unitario": valor_servico,
            "custo_total": custo_total,
            "tipo_servico": tipo_servico,
            "quantidade": quantidade
        }
    
    def calculate_product_pricing(self, custo_total: float, markup: float = None, tipo_produto: str = "lentes") -> Dict:
        """Calculate product final pricing with markup"""
        if markup is None:
            markup = self.markup_padrao.get(tipo_produto, 2.5)
        
        preco_venda = custo_total * markup
        margem_lucro = preco_venda - custo_total
        percentual_margem = (margem_lucro / preco_venda) * 100 if preco_venda > 0 else 0
        
        return {
            "custo_total": custo_total,
            "markup": markup,
            "preco_venda": preco_venda,
            "margem_lucro": margem_lucro,
            "percentual_margem": percentual_margem,
            "tipo_produto": tipo_produto
        }
    
    def generate_product_mix_analysis(self, vendas_mensais: Dict) -> Dict:
        """Generate product mix analysis"""
        total_vendas = sum(vendas_mensais.values())
        
        if total_vendas == 0:
            return {"erro": "Nenhuma venda informada"}
        
        mix_percentual = {}
        receita_por_categoria = {}
        
        for categoria, quantidade in vendas_mensais.items():
            percentual = (quantidade / total_vendas) * 100
            mix_percentual[categoria] = percentual
        
        return {
            "total_vendas": total_vendas,
            "mix_percentual": mix_percentual,
            "receita_por_categoria": receita_por_categoria
        }
    
    def _load_market_retail_prices(self) -> Dict:
        """Load retail prices from market reference for comparison"""
        return {
            "LT CR-39 ANTIRREFLEXO 1.56": {
                "base": "Esf. -6,00 a +4,00 / Cil. -0,25 a -2,00",
                "preco_venda": 362.00,
                "fornecedor_custo": "ATAK",
                "custo_fornecedor": 12.00
            },
            "LT CR-39 ANTIRREFLEXO EXTENDIDO 1.56": {
                "base": "Esf. -6,00 a +6,00 / Cil. -2,25 a -4,00",
                "preco_venda": 480.00,
                "fornecedor_custo": "ATAK",
                "custo_fornecedor": 30.00
            },
            "LT CR-39 FOTO ANTIRREFLEXO 1.56": {
                "base": "Esf. -4,00 a +4,00 / Cil. -0,25 a -2,00",
                "preco_venda": 590.00,
                "fornecedor_custo": "ATAK",
                "custo_fornecedor": 30.00
            },
            "LT CR-39 BLUE CUT ANTIRREFLEXO 1.56": {
                "base": "Esf. -6,00 a +4,00 / Cil. -0,25 a -2,00",
                "preco_venda": 640.00,
                "fornecedor_custo": "ATAK",
                "custo_fornecedor": 35.00
            },
            "LT POLI ANTIRREFLEXO 1.59": {
                "base": "Esf. -5,00 a +4,00 / Cil. -0,25 a -2,00",
                "preco_venda": 538.00,
                "fornecedor_custo": "ATAK",
                "custo_fornecedor": 30.00
            },
            "LT POLI BLUE CUT ANTIRREFLEXO 1.59": {
                "base": "Esf. -6,00 a +4,00 / Cil. -0,25 a -2,00",
                "preco_venda": 935.00,
                "fornecedor_custo": "ATAK",
                "custo_fornecedor": 110.00
            },
            "LT TRANSITIONS ANTIRREFLEXO 1.50": {
                "base": "Esf. -2,00 a +2,00 / Cil. -0,25 a -2,00",
                "preco_venda": 1850.00,
                "fornecedor_custo": "ATAK",
                "custo_fornecedor": 185.00
            },
            "LT ALTO ÍNDICE ANTIRREFLEXO 1.61": {
                "base": "Esf. -6,25 a -10,00 / Cil. -2,00",
                "preco_venda": 910.00,
                "fornecedor_custo": "ATAK",
                "custo_fornecedor": 70.00
            },
            "LT ALTO ÍNDICE ANTIRREFLEXO 1.67": {
                "base": "Esf. -10,25 a -12,00 / Cil. -2,00",
                "preco_venda": 1280.00,
                "fornecedor_custo": "ATAK",
                "custo_fornecedor": 150.00
            }
        }
    
    def calculate_market_markup(self, custo_fornecedor: float, preco_venda_mercado: float) -> Dict:
        """Calculate markup based on market reference prices"""
        if custo_fornecedor <= 0:
            return {"erro": "Custo deve ser maior que zero"}
        
        markup = preco_venda_mercado / custo_fornecedor
        margem_bruta = preco_venda_mercado - custo_fornecedor
        percentual_margem = (margem_bruta / preco_venda_mercado) * 100
        
        return {
            "custo_fornecedor": custo_fornecedor,
            "preco_venda_mercado": preco_venda_mercado,
            "markup": markup,
            "margem_bruta": margem_bruta,
            "percentual_margem": percentual_margem
        }
    
    def create_default_product_catalog(self) -> pd.DataFrame:
        """Create default product catalog with all suppliers"""
        produtos = []
        
        # Add lens products from all suppliers
        for fornecedor, lentes in self.fornecedores_lentes.items():
            for nome_lente, dados in lentes.items():
                custo = dados["custo"]
                pricing = self.calculate_product_pricing(custo, tipo_produto="lentes")
                
                produtos.append({
                    "Categoria": "Lentes",
                    "Fornecedor": fornecedor,
                    "Produto": nome_lente,
                    "Tipo": dados["tipo"],
                    "Base/Grau": dados["base"],
                    "Custo Unitário": custo,
                    "Markup": self.markup_padrao["lentes"],
                    "Preço Venda": pricing["preco_venda"],
                    "Margem %": pricing["percentual_margem"]
                })
        
        # Add frame products
        custo_armacao = self.custo_armacao_padrao
        pricing_armacao = self.calculate_product_pricing(custo_armacao, tipo_produto="armacoes")
        
        produtos.append({
            "Categoria": "Armações",
            "Fornecedor": "Média Mercado",
            "Produto": "Armação Padrão",
            "Tipo": "armacao",
            "Base/Grau": "Universal",
            "Custo Unitário": custo_armacao,
            "Markup": self.markup_padrao["armacoes"],
            "Preço Venda": pricing_armacao["preco_venda"],
            "Margem %": pricing_armacao["percentual_margem"]
        })
        
        # Add services
        servicos_basicos = [
            ("Exame de Vista", 50.00),
            ("Ajuste de Armação", 15.00),
            ("Limpeza Ultrassônica", 10.00),
            ("Troca de Plaquetas", 8.00),
            ("Conserto Simples", 25.00)
        ]
        
        for nome_servico, custo_servico in servicos_basicos:
            pricing_servico = self.calculate_product_pricing(custo_servico, tipo_produto="servicos")
            
            produtos.append({
                "Categoria": "Serviços",
                "Fornecedor": "Interno",
                "Produto": nome_servico,
                "Tipo": "servico",
                "Base/Grau": "N/A",
                "Custo Unitário": custo_servico,
                "Markup": self.markup_padrao["servicos"],
                "Preço Venda": pricing_servico["preco_venda"],
                "Margem %": pricing_servico["percentual_margem"]
            })
        
        return pd.DataFrame(produtos)
    
    def calculate_ticket_medio(self, df_vendas: pd.DataFrame) -> Dict:
        """Calculate average ticket from sales data"""
        if df_vendas.empty:
            return {"ticket_medio": 0, "erro": "Nenhuma venda informada"}
        
        total_receita = df_vendas["Preço Venda"].sum()
        total_vendas = len(df_vendas)
        ticket_medio = total_receita / total_vendas if total_vendas > 0 else 0
        
        return {
            "ticket_medio": ticket_medio,
            "total_receita": total_receita,
            "total_vendas": total_vendas,
            "receita_lentes": df_vendas[df_vendas["Categoria"] == "Lentes"]["Preço Venda"].sum(),
            "receita_armacoes": df_vendas[df_vendas["Categoria"] == "Armações"]["Preço Venda"].sum(),
            "receita_servicos": df_vendas[df_vendas["Categoria"] == "Serviços"]["Preço Venda"].sum()
        }