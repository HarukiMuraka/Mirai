import sys
import asyncio
from colorama import init, Fore, Style
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from interface.menu import MainMenu
from core.ai_engine import MiraiAI
from core.state_machine import StateMachine
from core.context_manager import ContextManager
from vtuber.vrm_engine import VRMEngine  # Mudou para VRM!
from perception.voice_listener import VoiceListener
from actions.speaker import Speaker
from memory.sistema_memoria import MemoriaCompleta

# NOVO: Importar features
from features import (
    VoiceInterruptionSystem,
    EnhancedSpeaker,
    ProactiveEventsSystem,
    InnerThoughtsSystem,
    AutoExpressionMapper,
    CameraVisionSystem
)

init(autoreset=True)

class Mirai:
    """Classe principal da Mirai COM TODAS AS FEATURES!"""
    
    def __init__(self):
        self.print_banner()
        self.ai = None
        self.vtuber = None
        self.state = None
        self.context = None
        self.menu = None
        self.voice = None
        self.speaker = None
        self.memoria = None
        
        # NOVO: Features avançadas
        self.voice_interruption = None
        self.proactive_events = None
        self.inner_thoughts = None
        self.auto_expression = None
        self.camera_vision = None
        
        self.running = False
        
    def print_banner(self):
        """Mostra o banner inicial"""
        print(f"\n{Fore.MAGENTA}╔═══════════════════════════════════╗")
        print(f"{Fore.MAGENTA}║        🌸 MIRAI v2.0 🌸          ║")
        print(f"{Fore.MAGENTA}║  IA VTuber com Open-LLM Features  ║")
        print(f"{Fore.MAGENTA}╚═══════════════════════════════════╝{Style.RESET_ALL}\n")
        
    async def initialize(self):
        """Inicializa todos os componentes"""
        print(f"{Fore.CYAN}[INFO] Iniciando sistemas da Mirai v2.0...{Style.RESET_ALL}\n")
        
        try:
            # Context Manager
            print(f"{Fore.YELLOW}→ Inicializando gerenciador de contexto...{Style.RESET_ALL}")
            self.context = ContextManager()
            
            # State Machine
            print(f"{Fore.YELLOW}→ Inicializando máquina de estados...{Style.RESET_ALL}")
            self.state = StateMachine()
            
            # IA Engine
            print(f"{Fore.YELLOW}→ Carregando modelo de IA...{Style.RESET_ALL}")
            self.ai = MiraiAI(self.context)
            await self.ai.initialize()
            
            # Speaker (TTS)
            print(f"{Fore.YELLOW}→ Inicializando sistema de voz...{Style.RESET_ALL}")
            self.speaker = Speaker()
            await self.speaker.initialize()
            
            # VTuber Engine (VRM)
            print(f"{Fore.YELLOW}→ Inicializando VRM Engine...{Style.RESET_ALL}")
            self.vtuber = VRMEngine()
            vtuber_ready = await self.vtuber.initialize()
            
            # Voice Listener
            print(f"{Fore.YELLOW}→ Inicializando reconhecimento de voz...{Style.RESET_ALL}")
            self.voice = VoiceListener()
            
            # Sistema de Memória
            print(f"{Fore.YELLOW}→ Inicializando sistema de memória...{Style.RESET_ALL}")
            self.memoria = MemoriaCompleta()
            stats = self.memoria.get_estatisticas()
            print(f"  ✓ Memória carregada ({stats['total_conversas']} conversas)")
            
            # ===== NOVO: Inicializar Features Avançadas =====
            
            print(f"\n{Fore.CYAN}[INFO] Inicializando features avançadas...{Style.RESET_ALL}")
            
            # 1. Voice Interruption
            print(f"{Fore.YELLOW}→ Sistema de Interrupção de Voz...{Style.RESET_ALL}")
            enhanced_speaker = EnhancedSpeaker(self.speaker)
            self.voice_interruption = VoiceInterruptionSystem(self.voice, enhanced_speaker)
            self.voice_interruption.start_monitoring()
            print(f"{Fore.GREEN}  ✓ Interrupção de voz ativa!{Style.RESET_ALL}")
            
            # 2. Inner Thoughts
            print(f"{Fore.YELLOW}→ Sistema de Pensamentos Internos...{Style.RESET_ALL}")
            self.inner_thoughts = InnerThoughtsSystem(self.ai)
            self.inner_thoughts.enable()
            
            # 3. Auto Expression Mapper
            print(f"{Fore.YELLOW}→ Mapeamento Automático de Expressões...{Style.RESET_ALL}")
            self.auto_expression = AutoExpressionMapper(self.vtuber)
            self.auto_expression.enable()
            
            # 4. Proactive Events
            print(f"{Fore.YELLOW}→ Sistema de Eventos Proativos...{Style.RESET_ALL}")
            self.proactive_events = ProactiveEventsSystem(self.ai, enhanced_speaker)
            await self.proactive_events.start()
            
            # 5. Camera Vision (opcional)
            print(f"{Fore.YELLOW}→ Sistema de Visão por Câmera...{Style.RESET_ALL}")
            self.camera_vision = CameraVisionSystem(self.ai)
            if self.camera_vision.initialize():
                print(f"{Fore.GREEN}  ✓ Câmera disponível!{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}  ⚠ Câmera não disponível (opcional){Style.RESET_ALL}")
            
            # Menu
            self.menu = MainMenu(self)
            
            print(f"\n{Fore.GREEN}✨ Todos os sistemas prontos! (Mirai v2.0){Style.RESET_ALL}\n")
            self.running = True
            return True
            
        except Exception as e:
            print(f"{Fore.RED}✗ Erro na inicialização: {e}{Style.RESET_ALL}")
            import traceback
            traceback.print_exc()
            return False
    
    async def run(self):
        """Loop principal"""
        if not await self.initialize():
            return
        
        # Saudação inicial
        greeting = self.ai.generate_greeting()
        print(f"{Fore.MAGENTA}Mirai: {greeting}{Style.RESET_ALL}\n")
        
        # Fala com expressão
        if self.auto_expression:
            await self.auto_expression.auto_set_expression(greeting)
        
        self.speaker.speak(greeting)
        
        # Mostrar menu
        await self.menu.show()
    
    async def shutdown(self):
        """Encerra o sistema"""
        print(f"\n{Fore.CYAN}[INFO] Encerrando Mirai...{Style.RESET_ALL}")
        
        # Para features
        if self.proactive_events:
            self.proactive_events.stop()
        
        if self.voice_interruption:
            self.voice_interruption.stop_monitoring()
        
        if self.camera_vision:
            self.camera_vision.shutdown()
        
        # Salva memória
        if self.memoria and self.context:
            print(f"{Fore.CYAN}Salvando conversas...{Style.RESET_ALL}")
            recent = self.context.get_recent_context(10)
            
            for i in range(0, len(recent) - 1, 2):
                if recent[i]['role'] == 'user' and i + 1 < len(recent):
                    if recent[i + 1]['role'] == 'assistant':
                        self.memoria.salvar_conversa(
                            recent[i]['content'],
                            recent[i + 1]['content']
                        )
        
        # Despedida
        farewell = self.ai.generate_farewell()
        print(f"{Fore.MAGENTA}Mirai: {farewell}{Style.RESET_ALL}")
        
        if self.auto_expression:
            await self.auto_expression.auto_set_expression(farewell)
        
        self.speaker.speak(farewell)
        
        if self.vtuber and self.vtuber.is_active:
            await self.vtuber.stop()
        
        self.running = False
        print(f"{Fore.GREEN}Até logo! ✨{Style.RESET_ALL}\n")

async def main():
    mirai = Mirai()
    try:
        await mirai.run()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[INFO] Interrompido pelo usuário{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[ERRO] {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()
    finally:
        await mirai.shutdown()

if __name__ == "__main__":
    asyncio.run(main())