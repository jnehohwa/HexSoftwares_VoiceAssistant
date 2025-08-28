# HexSoftwares Voice Assistant (Python)

Offline-first, modular assistant for the Hex Softwares Internship.
- Repo name follows the HexSoftwares_Project_Name rule.
- You'll post a short demo video + repo link on LinkedIn when done.

## Quickstart

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python run_gui.py
```

## Demo

See the assistant in action:
```bash
python demo.py
```

## Try commands

- `time` - Get current time
- `date` - Get current date
- `calc 2*(3+4)**2` - Calculator with complex expressions
- `calc sqrt(16) + 5**2` - Math functions (sqrt, sin, cos, etc.)
- `note Buy milk` - Take notes
- `joke` - Get random jokes
- `open Safari` - Open apps (macOS)
- `wiki Nelson Mandela` - Wikipedia summaries
- `weather Cape Town` - Current weather conditions
- `system info` - Comprehensive system monitoring
- `system cpu` - CPU usage and processor details
- `system memory` - Memory and RAM statistics
- `system disk` - Disk usage information
- `system processes` - Top processes by CPU usage
- `chat hello` - AI conversation and assistance
- `chat what can you do` - Ask about capabilities
- `help` - Show all commands

## Interface Options

- **GUI Mode**: `python run_gui.py` or `python -m src.voice_assistant.main --gui` (ChatGPT-style mobile interface)
- **CLI Mode**: `python -m src.voice_assistant.main` (Command line interface)
- **Voice Mode**: `python -m src.voice_assistant.main --voice` (Voice I/O - requires extras)

## Advanced Features

### **System Monitoring**
- **Real-time CPU monitoring** with usage percentages and frequency
- **Memory tracking** including RAM, swap, and available memory
- **Disk usage analysis** across all partitions
- **Process monitoring** showing top CPU-intensive processes
- **Network statistics** with interface information and data usage

### **AI Conversation**
- **Intelligent pattern matching** for natural language understanding
- **Context-aware responses** with conversation history
- **Multi-domain knowledge** covering time, weather, math, and system info
- **Professional responses** designed for business environments
- **Conversation memory** with recent interaction tracking

### **Enhanced Calculator**
- **Advanced math functions**: sqrt, sin, cos, tan, log, abs, round, floor, ceil
- **Complex expressions** with proper operator precedence
- **Scientific notation** support
- **Safe evaluation** with restricted function access

## GUI Features

**Beautiful Modern Interface**
- Dark theme with light blue color grading (`#4A90E2`)
- Mobile-optimized layout (400x700)
- Status bar with time, network, and battery indicators
- Upper control bar with info, CC, share, and settings buttons
- Welcome section with quick action buttons
- Bottom control bar with clear, settings, about, and close buttons
- Rounded corners and modern styling throughout

**Easy to Use**
- Quick action buttons for common commands
- Always-visible text input with emoji placeholder
- Real-time chat interface with styled messages
- Clear chat, settings, and about functionality
- Responsive design with hover effects

## Optional voice

Install voice libraries and run with `--voice` for real speech-to-text and text-to-speech:

1. Install dependencies: `pip install -r requirements.txt`
2. Download a Vosk model (e.g., vosk-model-small-en-us-0.15) and set `VA_MODEL_PATH` in `.env`
3. Run: `python -m src.voice_assistant.main --voice`
