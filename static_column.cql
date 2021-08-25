/*
to run this file do
cqlsh <host> <port> -f <file_address>
*/
/*
to run a file in cql shell do 
source '<file_address>'
*/
/*
Creating columns with a single value (static column)
In a table that uses clustering columns, non-clustering columns can be declared static in the table definition. Static columns are only static within a given partition.
*/

CREATE TABLE my_keyspace.t (
  k text,
  s text STATIC,
  i int,
  PRIMARY KEY (k, i)
);
INSERT INTO my_keyspace.t (k, s, i) VALUES ('k', 'I am shared', 0);
INSERT INTO my_keyspace.t (k, s, i) VALUES ('k', 'I am still shared', 1);
SELECT * FROM my_keyspace.t;
/*
Output:

 k |                  s | i   
----------------------------
k  | "I'm still shared" | 0 
k  | "I'm still shared" | 1   
*/
/*    
Restriction:
A table that does not define any clustering columns cannot have a static column. The table that does not have clustering columns has a one-row partition in which every column is inherently static.
A column designated to be the partition key cannot be static.
You can batch conditional updates to a static column.

Use the DISTINCT keyword to select static columns. In this case, the database retrieves only the beginning (static column) of the partition.
*/