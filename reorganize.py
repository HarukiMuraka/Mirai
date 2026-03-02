#!/usr/bin/env python3
"""
Reorganizador Automático da Mirai

Este script reorganiza automaticamente a estrutura do projeto Mirai
para deixá-lo limpo, organizado e fácil de editar.

Uso:
    python reorganize.py [--dry-run]
    
    --dry-run: Simula sem fazer mudanças
"""

import os
import shutil
import sys
from pathlib import Path
from datetime import datetime


class MiraiReorganizer:
    """Reorganiza estrutura do projeto Mirai"""
    
    def __init__(self, dry_run=False):
        self.dry_run = dry_run
        self.root = Path.cwd()
        self.changes = []
        
        # Cores para output
        self.GREEN = '\033[92m'
        self.YELLOW = '\033[93m'
        self.RED = '\033[91m'
        self.BLUE = '\033[94m'
        self.RESET = '\033[0m'
    
    def log(self, message, color=''):
        """Log colorido"""
        print(f"{color}{message}{self.RESET}")
        self.changes.append(message)
    
    def create_backup(self):
        """Cria backup antes de reorganizar"""
        self.log("\n📦 CRIANDO BACKUP...", self.BLUE)
        
        backup_name = f"mirai_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        backup_path = self.root.parent / backup_name
        
        if not self.dry_run:
            try:
                shutil.copytree(self.root, backup_path, 
                               ignore=shutil.ignore_patterns('__pycache__', '*.pyc', '.git'))
                self.log(f"✓ Backup criado: {backup_path}", self.GREEN)
            except Exception as e:
                self.log(f"✗ Erro ao criar backup: {e}", self.RED)
                return False
        else:
            self.log(f"[DRY-RUN] Criaria backup em: {backup_path}", self.YELLOW)
        
        return True
    
    def create_directory_structure(self):
        """Cria estrutura de diretórios"""
        self.log("\n📁 CRIANDO ESTRUTURA DE DIRETÓRIOS...", self.BLUE)
        
        directories = [
            "mirai",
            "mirai/utils",
            "data",
            "data/cache",
            "data/memory", 
            "data/logs",
            "docs",
            "tools",
            "examples",
            "plugins",
            "plugins/examples",
            "tests",
        ]
        
        for dir_path in directories:
            full_path = self.root / dir_path
            if not self.dry_run:
                full_path.mkdir(parents=True, exist_ok=True)
                self.log(f"  ✓ {dir_path}/", self.GREEN)
            else:
                self.log(f"  [DRY-RUN] Criaria: {dir_path}/", self.YELLOW)
    
    def create_gitkeep_files(self):
        """Cria .gitkeep em pastas vazias"""
        self.log("\n📌 CRIANDO .gitkeep...", self.BLUE)
        
        gitkeep_dirs = [
            "data",
            "data/cache",
            "data/memory",
            "data/logs",
            "roms",
        ]
        
        for dir_path in gitkeep_dirs:
            gitkeep = self.root / dir_path / ".gitkeep"
            if not self.dry_run:
                gitkeep.parent.mkdir(parents=True, exist_ok=True)
                gitkeep.touch()
                self.log(f"  ✓ {dir_path}/.gitkeep", self.GREEN)
            else:
                self.log(f"  [DRY-RUN] Criaria: {dir_path}/.gitkeep", self.YELLOW)
    
    def move_code_to_package(self):
        """Move código para pacote mirai/"""
        self.log("\n📦 MOVENDO CÓDIGO PARA PACOTE...", self.BLUE)
        
        code_folders = [
            "actions",
            "core", 
            "interface",
            "modes",
            "perception",
            "research",
            "vtuber",
        ]
        
        for folder in code_folders:
            src = self.root / folder
            dst = self.root / "mirai" / folder
            
            if src.exists() and src.is_dir():
                if not self.dry_run:
                    if dst.exists():
                        shutil.rmtree(dst)
                    shutil.move(str(src), str(dst))
                    self.log(f"  ✓ {folder}/ → mirai/{folder}/", self.GREEN)
                else:
                    self.log(f"  [DRY-RUN] Moveria: {folder}/ → mirai/{folder}/", self.YELLOW)
        
        # Move main.py
        main_src = self.root / "main.py"
        main_dst = self.root / "mirai" / "main.py"
        
        if main_src.exists():
            if not self.dry_run:
                shutil.move(str(main_src), str(main_dst))
                self.log(f"  ✓ main.py → mirai/main.py", self.GREEN)
            else:
                self.log(f"  [DRY-RUN] Moveria: main.py → mirai/main.py", self.YELLOW)
    
    def move_test_scripts(self):
        """Move scripts de teste para tools/"""
        self.log("\n🔧 MOVENDO SCRIPTS DE TESTE...", self.BLUE)
        
        test_files = [
            "diagnostico_ollama.py",
            "diagnostico_voz.py",
            "testar_sistema.py",
            "testar_voz.py",
            "teste_voz_rapido.py",
            "corrigir_dependencias.py",
        ]
        
        for file in test_files:
            src = self.root / file
            dst = self.root / "tools" / file
            
            if src.exists():
                if not self.dry_run:
                    shutil.move(str(src), str(dst))
                    self.log(f"  ✓ {file} → tools/{file}", self.GREEN)
                else:
                    self.log(f"  [DRY-RUN] Moveria: {file} → tools/{file}", self.YELLOW)
    
    def delete_temp_files(self):
        """Deleta arquivos temporários"""
        self.log("\n🗑️  DELETANDO ARQUIVOS TEMPORÁRIOS...", self.BLUE)
        
        temp_files = [
            "texto_extraido.txt",
        ]
        
        for file in temp_files:
            path = self.root / file
            if path.exists():
                if not self.dry_run:
                    path.unlink()
                    self.log(f"  ✓ Deletado: {file}", self.GREEN)
                else:
                    self.log(f"  [DRY-RUN] Deletaria: {file}", self.YELLOW)
    
    def move_docs(self):
        """Move documentação para docs/"""
        self.log("\n📚 ORGANIZANDO DOCUMENTAÇÃO...", self.BLUE)
        
        # Move prompts para atualizacoes.txt se existir
        prompts = self.root / "prompts para atualizacoes.txt"
        if prompts.exists():
            dst = self.root / "docs" / "PROMPTS.md"
            if not self.dry_run:
                shutil.move(str(prompts), str(dst))
                self.log(f"  ✓ prompts... → docs/PROMPTS.md", self.GREEN)
            else:
                self.log(f"  [DRY-RUN] Moveria: prompts... → docs/PROMPTS.md", self.YELLOW)
    
    def create_run_script(self):
        """Cria run.py na raiz"""
        self.log("\n🚀 CRIANDO LAUNCHER...", self.BLUE)
        
        run_py = self.root / "run.py"
        
        content = '''#!/usr/bin/env python3
"""
Mirai Launcher

Inicia a assistente virtual Mirai
"""

import sys
from pathlib import Path

# Adiciona pasta mirai ao path
sys.path.insert(0, str(Path(__file__).parent))

from mirai.main import main

if __name__ == "__main__":
    main()
'''
        
        if not self.dry_run:
            with open(run_py, 'w', encoding='utf-8') as f:
                f.write(content)
            self.log(f"  ✓ Criado: run.py", self.GREEN)
        else:
            self.log(f"  [DRY-RUN] Criaria: run.py", self.YELLOW)
    
    def create_init_files(self):
        """Cria __init__.py onde necessário"""
        self.log("\n📝 CRIANDO __init__.py...", self.BLUE)
        
        init_dirs = [
            "mirai",
            "mirai/utils",
            "plugins",
            "tests",
        ]
        
        for dir_path in init_dirs:
            init_file = self.root / dir_path / "__init__.py"
            if not self.dry_run:
                if not init_file.exists():
                    init_file.touch()
                    self.log(f"  ✓ {dir_path}/__init__.py", self.GREEN)
            else:
                self.log(f"  [DRY-RUN] Criaria: {dir_path}/__init__.py", self.YELLOW)
    
    def update_gitignore(self):
        """Atualiza .gitignore"""
        self.log("\n🚫 ATUALIZANDO .gitignore...", self.BLUE)
        
        gitignore_content = '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
.venv

# IDE
.vscode/
.idea/
*.swp
*.swo

# Mirai específico
data/cache/*
data/memory/*
data/logs/*
!data/.gitkeep
!data/*/.gitkeep

config/gemini_key.txt
config/local_*.json
.env

# Temporários
*.tmp
*.log
temp/
temp_audio/

# Sistema
.DS_Store
Thumbs.db
'''
        
        gitignore = self.root / ".gitignore"
        
        if not self.dry_run:
            with open(gitignore, 'w', encoding='utf-8') as f:
                f.write(gitignore_content)
            self.log(f"  ✓ .gitignore atualizado", self.GREEN)
        else:
            self.log(f"  [DRY-RUN] Atualizaria: .gitignore", self.YELLOW)
    
    def create_basic_docs(self):
        """Cria documentação básica"""
        self.log("\n📖 CRIANDO DOCUMENTAÇÃO BÁSICA...", self.BLUE)
        
        docs = {
            "INSTALLATION.md": "# Guia de Instalação\n\nTODO: Adicionar instruções de instalação",
            "USAGE.md": "# Guia de Uso\n\nTODO: Adicionar instruções de uso",
            "PLUGINS.md": "# Como Criar Plugins\n\nTODO: Adicionar tutorial de plugins",
            "CONTRIBUTING.md": "# Como Contribuir\n\nTODO: Adicionar guia de contribuição",
            "FEATURES.md": "# Lista de Features\n\nTODO: Listar todas as features",
            "CHANGELOG.md": "# Changelog\n\n## v2.0.0 (Em Desenvolvimento)\n- Reorganização completa da estrutura",
        }
        
        for filename, content in docs.items():
            doc_path = self.root / "docs" / filename
            if not self.dry_run:
                with open(doc_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.log(f"  ✓ docs/{filename}", self.GREEN)
            else:
                self.log(f"  [DRY-RUN] Criaria: docs/{filename}", self.YELLOW)
    
    def show_summary(self):
        """Mostra resumo das mudanças"""
        self.log("\n" + "="*60, self.BLUE)
        self.log("RESUMO DA REORGANIZAÇÃO", self.BLUE)
        self.log("="*60, self.BLUE)
        
        if self.dry_run:
            self.log("\n⚠️  MODO DRY-RUN - Nenhuma mudança foi feita", self.YELLOW)
            self.log("Execute sem --dry-run para aplicar as mudanças", self.YELLOW)
        else:
            self.log("\n✅ REORGANIZAÇÃO CONCLUÍDA!", self.GREEN)
        
        self.log(f"\nTotal de operações: {len(self.changes)}", self.BLUE)
        
        self.log("\n📋 PRÓXIMOS PASSOS:", self.BLUE)
        if not self.dry_run:
            self.log("1. Teste a aplicação: python run.py", self.YELLOW)
            self.log("2. Corrija imports se necessário", self.YELLOW)
            self.log("3. Commit as mudanças: git add . && git commit", self.YELLOW)
        else:
            self.log("1. Revise as mudanças propostas", self.YELLOW)
            self.log("2. Execute sem --dry-run para aplicar", self.YELLOW)
    
    def run(self):
        """Executa reorganização completa"""
        self.log("🌸 MIRAI REORGANIZER", self.BLUE)
        self.log("="*60, self.BLUE)
        
        if self.dry_run:
            self.log("\n⚠️  MODO DRY-RUN ATIVADO", self.YELLOW)
            self.log("Simulando mudanças sem aplicá-las...\n", self.YELLOW)
        
        # Backup
        if not self.create_backup():
            self.log("\n❌ Erro ao criar backup. Abortando.", self.RED)
            return False
        
        # Executar reorganização
        try:
            self.create_directory_structure()
            self.create_gitkeep_files()
            self.move_code_to_package()
            self.move_test_scripts()
            self.delete_temp_files()
            self.move_docs()
            self.create_run_script()
            self.create_init_files()
            self.update_gitignore()
            self.create_basic_docs()
            
            self.show_summary()
            return True
        
        except Exception as e:
            self.log(f"\n❌ ERRO: {e}", self.RED)
            self.log("Restaure do backup se necessário", self.YELLOW)
            return False


def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Reorganiza estrutura do projeto Mirai"
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Simula sem fazer mudanças reais'
    )
    
    args = parser.parse_args()
    
    reorganizer = MiraiReorganizer(dry_run=args.dry_run)
    success = reorganizer.run()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()