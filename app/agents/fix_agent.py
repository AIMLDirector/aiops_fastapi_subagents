from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
from dotenv import load_dotenv

load_dotenv()

async def fix_agent(text: str) -> str:
    res = await llm.ainvoke(
        f"Provide immediate fix, long-term fix, and prevention steps.\n{text}"
    )
    return res.content.strip()