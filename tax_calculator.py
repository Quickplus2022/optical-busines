import pandas as pd

class TaxCalculator:
    """Calculator for Brazilian tax regimes: Simples Nacional and Lucro Presumido"""
    
    def __init__(self):
        # Simples Nacional tables for 2024 (Anexo I - Comércio)
        self.simples_anexo_1 = [
            {"faixa_inicial": 0, "faixa_final": 180000, "aliquota": 4.0, "deducao": 0},
            {"faixa_inicial": 180000.01, "faixa_final": 360000, "aliquota": 7.3, "deducao": 5940},
            {"faixa_inicial": 360000.01, "faixa_final": 720000, "aliquota": 9.5, "deducao": 13860},
            {"faixa_inicial": 720000.01, "faixa_final": 1800000, "aliquota": 10.7, "deducao": 22500},
            {"faixa_inicial": 1800000.01, "faixa_final": 3600000, "aliquota": 14.3, "deducao": 87300},
            {"faixa_inicial": 3600000.01, "faixa_final": 4800000, "aliquota": 19.0, "deducao": 378000}
        ]
        
        # Simples Nacional Anexo II - Indústria
        self.simples_anexo_2 = [
            {"faixa_inicial": 0, "faixa_final": 180000, "aliquota": 4.5, "deducao": 0},
            {"faixa_inicial": 180000.01, "faixa_final": 360000, "aliquota": 7.8, "deducao": 5940},
            {"faixa_inicial": 360000.01, "faixa_final": 720000, "aliquota": 10.0, "deducao": 13860},
            {"faixa_inicial": 720000.01, "faixa_final": 1800000, "aliquota": 11.2, "deducao": 22500},
            {"faixa_inicial": 1800000.01, "faixa_final": 3600000, "aliquota": 14.7, "deducao": 85500},
            {"faixa_inicial": 3600000.01, "faixa_final": 4800000, "aliquota": 30.0, "deducao": 720000}
        ]
        
        # Simples Nacional Anexo III - Serviços
        self.simples_anexo_3 = [
            {"faixa_inicial": 0, "faixa_final": 180000, "aliquota": 6.0, "deducao": 0},
            {"faixa_inicial": 180000.01, "faixa_final": 360000, "aliquota": 11.2, "deducao": 9360},
            {"faixa_inicial": 360000.01, "faixa_final": 720000, "aliquota": 13.5, "deducao": 17640},
            {"faixa_inicial": 720000.01, "faixa_final": 1800000, "aliquota": 16.0, "deducao": 35640},
            {"faixa_inicial": 1800000.01, "faixa_final": 3600000, "aliquota": 21.0, "deducao": 125640},
            {"faixa_inicial": 3600000.01, "faixa_final": 4800000, "aliquota": 33.0, "deducao": 648000}
        ]
    
    def get_simples_table(self, anexo):
        """Get the appropriate Simples Nacional table based on annexe"""
        if anexo == "Anexo I - Comércio":
            return self.simples_anexo_1
        elif anexo == "Anexo II - Indústria":
            return self.simples_anexo_2
        elif anexo == "Anexo III - Serviços":
            return self.simples_anexo_3
        else:
            return self.simples_anexo_1  # Default to commerce
    
    def calculate_simples_nacional(self, receita_anual, anexo="Anexo I - Comércio"):
        """Calculate Simples Nacional tax based on annual revenue"""
        try:
            table = self.get_simples_table(anexo)
            
            # Find the appropriate tax bracket
            aliquota_efetiva = 4.0  # Default
            deducao = 0
            
            for faixa in table:
                if faixa["faixa_inicial"] <= receita_anual <= faixa["faixa_final"]:
                    aliquota_efetiva = faixa["aliquota"]
                    deducao = faixa["deducao"]
                    break
            
            # Calculate effective tax rate
            if receita_anual > 0:
                aliquota_efetiva = ((receita_anual * aliquota_efetiva / 100) - deducao) / receita_anual * 100
            
            # Calculate taxes
            tributo_anual = receita_anual * aliquota_efetiva / 100
            tributo_mensal = tributo_anual / 12
            
            return {
                "regime": "Simples Nacional",
                "anexo": anexo,
                "receita_anual": receita_anual,
                "aliquota_efetiva": aliquota_efetiva,
                "tributo_anual": tributo_anual,
                "tributo_mensal": tributo_mensal
            }
            
        except Exception as e:
            return {
                "regime": "Simples Nacional",
                "anexo": anexo,
                "receita_anual": receita_anual,
                "aliquota_efetiva": 4.0,
                "tributo_anual": receita_anual * 0.04,
                "tributo_mensal": receita_anual * 0.04 / 12,
                "error": str(e)
            }
    
    def calculate_lucro_presumido(self, receita_anual):
        """Calculate Lucro Presumido tax regime"""
        try:
            # Tax rates for Lucro Presumido
            # PIS: 0.65%, COFINS: 3.0%
            pis_cofins = receita_anual * 0.0365  # 3.65%
            
            # Presumed profit bases
            comercio_presumido = receita_anual * 0.08  # 8% for commerce
            servicos_presumido = receita_anual * 0.32  # 32% for services
            
            # For optical shop (mixed commerce/services), use weighted average
            base_presumida = (comercio_presumido * 0.7) + (servicos_presumido * 0.3)
            
            # IRPJ: 15% on presumed profit + additional 10% on excess of R$ 240,000/year
            irpj = base_presumida * 0.15
            irpj_adicional = max(0, (base_presumida - 240000) * 0.10)
            
            # CSLL: 9% on presumed profit
            csll = base_presumida * 0.09
            
            # Total taxes
            total_tributos = pis_cofins + irpj + irpj_adicional + csll
            aliquota_total = (total_tributos / receita_anual) * 100
            
            return {
                "regime": "Lucro Presumido",
                "receita_anual": receita_anual,
                "base_presumida": base_presumida,
                "pis_cofins": pis_cofins,
                "irpj": irpj,
                "irpj_adicional": irpj_adicional,
                "csll": csll,
                "tributo_anual": total_tributos,
                "tributo_mensal": total_tributos / 12,
                "aliquota_total": aliquota_total
            }
            
        except Exception as e:
            return {
                "regime": "Lucro Presumido",
                "receita_anual": receita_anual,
                "tributo_anual": receita_anual * 0.12,  # Default 12%
                "tributo_mensal": receita_anual * 0.12 / 12,
                "aliquota_total": 12.0,
                "error": str(e)
            }
    
    def compare_tax_regimes(self, receita_anual, anexo="Anexo I - Comércio"):
        """Compare Simples Nacional vs Lucro Presumido"""
        simples = self.calculate_simples_nacional(receita_anual, anexo)
        presumido = self.calculate_lucro_presumido(receita_anual)
        
        economia_anual = abs(simples["tributo_anual"] - presumido["tributo_anual"])
        melhor_regime = "Simples Nacional" if simples["tributo_anual"] < presumido["tributo_anual"] else "Lucro Presumido"
        
        return {
            "simples_nacional": simples,
            "lucro_presumido": presumido,
            "melhor_regime": melhor_regime,
            "economia_anual": economia_anual,
            "diferenca_percentual": (economia_anual / min(simples["tributo_anual"], presumido["tributo_anual"])) * 100
        }
    
    def calculate_tax_by_regime(self, receita_mensal, regime, anexo="Anexo I - Comércio"):
        """Calculate monthly tax based on regime"""
        receita_anual = receita_mensal * 12
        
        if regime == "Simples Nacional":
            result = self.calculate_simples_nacional(receita_anual, anexo)
            return result["tributo_mensal"]
        elif regime == "Lucro Presumido":
            result = self.calculate_lucro_presumido(receita_anual)
            return result["tributo_mensal"]
        else:
            # Default to Simples Nacional
            result = self.calculate_simples_nacional(receita_anual, anexo)
            return result["tributo_mensal"]
