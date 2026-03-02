from mirai.modes.base_mode import BaseMode
from mirai.perception.text_input import TextInput
from colorama import Fore, Style
import asyncio
import time

class ConversationMode(BaseMode):
    def __init__(self, mirai_instance):
        super().__init__(mirai_instance)
        self.listening = False
        self.autonomous_active = False
        
    async def enter(self):
        self.is_active = True
        self.state.set_state("conversation")
        self.print_mode_header("MODO CONVERSA")
        
        print(f"{Fore.YELLOW}Escolha o tipo de conversa:{Style.RESET_ALL}")
        print("1. 💬 Por Texto (Recomendado)")
        print("2. 🎤 Por Voz (precisa SpeechRecognition)")
        print("3. 🤖 Conversa Autônoma (Mirai inicia conversas)")
        print("0. ⬅️  Voltar")
        
        choice = input(f"\n{Fore.MAGENTA}Opção: {Style.RESET_ALL}")
        
        if choice == "1":
            await self.text_conversation()
        elif choice == "2":
            await self.voice_conversation()
        elif choice == "3":
            await self.autonomous_conversation()
    
    async def exit(self):
        self.is_active = False
        self.autonomous_active = False
        print(f"\n{Fore.CYAN}Saindo do modo conversa...{Style.RESET_ALL}")
    
    async def process_input(self, user_input, enable_search=True):
        """Processa input"""
        if not user_input or user_input.strip() == "":
            return None
        
        if user_input.lower() in ['sair', 'exit', 'voltar', 'parar', 'tchau']:
            return "EXIT"
        
        # Gera resposta
        response = self.ai.generate_response(
            user_input, 
            mode="conversation", 
            enable_search=enable_search
        )
        
        return response
    
    async def text_conversation(self):
        """Conversa por texto - PRINCIPAL"""
        print(f"\n{Fore.GREEN}💬 Modo texto ativado!{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Dica: Fale naturalmente! Eu entendo contexto.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Digite 'sair' para voltar{Style.RESET_ALL}\n")
        
        # Saudação
        greeting = self.ai.generate_greeting()
        print(f"{Fore.MAGENTA}Mirai: {greeting}{Style.RESET_ALL}\n")
        
        if self.speaker.enabled:
            await asyncio.to_thread(self.speaker.speak, greeting)
        
        text_input = TextInput()
        
        while self.is_active:
            user_input = text_input.get_input(f"{Fore.GREEN}Você: {Style.RESET_ALL}")
            
            if not user_input:
                continue
            
            print(f"{Fore.CYAN}💭 Pensando...{Style.RESET_ALL}", end='\r')
            
            result = await self.process_input(user_input)
            
            print(" " * 50, end='\r')
            
            if result == "EXIT":
                farewell = "Até logo! Foi legal conversar!"
                print(f"{Fore.MAGENTA}Mirai: {farewell}{Style.RESET_ALL}\n")
                if self.speaker.enabled:
                    await asyncio.to_thread(self.speaker.speak, farewell)
                break
            
            if result:
                print(f"{Fore.MAGENTA}Mirai: {result}{Style.RESET_ALL}\n")
                
                # Fala se tiver speaker
                if self.speaker.enabled:
                    # Resumo para fala (primeiras 2 frases)
                    speech_text = '.'.join(result.split('.')[:2]) + '.'
                    if len(speech_text) < 200:
                        await asyncio.to_thread(self.speaker.speak, speech_text)
    
    async def voice_conversation(self):
        """Conversa por voz"""
        try:
            from mirai.perception.voice_listener import VoiceListener
        except ImportError:
            print(f"{Fore.RED}❌ SpeechRecognition não instalado!{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Instale: pip install SpeechRecognition{Style.RESET_ALL}\n")
            input("Pressione Enter...")
            return
        
        print(f"\n{Fore.GREEN}🎤 Modo voz ativado!{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Diga 'sair' para voltar{Style.RESET_ALL}\n")
        
        voice = VoiceListener()
        if not voice.initialize():
            print(f"{Fore.RED}Erro ao inicializar microfone!{Style.RESET_ALL}")
            input("Pressione Enter...")
            return
        
        voice.recognizer.pause_threshold = 1.0
        voice.recognizer.phrase_time_limit = 10
        
        while self.is_active:
            try:
                print(f"{Fore.CYAN}🎤 Escutando...{Style.RESET_ALL}", end='\r')
                
                user_input = voice.listen_once()
                
                print(" " * 50, end='\r')
                
                if not user_input:
                    continue
                
                print(f"{Fore.CYAN}Você: {user_input}{Style.RESET_ALL}")
                print(f"{Fore.CYAN}💭 Pensando...{Style.RESET_ALL}", end='\r')
                
                result = await self.process_input(user_input)
                
                print(" " * 50, end='\r')
                
                if result == "EXIT":
                    break
                
                if result:
                    print(f"{Fore.MAGENTA}Mirai: {result}{Style.RESET_ALL}\n")
                    
                    if self.speaker.enabled:
                        await asyncio.to_thread(self.speaker.speak, result)
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"{Fore.RED}Erro: {e}{Style.RESET_ALL}")
    
    async def autonomous_conversation(self):
        """Conversa autônoma - Mirai toma iniciativa"""
        print(f"\n{Fore.GREEN}🤖 Modo Autônomo Ativado!{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Mirai vai conversar e tomar iniciativa!{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Ela fala se você ficar em silêncio por 20-30s{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Digite 'parar' para sair{Style.RESET_ALL}\n")
        
        # Saudação
        greeting = self.ai.generate_greeting()
        print(f"{Fore.MAGENTA}Mirai: {greeting}{Style.RESET_ALL}\n")
        
        if self.speaker.enabled:
            await asyncio.to_thread(self.speaker.speak, greeting)
        
        self.autonomous_active = True
        text_input = TextInput()
        last_interaction = time.time()
        silence_threshold = 25  # segundos
        
        while self.is_active and self.autonomous_active:
            # Check timeout para iniciativa
            time_since_last = time.time() - last_interaction
            
            if time_since_last >= silence_threshold:
                # Mirai toma iniciativa
                initiative = self.ai.generate_initiative()
                
                print(f"{Fore.YELLOW}[Mirai percebe o silêncio]{Style.RESET_ALL}")
                print(f"{Fore.MAGENTA}Mirai: {initiative}{Style.RESET_ALL}\n")
                
                if self.speaker.enabled:
                    await asyncio.to_thread(self.speaker.speak, initiative)
                
                last_interaction = time.time()
                continue
            
            # Input com timeout
            print(f"{Fore.GREEN}Você: {Style.RESET_ALL}", end='', flush=True)
            
            try:
                # Input não-bloqueante
                import select
                import sys
                
                # Windows não tem select para stdin, então usamos input normal
                if sys.platform == 'win32':
                    user_input = input()
                else:
                    # Unix-like: input com timeout
                    ready, _, _ = select.select([sys.stdin], [], [], 5)
                    if ready:
                        user_input = sys.stdin.readline().strip()
                    else:
                        continue
                
                if not user_input:
                    continue
                
                last_interaction = time.time()
                
                if user_input.lower() in ['parar', 'sair', 'exit']:
                    farewell = "Entendido! Foi legal conversar!"
                    print(f"\n{Fore.MAGENTA}Mirai: {farewell}{Style.RESET_ALL}")
                    if self.speaker.enabled:
                        await asyncio.to_thread(self.speaker.speak, farewell)
                    break
                
                print(f"{Fore.CYAN}💭 Pensando...{Style.RESET_ALL}", end='\r')
                
                result = await self.process_input(user_input, enable_search=True)
                
                print(" " * 50, end='\r')
                
                if result and result != "EXIT":
                    print(f"{Fore.MAGENTA}Mirai: {result}{Style.RESET_ALL}\n")
                    
                    if self.speaker.enabled:
                        await asyncio.to_thread(self.speaker.speak, result)
                
            except Exception as e:
                print(f"\n{Fore.RED}Erro: {e}{Style.RESET_ALL}")
                continue