# Cypher Language

## Style Recommendations

Cypher style recommendations
Here are the Neo4j-recommended Cypher coding standards that we use in this training:

- Node labels are CamelCase and begin with an upper-case letter (examples:
  Person, NetworkAddress). Note that node labels are case-sensitive.
- Property keys, variables, parameters, aliases, and functions are
  camelCase and begin with a lower-case letter (examples: businessAddress,
  title). Note that these elements are case-sensitive.
- Relationship types are in upper-case and can use the
  underscore. (examples: ACTED_IN, FOLLOWS). Note that relationship types
  are case-sensitive and that you cannot use the “-” character in a
  relationship type.
- Cypher keywords are upper-case (examples: MATCH, RETURN). Note that
  Cypher keywords are case-insensitive, but a best practice is to use
  upper-case.
- String constants are in single quotes, unless the string contains a
  quote or apostrophe (examples: ‘The Matrix’, “Something’s Gotta
  Give”). Note that you can also escape single or double quotes within
  strings that are quoted with the same using a backslash character.
- Specify variables only when needed for use later in the Cypher
  statement.
- Place named nodes and relationships (that use variables) before
  anonymous nodes and relationships in your MATCH clauses when possible.
- Specify anonymous relationships with `-->`, `--`, or `<--`

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


We can inspect properties for specific nodes by doing:

    MATCH (m:Movies) RETURN keys(m)

Remember that there is no answer to what kind of properties do
the "Movie" nodes have, since neo4j does not impose constraints,
hence different movies may have a different number of properties
or even completely different properties.

## Match

    MATCH (n)           // returns all nodes in the graph
    RETURN n
    
    MATCH (p:Person)    // returns all Person nodes in the graph
    RETURN p


## Inspect Labels and other useful information

We can also explore labels and properties associated to these labels
by using the following query:

    MATCH (n)
    RETURN labels(n), keys(n), size(keys(n)), count(*)
    ORDER BY size(keys(n)) DESC




## Retrieving Nodes Filtered by a property value


    MATCH (variable {propertyKey: propertyValue})
    RETURN variable
    
    MATCH (variable:Label {propertyKey: propertyValue, propertyKey2: propertyValue2})
    RETURN variable
    
    
    MATCH (p:Person {born: 1970})
    RETURN p
    
    MATCH (m:Movie {released: 2003, tagline: 'Free your mind'})
    RETURN m

To return specific property values we can do:

    MATCH (variable {prop1: value})
    RETURN variable.prop2
    
    MATCH (variable:Label {prop1: value})
    RETURN variable.prop2

    MATCH (variable:Label {prop1: value, prop2: value})
    RETURN variable.prop3
    
    MATCH (variable {prop1:value})
    RETURN variable.prop2, variable.prop3


We can also specify aliases:

    MATCH (variable:Label {propertyKey1: propertyValue1})
    RETURN variable.propertyKey2 AS alias2
    
    MATCH (p:Person {born: 1965})
    RETURN p.name AS name, p.born AS `birth year`


## Relationships

Here is how Cypher uses ASCII art for specifying paths used for a query:

    ()          // a node
    ()--()      // 2 nodes have some type of relationship
    ()-->()     // the first node has a relationship to the second node
    ()<--()     // the second node has a relationship to the first node

Some example queries may be:


    MATCH (node1)-[:REL_TYPE]->(node2)
    RETURN node1, node2
    
    MATCH (node1)-[:REL_TYPEA | :REL_TYPEB]->(node2)
    RETURN node1, node2
    
    MATCH (p:Person)-[rel:ACTED_IN]->(m:Movie {title: 'The Matrix'})
    RETURN p, rel, m


find all movies related to tom hanks and print title and relationship type:
match (:person {name:"tom hanks"})-[r]->(m:movie) return m.title,type(r)


## WHERE clause

To have more flexibility within our queries we can use the WHERE clause.


Let's see some examples:

     MATCH (p:Person)-[:ACTED_IN]->(m:Movie)
     WHERE m.released = 2008
     RETURN p, m
     
     MATCH (p:Person)-[:ACTED_IN]->(m:Movie)
     WHERE m.released = 2008 OR m.released = 2009
     RETURN p, m


     MATCH (a:Person)-[:ACTED_IN]->(m:Movie)
     WHERE a.name = 'Tom Cruise'
     RETURN m.title as Movie


We can also specify ranges:

    MATCH (p:Person)-[:ACTED_IN]->(m:Movie)
    WHERE 2003 <= m.released <= 2004
    RETURN p.name, m.title, m.released

### Filter by Label with WHERE

We can also filter by labels within WHERE e.g.,:
can be rewritten using WHERE clauses as follows:

    MATCH (p)
    WHERE p:Person
    RETURN p.name

this allows extra flexibility when specifying a query, for example:
MATCH (p)-[:ACTED_IN]->(m)
WHERE p:Person AND m:Movie AND m.title='The Matrix'
RETURN p.name

### Test the existence of a property with WHERE
MATCH (p:Person)-[:ACTED_IN]->(m:Movie)
WHERE p.name='Jack Nicholson' AND exists(m.tagline)
RETURN m.title, m.tagline


### Test strings with WHERE

There are three main functions to compare strings within
a WHERE clause: STARTS WITH, ENDS WITH, and CONTAINS.

    MATCH (p:Person)-[:ACTED_IN]->()
    WHERE p.name STARTS WITH 'Michael'
    RETURN p.name
    
    MATCH (p:Person)-[:ACTED_IN]->()
    WHERE toLower(p.name) STARTS WITH 'michael'
    RETURN p.name


### Test regex with WHERE

    MATCH (p:Person)
    WHERE p.name =~'Tom.*'
    RETURN p.name


### Test patterns with WHERE 

We can also use WHERE to query with specific patterns.
For example to include negation stuff.

For example, if we want to return all Person nodes of people who wrote movies
we can do:

    MATCH (p:Person)-[:WROTE]->(m:Movie)
    RETURN p.name, m.title

We modify this query to exclude people who directed that movie:

    MATCH (p:Person)-[:WROTE]->(m:Movie)
    WHERE NOT exists( (p)-[:DIRECTED]->(m) )
    RETURN p.name, m.title

Here is another example where we want to find Gene Hackman and the movies
that he acted in with another person who also directed the movie.

    MATCH (gene:Person)-[:ACTED_IN]->(m:Movie)<-[:ACTED_IN]-(other:Person)
    WHERE gene.name= 'Gene Hackman'
    AND exists( (other)-[:DIRECTED]->(m) )
    RETURN  gene, other, m


### Test with lists in WHERE

If you have a set of values you want to test with, you can place them
in a list or you can test with an existing list in the graph.

In this example, we only want to retrieve Person nodes of people born in 1965 or 1970:

    MATCH (p:Person)
    WHERE p.born IN [1965, 1970]
    RETURN p.name as name, p.born as yearBorn

You can also compare a value to an existing list in the graph.
We know that the :ACTED_IN relationship has a property, roles that
contains the list of roles an actor had in a particular movie they acted
in. Here is the query we write to return the name of the actor who played
Neo in the movie The Matrix:

MATCH (p:Person)-[r:ACTED_IN]->(m:Movie)
WHERE  'Neo' IN r.roles AND m.title='The Matrix'
RETURN p.name



## Varying Length Paths

Any graph that represents social networking, trees, or hierarchies will
most likely have multiple paths of varying lengths. Think of the connected
relationship in LinkedIn and how connections are made by people connected
to more people. The Movie database for this training does not have much
depth of relationships, but it does have the :FOLLOWS relationship that
you learned about earlier.


We can write a MATCH clause where you want to find all of the followers of
the followers of a Person by specifying a numeric value for the number
of hops in the path. Here is an example where we want to retrieve all
Person nodes that are exactly two hops away:


    MATCH (follower:Person)-[:FOLLOWS*2]->(p:Person)
    WHERE follower.name = 'Paul Blythe'
    RETURN p

If we had specified [:FOLLOWS*] rather than [:FOLLOWS*2], the query would
return all Person nodes that are in the :FOLLOWS path from Paul Blythe.

In general, we can retrieve all paths of any length with the relationship
:RELTYPE form nodeA to nodeB and beyond by doing:

    (nodeA)-[:RELTYPE*]->(nodeB)

Retrieve the paths of lengths 1, 2, or 3 with the relationship, :RELTYPE
from nodeA to nodeB, nodeB to nodeC, as well as, nodeC to nodeD)
(up to three hops):

    (node1)-[:RELTYPE*1..3]->(node2)

To find nodes that are exactly 3 hops away we can just do:
    
    (node1)-[:RELTYPE*3]->(node2)

We can also find the shortest path in a graph that has many ways of
traversing the graph to get to the same node with the `shortestPath()`
function.

In this example, we want to discover a shortest path between the movies
The Matrix and A Few Good Men. In our MATCH clause, we set the variable p
to the result of calling shortestPath(), and then return p. In the call
to shortestPath(), notice that we specify * for the relationship. This
means any relationship; for the traversal.

    MATCH p = shortestPath((m1:Movie)-[*]-(m2:Movie))
    WHERE m1.title = 'A Few Good Men' AND
          m2.title = 'The Matrix'
          RETURN  p

Using the shortestPath algorithm is faster wrt using [:RELTYPE*1..N].


## Optional Matching

OPTIONAL MATCH matches patterns with your graph, just like MATCH does. The
difference is that if no matches are found, OPTIONAL MATCH will use NULLs
for missing parts of the pattern. OPTIONAL MATCH could be considered
the Cypher equivalent of the outer join in SQL.

Here is an example where we query the graph for all people whose name
starts with James. The OPTIONAL MATCH is specified to include people
who have reviewed movies:

    MATCH (p:Person)
    WHERE p.name STARTS WITH 'James'
    OPTIONAL MATCH (p)-[r:REVIEWED]->(m:Movie)
    RETURN p.name, type(r), m.title

Notice that for all rows that do not have the :REVIEWED relationship,
a null value is returned for the movie part of the query, as well as
the relationship.

We can think about optional match as a sort of SQL "Outer Join".

## Aggregation in Cypher

Aggregation in Cypher is different from aggregation in SQL. In Cypher,
you need not specify a grouping key. As soon as an aggregation function
is used, all non-aggregated result columns become grouping keys. The
grouping is implicitly done, based upon the fields in the RETURN clause.

For example, in this Cypher statement, all rows returned with the same
values for a.name and d.name are counted and only returned once.

    // implicitly groups by a.name and d.name
    MATCH (a)-[:ACTED_IN]->(m)<-[:DIRECTED]-(d)
    RETURN a.name, d.name, count(*)


## Collecting Results

Cypher has a built-in function, collect() that enables you to aggregate
a value into a list. Here is an example where we collect the list of
movies that Tom Cruise acted in:

    MATCH (p:Person)-[:ACTED_IN]->(m:Movie)
    WHERE p.name ='Tom Cruise'
    RETURN collect(m.title) AS `movies for Tom Cruise`

Basically collect will give us a list instead of an entire
column of data in case of RETURN m.title.

## Counting Results

The cypher `count()` function is useful whenever we want to count
the number of occurrences of a particular query result.

Example:

    MATCH (actor:Person)-[:ACTED_IN]->(m:Movie)<-[:DIRECTED]-(director:Person)
    RETURN actor.name, director.name, count(m) AS collaborations, collect(m.title) AS movies

There are more aggregating functions such as min() or max() that you
can also use in your queries. These are described in the Aggregating
Functions section of the Neo4j Cypher Manual.


## Additional Processing using "WITH"

During the execution of a MATCH clause, you can specify that you
want some intermediate calculations or values that will be used for
further processing of the query, or for limiting the number of results
before further processing is done. You use the WITH clause to perform
intermediate processing or data flow operations.

Here is an example where we start the query processing by retrieving
all actors and their movies. During the query processing, want to only
return actors that have 2 or 3 movies. All other actors and the aggregated
results are filtered out. This type of query is a replacement for SQL’s
“HAVING” clause. The WITH clause does the counting and collecting,
but is then used in the subsequent WHERE clause to limit how many paths
are visited.


    MATCH (a:Person)-[:ACTED_IN]->(m:Movie)
    WITH  a, count(a) AS numMovies, collect(m.title) as movies
    WHERE numMovies > 1 AND numMovies < 4
    RETURN a.name, numMovies, movies


WITH in this case allows us what fieds we are interested in also
if they are subject to intermediate computations.
In this case we get for each path of type (person acted in movie)
the "person", the how many movies that person acted in, and the
titles of movies.


Here is another example where we want to find all actors who have acted
in at least five movies, and find (optionally) the movies they directed
and return the person and those movies.

    MATCH (p:Person)
    WITH p, size((p)-[:ACTED_IN]->(:Movie)) AS movies
    WHERE movies >= 5
    OPTIONAL MATCH (p)-[:DIRECTED]->(m:Movie)
    RETURN p.name, m.title


## Advanced Query Processing

We can eliminate duplicate results by using the `DISTINCT` cypher
command.

For example, we may query something like this:

    MATCH (p:Person)-[:DIRECTED | :ACTED_IN]->(m:Movie)
    WHERE p.name = 'Tom Hanks'
    RETURN m.released, collect(m.title) AS movies

And observe the duplicated results in "movies", at this point we may do:

    MATCH (p:Person)-[:DIRECTED | :ACTED_IN]->(m:Movie)
    WHERE p.name = 'Tom Hanks'
    RETURN m.released, collect(DISTINCT m.title) AS movies

In order to have a list of unique values for the "movies".

Another example to eliminate duplication may be:

    MATCH (p:Person)-[:DIRECTED | :ACTED_IN]->(m:Movie)
    WHERE p.name = 'Tom Hanks'
    WITH DISTINCT m
    RETURN m.released, m.title


## Controlling Output

### Ordering Results

In this example, we specify that the release date of the movies for Tom
Hanks will be returned in descending order.

    MATCH (p:Person)-[:DIRECTED | :ACTED_IN]->(m:Movie)
    WHERE p.name = 'Tom Hanks'
    RETURN m.released, collect(DISTINCT m.title) AS movies ORDER BY m.released DESC


### Limiting the Results

We can also limit the number of output results in the output.

Suppose you want to see the titles of the ten most recently released
movies. You could do so as follows where you limit the number of results
using the LIMIT keyword as follows:


    MATCH (m:Movie)
    RETURN m.title as title, m.released as year ORDER BY m.released DESC LIMIT 10

We can also use "WITH" to limit the number of results.
In this example, we count the number of movies during the query and we
return the results once we have reached 5 movies:

MATCH (a:Person)-[:ACTED_IN]->(m:Movie)
WITH a, count(*) AS numMovies, collect(m.title) as movies
WHERE numMovies = 5
RETURN a.name, numMovies, movies

## Date

Cypher has a built-in date() function, as well as other temporal values
and functions that you can use to calculate temporal values. You use
a combination of numeric, temporal, spatial, list and string functions
to calculate values that are useful to your application. For example,
suppose you wanted to calculate the age of a Person node, given a year
they were born (the born property must exist and have a value).

Here is example Cypher to retrieve all actors from the graph, and if
they have a value for born, calculate the age value.

    MATCH (actor:Person)-[:ACTED_IN]->(:Movie)
    WHERE exists(actor.born)
    // calculate the age
    with DISTINCT actor, date().year  - actor.born as age
    RETURN actor.name, age as `age today`
    ORDER BY actor.born DESC


## Creating Data


### Creating Nodes

Let'ss see some examples, the general form is:

    CREATE (optionalVariable optionalLabels {optionalProperties})

For example: 

    CREATE (:Movie {title: 'Batman Begins'})

We can use more labels by doing:

    CREATE (:Movie:Action {title: 'Batman Begins'})


We can create multiple nodes by doing:

    CREATE
    (:Person {name: 'Michael Caine', born: 1933}),
    (:Person {name: 'Liam Neeson', born: 1952}),
    (:Person {name: 'Katie Holmes', born: 1978}),
    (:Person {name: 'Benjamin Melniker', born: 1913})


NOTE:
The graph engine will create a node with the same properties of a
node that already exists. You can prevent this from happening in one
of two ways:
1. You can use MERGE rather than CREATE when creating the node.
2. You can add constraints to your graph.

### Adding Labels

We can use the "SET" instruction to add labels to node, for example:

MATCH (m:Movie)
WHERE m.title = 'Batman Begins'
SET m:Action
RETURN labels(m)

### Removing Labels

We can use the "REMOVE" instruction to add labels to node, for example:

MATCH (m:Movie)
WHERE m.title = 'Batman Begins'
REMOVE m:Action
RETURN labels(m)


### Adding Properties to a Node

We can use "SET" also to set properties for a node, for example:

SET x.propertyName1 = value1, x.propertyName2 = value2
SET x = {propertyName1: value1, propertyName2: value2}
SET x += {propertyName1: value1, propertyName2: value2}I

If the property does not exist, it is added to the node. If the property
exists, its value is updated. If the value specified is null, the property
is removed.

A practical example may be:

    MATCH (m:Movie)
    WHERE m.title = 'Batman Begins'
    SET m.released = 2005, m.lengthInMinutes = 140
    RETURN m

Another example, using JSON style notation is:

    MATCH (m:Movie)
    WHERE m.title = 'Batman Begins'
    SET  m = {title: 'Batman Begins',
              released: 2005,
              lengthInMinutes: 140,
              videoFormat: 'DVD',
              grossMillions: 206.5}
    RETURN m


Here is an example where we use the JSON-style object to add the awards property to the node and update the grossMillions property:

    MATCH (m:Movie)
    WHERE m.title = 'Batman Begins'
    SET  m += { grossMillions: 300,
                awards: 66}
    RETURN m



### Removing Properties from a Node

We can remove properties from nodes by doing:

    REMOVE x.propertyName
or

    SET x.propertyName = null


An example may be:

    MATCH (m:Movie)
    WHERE m.title = 'Batman Begins'
    SET m.grossMillions = null
    REMOVE m.videoFormat
    RETURN m


## Creating Relationships

We can generally create relationships using the following
general forms:

    CREATE (x)-[:REL_TYPE]->(y)
    CREATE (x)<-[:REL_TYPE]-(y)


Here is an example. We want to connect the actor, Michael Caine with
the movie, Batman Begins. We first retrieve the nodes of interest,
then we create the relationship:

    MATCH (a:Person), (m:Movie)
    WHERE a.name = 'Michael Caine' AND m.title = 'Batman Begins'
    CREATE (a)-[:ACTED_IN]->(m)
    RETURN a, m

Another example is:

    MATCH (a:Person), (m:Movie), (p:Person)
    WHERE a.name = 'Liam Neeson' AND
          m.title = 'Batman Begins' AND
          p.name = 'Benjamin Melniker'
    CREATE (a)-[:ACTED_IN]->(m)<-[:PRODUCED]-(p)
    RETURN a, m, p


At the same way note that we can create/delete or update relationships
as we did with nodes.


## Merge Data in Graphs

If you use CREATE:

The result is:

Node - If a node with the same property values exists, a duplicate node is created.

Label - If the label already exists for the node, the node is not updated.

Property - If the node or relationship property already exists, it is
           updated with the new value.  Note: If you specify a set of properties
           to be created using = rather than +=, existing properties are removed
           if they are not included in the set.

Relationship - If the relationship exists, a duplicate relationship is created.

WARNING: You should never create duplicate nodes or relationships in a graph.

The MERGE clause is used to find elements in the graph. If the element
is not found, it is created.

You use the MERGE clause to:

- Create a unique node based on label and key information for a property
  and if it exists, optionally update it.
- Create a unique relationship.
- Create a node and relationship to it uniquely in the context of another node.


### Using MERGE to create nodes


Here is the general syntax for the MERGE clause for creating a node:

    MERGE (variable:Label{nodeProperties})
    RETURN variable

For example:

    MERGE (a:Actor {name: 'Michael Caine'})
    SET a.born = 1933
    RETURN a

