import asyncio
import sys
import os
from pathlib import Path
from colorama import init, Fore, Style

# Path
sys.path.insert(0, str(Path(__file__).parent))

# Imports otimizados
from mirai.core.ai_engine import MiraiAI
from mirai.core.context_manager import ContextManager
from mirai.actions.speaker import Speaker
from mirai.actions.app_launcher import AppLauncher
from mirai.interface.menu import MenuPrincipal
from mirai.perception.text_input import TextInput
init(autoreset=True)


class Mirai:
    """Mirai v2.0 - Otimizada e Unificada"""
    
    def __init__(self):
        self.print_startup()
        
        # Componentes principais
        self.ai = None
        self.vtuber = None
        self.state = None
        self.context = None
        self.menu = None
        self.speaker = None
        self.running = False
    
    def print_startup(self):
        """Banner de inicialização"""
        print(f"\n{Fore.MAGENTA}{'='*60}")
        print(f"{Fore.MAGENTA}          🌸 MIRAI v2.0 - INICIANDO 🌸")
        print(f"{Fore.MAGENTA}{'='*60}{Style.RESET_ALL}\n")
    
    async def initialize(self):
        """Inicialização OTIMIZADA"""
        print(f"{Fore.CYAN}[1/6] Iniciando sistemas...{Style.RESET_ALL}\n")
        
        try:
            # Context Manager (rápido)
            print(f"{Fore.YELLOW}→ Context Manager...{Style.RESET_ALL}", end=' ')
            self.context = ContextManager()
            print(f"{Fore.GREEN}✓{Style.RESET_ALL}")
            
            # State Machine (rápido)
            print(f"{Fore.YELLOW}→ State Machine...{Style.RESET_ALL}", end=' ')
            self.state = StateMachine()
            print(f"{Fore.GREEN}✓{Style.RESET_ALL}")
            
            # IA Engine (pode demorar)
            print(f"{Fore.YELLOW}→ IA Engine...{Style.RESET_ALL}")
            self.ai = MiraiAI(self.context)
            await self.ai.initialize()
            
            # Speaker/TTS (pode demorar)
            print(f"{Fore.YELLOW}→ Sistema de Voz...{Style.RESET_ALL}")
            self.speaker = Speaker()
            await self.speaker.initialize()
            
            # VTuber (opcional, não bloqueia)
            print(f"{Fore.YELLOW}→ VTuber Engine...{Style.RESET_ALL}", end=' ')
            self.vtuber = VTuberEngine()
            
            # Tenta inicializar VTuber (não bloqueia se falhar)
            try:
                vtuber_ready = await asyncio.wait_for(
                    self.vtuber.initialize(),
                    timeout=3.0  # Timeout de 3s
                )
                if vtuber_ready:
                    print(f"{Fore.GREEN}✓{Style.RESET_ALL}")
                else:
                    print(f"{Fore.YELLOW}○ (modo texto){Style.RESET_ALL}")
            except asyncio.TimeoutError:
                print(f"{Fore.YELLOW}○ (timeout){Style.RESET_ALL}")
            except:
                print(f"{Fore.YELLOW}○ (não disponível){Style.RESET_ALL}")
            
            # Menu
            print(f"{Fore.YELLOW}→ Interface...{Style.RESET_ALL}", end=' ')
            self.menu = MenuPrincipal(self)
            print(f"{Fore.GREEN}✓{Style.RESET_ALL}")
            
            print(f"\n{Fore.GREEN}✓ Todos os sistemas prontos!{Style.RESET_ALL}\n")
            self.running = True
            return True
            
        except Exception as e:
            print(f"\n{Fore.RED}✗ Erro: {e}{Style.RESET_ALL}")
            import traceback
            traceback.print_exc()
            return False
    
    async def run(self):
        """Loop principal"""
        if not await self.initialize():
            print(f"{Fore.RED}Falha na inicialização!{Style.RESET_ALL}")
            return
        
        # Saudação
        greeting = self.ai.generate_greeting()
        print(f"{Fore.MAGENTA}Mirai: {greeting}{Style.RESET_ALL}\n")
        
        # Fala de forma assíncrona (não trava)
        asyncio.create_task(self._speak_async(greeting))
        
        # VTuber expressão
        if self.vtuber and self.vtuber.is_active:
            await self.vtuber.set_expression("happy")
        
        # Menu principal
        await self.menu.show()
    
    async def shutdown(self):
        """Encerramento OTIMIZADO"""
        print(f"\n{Fore.CYAN}Encerrando Mirai...{Style.RESET_ALL}")
        
        # Despedida
        farewell = self.ai.generate_farewell()
        print(f"{Fore.MAGENTA}Mirai: {farewell}{Style.RESET_ALL}")
        
        # Fala (não espera terminar)
        try:
            self.speaker.speak(farewell)
        except:
            pass
        
        # VTuber
        if self.vtuber and self.vtuber.is_active:
            await self.vtuber.set_expression("sad")
            await self.vtuber.stop()
        
        self.running = False
        print(f"{Fore.GREEN}Até logo! ✨{Style.RESET_ALL}\n")
    
    async def _speak_async(self, text):
        """Fala assíncrona"""
        import threading
        thread = threading.Thread(target=self.speaker.speak, args=(text,), daemon=True)
        thread.start()


async def main():
    """Main assíncrono"""
    mirai = Mirai()
    
    try:
        await mirai.run()
    
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[INTERROMPIDO]{Style.RESET_ALL}")
    
    except Exception as e:
        print(f"{Fore.RED}[ERRO] {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()
    
    finally:
        await mirai.shutdown()


if __name__ == "__main__":
    # Verifica Python 3.10+
    if sys.version_info < (3, 10):
        print(f"{Fore.RED}Erro: Python 3.10+ necessário!{Style.RESET_ALL}")
        print(f"Versão atual: {sys.version}")
        sys.exit(1)
    
    # Roda
    asyncio.run(main())