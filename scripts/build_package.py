

import os
import sys
import shutil
import zipfile
import tarfile
import json
from datetime import datetime
import subprocess

def create_build_info():

    build_info = {
        "build_timestamp": datetime.now().isoformat(),
        "repository": os.getenv('GITHUB_REPOSITORY', 'local-build'),
        "commit_sha": os.getenv('GITHUB_SHA', 'unknown')[:8],
        "branch": os.getenv('GITHUB_REF', 'unknown').split('/')[-1],
        "actor": os.getenv('GITHUB_ACTOR', 'local-user'),
        "run_id": os.getenv('GITHUB_RUN_ID', 'local-run'),
        "workflow": os.getenv('GITHUB_WORKFLOW', 'Local Build'),
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "build_platform": os.name,
        "project_name": "Crocodile Analyzer",
        "project_version": "1.0.0"
    }
    
    with open('dist/build-info.json', 'w') as f:
        json.dump(build_info, f, indent=2)
    
    return build_info

def create_requirements_check():

    try:
        result = subprocess.run([sys.executable, '-m', 'pip', 'list', '--format=json'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            installed_packages = json.loads(result.stdout)
            with open('dist/installed-packages.json', 'w') as f:
                json.dump(installed_packages, f, indent=2)
            print(f" Documentadas {len(installed_packages)} dependências instaladas")
        else:
            print("  Não foi possível listar as dependências instaladas")
    except Exception as e:
        print(f"  Erro ao verificar dependências: {e}")

def package_application():

    print(" Iniciando empacotamento da aplicação...")
    
    
    if os.path.exists('dist'):
        shutil.rmtree('dist')
    os.makedirs('dist', exist_ok=True)
    
   
    essential_files = [
        'crocodile_analyzer_terminal.py',
        'crocodile_dataset.csv',
        'requirements.txt',
        'README.md'
    ]
    
 
    optional_files = [
        'test_crocodile_analyzer.py'
    ]
    

    for file in essential_files:
        if os.path.exists(file):
            shutil.copy2(file, 'dist/')
            print(f" Copiado: {file}")
        else:
            print(f" Arquivo essencial não encontrado: {file}")
            return False
    

    for file in optional_files:
        if os.path.exists(file):
            shutil.copy2(file, 'dist/')
            print(f"✅ Copiado (opcional): {file}")
    

    if os.path.exists('scripts'):
        shutil.copytree('scripts', 'dist/scripts')
        print("✅ Copiado: diretório scripts/")
    

    build_info = create_build_info()
    print(" Criado: build-info.json")
    

    create_requirements_check()
    

    create_installation_instructions()
    

    create_zip_package(build_info)
    create_tar_package(build_info)
    

    calculate_package_stats()
    
    print(" Empacotamento concluído com sucesso!")
    return True

def create_installation_instructions():

    instructions = """# Crocodile Analyzer - Instruções de Instalação

##  Requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

##  Instalação

1. Extrair o pacote:
   ```bash
   # Para arquivo .zip
   unzip crocodile-analyzer-*.zip
   cd crocodile-analyzer-*/
   
   # Para arquivo .tar.gz
   tar -xzf crocodile-analyzer-*.tar.gz
   cd crocodile-analyzer-*/
   ```

2. Instalar dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Executar a aplicação:
   ```bash
   python crocodile_analyzer_terminal.py
   ```

##  Executar Testes (se incluídos)
```bash
pip install pytest
pytest test_crocodile_analyzer.py -v
```

##  Arquivos Incluídos
- `crocodile_analyzer_terminal.py` - Aplicação principal
- `crocodile_dataset.csv` - Dataset de crocodilos
- `requirements.txt` - Dependências Python
- `README.md` - Documentação do projeto
- `build-info.json` - Informações da build
- `installed-packages.json` - Dependências documentadas
- `INSTALL.md` - Este arquivo

##   Informações da Build
Este pacote foi gerado automaticamente pelo pipeline CI/CD do projeto C14.
"""
    
    with open('dist/INSTALL.md', 'w') as f:
        f.write(instructions)
    
    print(" Criado: INSTALL.md")

def create_zip_package(build_info):

    version = build_info['project_version']
    commit = build_info['commit_sha']
    zip_filename = f"crocodile-analyzer-v{version}-{commit}.zip"
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk('dist'):
            for file in files:
                file_path = os.path.join(root, file)
                arc_name = os.path.relpath(file_path, 'dist')
                zipf.write(file_path, arc_name)
    
    print(f" Criado pacote ZIP: {zip_filename}")

def create_tar_package(build_info):

    version = build_info['project_version']
    commit = build_info['commit_sha']
    tar_filename = f"crocodile-analyzer-v{version}-{commit}.tar.gz"
    
    with tarfile.open(tar_filename, "w:gz") as tarf:
        for root, dirs, files in os.walk('dist'):
            for file in files:
                file_path = os.path.join(root, file)
                arc_name = os.path.relpath(file_path, 'dist')
                tarf.add(file_path, arcname=arc_name)
    
    print(f" Criado pacote TAR.GZ: {tar_filename}")

def calculate_package_stats():

    print("\n ESTATÍSTICAS DOS PACOTES:")
    print("-" * 40)
    
    for file in os.listdir('.'):
        if file.endswith(('.zip', '.tar.gz')) and 'crocodile-analyzer' in file:
            size = os.path.getsize(file)
            size_mb = size / (1024 * 1024)
            print(f"{file}: {size:,} bytes ({size_mb:.2f} MB)")

    dist_size = 0
    file_count = 0
    for root, dirs, files in os.walk('dist'):
        for file in files:
            file_path = os.path.join(root, file)
            dist_size += os.path.getsize(file_path)
            file_count += 1
    
    print(f"\nDiretório dist: {file_count} arquivos, {dist_size:,} bytes ({dist_size/(1024*1024):.2f} MB)")

def validate_package():
 
    print("\n Validando pacote...")
    
   
    essential_files = [
        'dist/crocodile_analyzer_terminal.py',
        'dist/crocodile_dataset.csv',
        'dist/requirements.txt',
        'dist/build-info.json'
    ]
    
    all_present = True
    for file in essential_files:
        if os.path.exists(file):
            print(f" {file}")
        else:
            print(f" {file}")
            all_present = False
    

    zip_files = [f for f in os.listdir('.') if f.endswith('.zip') and 'crocodile-analyzer' in f]
    tar_files = [f for f in os.listdir('.') if f.endswith('.tar.gz') and 'crocodile-analyzer' in f]
    
    if zip_files:
        print(f"Pacote ZIP criado: {zip_files[0]}")
    else:
        print(" Pacote ZIP não encontrado")
        all_present = False
    
    if tar_files:
        print(f" Pacote TAR.GZ criado: {tar_files[0]}")
    else:
        print(" Pacote TAR.GZ não encontrado")
        all_present = False
    
    return all_present

def main():
    
    print(" Iniciando processo de build...")
    
    try:
        success = package_application()
        if success and validate_package():
            print("\n BUILD CONCLUÍDA COM SUCESSO!")
            sys.exit(0)
        else:
            print("\n FALHA NA BUILD!")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n ERRO DURANTE A BUILD: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()