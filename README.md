# inserts

### How to use
To use this script, you need a .sql that contains all of the *CREATE TABLE*
statements of the tables that you want to generate inserts for, ordered by
dependecy, this means that if you have a table users that depends on a table
roles, *CREATE TABLE users* should appear first in the file.
Also, all of the MySQL reserved words should be in UPPERCASE.

#### Supported datatypes
*CHAR(1)*
*INT*
*DATETIME*
*DATE*
*VARCHAR*
*TEXT*

You need python3.6 to execute this script.
If you're sure that everything is ok, you can generate the code with the
following command.

*python3.6 inserts.py n /path/to/script.sql*

Where n is the number of inserts you want to generate for each table.
