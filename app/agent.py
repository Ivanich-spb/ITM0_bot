import os
import random
from app.models import QueryResponse
from langchain.schema import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableMap
from app.utils import ChatOpenAI
from langchain.agents import Tool, initialize_agent
from langchain.agents import AgentExecutor, create_react_agent
from langchain import hub
from langchain.prompts import PromptTemplate
from langchain_community.utilities import SerpAPIWrapper
from langchain.agents import load_tools


tools = load_tools(["serpapi"])

# Initialize API Key and LLM
api_key = os.getenv("OPENAI_API_KEY")
serp_key = os.getenv("SERPAPI_API_KEY")
llm = ChatOpenAI(temperature=0.0, course_api_key=api_key)

# Get the prompt to use - you can modify this!
prompt = hub.pull("hwchase17/react")

modified_template = prompt.template + "\n\n "
            
modified_prompt = PromptTemplate(
    input_variables=prompt.input_variables,
    template=modified_template
)


# Construct the ReAct agent
agent = create_react_agent(llm, tools, prompt)

# Create an agent executor by passing in the agent and tools
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, max_iterations=2)

def get_response(query: str, query_id: int) -> QueryResponse:
    try:
        result = agent_executor.invoke({"input": query})
        reasoning = result['output']
        
        # Determine the answer if the query contains multiple choice options
        answer = None
        if "\n" in query:
            options = query.split("\n")[1:]
            for i, option in enumerate(options, start=1):
                if option.strip() in reasoning:
                    answer = i
                    break
            if answer is None:
                answer = random.randint(1, len(options))  # Random answer if no match found

        response = {
            "id": query_id,
            "answer": answer,
            "reasoning": reasoning,
            "sources": []  # Add sources if any
        }
        return QueryResponse(**response)
    except Exception as e:
        raise RuntimeError(f"Error in agent execution: {e}")
