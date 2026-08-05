# 🏥 MediAssistAI - Healthcare Chatbot

A simple yet powerful AI-powered healthcare chatbot built with Streamlit and Groq's LLM.

## ✨ Features

- **Healthcare Q&A**: Ask any health-related questions
- **AI-Powered Responses**: Uses Groq's Llama model for intelligent answers
- **Chat Memory**: Maintains conversation history within the session
- **Simple & Clean UI**: User-friendly interface

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.8+
- Groq API Key (get free at https://console.groq.com)

### 2. Setup

Clone or navigate to the project directory:
```bash
cd /Users/maheswari/Documents/HealthcareAIChatbot
```

Install dependencies:
```bash
pip install -r requirements.txt
```

### 3. Configure API Key

Update `.env` file with your Groq API key:
```
GROQ_API_KEY=your_api_key_here
```

### 4. Run the Chatbot

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 📝 Usage

1. Type your healthcare question in the chat input
2. Click send or press Enter
3. Wait for the AI to generate a response
4. Continue the conversation

## ❓ Sample Questions

- What are the symptoms of diabetes?
- How much water should I drink daily?
- What's a healthy BMI range?
- Tips for better sleep
- How to manage stress naturally?

## ⚠️ Disclaimer

This chatbot is for informational purposes only. Always consult with qualified healthcare professionals for medical advice, diagnosis, or treatment.

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **LLM**: Groq (Llama 3.3 70B)
- **Language**: Python

## 📁 Project Structure

```
HealthcareAIChatbot/
├── app.py                 # Main Streamlit app
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (API keys)
│
└── chatbot/
    ├── groq_client.py     # Groq API client
    ├── response.py        # Response generation logic
    ├── prompts.py         # System prompts
    └── memory.py          # Chat memory management
```

## 📄 License

Open source for educational purposes.
