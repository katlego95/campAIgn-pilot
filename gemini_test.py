from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI # We'll use this for Gemini
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()


# 1. Define your LLM (using a correct Gemini model, see next section)
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

# 2. Define your prompt
prompt = ChatPromptTemplate.from_messages(
    [("user", "Write a viral tweet promoting the game: {game_name}")]
)

# 3. Create the chain using LCEL
chain = prompt | llm | StrOutputParser()

# 4. Invoke the chain
result = chain.invoke({"game_name": "Diablo II"})
print(result)
