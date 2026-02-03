"""
TESTE DE INSTALAÇÃO - MIRAI v2.0
Verifica se todos os arquivos estão corretos
"""

import sys
from pathlib import Path
from colorama import Fore, Style, init

init(autoreset=True)

print(f"\n{Fore.CYAN}{'='*60}")
print(f"{Fore.MAGENTA}🔍 TESTE DE INSTALAÇÃO - MIRAI v2.0")
print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")

# Testes
tests_passed = 0
tests_failed = 0

def test(name, condition, error_msg=""):
    global tests_passed, tests_failed
    
    if condition:
        print(f"{Fore.GREEN}✓ {name}{Style.RESET_ALL}")
        tests_passed += 1
        return True
    else:
        print(f"{Fore.RED}✗ {name}{Style.RESET_ALL}")
        if error_msg:
            print(f"  {Fore.YELLOW}→ {error_msg}{Style.RESET_ALL}")
        tests_failed += 1
        return False

# 1. Versão Python
print(f"{Fore.YELLOW}[1/10] Python{Style.RESET_ALL}")
version = sys.version_info
test(
    f"Python {version.major}.{version.minor}.{version.micro}",
    version >= (3, 10),
    "Necessário Python 3.10+"
)

# 2. State Machine
print(f"\n{Fore.YELLOW}[2/10] State Machine{Style.RESET_ALL}")
try:
    from core.state_machine import SystemState
    
    has_principal = 'PRINCIPAL' in [s.name for s in SystemState]
    test(
        "Estado PRINCIPAL existe",
        has_principal,
        "Arquivo core/state_machine.py NÃO foi substituído!"
    )
    
    if has_principal:
        test("Pode criar estado principal", SystemState.PRINCIPAL.value == "principal")
except Exception as e:
    test("Import state_machine", False, str(e))

# 3. Modo Principal
print(f"\n{Fore.YELLOW}[3/10] Modo Principal{Style.RESET_ALL}")
try:
    from modes.modo_principal import ModoPrincipal
    test("Import modo_principal", True)
except Exception as e:
    test("Import modo_principal", False, str(e))

# 4. Menu
print(f"\n{Fore.YELLOW}[4/10] Menu{Style.RESET_ALL}")
try:
    from interface.menu import MenuPrincipal
    test("Import menu", True)
except Exception as e:
    test("Import menu", False, str(e))

# 5. Core
print(f"\n{Fore.YELLOW}[5/10] Core{Style.RESET_ALL}")
try:
    from core.ai_engine import MiraiAI
    test("AI Engine", True)
except Exception as e:
    test("AI Engine", False, str(e))

try:
    from core.context_manager import ContextManager
    test("Context Manager", True)
except Exception as e:
    test("Context Manager", False, str(e))

# 6. Actions
print(f"\n{Fore.YELLOW}[6/10] Actions{Style.RESET_ALL}")
try:
    from actions.speaker import Speaker
    test("Speaker", True)
except Exception as e:
    test("Speaker", False, str(e))

# 7. Perception
print(f"\n{Fore.YELLOW}[7/10] Perception{Style.RESET_ALL}")
try:
    from perception.text_input import TextInput
    test("Text Input", True)
except Exception as e:
    test("Text Input", False, str(e))

try:
    from perception.voice_listener import VoiceListener
    test("Voice Listener", True)
except Exception as e:
    test("Voice Listener", False, str(e))

# 8. VTuber
print(f"\n{Fore.YELLOW}[8/10] VTuber{Style.RESET_ALL}")
try:
    from vtuber.vrm_engine import VRMEngine
    test("VRM Engine", True)
except Exception as e:
    test("VRM Engine", False, str(e))

# 9. Dependências Extras
print(f"\n{Fore.YELLOW}[9/10] Dependências{Style.RESET_ALL}")

try:
    import pytesseract
    test("pytesseract", True)
except ImportError:
    test("pytesseract", False, "pip install pytesseract")

try:
    import cv2
    test("opencv-python", True)
except ImportError:
    test("opencv-python", False, "pip install opencv-python")

try:
    import numpy
    test("numpy", True)
except ImportError:
    test("numpy", False, "pip install numpy")

# 10. Estrutura de Pastas
print(f"\n{Fore.YELLOW}[10/10] Estrutura{Style.RESET_ALL}")

required_files = [
    "main.py",
    "core/state_machine.py",
    "core/ai_engine.py",
    "interface/menu.py",
    "modes/modo_principal.py",
]

for file in required_files:
    test(f"{file}", Path(file).exists(), f"Arquivo não encontrado: {file}")

# Resultado
print(f"\n{Fore.CYAN}{'='*60}")
print(f"{Fore.MAGENTA}📊 RESULTADO")
print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")

total = tests_passed + tests_failed
percentage = (tests_passed / total * 100) if total > 0 else 0

print(f"  Testes aprovados: {Fore.GREEN}{tests_passed}{Style.RESET_ALL}")
print(f"  Testes falhados:  {Fore.RED}{tests_failed}{Style.RESET_ALL}")
print(f"  Total:            {total}")
print(f"  Porcentagem:      {Fore.YELLOW}{percentage:.1f}%{Style.RESET_ALL}\n")

if tests_failed == 0:
    print(f"{Fore.GREEN}╔════════════════════════════════════════╗")
    print(f"{Fore.GREEN}║  ✅ TUDO CERTO! PODE EXECUTAR! ✅     ║")
    print(f"{Fore.GREEN}╚════════════════════════════════════════╝{Style.RESET_ALL}\n")
    print(f"{Fore.CYAN}Execute: python main.py{Style.RESET_ALL}\n")
else:
    print(f"{Fore.RED}╔════════════════════════════════════════╗")
    print(f"{Fore.RED}║  ❌ ERROS ENCONTRADOS ❌              ║")
    print(f"{Fore.RED}╚════════════════════════════════════════╝{Style.RESET_ALL}\n")
    
    print(f"{Fore.YELLOW}AÇÕES NECESSÁRIAS:{Style.RESET_ALL}\n")
    
    if 'PRINCIPAL' not in str(sys.modules.get('core.state_machine', '')):
        print(f"{Fore.RED}1. Substituir core/state_machine.py{Style.RESET_ALL}")
        print(f"   Arquivo atual NÃO tem o estado PRINCIPAL\n")
    
    if 'ModoPrincipal' not in str(sys.modules.get('modes.modo_principal', '')):
        print(f"{Fore.RED}2. Criar modes/modo_principal.py{Style.RESET_ALL}")
        print(f"   Arquivo não existe ou não pode ser importado\n")
    
    print(f"{Fore.CYAN}Consulte: INSTALACAO.md{Style.RESET_ALL}\n")

print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")