# 🤖 Jarvis AI Assistant (Host-Based Gemini V1)

Jarvis is a high-speed, voice-activated desktop assistant inspired by the J.A.R.V.I.S. system from Iron Man. It provides conversational intelligence via the Gemini API and offers direct control over local system functions (app launching, time check) through a resilient, synchronous Python loop.

## ✨ Key Features

  * **Zero-Latency TTS:** Uses **`pyttsx3`** for instant, offline speech synthesis, eliminating network delay.
  * **Resilience:** Features a robust **Model Fallback System** that automatically rotates to a backup model (`gemini-pro`) if the primary model (`gemini-flash`) hits an API quota limit (Error 429).
  * **Local Automation:** Executes shell commands (`subprocess`) to open applications like VS Code and Chrome.
  * **Wake Word Activation:** The system remains quiet until the wake word **"Jarvis"** is detected in the speech stream.
  * **Persona:** Configured with a formal, British persona via the Gemini system prompt.

-----

## 🛠️ Setup & Installation

### Prerequisites

  * Python 3.10+
  * A working microphone and speakers.
  * A **Google Gemini API Key**.

### 1\. Clone & Install Dependencies

```bash
# Clone the repository
git clone https://github.com/Hasan-Oz/Jarvis-AI-Assistant-Gemini.git
cd Jarvis-AI-Assistant-Gemini

# Create and activate a virtual environment
python -m venv venv
./venv/Scripts/activate 

# Install required libraries
pip install -r requirements.txt
```

### 2\. Configure API Key

Create a file named **`.env`** in the project's root directory and add your key. **Do not commit this file to GitHub.**

```env
# CRITICAL: Replace with your actual key
GEMINI_API_KEY=AIzaSyA...YourKeyHere
```

### 3\. Run the System

```bash
python jarvis.py
```

Jarvis will initialize the voice engine and then wait for your command.

-----

## 🗣️ Usage (Commands)

The system requires the **wake word** "Jarvis" before executing any command.

| Use Case | Example Command | Execution |
| :--- | :--- | :--- |
| **Cloud Query** | "Jarvis, explain the difference between Git and GitHub." | Sent to Gemini API. |
| **App Control** | "Jarvis, open VS Code." | Executes local shell command (`subprocess`). |
| **Temporal Check** | "Jarvis, what time is it now?" | Executes local `datetime` function (instant, zero quota). |
| **System Stop** | "Jarvis, shut down." | Closes the Python script cleanly. |

-----

## 🧠 Architecture Overview

The system operates as a **Synchronous Host Loop**, prioritizing speed by making immediate decisions locally.

1.  **Input:** Microphone feeds $\rightarrow$ **SpeechRecognition** (Google STT).
2.  **Filter:** Code checks if the transcribed text contains **"Jarvis"**.
3.  **Router:** Logic determines if the command is local (Time/App) or requires the cloud.
4.  **Cloud/Action:** If Cloud, the **Gemini 2.0 Flash** API is called with **Fallback Logic**. If Local, the OS command runs.
5.  **Output:** **Pyttsx3** converts the final response to audio instantly.

-----

## 🔮 Future Roadmap (V2 Goals)

  * **Long-Term Memory (RAG):** Implement **ChromaDB** and **SQLite** to store personalized notes and conversation history, allowing Jarvis to answer questions based on past context.
  * **Vision Capabilities:** Utilize Gemini's multimodal features to allow Jarvis to analyze screenshots or webcam feeds.
  * **Home Automation:** Connect the logic to external APIs (e.g., Home Assistant) for smart home control.
