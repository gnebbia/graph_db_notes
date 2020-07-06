import random
import string
import time
import pandas as pd
import matplotlib 
import matplotlib.pyplot as plt
from py2neo import Graph, Node, NodeMatcher

def randomString(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

graph = Graph("bolt://localhost:7687", auth=("neo4j", "pass1"))

## What is the Schema? 
print("----------  Explore Schema  ----------")
print(graph.run("CALL db.schema.visualization()").data())


## Inserting a Node

### Example 1
node = Node("Person", "Hacker", name="Gianni",
        age=40, is_citizen=True, count=1)

graph.create(node)

### Example 2
props = {
        'name': "Valerio",
        'age': 29,
        'occupation': "teacher",
}

node2 = Node("Person", "Teacher",**props)
graph.create(node2)

## Example 3
labels = ["Person", "Police Officer"]
props  = {"age": 20, "name": "John Doe"}

node3 = Node(*labels, **props)

## Update a Node

### Example 1

# We have to create a matcher to find our node
matcher = NodeMatcher(graph)
node_gianni = matcher.match("Person", name="Gianni").first()

# Add new features
node_gianni['Occupation'] = "Mason"
node_gianni['Sign'] = "Capricorn"

# Update node in the database
graph.push(node_gianni)


### Example 2

# We have to create a matcher to find our node
matcher = NodeMatcher(graph)
node_gianni = matcher.match("Person", name="Gianni").first()

# Add new features
node_gianni['Occupation'] = "Bricklayer"
node_gianni['Sign'] = "Capricorn"

# Add a new label
node_gianni.add_label("Astrologist")
graph.push(node_gianni)


# Inserting multiple nodes Transactions vs Basic Queries

strings = []
for i in range(1000):
    strings.append(randomString())

start = time.time()
tx = graph.begin()
for i in range(10):
    node_tmp = Node(name=strings[i])
    tx.create(node_tmp)
tx.commit()
end = time.time()
print("Transactions take this time:")
print(end - start)


start = time.time()
for i in range(10):
    node_tmp = Node(name=strings[i])
    graph.create(node_tmp)
end = time.time()
print("Basic Queries take this time:")
print(end - start)

# Conclusion: Transactions are generally faster


## How Many Nodes do we have for each label?
print("----------  Counting Nodes by Labels  ----------")

result = {"label": [], "count": []}
for label in graph.run("CALL db.labels()").to_series():
    query = f"MATCH (:`{label}`) RETURN count(*) as count"
    count = graph.run(query).to_data_frame().iloc[0]['count']
    result["label"].append(label)
    result["count"].append(count)
nodes_df = pd.DataFrame(data=result)
sortedval = nodes_df.sort_values("count")
print(sortedval)


## Visualize the counts using matplotlib

nodes_df.plot(kind='bar', x='label', y='count', legend=None, title="Node Cardinalities")
plt.yscale("log")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


## What kind of relationships do we have in our graph?
print("----------  Counting Relationships by Types  ----------")
result = {"relType": [], "count": []}
for relationship_type in graph.run("CALL db.relationshipTypes()").to_series():
    query = f"MATCH ()-[:`{relationship_type}`]->() RETURN count(*) as count"
    count = graph.run(query).to_data_frame().iloc[0]['count']
    result["relType"].append(relationship_type)
    result["count"].append(count)
rels_df = pd.DataFrame(data=result)
sortedval = rels_df.sort_values("count")
print(sortedval)

## Visualize Relationship Types
rels_df.plot(kind='bar', x='relType', y='count', legend=None, title="Relationship Cardinalities")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


## In general to perform a query
query = """
MATCH (a:Article)
RETURN size((a)<-[:CITED]-()) AS citations
"""

citation_df = graph.run(query).to_data_frame()
citation_df.describe([.25, .5, .75, .9, .99])


