import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()


class Neo4jManager:
    def __init__(self):
        self.driver = GraphDatabase.driver(
            os.getenv("NEO4J_URI"),
            auth=(os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD"))
        )

    def close(self):
        self.driver.close()

    def build_graph(self, functions, calls):
        with self.driver.session() as session:
            # 1. Create Function Nodes
            for func in functions:
                session.run(
                    """
                    MERGE (f:Function {name: $name})
                    SET f.source_code = $source,
                        f.docstring = $docstring
                    """,
                    name=func["name"],
                    source=func["source_code"],
                    docstring=func["docstring"]
                )

            # 2. Create CALLS Relationships
            for call in calls:
                session.run(
                    """
                    MATCH (caller:Function {name: $caller_name})
                    MATCH (callee:Function {name: $callee_name})
                    MERGE (caller)-[:CALLS]->(callee)
                    """,
                    caller_name=call["caller"],
                    callee_name=call["callee"]
                )
        print("Knowledge Graph successfully populated.")


# Example Execution

if __name__ == "__main__":
    from ast_parser import parse_file

    # Change this line right here:
    funcs, calls = parse_file("test_code.py")

    db = Neo4jManager()
    db.build_graph(funcs, calls)
    db.close()