# Graph Database

A graph database is all about relationships.
It is very performant, especially when information
must be retrieved.
In addition these kind of databases are very flexible,
since there is no imposed structure/constraints.

They also fit nicely in the AGILE development, since,
changes or in general any modification does not easily
disrupt the DB structure/operation.

Graph database have their own query languages to retrieve
and store data.

In a graph database we have:
- Nodes;
- Relationships;
- Properties applied to nodes and relationships;


## Relational vs Graph

Let's see a comparison between relational DBs and graph
DBs, to see how concepts more or less translate from
one DB typology to the other (Relational vs Graph):
- Tables -> Nodes
- Predefined Schema (with NULL values here and there) -> No schema (no worries about NULL values)
- Relations with foreign keys -> Relation is first class citizen (no data duplication)
- Related data fetched with joins -> Related data fetched with a pattern

Note that graph databases are not always better than relational databases,
but they shine in terms of performance when data is not highly
structured and we are interested in finding relations between nodes.
For example queries like, find all the elements related to these elements
who have this relationship with these other elements are very performant
with graphs.

So we should still prefer a Relational DB whenever we have:
- Highly structured data;
- Frequent calculations within one table;
- Grouping of data, when data naturally fits in a table structure;


## Document vs Graph

Let's see a comparison between document DBs and graph
DBs, to see how concepts more or less translate from
one DB typology to the other (Document vs Graph):
- Document -> Nodes
- No Schema -> No schema
- Relations with foreign keys or embedded -> Relation is first class citizen
- Related data fetched with joins or embedded -> Related data fetched with a pattern

Note that graph databases are not always better than document databases,
but they shine in terms of performance when data is not highly
structured and we are interested in finding relations between nodes.
For example queries like, find all the elements related to these elements
who have this relationship with these other elements are very performant
with graphs.

In general document databases are very good when we want to pieces of
information which can be easily retrieved and stored as objects in
code.


