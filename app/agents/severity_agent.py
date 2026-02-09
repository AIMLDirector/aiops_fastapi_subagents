from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


async def severity_agent(text: str) -> str:
    res = await llm.ainvoke(
        f"Classify severity (P1, P2, P3, P4). Only output one.\n{text}"
    )
    return res.content.strip()