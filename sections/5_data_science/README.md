# Data Science with neo4j

We can use py2neo for python which is a common choice.

    from py2neo import Graph
    graph = Graph("bolt://52.3.242.176:33698", auth=("neo4j", "Password11!!!"))
    graph.run("CALL db.schema()").data()


