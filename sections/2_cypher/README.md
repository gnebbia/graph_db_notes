# Cypher Language

## Nodes

Here are simplified syntax examples for specifying a node:

()                           ;; anonymous node
(variable)                   ;; node which will be referred by a variable called "variable"
(:Label)                     ;; all the nodes with the label "Label"
(variable:Label)             ;; all the nodes with the label "Label" and they will be referred with a variable
(:Label1:Label2)             ;; all the nodes belonging to these two labels
(variable:Label1:Label2)     ;; all the nodes belonging to these two labels and will be referred with a variable

Practical examples:

()                  // anonymous node not be referenced later in the query
(p)                 // variable p, a reference to a node used later
(:Person)           // anonymous node of type Person
(p:Person)          // p, a reference to a node of type Person
(p:Actor:Director)  // p, a reference to a node of types Actor and Director


## Schema

When we are first learning about data in a graph, it is helpful
to examine the data model of the graph.
We can do this by doing:

CALL db.schema


We can inspect all properties of the graph

CALL db.propertyKeys

## Match

MATCH (n)           // returns all nodes in the graph
RETURN n

MATCH (p:Person)    // returns all Person nodes in the graph
RETURN p


## Retrieving Nodes Filtered by a property value


MATCH (variable {propertyKey: propertyValue})
RETURN variable

MATCH (variable:Label {propertyKey: propertyValue, propertyKey2: propertyValue2})
RETURN variable


MATCH (p:Person {born: 1970})
RETURN p

MATCH (m:Movie {released: 2003, tagline: 'Free your mind'})
RETURN m
