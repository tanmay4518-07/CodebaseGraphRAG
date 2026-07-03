import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()


def compute_pagerank():
    driver = GraphDatabase.driver(
        os.getenv("NEO4J_URI"),
        auth=(os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD"))
    )

    with driver.session() as session:
        print("1. Cleaning up previous projections...")
        # Drop the in-memory graph if it already exists from a previous run
        session.run("CALL gds.graph.drop('codebase_graph', false) YIELD graphName")

        print("2. Projecting codebase structure into GDS memory...")
        # Load the specific nodes and edges we want to analyze into RAM
        session.run("""
            CALL gds.graph.project(
                'codebase_graph',
                'Function',
                'CALLS'
            )
        """)

        print("3. Executing PageRank...")
        # Run the algorithm and write the scores back to the database as properties
        result = session.run("""
            CALL gds.pageRank.write('codebase_graph', {
                maxIterations: 20,
                dampingFactor: 0.85,
                writeProperty: 'pagerank_score'
            })
            YIELD nodePropertiesWritten, ranIterations
            RETURN nodePropertiesWritten, ranIterations
        """)

        record = result.single()
        print(
            f"Success! Mathematically scored {record['nodePropertiesWritten']} functions in {record['ranIterations']} iterations.")

    driver.close()


if __name__ == "__main__":
    compute_pagerank()