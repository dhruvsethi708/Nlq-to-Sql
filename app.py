from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os
import sqlite3

import google.generativeai as genai

print(os.getenv("GOOGLE_AI_KEY"))

genai.configure(api_key=os.getenv("GOOGLE_AI_KEY"))


print("step2")


def get_gemini_response(question, prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content([prompt[0], question])
    return response.text.strip()


# Optional Feature - Connecting to database
def read_sql_query(sql, db):
    try:
        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute(sql)
        rows = c.fetchall()
        conn.close()
        return rows
    except Exception as e:
        return str(e)


prompt = [
    f"""
    You are an expert SQL assistant. Convert English questions into SQL queries based on the given database schema.

    **Database Structure:**
    
    **Instructions:**
    - Generate a valid SQL query using the given database schema.
    - Ensure correct table and column references.
    - The SQL query should NOT include triple backticks (`).
    - Provide only the SQL query as output.

    **Example:**
    If the schema is "employees table with columns: ID, Name, Salary, Department"
    - Question: "Who has the highest salary?"
    - Query: "SELECT Name FROM employees ORDER BY Salary DESC LIMIT 1;"
    """
]

# // Static prompt with database structure defined
prompt_static = [
    """
    You are an expert in converting English questions to optimized SQL queries.

    The SQL database is named **"database.db"**, and it contains a table called **"demo"** with the following columns:  
    - **Name** (TEXT)  
    - **Email** (TEXT)  
    - **Password** (TEXT)  
    - **Runs** (INTEGER)  
    - **Wins** (INTEGER)  
    - **Losses** (INTEGER)  
    - **Ties** (INTEGER)  
    - **Centuries** (INTEGER)  

    #### **Instructions:**
    1. **Convert any given question into a valid SQL query** that can be executed in SQLite.  
    2. **Follow best practices** for SQL query writing, ensuring correctness and efficiency.  
    3. The query should **not** include triple backticks (```) at the beginning or end.  
    4. **Provide only the SQL query** as output, without explanations or additional text.  
    5. Use appropriate SQL functions where necessary, such as `ORDER BY`, `GROUP BY`, `LIMIT`, and `CASE`.  
    6. Ensure that column names are correctly referenced.  

    #### **Examples:**  
    - **Q:** "What is the average number of runs scored by Virat Kohli?"  
    **A:**  
    ```sql
    SELECT CASE 
            WHEN (Wins + Losses + Ties) > 0 
            THEN Runs / (Wins + Losses + Ties) 
            ELSE NULL 
        END 
    FROM demo 
    WHERE Name = 'Virat Kohli';
  """
]


# Streamlit app
st.set_page_config(page_title="SQL Query Generator", page_icon="🧠")
background_image_url = "https://images.unsplash.com/photo-1547149600-a6cdf8fce60c?fm=jpg&q=60&w=3000&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NTh8fGNoYXQlMjBiYWNrZ3JvdW5kfGVufDB8fDB8fHww" 
st.markdown(
            # background: linear-gradient(135deg, #1a2a6c, #b21f1f, #fdbb2d);
    f"""
    <style>
        .stApp {{
            background: url('{background_image_url}') no-repeat center center fixed;
            background-size: cover;
            color: white;
            padding: 20px;
        }}
        h1 {{
            text-align: center;
            font-size: 36px;
            font-weight: bold;
            color: #FFD700; /* Gold color for contrast */
            margin-bottom: 10px;
        }}
        .input-box {{
            border-radius: 25px;
            border: 1px solid rgba(255, 255, 255, 0.5);
            padding: 12px;
            width: 100%;
            font-size: 16px;
            background-color: rgba(255, 255, 255, 0.1); /* Light transparent background */
            color: white;
            outline: none;
        }}
        .input-box::placeholder {{
            color: rgba(255, 255, 255, 0.7); /* Light placeholder color */
        }}
        .chat-button {{
            background-color: #25D366;
            color: white;
            border-radius: 25px;
            padding: 12px 24px;
            font-size: 18px;
            font-weight: bold;
            border: none;
            cursor: pointer;
            transition: background-color 0.3s ease-in-out;
        }}
        .chat-button:hover {{
            background-color: #1DA851;
        }}
        .stButton>button {{
            background-color: #25D366;
            color: white;
            border-radius: 25px;
            padding: 12px 24px;
            font-size: 18px;
            font-weight: bold;
            border: none;
            cursor: pointer;
            transition: background-color 0.3s ease-in-out;
        }}
        .stButton>button:hover {{
            background-color: #1DA851;
        }}
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <h1 style='text-align: center; color: #4CAF50;'>🧠 SQL Query Generator</h1>
    <p style='text-align: center; font-size: 18px;'>Convert natural language questions into SQL queries effortlessly!</p>
    """,
    unsafe_allow_html=True
)

st.markdown("<h3>🔍 Enter Your Question</h3>", unsafe_allow_html=True)
question = st.text_input(
    "Type your question in plain English:",
    key="input",
    placeholder="e.g., Who has the highest runs?",
    help="Example: 'How many centuries has Virat Kohli scored?'"
)
st.markdown("<br>", unsafe_allow_html=True)
submit = st.button("⚡ Generate SQL Query", use_container_width=True)

if submit and question:
    response = get_gemini_response(question, prompt)
    print(response)

    st.markdown("<h3>📝 Generated SQL Query</h3>", unsafe_allow_html=True)
    st.code(response, language="sql")

st.markdown("---")
st.markdown(
    "<p style='text-align: center; font-size: 14px; color: gray;'>🚀 Built with Streamlit | SQL Query Generator</p>",
    unsafe_allow_html=True
)