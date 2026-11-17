from langchain_ollama import ChatOllama

from langgraph.prebuilt import create_react_agent

from agent.tools import (
    get_dataset_information,
    execute_sql,
    get_revenue_summary
)

from config.settings import MODEL_NAME


llm = ChatOllama(
    model=MODEL_NAME,
    temperature=0
)


tools = [
    get_dataset_information,
    execute_sql,
    get_revenue_summary
]


SYSTEM_PROMPT = """
You are RetailOps AI, an expert business intelligence analyst.

Your responsibility is to analyse uploaded business datasets.

Rules:

1. Always use available tools when actual dataset information is required.
2. Never invent sales numbers.
3. Use SQL to retrieve relevant information.
4. Explain results in simple business language.
5. If information is unavailable, clearly mention it.
6. Provide useful business insights.
7. Do not assume that every dataset contains a price column.
8. Inspect available columns before writing SQL queries.
9. Only analyse the uploaded dataset.
10. Clearly distinguish calculated facts from recommendations.

You are a professional data analyst.
"""


agent = create_react_agent(
    model=llm,
    tools=tools,
    prompt=SYSTEM_PROMPT
)


def ask_agent(question):

    response = agent.invoke({
        "messages": [
            {"role": "user", "content": question}
        ]
    })

    return response["messages"][-1].content