import customtkinter as ctk
import tkinter as tk
import threading
import time
from .utils.router import Router
from .utils.config import get_settings
from .skills.time_skill import TimeSkill
from .skills.notes_skill import NotesSkill
from .skills.apps_skill import AppsSkill
from .skills.joke_skill import JokeSkill
from .skills.calc_skill import CalcSkill
from .skills.wikipedia_skill import WikipediaSkill
from .skills.weather_skill import WeatherSkill

class VoiceAssistantGUI:
    def __init__(self):
        # Set appearance mode and color theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        
        # Create main window
        self.root = ctk.CTk()
        self.root.title("HexSoftwares Voice Assistant")
        self.root.geometry("400x700")  # Mobile-like dimensions
        self.root.minsize(350, 600)
        
        # Configure grid
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        
        # Initialize router
        settings = get_settings()
        self.router = Router([
            TimeSkill(settings.locale),
            NotesSkill(),
            AppsSkill(),
            JokeSkill(),
            CalcSkill(),
            WikipediaSkill(),
            WeatherSkill(),
        ])
        
        # Create GUI elements
        self.create_widgets()
        
        # Voice state
        self.voice_mode = False
        self.is_listening = False
        self.voice_thread = None
        
    def create_widgets(self):
        # Status bar (simulated)
        status_frame = ctk.CTkFrame(self.root, fg_color="#000000", height=30)
        status_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        status_frame.grid_columnconfigure(0, weight=1)
        
        # Status bar content
        status_label = ctk.CTkLabel(
            status_frame,
            text="03:52  DND  5G  79%",
            font=ctk.CTkFont(size=12),
            text_color="#FFFFFF"
        )
        status_label.grid(row=0, column=0, padx=15, pady=5)
        
        # Upper control bar
        upper_controls = ctk.CTkFrame(self.root, fg_color="transparent", height=50)
        upper_controls.grid(row=1, column=0, sticky="ew", padx=20, pady=(10, 0))
        upper_controls.grid_columnconfigure(4, weight=1)
        
        # Control buttons (i, CC, share, settings)
        controls = ["i", "CC", "↑", "≡"]
        for i, control in enumerate(controls):
            btn = ctk.CTkButton(
                upper_controls,
                text=control,
                font=ctk.CTkFont(size=14),
                width=40,
                height=40,
                corner_radius=20,
                fg_color="#2A2A2A",
                hover_color="#3A3A3A",
                text_color="#FFFFFF"
            )
            btn.grid(row=0, column=i, padx=5)
        
        # Main content area
        main_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        main_frame.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)
        
        # Chat display
        self.chat_display = ctk.CTkTextbox(
            main_frame,
            font=ctk.CTkFont(size=14),
            fg_color="#000000",
            text_color="#FFFFFF",
            wrap="word",
            border_width=0
        )
        self.chat_display.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        
        # Scrollbar for chat
        chat_scrollbar = ctk.CTkScrollbar(main_frame, command=self.chat_display.yview)
        chat_scrollbar.grid(row=0, column=1, sticky="ns")
        self.chat_display.configure(yscrollcommand=chat_scrollbar.set)
        
        # Welcome section
        welcome_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        welcome_frame.grid(row=3, column=0, pady=20, sticky="ew")
        welcome_frame.grid_columnconfigure(0, weight=1)
        
        # Welcome title
        welcome_title = ctk.CTkLabel(
            welcome_frame,
            text="HexSoftwares AI Assistant",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#4A90E2"
        )
        welcome_title.pack(pady=(0, 10))
        
        # Welcome subtitle
        welcome_subtitle = ctk.CTkLabel(
            welcome_frame,
            text="Your intelligent companion",
            font=ctk.CTkFont(size=16),
            text_color="#CCCCCC"
        )
        welcome_subtitle.pack(pady=(0, 20))
        
        # Quick actions frame
        quick_actions = ctk.CTkFrame(welcome_frame, fg_color="#1A1A1A", corner_radius=15)
        quick_actions.pack(fill="x", padx=20, pady=10)
        
        # Quick action buttons
        actions = [
            ("Time", "time"),
            ("Date", "date"),
            ("Calculator", "calc 2+2"),
            ("Joke", "joke"),
            ("System Info", "system info"),
            ("AI Chat", "chat hello")
        ]
        
        # Voice control frame
        voice_frame = ctk.CTkFrame(welcome_frame, fg_color="#1A1A1A", corner_radius=15)
        voice_frame.pack(fill="x", padx=20, pady=10)
        
        # Voice control label
        voice_label = ctk.CTkLabel(
            voice_frame,
            text="Voice Controls",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#4A90E2"
        )
        voice_label.pack(pady=(15, 10))
        
        # Voice buttons frame
        voice_buttons = ctk.CTkFrame(voice_frame, fg_color="transparent")
        voice_buttons.pack(fill="x", padx=15, pady=(0, 15))
        
        # Voice control buttons
        voice_actions = [
            ("Listen", self.start_voice_listening),
            ("Stop", self.stop_voice_listening),
            ("Voice Mode", self.toggle_voice_mode)
        ]
        
        for i, (text, command) in enumerate(voice_actions):
            btn = ctk.CTkButton(
                voice_buttons,
                text=text,
                font=ctk.CTkFont(size=12),
                height=30,
                fg_color="#2A2A2A",
                hover_color="#4A90E2",
                text_color="#FFFFFF",
                command=command
            )
            btn.pack(side="left", padx=5, expand=True)
        
        for i, (text, command) in enumerate(actions):
            btn = ctk.CTkButton(
                quick_actions,
                text=text,
                font=ctk.CTkFont(size=14),
                height=35,
                fg_color="#2A2A2A",
                hover_color="#4A90E2",
                text_color="#FFFFFF",
                command=lambda cmd=command: self.quick_action(cmd)
            )
            btn.pack(fill="x", padx=15, pady=5)
        
        # Bottom control bar
        bottom_controls = ctk.CTkFrame(self.root, fg_color="transparent", height=80)
        bottom_controls.grid(row=4, column=0, sticky="ew", padx=20, pady=(0, 20))
        bottom_controls.grid_columnconfigure(4, weight=1)
        
        # Bottom control buttons (clear, settings, about, close)
        bottom_btns = ["Clear", "Settings", "About", "Close"]
        bottom_commands = [self.clear_chat, self.show_settings, self.show_about, self.close_app]
        
        for i, (btn_text, command) in enumerate(zip(bottom_btns, bottom_commands)):
            btn = ctk.CTkButton(
                bottom_controls,
                text=btn_text,
                font=ctk.CTkFont(size=16),
                width=50,
                height=50,
                corner_radius=25,
                fg_color="#2A2A2A",
                hover_color="#3A3A3A",
                text_color="#FFFFFF",
                command=command
            )
            btn.grid(row=0, column=i, padx=5)
        
        # Gesture indicator
        gesture_indicator = ctk.CTkFrame(bottom_controls, fg_color="#FFFFFF", width=40, height=4)
        gesture_indicator.grid(row=1, column=2, pady=(10, 0))
        
        # Input frame (always visible)
        self.input_frame = ctk.CTkFrame(self.root, fg_color="#1A1A1A", corner_radius=15)
        self.input_frame.grid(row=5, column=0, padx=20, pady=(20, 20), sticky="ew")
        self.input_frame.grid_columnconfigure(0, weight=1)
        
        # Text input
        self.text_input = ctk.CTkEntry(
            self.input_frame,
            placeholder_text="Type your message or command...",
            font=ctk.CTkFont(size=14),
            height=45,
            fg_color="#2A2A2A",
            text_color="#FFFFFF",
            border_color="#4A90E2",
            corner_radius=10
        )
        self.text_input.grid(row=0, column=0, sticky="ew", padx=(15, 10), pady=15)
        self.text_input.bind("<Return>", self.handle_text_input)
        
        # Send button
        send_button = ctk.CTkButton(
            self.input_frame,
            text="Send",
            font=ctk.CTkFont(size=14, weight="bold"),
            width=90,
            height=45,
            fg_color="#4A90E2",
            hover_color="#357ABD",
            corner_radius=10,
            command=self.handle_text_input
        )
        send_button.grid(row=0, column=1, padx=(0, 15), pady=15)
        
        # Welcome message
        self.add_message("Assistant", "Hello! I'm your HexSoftwares Voice Assistant. How can I help you today?")
        
    def quick_action(self, command):
        """Handle quick action button clicks"""
        self.add_message("You", command)
        response = self.router.dispatch(command)
        self.add_message("Assistant", response)
    
    def clear_chat(self):
        """Clear the chat display"""
        self.chat_display.delete(1.0, tk.END)
        self.add_message("System", "Chat cleared!")
    
    def show_settings(self):
        """Show settings information"""
        self.add_message("System", "Settings:\n• Theme: Dark\n• Language: English\n• Voice: Disabled\n• Auto-save: Enabled")
    
    def show_about(self):
        """Show about information"""
        self.add_message("System", "About HexSoftwares AI Assistant:\n• Version: 1.0.0\n• Built with Python & CustomTkinter\n• Created for Hex Softwares Internship\n• Features: Time, Calculator, Notes, Jokes, App Control")
    
    def start_voice_listening(self):
        """Start voice listening"""
        if self.is_listening:
            return
        
        self.is_listening = True
        self.add_message("System", "Listening... Speak now!")
        
        # Start voice thread
        self.voice_thread = threading.Thread(target=self._voice_listen, daemon=True)
        self.voice_thread.start()
    
    def stop_voice_listening(self):
        """Stop voice listening"""
        self.is_listening = False
        self.add_message("System", "Voice listening stopped.")
        
        # Wait for voice thread to finish if it exists
        if self.voice_thread and self.voice_thread.is_alive():
            self.voice_thread.join(timeout=1.0)
    
    def toggle_voice_mode(self):
        """Toggle voice mode on/off"""
        self.voice_mode = not self.voice_mode
        status = "enabled" if self.voice_mode else "disabled"
        self.add_message("System", f"Voice mode {status}.")
    
    def _voice_listen(self):
        """Voice listening thread"""
        try:
            # Use a simpler voice input method for GUI
            text = self._simple_voice_input()
            if text and self.is_listening:
                # Use after() to safely update GUI from main thread
                self.after(0, lambda: self._process_voice_input(text))
        except Exception as e:
            self.after(0, lambda: self.add_message("System", f"Voice error: {e}"))
        finally:
            self.after(0, lambda: setattr(self, 'is_listening', False))
    
    def _simple_voice_input(self):
        """Simple voice input that works better with GUI"""
        try:
            import vosk
            import sounddevice as sd
            import json
            import os
            from .utils.config import get_settings
            
            settings = get_settings()
            
            # Check if Vosk model is available
            if not settings.model_path or not os.path.isdir(settings.model_path):
                return "demo voice command"
            
            # Initialize Vosk
            model = vosk.Model(settings.model_path)
            samplerate = 16000
            rec = vosk.KaldiRecognizer(model, samplerate)
            
            # Record audio
            duration = max(2, settings.stt_seconds)
            audio_data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
            sd.wait()
            
            # Process audio
            if rec.AcceptWaveform(audio_data.tobytes()):
                result = json.loads(rec.Result())
                return result.get("text", "").strip()
            else:
                result = json.loads(rec.FinalResult())
                return result.get("text", "").strip()
                
        except Exception as e:
            print(f"Voice input error: {e}")
            return "demo voice command"
    
    def _process_voice_input(self, text):
        """Process voice input on main thread"""
        try:
            # Add user message
            self.add_message("You", text)
            
            # Process command
            response = self.router.dispatch(text)
            
            # Add assistant response
            self.add_message("Assistant", response)
            
            # Speak response if voice mode is on
            if self.voice_mode:
                # Run TTS in separate thread to avoid blocking GUI
                tts_thread = threading.Thread(
                    target=self._speak_response, 
                    args=(response,), 
                    daemon=True
                )
                tts_thread.start()
        except Exception as e:
            self.add_message("System", f"Error processing voice: {e}")
    
    def _speak_response(self, text):
        """Speak response in background thread"""
        try:
            from .tts import speak
            speak(text)
        except Exception as e:
            print(f"TTS error: {e}")
    
    def handle_text_input(self, event=None):
        text = self.text_input.get().strip()
        if not text:
            return
        
        # Clear input
        self.text_input.delete(0, tk.END)
        
        # Add user message
        self.add_message("You", text)
        
        # Process command
        response = self.router.dispatch(text)
        
        # Add assistant response
        self.add_message("Assistant", response)
    
    def add_message(self, sender: str, message: str):
        if sender == "You":
            # User message styling
            self.chat_display.insert(tk.END, "\n")
            self.chat_display.insert(tk.END, "You\n", "user_header")
            self.chat_display.insert(tk.END, f"{message}\n", "user_message")
        else:
            # Assistant message styling
            self.chat_display.insert(tk.END, "\n")
            self.chat_display.insert(tk.END, "Assistant\n", "assistant_header")
            self.chat_display.insert(tk.END, f"{message}\n", "assistant_message")
        
        self.chat_display.see(tk.END)
        
        # Configure tags for styling
        self.chat_display.tag_config("user_header", foreground="#4A90E2")
        self.chat_display.tag_config("user_message", foreground="#FFFFFF")
        self.chat_display.tag_config("assistant_header", foreground="#CCCCCC")
        self.chat_display.tag_config("assistant_message", foreground="#FFFFFF")
    
    def show_help(self):
        help_text = self.router.help()
        self.add_message("Assistant", f"Available commands:\n{help_text}")
    
    def close_app(self):
        """Close the application"""
        self.on_closing()
    
    def on_closing(self):
        """Handle window closing"""
        # Stop voice listening if active
        if self.is_listening:
            self.stop_voice_listening()
        
        # Destroy the window
        self.root.destroy()
    
    def run(self):
        # Bind window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

def main():
    app = VoiceAssistantGUI()
    app.run()

if __name__ == "__main__":
    main()
