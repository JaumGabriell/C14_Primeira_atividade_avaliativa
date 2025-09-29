#!/usr/bin/env python3

import pytest
import pandas as pd
import os
import sys
from unittest.mock import patch, MagicMock
from crocodile_analyzer_terminal import CrocodileAnalyzer


@pytest.fixture
def sample_csv_file(tmp_path):
    
    csv_content = """Observation ID,Common Name,Scientific Name,Family,Genus,Observed Length (m),Observed Weight (kg),Age Class,Sex,Date of Observation,Country/Region,Habitat Type,Conservation Status,Observer Name,Notes
1,Morelet's Crocodile,Crocodylus moreletii,Crocodylidae,Crocodylus,1.9,62,Adult,Male,31-03-2018,Belize,Swamps,Least Concern,Allison Hill,Test observation 1
2,American Crocodile,Crocodylus acutus,Crocodylidae,Crocodylus,4.09,334.5,Adult,Male,28-01-2015,Venezuela,Mangroves,Vulnerable,Brandon Hall,Test observation 2
3,Orinoco Crocodile,Crocodylus intermedius,Crocodylidae,Crocodylus,1.08,118.2,Juvenile,Unknown,07-12-2010,Venezuela,Flooded Savannas,Critically Endangered,Melissa Peterson,Test observation 3
4,Morelet's Crocodile,Crocodylus moreletii,Crocodylidae,Crocodylus,2.42,90.4,Adult,Male,01-11-2019,Mexico,Rivers,Least Concern,Edward Fuller,Test observation 4
5,Mugger Crocodile,Crocodylus palustris,Crocodylidae,Crocodylus,3.75,269.4,Adult,Unknown,15-07-2019,India,Rivers,Vulnerable,Donald Reid,Test observation 5"""
    
    csv_file = tmp_path / "test_crocodiles.csv"
    csv_file.write_text(csv_content)
    return str(csv_file)


class TestCrocodileAnalyzer:
    
    def test_1_initialization_with_valid_file(self, sample_csv_file):
        analyzer = CrocodileAnalyzer(sample_csv_file)
        assert analyzer.csv_file == sample_csv_file
        assert analyzer.data is not None
        assert len(analyzer.data) == 5
        assert 'Common Name' in analyzer.data.columns
    
    def test_2_initialization_with_invalid_file(self):
        with pytest.raises(SystemExit):
            with patch('builtins.print') as mock_print:
                CrocodileAnalyzer("arquivo_inexistente.csv")
                mock_print.assert_called()
    
    def test_3_basic_info_function(self, sample_csv_file, capsys):
        analyzer = CrocodileAnalyzer(sample_csv_file)
        analyzer.function_1_basic_info()
        
        captured = capsys.readouterr()
        assert "INFORMAÇÕES BÁSICAS DO DATASET" in captured.out
        assert "Total de observações: 5" in captured.out
        assert "Total de colunas: 15" in captured.out
        assert "Common Name" in captured.out
    
    def test_4_species_count_function(self, sample_csv_file, capsys):
        analyzer = CrocodileAnalyzer(sample_csv_file)
        analyzer.function_2_species_count()
        
        captured = capsys.readouterr()
        assert "CONTAGEM POR ESPÉCIE" in captured.out
        assert "Morelet's Crocodile" in captured.out
        assert "2 observações" in captured.out
        assert "Total de espécies únicas: 4" in captured.out
    
    def test_5_size_statistics_function(self, sample_csv_file, capsys):
        analyzer = CrocodileAnalyzer(sample_csv_file)
        analyzer.function_3_size_statistics()
        
        captured = capsys.readouterr()
        assert "ESTATÍSTICAS DE COMPRIMENTO" in captured.out
        assert "Média:" in captured.out
        assert "Mediana:" in captured.out
        assert "Desvio padrão:" in captured.out
        assert "metros" in captured.out
        
       
        assert "2.65" in captured.out or "2.64" in captured.out  

    def test_6_weight_statistics_function(self, sample_csv_file, capsys):

        analyzer = CrocodileAnalyzer(sample_csv_file)
        analyzer.function_4_weight_statistics()
        
        captured = capsys.readouterr()
        assert "ESTATÍSTICAS DE PESO" in captured.out
        assert "Média:" in captured.out
        assert "kg" in captured.out
        assert "Total de medições válidas: 5" in captured.out
        
        assert "Mínimo:" in captured.out
        assert "Máximo:" in captured.out
        assert "1º Quartil:" in captured.out
        assert "3º Quartil:" in captured.out
    
    def test_7_habitat_distribution_function(self, sample_csv_file, capsys):
        analyzer = CrocodileAnalyzer(sample_csv_file)
        analyzer.function_5_habitat_distribution()
        
        captured = capsys.readouterr()
        assert "DISTRIBUIÇÃO POR HABITAT" in captured.out
        assert "Rivers" in captured.out
        assert "%" in captured.out
        
      
        assert "20.0%" in captured.out 
        assert "40.0%" in captured.out  
    
    def test_8_sex_distribution_function(self, sample_csv_file, capsys):
        analyzer = CrocodileAnalyzer(sample_csv_file)
        analyzer.function_8_sex_distribution()
        
        captured = capsys.readouterr()
        assert "DISTRIBUIÇÃO POR SEXO" in captured.out
        assert "Male" in captured.out
        assert "Unknown" in captured.out
        assert "%" in captured.out
        
        # Verificar se as contagens estão corretas (3 machos, 2 desconhecidos)
        assert "60.0%" in captured.out  # Male
        assert "40.0%" in captured.out  # Unknown
    
    def test_9_country_analysis_function(self, sample_csv_file, capsys):
        analyzer = CrocodileAnalyzer(sample_csv_file)
        analyzer.function_9_country_analysis()
        
        captured = capsys.readouterr()
        assert "OBSERVAÇÕES POR PAÍS/REGIÃO" in captured.out
        assert "Venezuela" in captured.out
        assert "Belize" in captured.out
        assert "Mexico" in captured.out
        assert "India" in captured.out
        assert "%" in captured.out
        
        # Verificar contagens (Venezuela: 2, outros: 1 cada)
        assert "40.0%" in captured.out  # Venezuela
        assert "20.0%" in captured.out  # Outros países
    
    def test_10_largest_specimens_function(self, sample_csv_file, capsys):
        analyzer = CrocodileAnalyzer(sample_csv_file)
        analyzer.function_10_largest_specimens()
        
        captured = capsys.readouterr()
        assert "MAIORES ESPÉCIMES (COMPRIMENTO)" in captured.out
        assert "American Crocodile" in captured.out
        assert "4.09m" in captured.out
        assert "Venezuela" in captured.out
        
        # Verificar ordenação (o maior deve aparecer primeiro)
        lines = captured.out.split('\n')
        first_specimen_line = next(line for line in lines if "1." in line and "m |" in line)
        assert "4.09" in first_specimen_line
        
    def test_11_heaviest_specimens_function(self, sample_csv_file, capsys):
        analyzer = CrocodileAnalyzer(sample_csv_file)
        analyzer.function_11_heaviest_specimens()
        
        captured = capsys.readouterr()
        assert "ESPÉCIMES MAIS PESADOS" in captured.out
        assert "American Crocodile" in captured.out
        assert "334.5kg" in captured.out
        assert "Venezuela" in captured.out
        
        # Verificar ordenação (o mais pesado deve aparecer primeiro)
        lines = captured.out.split('\n')
        first_specimen_line = next(line for line in lines if "1." in line and "kg |" in line)
        assert "334.5" in first_specimen_line
    
    def test_12_size_categories_function(self, sample_csv_file, capsys):
        analyzer = CrocodileAnalyzer(sample_csv_file)
        analyzer.function_12_size_categories()
        
        captured = capsys.readouterr()
        assert "CATEGORIZAÇÃO POR TAMANHO" in captured.out
        assert "Pequeno (<1.5m)" in captured.out
        assert "Médio (1.5-3m)" in captured.out
        assert "Grande (3-4.5m)" in captured.out
        assert "%" in captured.out
        
        # Verificar categorias baseadas nos dados de teste
        # 1.08m -> Pequeno, 1.9m e 2.42m -> Médio, 3.75m e 4.09m -> Grande
        assert "20.0%" in captured.out  # 1 Pequeno
        assert "40.0%" in captured.out  # 2 Médios
        # 2 Grandes também serão 40%
    
    def test_13_yearly_observations_function(self, sample_csv_file, capsys):
        analyzer = CrocodileAnalyzer(sample_csv_file)
        analyzer.function_13_yearly_observations()
        
        captured = capsys.readouterr()
        assert "OBSERVAÇÕES POR ANO" in captured.out
        assert "observações" in captured.out
        
        # Verificar anos presentes nos dados de teste
        assert "2010" in captured.out
        assert "2015" in captured.out
        assert "2018" in captured.out
        assert "2019" in captured.out
    
    def test_14_correlation_analysis_function(self, sample_csv_file, capsys):
        analyzer = CrocodileAnalyzer(sample_csv_file)
        analyzer.function_14_correlation_analysis()
        
        captured = capsys.readouterr()
        assert "CORRELAÇÃO PESO vs COMPRIMENTO" in captured.out
        assert "Coeficiente de correlação de Pearson:" in captured.out
        assert "Dados válidos para análise: 5" in captured.out
        
        # Como temos dados válidos, deve mostrar uma correlação
        correlation_patterns = [
            "Correlação muito forte",
            "Correlação forte",
            "Correlação moderada", 
            "Correlação fraca",
            "Correlação muito fraca"
        ]
        assert any(pattern in captured.out for pattern in correlation_patterns)

    def test_15_species_by_habitat(self, sample_csv_file, capsys):
        analyzer = CrocodileAnalyzer(sample_csv_file)
        analyzer.function_15_species_by_habitat()

        captured = capsys.readouterr()
        assert "DIVERSIDADE DE ESPÉCIES POR HABITAT" in captured.out
        assert "Swamps" in captured.out
        assert "Mangroves" in captured.out
        assert "Flooded Savannas" in captured.out
        assert "Rivers" in captured.out
        assert "espécies diferentes" in captured.out


    def test_16_adult_vs_juvenile(self, sample_csv_file, capsys):
        analyzer = CrocodileAnalyzer(sample_csv_file)
        analyzer.function_16_adult_vs_juvenile()

        captured = capsys.readouterr()
        assert "COMPARAÇÃO ADULTO vs JUVENIL" in captured.out
        assert "ADULTOS:" in captured.out
        assert "JUVENIS:" in captured.out
        assert "Comprimento médio" in captured.out
        assert "Peso médio" in captured.out
        assert "observações" in captured.out


    def test_17_endangered_species(self, sample_csv_file, capsys):
        analyzer = CrocodileAnalyzer(sample_csv_file)
        analyzer.function_17_endangered_species()

        captured = capsys.readouterr()
        assert "ESPÉCIES AMEAÇADAS DE EXTINÇÃO" in captured.out
        assert "Critically Endangered" in captured.out
        assert "Vulnerable" in captured.out
        assert "obs." in captured.out
        assert "Orinoco Crocodile" in captured.out or "Mugger Crocodile" in captured.out


    def test_18_observer_statistics(self, sample_csv_file, capsys):
        analyzer = CrocodileAnalyzer(sample_csv_file)
        analyzer.function_18_observer_statistics()

        captured = capsys.readouterr()
        assert "ESTATÍSTICAS DOS OBSERVADORES" in captured.out
        assert "Observador mais ativo:" in captured.out
        assert "Total de observadores:" in captured.out
        assert "Média de observações por observador:" in captured.out
        assert "Top 10 observadores mais ativos:" in captured.out
        assert "Allison Hill" in captured.out
        assert "Brandon Hall" in captured.out


    def test_19_missing_data_analysis(self, sample_csv_file, capsys):
        analyzer = CrocodileAnalyzer(sample_csv_file)
        analyzer.function_19_missing_data_analysis()

        captured = capsys.readouterr()
        assert "ANÁLISE DE DADOS FALTANTES" in captured.out
        assert "Dados faltantes por coluna:" in captured.out
        assert "Completo" in captured.out or "%" in captured.out
        assert "Total de registros: 5" in captured.out


    def test_20_summary_report(self, sample_csv_file, capsys):
        analyzer = CrocodileAnalyzer(sample_csv_file)
        analyzer.function_20_summary_report()

        captured = capsys.readouterr()
        assert "RELATÓRIO RESUMO COMPLETO DO DATASET" in captured.out
        assert "Total de observações" in captured.out
        assert "Espécies únicas" in captured.out
        assert "Países/regiões" in captured.out
        assert "Tipos de habitat" in captured.out
        assert "Observadores" in captured.out
        assert "Comprimento:" in captured.out
        assert "Peso:" in captured.out
        assert "Espécies em perigo crítico/extinção:" in captured.out
        assert "Completude média" in captured.out
        
if __name__ == "__main__":
    pytest.main(["-v", __file__])
