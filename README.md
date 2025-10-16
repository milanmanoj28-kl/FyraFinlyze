FyraFinlyze
A smart personal finance assistant chatbot using Groq LLM and Python.

--Features

Upload .xlsx or .csv files
Chat with your financial data in natural language
Get automated insights and summaries
Powered by Groq’s high-speed inference API
Simple and elegant Streamlit UI with dark mode
API-key based configuration (safe for future model changes)

--Tech Stack

Python 3.10+
Streamlit – UI Framework
Pandas – Data processing
Groq API – LLM engine for fast response generation
OpenAI-compatible models via Groq

--Set Your Groq API Key

Visit https://console.groq.com
Sign in → Navigate to API Keys
Generate a new key and copy it.
code : setx GROQ_API_KEY "your_api_key_here"  (for windows)
code: export GROQ_API_KEY="your_api_key_here" (for macbook)

--Run the Application

--How It Works

User uploads a .xlsx or .csv financial file
The app reads it using Pandas
User asks natural questions like:
“What’s my total spending this month?”
“Which category has the highest expense?”
The query is sent to Groq’s LLM API
The model processes the question and data, returning a clean answer
Streamlit displays the result beautifully in the chat UI.

--About the Groq API

Groq provides ultra-fast inference using their LPU (Language Processing Unit) technology.
The Groq API works just like the OpenAI API.
Current models include:
mixtral-8x7b
llama3-8b-8192
gemma-7b-it

--If a model gets deprecated in the future:

Go to https://console.groq.com/docs/models
Choose a new available model name
Replace it in your code
Restart the app
That’s it — no further code change needed!

--Future Model Decommissioning – What to Do

Groq (like OpenAI) may retire old models.
If your current model stops working:
Visit the Groq API Models page
Pick a new active model (e.g., llama3-70b if available)
Update this line in your code:
model = "new_model_name"

--Author

Milan Manoj
Jain University, Bangalore
Data Science & Analytics Student

