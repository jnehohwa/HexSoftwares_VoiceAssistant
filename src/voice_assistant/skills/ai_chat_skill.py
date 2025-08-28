import re
import random
from datetime import datetime
from .base import Skill

class AIChatSkill(Skill):
    def __init__(self):
        self.conversation_history = []
        self.patterns = {
            # Greetings
            r'\b(hi|hello|hey|good morning|good afternoon|good evening)\b': [
                "Hello! How can I assist you today?",
                "Hi there! What can I help you with?",
                "Greetings! How may I be of service?",
                "Hello! I'm here to help with any tasks you need."
            ],
            
            # How are you
            r'\b(how are you|how do you do|are you ok)\b': [
                "I'm functioning perfectly! Thank you for asking. How are you doing?",
                "I'm doing great! Ready to help with any tasks you have.",
                "I'm excellent! My systems are running smoothly. How about you?"
            ],
            
            # What can you do
            r'\b(what can you do|what are your capabilities|help|abilities)\b': [
                "I can help with time, calculations, notes, jokes, app control, Wikipedia searches, weather info, system monitoring, and general conversation!",
                "My capabilities include: time/date, math calculations, note-taking, jokes, opening apps, web searches, weather data, system stats, and AI chat.",
                "I'm a versatile assistant! I can handle tasks, answer questions, provide information, and engage in conversation."
            ],
            
            # Weather patterns
            r'\b(weather|temperature|hot|cold|rain|sunny)\b': [
                "I can check the weather for any city! Just say 'weather [city name]' and I'll get you the current conditions.",
                "For weather information, try asking me about a specific city. For example: 'weather London' or 'weather New York'."
            ],
            
            # Time patterns
            r'\b(time|clock|hour|minute)\b': [
                "I can tell you the current time! Just say 'time' and I'll give you the exact time.",
                "For time information, simply say 'time' and I'll provide the current time and date."
            ],
            
            # Math patterns
            r'\b(calculate|math|equation|solve)\b': [
                "I can perform calculations! Use 'calc' followed by your expression. For example: 'calc 2+2' or 'calc sqrt(16)'.",
                "For mathematical calculations, use the 'calc' command. I support basic operations and math functions like sqrt, sin, cos, etc."
            ],
            
            # System patterns
            r'\b(system|computer|performance|slow|fast)\b': [
                "I can monitor your system! Try 'system info' for comprehensive stats, or 'system cpu' for processor details.",
                "For system information, use commands like 'system info', 'system memory', or 'system processes'."
            ],
            
            # Thank you
            r'\b(thank you|thanks|appreciate it)\b': [
                "You're very welcome! I'm here to help.",
                "My pleasure! Is there anything else you need assistance with?",
                "Glad I could help! Feel free to ask for more assistance."
            ],
            
            # Goodbye
            r'\b(bye|goodbye|see you|farewell|exit|quit)\b': [
                "Goodbye! Have a great day!",
                "See you later! Don't hesitate to call if you need help again.",
                "Take care! I'll be here when you need assistance."
            ],
            
            # Name
            r'\b(what is your name|who are you|your name)\b': [
                "I'm the HexSoftwares Voice Assistant, your AI companion!",
                "My name is HexSoftwares Voice Assistant. I'm here to help with various tasks and provide intelligent assistance.",
                "I'm your HexSoftwares AI Assistant, designed to make your digital life easier!"
            ],
            
            # Intelligence
            r'\b(are you intelligent|smart|clever|ai|artificial intelligence)\b': [
                "I'm designed to be helpful and intelligent! I can process information, perform calculations, and assist with various tasks.",
                "I'm an AI assistant with capabilities for natural language processing, mathematical operations, and system monitoring.",
                "I'm built with intelligent features to understand and respond to your needs effectively!"
            ],
            
            # Company
            r'\b(hexsoftwares|hex software|company|internship)\b': [
                "HexSoftwares is an innovative software company! I was created as part of an internship project to demonstrate AI and voice assistant capabilities.",
                "I'm a product of HexSoftwares, developed during an internship to showcase modern AI assistant technology.",
                "HexSoftwares is my creator! This project demonstrates advanced voice assistant and AI integration capabilities."
            ]
        }
        
        # Fallback responses for when no pattern matches
        self.fallbacks = [
            "That's an interesting question! I'm designed to help with specific tasks like time, calculations, weather, and system monitoring.",
            "I'm not sure I understand that completely. Could you try asking about time, weather, calculations, or system information?",
            "I'm here to assist with practical tasks. Try asking me about the time, weather, or system status!",
            "I'm focused on helping with specific tasks. You can ask me about time, date, calculations, notes, weather, or system information.",
            "I'm designed to be helpful with concrete tasks. Try commands like 'time', 'weather London', or 'system info'!"
        ]

    def names(self):
        return ["chat", "talk", "conversation", "ai", "assistant"]

    def handle(self, cmd: str, args: str) -> str:
        # Store conversation
        full_input = f"{cmd} {args}".strip()
        self.conversation_history.append({
            'input': full_input,
            'timestamp': datetime.now()
        })
        
        # Keep only last 10 conversations
        if len(self.conversation_history) > 10:
            self.conversation_history = self.conversation_history[-10:]
        
        # If no args, provide general help
        if not args:
            return self._get_general_response()
        
        # Try to match patterns
        response = self._match_patterns(args)
        if response:
            return response
        
        # Fallback response
        return random.choice(self.fallbacks)

    def _match_patterns(self, text):
        """Match input text against known patterns"""
        text_lower = text.lower()
        
        for pattern, responses in self.patterns.items():
            if re.search(pattern, text_lower):
                return random.choice(responses)
        
        return None

    def _get_general_response(self):
        """Provide a general response when no specific input is given"""
        responses = [
            "Hello! I'm your AI assistant. I can help with time, calculations, weather, system monitoring, and more. What would you like to know?",
            "Hi there! I'm here to assist you. Try asking me about the time, weather, or system information.",
            "Greetings! I'm your intelligent assistant. I can handle various tasks - just let me know what you need!",
            "Hello! I'm ready to help. You can ask me about time, date, weather, calculations, or system status."
        ]
        return random.choice(responses)
