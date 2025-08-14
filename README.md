# 🤖 My Dell G15 5530 Specs AI Bot

Hey! This is a little project I built to practice my AI skills. It's a simple AI assistant that can answer questions about my Dell G15 5530 laptop. I fed it a text file with all the specs, so it uses that as its brain and won't make stuff up.

### Why I Built This

I made this right after finishing two IBM SkillsBuild courses: **"Introduction to Retrieval Augmented Generation"** and **"Ethical Considerations for Generative AI"**. I wanted to see if I could actually build something with what I learned instead of just having the certificates.

### How It Works

It uses a technique called **RAG (Retrieval-Augmented Generation)**. Basically, instead of the AI just guessing, it first *looks up* the answer in the `knowledge.txt` file I gave it and then uses that info to reply.

I also told it to not answer questions if they aren't about my laptop. That was the "AI Ethics" part of my learning – making sure the bot stays on topic and doesn't give bad answers.

### Tech I Used

-   **Python**
-   **Streamlit** (for the simple UI)
-   **LangChain** (to connect everything together)
-   **Google's Gemini API** (for the actual AI model)
-   **FAISS** (for the fast text search)

### 🚀 How to Run It

If you want to try it yourself:

1.  **Clone the repo:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/Dell-G15-Specs-AI-Assistant.git](https://github.com/YOUR_USERNAME/Dell-G15-Specs-AI-Assistant.git)
    cd Dell-G15-Specs-AI-Assistant
    ```
    (Remember to replace `YOUR_USERNAME` with your actual GitHub username!)

2.  **Install the stuff it needs:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up your API Key:**
    -   Make a new file in the folder and call it `.env`
    -   Inside that file, put your Google AI API key like this:
        ```
        GOOGLE_API_KEY="YOUR_API_KEY_HERE"
        ```

4.  **Run the app:**
    ```bash
    streamlit run app.py
    ```
    Or if that doesn't work, try:
    ```bash
    python -m streamlit run app.py
    ```

### What I Learned

This was a great project! It really helped me understand how RAG actually works from start to finish, not just in theory. It was also cool to see how a simple prompt can totally control the AI's behavior. Connecting all the different libraries was a bit of a challenge at first, but I'm happy I got it working!
