# 46. PL/Python - Python Procedural Language

The PL/Python procedural language allows PostgreSQL functions to be written in the [Python language](https://www.python.org/).

To install PL/Python in a particular database, use `CREATE EXTENSION plpythonu` \(but see also [Section 46.1](https://www.postgresql.org/docs/current/plpython-python23.html)\).

#### Tip

If a language is installed into `template1`, all subsequently created databases will have the language installed automatically.

PL/Python is only available as an “untrusted” language, meaning it does not offer any way of restricting what users can do in it and is therefore named `plpythonu`. A trusted variant `plpython` might become available in the future if a secure execution mechanism is developed in Python. The writer of a function in untrusted PL/Python must take care that the function cannot be used to do anything unwanted, since it will be able to do anything that could be done by a user logged in as the database administrator. Only superusers can create functions in untrusted languages such as `plpythonu`.

#### Note

Users of source packages must specially enable the build of PL/Python during the installation process. \(Refer to the installation instructions for more information.\) Users of binary packages might find PL/Python in a separate subpackage.

