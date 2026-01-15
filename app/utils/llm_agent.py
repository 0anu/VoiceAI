from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
import os

class LLMAgent:
    def __init__(self, embeddings_manager, groq_api_key=None):
        
        if groq_api_key:
            os.environ["GROQ_API_KEY"] = groq_api_key
        
        self.embeddings_manager = embeddings_manager

        self.llm = ChatGroq(
            model="groq-alpha", 
            temperature=0,
            max_retries=2
            )
        
        @tool(response_format="content_and_artifact")
        def retrieve_context(query: str):
            return self.embeddings_manager.retrive_context(query)[0]
        
        system_prompt = (
            "Use the retrieve_context tool to get info from CSV (table, column names, descriptions). "
            "Write SQL to answer the user's query. Return only the SQL."
        )

        self.agent = create_agent(
            self.llm,
            [retrieve_context],
            system_prompt=system_prompt
        )
    
    def generate_sql(self, query):

        result = self.agent.invoke({"message": [HumanMessage(content=query)]})

        return result["message"][-1].content
    