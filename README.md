# 📄 Gemini PDF Chatbot with Dynamic Model Selection

A Streamlit-based AI Chatbot that allows you to "chat" with your PDF documents using Google's Gemini models. 

Unlike standard RAG implementations, **this app dynamically fetches available models from your API Key**, ensuring compatibility even if Google changes model names (e.g., `gemini-pro` vs `gemini-1.5-flash`).

## 🚀 Features

* **🔍 Dynamic Model Detection:** Automatically connects to Google API, lists available models compatible with your key, and lets you choose the best one. No more "404 Model Not Found" errors!
* **📂 Multi-PDF Support:** Upload multiple documents at once and analyze them together.
* **💬 Persistent Chat History:** Remembers your conversation context within the session.
* **🔐 Privacy Focused:** Runs locally using your own API Key. Your documents are not stored on any third-party vector database servers.
* **⚡ Powered by Gemini:** Utilizes the massive context window of Google's Gemini models for accurate summarization and Q&A.

## 🛠️ Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/gemini-pdf-chatbot.git](https://github.com/YOUR_USERNAME/gemini-pdf-chatbot.git)
    cd gemini-pdf-chatbot
    ```

2.  **Create a virtual environment (Optional but recommended):**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## ▶️ Usage

1.  Run the app:
    ```bash
    streamlit run app.py
    ```
2.  The app will open in your browser.
3.  Enter your **Google Gemini API Key** (Get it [here](https://aistudio.google.com/app/apikey)).
4.  The app will automatically verify the key and list available models in the dropdown menu.
5.  Upload your PDF files and start asking questions!

## 🧩 Tech Stack

* [Python](https://www.python.org/)
* [Streamlit](https://streamlit.io/) (UI)
* [Google Generative AI](https://ai.google.dev/) (LLM)
* [PyPDF2](https://pypi.org/project/PyPDF2/) (PDF Processing)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License


This project is open source and available under the [MIT License](LICENSE).
