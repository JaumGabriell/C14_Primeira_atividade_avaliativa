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
        
if __name__ == "__main__":
    pytest.main(["-v", __file__])
