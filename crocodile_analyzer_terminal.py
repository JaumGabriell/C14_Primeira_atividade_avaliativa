#!/usr/bin/env python3

import pandas as pd
import os
import sys

class CrocodileAnalyzer:

    
    def __init__(self, csv_file):
        
        self.csv_file = csv_file
        self.data = None
        self.load_data()
    
    def load_data(self):

        try:
            self.data = pd.read_csv(self.csv_file)
            print(f"Dataset carregado com sucesso! {len(self.data)} observações encontradas.\n")
        except FileNotFoundError:
            print(f"Erro: Arquivo {self.csv_file} não encontrado!")
            sys.exit(1)
        except Exception as e:
            print(f"Erro ao carregar dados: {e}")
            sys.exit(1)
    
    def function_1_basic_info(self):
        print("=" * 60)
        print("INFORMAÇÕES BÁSICAS DO DATASET")
        print("=" * 60)
        print(f"Total de observações: {len(self.data)}")
        print(f"Total de colunas: {len(self.data.columns)}")
        print(f"Tamanho em memória: {self.data.memory_usage(deep=True).sum() / 1024:.2f} KB")
        print(f"\nColunas disponíveis:")
        for i, col in enumerate(self.data.columns, 1):
            print(f"  {i:2d}. {col}")
        print(f"\nTipos de dados:")
        print(self.data.dtypes)
    
    def function_2_species_count(self):
        print("=" * 60)
        print("CONTAGEM POR ESPÉCIE")
        print("=" * 60)
        species_count = self.data['Common Name'].value_counts()
        for i, (species, count) in enumerate(species_count.head(10).items(), 1):
            print(f"{i:2d}. {species:<35} | {count:3d} observações")
        print(f"\nTotal de espécies únicas: {len(species_count)}")
    
    def function_3_size_statistics(self):
        print("=" * 60)
        print("ESTATÍSTICAS DE COMPRIMENTO")
        print("=" * 60)
        length_data = self.data['Observed Length (m)'].dropna()
        print(f"Média: {length_data.mean():.2f} metros")
        print(f"Mediana: {length_data.median():.2f} metros")
        print(f"Desvio padrão: {length_data.std():.2f} metros")
        print(f"Mínimo: {length_data.min():.2f} metros")
        print(f"Máximo: {length_data.max():.2f} metros")
        print(f"1º Quartil: {length_data.quantile(0.25):.2f} metros")
        print(f"3º Quartil: {length_data.quantile(0.75):.2f} metros")
        print(f"Total de medições válidas: {len(length_data)}")
    
    def function_4_weight_statistics(self):
        print("=" * 60)
        print("ESTATÍSTICAS DE PESO")
        print("=" * 60)
        weight_data = self.data['Observed Weight (kg)'].dropna()
        print(f"Média: {weight_data.mean():.2f} kg")
        print(f"Mediana: {weight_data.median():.2f} kg")
        print(f"Desvio padrão: {weight_data.std():.2f} kg")
        print(f"Mínimo: {weight_data.min():.2f} kg")
        print(f"Máximo: {weight_data.max():.2f} kg")
        print(f"1º Quartil: {weight_data.quantile(0.25):.2f} kg")
        print(f"3º Quartil: {weight_data.quantile(0.75):.2f} kg")
        print(f"Total de medições válidas: {len(weight_data)}")
    
    def function_5_habitat_distribution(self):
        print("=" * 60)
        print("DISTRIBUIÇÃO POR HABITAT")
        print("=" * 60)
        habitat_dist = self.data['Habitat Type'].value_counts()
        for i, (habitat, count) in enumerate(habitat_dist.items(), 1):
            percentage = (count / len(self.data)) * 100
            print(f"{i:2d}. {habitat:<25} | {count:3d} ({percentage:5.1f}%)")
    
    def function_6_conservation_status(self):
        print("=" * 60)
        print("STATUS DE CONSERVAÇÃO")
        print("=" * 60)
        conservation = self.data['Conservation Status'].value_counts()
        for status, count in conservation.items():
            percentage = (count / len(self.data)) * 100
            print(f"{status:<20} | {count:3d} ({percentage:5.1f}%)")
    
    def function_7_age_class_analysis(self):
        print("=" * 60)
        print("DISTRIBUIÇÃO POR IDADE")
        print("=" * 60)
        age_dist = self.data['Age Class'].value_counts()
        for age, count in age_dist.items():
            percentage = (count / len(self.data)) * 100
            print(f"{age:<15} | {count:3d} ({percentage:5.1f}%)")
            
    def function_8_sex_distribution(self):
        print("=" * 60)
        print("DISTRIBUIÇÃO POR SEXO")
        print("=" * 60)
        sex_dist = self.data['Sex'].value_counts()
        for sex, count in sex_dist.items():
            percentage = (count / len(self.data)) * 100
            print(f"{sex:<10} | {count:3d} ({percentage:5.1f}%)")
    
    def function_9_country_analysis(self):
        print("=" * 60)
        print("OBSERVAÇÕES POR PAÍS/REGIÃO")
        print("=" * 60)
        country_dist = self.data['Country/Region'].value_counts()
        for i, (country, count) in enumerate(country_dist.head(15).items(), 1):
            percentage = (count / len(self.data)) * 100
            print(f"{i:2d}. {country:<25} | {count:3d} ({percentage:5.1f}%)")
    
    def function_10_largest_specimens(self):
        print("=" * 60)
        print("MAIORES ESPÉCIMES (COMPRIMENTO)")
        print("=" * 60)
        largest = self.data.nlargest(10, 'Observed Length (m)')
        for i, (idx, row) in enumerate(largest.iterrows(), 1):
            print(f"{i:2d}. {row['Common Name']:<30} | {row['Observed Length (m)']:5.2f}m | {row['Country/Region']}")
    def function_11_heaviest_specimens(self):
        print("=" * 60)
        print("ESPÉCIMES MAIS PESADOS")
        print("=" * 60)
        heaviest = self.data.nlargest(10, 'Observed Weight (kg)')
        for i, (idx, row) in enumerate(heaviest.iterrows(), 1):
            print(f"{i:2d}. {row['Common Name']:<30} | {row['Observed Weight (kg)']:6.1f}kg | {row['Country/Region']}")
    
    def function_12_size_categories(self):
        print("=" * 60)
        print("CATEGORIZAÇÃO POR TAMANHO")
        print("=" * 60)
        
        def categorize_size(length):
            if pd.isna(length):
                return 'Desconhecido'
            elif length < 1.5:
                return 'Pequeno (<1.5m)'
            elif length < 3.0:
                return 'Médio (1.5-3m)'
            elif length < 4.5:
                return 'Grande (3-4.5m)'
            else:
                return 'Muito Grande (>4.5m)'
        
        
        temp_data = self.data.copy()
        temp_data['Size_Category'] = temp_data['Observed Length (m)'].apply(categorize_size)
        size_dist = temp_data['Size_Category'].value_counts()
        
        for category, count in size_dist.items():
            percentage = (count / len(self.data)) * 100
            print(f"{category:<20} | {count:3d} ({percentage:5.1f}%)")
    
    def function_13_yearly_observations(self):
        print("=" * 60)
        print("OBSERVAÇÕES POR ANO")
        print("=" * 60)
        try:
            
            dates = pd.to_datetime(self.data['Date of Observation'], format='%d-%m-%Y', errors='coerce')
            yearly = dates.dt.year.value_counts().sort_index()
            
            for year, count in yearly.items():
                if not pd.isna(year):
                    print(f"{int(year)} | {'*' * (count // 5)}{count:3d} observações")
        except (ValueError, TypeError) as e:
            print(f"Erro na conversão de datas: {e}")
    
    def function_14_correlation_analysis(self):
        print("=" * 60)
        print("CORRELAÇÃO PESO vs COMPRIMENTO")
        print("=" * 60)
        

        valid_data = self.data[['Observed Length (m)', 'Observed Weight (kg)']].dropna()
        
        if len(valid_data) > 1:
            correlation = valid_data['Observed Length (m)'].corr(valid_data['Observed Weight (kg)'])
            print(f"Coeficiente de correlação de Pearson: {correlation:.4f}")
            
            if correlation > 0.8:
                print("Correlação muito forte e positiva")
            elif correlation > 0.6:
                print("Correlação forte e positiva")
            elif correlation > 0.4:
                print("Correlação moderada e positiva")
            elif correlation > 0.2:
                print("Correlação fraca e positiva")
            else:
                print("Correlação muito fraca")
            
            print(f"\nDados válidos para análise: {len(valid_data)}")
        else:
            print("Dados insuficientes para análise de correlação")
    def function_15_species_by_habitat(self):
        print("=" * 60)
        print("DIVERSIDADE DE ESPÉCIES POR HABITAT")
        print("=" * 60)
        
        habitat_diversity = self.data.groupby('Habitat Type')['Common Name'].nunique().sort_values(ascending=False)
        
        for habitat, species_count in habitat_diversity.items():
            print(f"{habitat:<25} | {species_count:2d} espécies diferentes")
    
    def function_16_adult_vs_juvenile(self):
        print("=" * 60)
        print("COMPARAÇÃO ADULTO vs JUVENIL")
        print("=" * 60)
        
        adults = self.data[self.data['Age Class'] == 'Adult']
        juveniles = self.data[self.data['Age Class'] == 'Juvenile']
        
        print("ADULTOS:")
        if len(adults) > 0:
            adult_length = adults['Observed Length (m)'].dropna()
            adult_weight = adults['Observed Weight (kg)'].dropna()
            print(f"  Comprimento médio: {adult_length.mean():.2f}m")
            print(f"  Peso médio: {adult_weight.mean():.2f}kg")
            print(f"  Total: {len(adults)} observações")
        
        print("\nJUVENIS:")
        if len(juveniles) > 0:
            juv_length = juveniles['Observed Length (m)'].dropna()
            juv_weight = juveniles['Observed Weight (kg)'].dropna()
            print(f"  Comprimento médio: {juv_length.mean():.2f}m")
            print(f"  Peso médio: {juv_weight.mean():.2f}kg")
            print(f"  Total: {len(juveniles)} observações")
    
    def function_17_endangered_species(self):
        print("=" * 60)
        print("ESPÉCIES AMEAÇADAS DE EXTINÇÃO")
        print("=" * 60)
        
        endangered_status = ['Critically Endangered', 'Endangered', 'Vulnerable']
        endangered = self.data[self.data['Conservation Status'].isin(endangered_status)]
        
        if len(endangered) > 0:
            endangered_species = endangered.groupby(['Common Name', 'Conservation Status']).size().reset_index(name='Count')
            
            for _, row in endangered_species.iterrows():
                print(f"{row['Common Name']:<35} | {row['Conservation Status']:<20} | {row['Count']} obs.")
        else:
            print("Nenhuma espécie ameaçada encontrada no dataset")
    
    def function_18_observer_statistics(self):
        print("=" * 60)
        print("ESTATÍSTICAS DOS OBSERVADORES")
        print("=" * 60)
        
        observer_stats = self.data['Observer Name'].value_counts()
        print(f"Total de observadores: {len(observer_stats)}")
        print(f"Observador mais ativo: {observer_stats.index[0]} ({observer_stats.iloc[0]} observações)")
        print(f"Média de observações por observador: {observer_stats.mean():.1f}")
        
        print("\nTop 10 observadores mais ativos:")
        for i, (observer, count) in enumerate(observer_stats.head(10).items(), 1):
            print(f"{i:2d}. {observer:<25} | {count:3d} observações")
    
    def function_19_missing_data_analysis(self):
        print("=" * 60)
        print("ANÁLISE DE DADOS FALTANTES")
        print("=" * 60)
        
        missing_data = self.data.isnull().sum()
        total_rows = len(self.data)
        
        print(f"Total de registros: {total_rows}")
        print("\nDados faltantes por coluna:")
        
        for column, missing_count in missing_data.items():
            if missing_count > 0:
                percentage = (missing_count / total_rows) * 100
                print(f"{column:<30} | {missing_count:3d} ({percentage:5.1f}%)")
            else:
                print(f"{column:<30} | Completo")
    
    def function_20_summary_report(self):
        print("=" * 80)
        print("RELATÓRIO RESUMO COMPLETO DO DATASET")
        print("=" * 80)
        
        print(f"DADOS GERAIS:")
        print(f"   Total de observações: {len(self.data)}")
        print(f"   Espécies únicas: {self.data['Common Name'].nunique()}")
        print(f"   Países/regiões: {self.data['Country/Region'].nunique()}")
        print(f"   Tipos de habitat: {self.data['Habitat Type'].nunique()}")
        print(f"   Observadores: {self.data['Observer Name'].nunique()}")
        
        print(f"\nMEDIDAS FÍSICAS:")
        length_stats = self.data['Observed Length (m)'].describe()
        weight_stats = self.data['Observed Weight (kg)'].describe()
        print(f"   Comprimento: {length_stats['min']:.2f}m - {length_stats['max']:.2f}m (média: {length_stats['mean']:.2f}m)")
        print(f"   Peso: {weight_stats['min']:.1f}kg - {weight_stats['max']:.1f}kg (média: {weight_stats['mean']:.1f}kg)")
        
        print(f"\nCONSERVAÇÃO:")
        conservation_counts = self.data['Conservation Status'].value_counts()
        endangered = conservation_counts.get('Critically Endangered', 0) + conservation_counts.get('Endangered', 0)
        print(f"   Espécies em perigo crítico/extinção: {endangered}")
        print(f"   Status mais comum: {conservation_counts.index[0]} ({conservation_counts.iloc[0]} obs.)")
        
        print(f"\nQUALIDADE DOS DADOS:")
        completeness = ((len(self.data) - self.data.isnull().sum()) / len(self.data) * 100)
        avg_completeness = completeness.mean()
        print(f"   Completude média: {avg_completeness:.1f}%")
        print(f"   Coluna mais completa: {completeness.idxmax()} ({completeness.max():.1f}%)")
        if completeness.min() < 100:
            print(f"   Coluna com mais dados faltantes: {completeness.idxmin()} ({completeness.min():.1f}%)")


def show_menu():
    print("\n" + "=" * 80)
    print("🐊 ANÁLISE INTERATIVA DO DATASET DE CROCODILOS 🐊")
    print("=" * 80)
    print("Escolha uma das 20 opções de análise:")
    print()
    
    options = [
        "1.  Informações básicas do dataset",
        "2.  Contagem por espécie",  
        "3.  Estatísticas de comprimento",
        "4.  Estatísticas de peso",
        "5.  Distribuição por habitat",
        "6.  Status de conservação",
        "7.  Análise por classe etária",
        "8.  Distribuição por sexo",
        "9.  Análise por país/região",
        "10. Maiores espécimes (comprimento)",
        "11. Espécimes mais pesados",
        "12. Categorização por tamanho",
        "13. Observações por ano",
        "14. Correlação peso vs comprimento",
        "15. Espécies por habitat",
        "16. Comparação adulto vs juvenil",
        "17. Espécies ameaçadas de extinção",
        "18. Estatísticas dos observadores",
        "19. Análise de dados faltantes",
        "20. Relatório resumo completo"
    ]
    
    
    for i in range(0, len(options), 2):
        left = options[i] if i < len(options) else ""
        right = options[i+1] if i+1 < len(options) else ""
        print(f"{left:<40} {right}")
    
    print()
    print("0.  Sair")
    print("=" * 80)

def main():
    
    csv_file = 'crocodile_dataset.csv'
    if not os.path.exists(csv_file):
        print(f"Arquivo {csv_file} não encontrado no diretório atual!")
        print("Certifique-se de que o arquivo está no mesmo diretório do programa.")
        return
    

    analyzer = CrocodileAnalyzer(csv_file)
    

    functions = {
        1: analyzer.function_1_basic_info,
        2: analyzer.function_2_species_count,
        3: analyzer.function_3_size_statistics,
        4: analyzer.function_4_weight_statistics,
        5: analyzer.function_5_habitat_distribution,
        6: analyzer.function_6_conservation_status,
        7: analyzer.function_7_age_class_analysis,
        8: analyzer.function_8_sex_distribution,
        9: analyzer.function_9_country_analysis,
        10: analyzer.function_10_largest_specimens,
        11: analyzer.function_11_heaviest_specimens,
        12: analyzer.function_12_size_categories,
        13: analyzer.function_13_yearly_observations,
        14: analyzer.function_14_correlation_analysis,
        15: analyzer.function_15_species_by_habitat,
        16: analyzer.function_16_adult_vs_juvenile,
        17: analyzer.function_17_endangered_species,
        18: analyzer.function_18_observer_statistics,
        19: analyzer.function_19_missing_data_analysis,
        20: analyzer.function_20_summary_report
    }
    
    
    while True:
        show_menu()
        
        try:
            choice = input("Digite sua opção (0-20): ").strip()
            
            if choice == '0':
                print("\nObrigado por usar o Analisador de Crocodilos! Até mais!")
                break
            
            choice_int = int(choice)
            
            if choice_int in functions:
                print("\n")
                functions[choice_int]()
                input("\nPressione ENTER para continuar...")
            else:
                print("Opção inválida! Por favor, digite um número de 0 a 20.")
                input("Pressione ENTER para continuar...")
                
        except ValueError:
            print("Por favor, digite apenas números!")
            input("Pressione ENTER para continuar...")
        except KeyboardInterrupt:
            print("\n\nPrograma interrompido pelo usuário. Até mais!")
            break
        except Exception as e:
            print(f"Erro inesperado: {e}")
            input("Pressione ENTER para continuar...")

if __name__ == "__main__":
    main()
