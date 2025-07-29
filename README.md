# Desktop Assistant Agent 🤖

An intelligent desktop assistant agent that can interact with your operating system and perform various automated tasks.

## 📋 Prerequisites

- Python 3.8 or higher
- Node.js 16.x or higher
- Git
- OpenAI API key

## 🔗 External Dependencies

This project works in conjunction with the [agent-react-interface](https://github.com/OsianJL/agent-react-interface), which provides the user interface for sending prompts to the agent. **Both repositories must be properly configured for the system to work correctly.**

## 🚀 Installation

1. Clone this repository:
```bash
git clone https://github.com/OsianJL/desktop_assistant_agent.git
cd desktop_assistant_agent
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# On Linux/Mac:
source venv/bin/activate
# On Windows:
.\venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## ⚙️ Configuration

1. Clone the agent-react-interface repository from: [https://github.com/OsianJL/agent-react-interface](https://github.com/OsianJL/agent-react-interface)

2. Create a `.env` file in the root directory and add your OpenAI API key:
```bash
OPENAI_API_KEY=your_api_key_here
```

## 🎮 Usage

1. Start the agent:
```bash
uvicorn api:app --reload
```

2. Start the React interface following the instructions in the agent-react-interface repository

3. Access the web interface at `http://localhost:3000`

## 🤝 Contributing

Contributions are welcome. Please follow these steps:

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **OsianJL** - *Initial work* - [GitHub](https://github.com/OsianJL)

## 🙏 Acknowledgments

- Thanks to all contributors who participate in this project
- Special thanks to the agent-react-interface development team

## ❗ Important Notes

- Ensure all prerequisites are installed before starting
- Make sure to set up your OpenAI API key in the `.env` file
- Both repositories (desktop_assistant_agent and agent-react-interface) must be properly configured
- For issues or suggestions, please open an issue in the corresponding repository

---
⌨️ with ❤️ by [OsianJL](https://github.com/OsianJL)
