import os
import argparse
from datetime import datetime

AUTHOR = "Luis Claudio De Vita"
YEAR = 2025
HEADER_TEMPLATE = f"""# Copyright (c) {YEAR} {AUTHOR}
# Licenciado sob MIT License (ver LICENSE no diretório raiz)
# ==========================================================
"""
# ================================================

def process_file(filepath: str, check_only: bool = False) -> bool:
    """
    Processa um arquivo individual
    Retorna True se o arquivo foi modificado/está correto
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Verifica se já tem cabeçalho
    if content.startswith('# Copyright'):
        return True
    
    if check_only:
        return False
    
    # Adiciona cabeçalho
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(HEADER_TEMPLATE + '\n' + content)
    return True

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true',
                       help='Modo verificação (não altera arquivos)')
    parser.add_argument('--exclude', nargs='+', 
                       default=['venv', '.git', '__pycache__', 'migrations'],
                       help='Diretórios para excluir')
    args = parser.parse_args()

    modified_files = []
    error_files = []

    for root, dirs, files in os.walk('.'):
        # Remove diretórios excluídos
        dirs[:] = [d for d in dirs if d not in args.exclude]
        
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                try:
                    success = process_file(filepath, args.check)
                    if not success:
                        error_files.append(filepath)
                    elif not args.check:
                        modified_files.append(filepath)
                except Exception as e:
                    print(f"Erro processando {filepath}: {str(e)}")
                    error_files.append(filepath)

    # Relatório
    if args.check:
        if error_files:
            print(f"\n❌ {len(error_files)} arquivos sem cabeçalho:")
            for f in error_files:
                print(f" - {f}")
            exit(1)
        else:
            print("✅ Todos os arquivos Python possuem cabeçalho de licença")
    else:
        print(f"\n✏️ {len(modified_files)} arquivos atualizados em {YEAR}:")
        for f in modified_files:
            print(f" - {f}")
        
        if error_files:
            print(f"\n⚠️ {len(error_files)} arquivos com erro:")
            for f in error_files:
                print(f" - {f}")

if __name__ == '__main__':
    main()