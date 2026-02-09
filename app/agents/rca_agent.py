from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


async def rca_agent(text: str) -> str:
    res = await llm.ainvoke(
        f"Provide root cause analysis in 2 to 3 sentences.\n{text}"
    )
    return res.content.strip()