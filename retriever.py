import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_neo4j import Neo4jGraph, Neo4jVector, GraphCypherQAChain
from langchain_core.prompts.prompt import PromptTemplate

load_dotenv()


def initialize_graphrag():
    graph = Neo4jGraph(
        url=os.getenv("NEO4J_URI"),
        username=os.getenv("NEO4J_USERNAME"),
        password=os.getenv("NEO4J_PASSWORD")
    )

    llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash", temperature=0)

    vector_store = Neo4jVector.from_existing_graph(
        embedding=GoogleGenerativeAIEmbeddings(model="gemini-embedding-2-preview"),
        url=os.getenv("NEO4J_URI"),
        username=os.getenv("NEO4J_USERNAME"),
        password=os.getenv("NEO4J_PASSWORD"),
        index_name="function_source_index",
        node_label="Function",
        text_node_properties=["source_code", "docstring"],
        embedding_node_property="embedding",
    )

    # --- NEW: Custom Cypher Prompt leveraging PageRank ---
    cypher_template = """Task: Generate Cypher statement to query a graph database.
    Instructions:
    Use only the provided relationship types and properties in the schema.
    If a user asks about the 'most critical' functions, 'bottlenecks', or 'impact', you MUST order the return results by the 'pagerank_score' property descending.

    Schema:
    {schema}

    Question: {question}
    """
    custom_prompt = PromptTemplate(
        input_variables=["schema", "question"],
        template=cypher_template
    )

    chain = GraphCypherQAChain.from_llm(
        llm=llm,
        graph=graph,
        verbose=True,
        allow_dangerous_requests=True,
        cypher_prompt=custom_prompt  # Injecting the structural rules
    )

    return chain


if __name__ == "__main__":
    qa_chain = initialize_graphrag()

    question = "What are the top 3 most critical bottlenecks in this codebase?"

    print(f"Query: {question}\n")
    response = qa_chain.invoke({"query": question})
    print(f"Analysis: {response['result']}")