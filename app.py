from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os
import sqlite3

import google.generativeai as genai
# print(genai.__version__)

print(os.getenv("GOOGLE_AI_KEY"))

genai.configure(api_key=os.getenv("GOOGLE_AI_KEY"))
# models = genai.list_models()
# for model in models:
#     print(model.name)


print("step2")


def get_gemini_response(question, prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content([prompt[0], question])
    return response.text.strip()


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
# {database_schema}
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
background_image_url = "https://images.unsplash.com/photo-1521747116042-5a810fda9664"  # Replace with any soothing background image URL
st.markdown(
    """
    <style>
        body {
            background: linear-gradient(135deg, #1a2a6c, #b21f1f, #fdbb2d);
            background-attachment: fixed;
            color: white;
        }
        .stApp {
            background-color: rgba(255, 255, 255, 0.2);
            border-radius: 15px;
            padding: 20px;
            box-shadow: 5px 5px 15px rgba(0,0,0,0.3);
        }
        h1 {
            text-align: center;
            font-size: 36px;
            font-weight: bold;
            color: white;
            margin-bottom: 10px;
        }
        .input-box {
            border-radius: 25px;
            border: 1px solid white;
            padding: 10px;
            width: 100%;
            font-size: 16px;
        }
        .chat-button {
            background-color: #25D366;
            color: white;
            border-radius: 25px;
            padding: 10px 20px;
            font-size: 18px;
            font-weight: bold;
            border: none;
        }
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

# st.markdown("<h3>📌 Define Your Database Structure</h3>", unsafe_allow_html=True)
# database_schema = st.text_area(
#     "Describe your database structure (tables, columns, data types)",
#     placeholder="Example: 'My database has a table called employees with columns: ID (integer), Name (text), Salary (float), Department (text)'",
#     help="Describe your table names and columns. Example: 'My database has a table orders with columns: OrderID, CustomerName, Amount, Date.'"
# )

# st.markdown("---")
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
    data = read_sql_query(response, "database.db")

    st.markdown("<h3>📝 Generated SQL Query</h3>", unsafe_allow_html=True)
    st.code(response, language="sql")

    if isinstance(data, str):  # If an error occurred
        st.error(f"⚠️ SQL Execution Error: {data}")
    elif data:
        st.table(data)  # Display results in table format
    else:
        st.warning("⚠️ No data found for the given query.")

    # st.subheader("The Response is:")
    # st.header(response)
    # st.header(data[0][0])

st.markdown("---")
st.markdown(
    "<p style='text-align: center; font-size: 14px; color: gray;'>🚀 Built with Streamlit | SQL Query Generator</p>",
    unsafe_allow_html=True
)