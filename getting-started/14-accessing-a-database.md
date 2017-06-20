# 1.4. 存取一個資料庫[^1]

Once you have created a database, you can access it by:

* Running thePostgreSQLinteractive terminal program, called_psql_, which allows you to interactively enter, edit, and executeSQLcommands.

* Using an existing graphical frontend tool likepgAdminor an office suite withODBCorJDBCsupport to create and manipulate a database. These possibilities are not covered in this tutorial.

* Writing a custom application, using one of the several available language bindings. These possibilities are discussed further in[Part IV](https://www.postgresql.org/docs/10/static/client-interfaces.html).

You probably want to start up`psql`to try the examples in this tutorial. It can be activated for the`mydb`database by typing the command:

```
$
psql mydb
```

If you do not supply the database name then it will default to your user account name. You already discovered this scheme in the previous section using`createdb`.

In`psql`, you will be greeted with the following message:

```
psql (10beta1)
Type "help" for help.

mydb=
>
```

The last line could also be:

```
mydb=#

```

That would mean you are a database superuser, which is most likely the case if you installed thePostgreSQLinstance yourself. Being a superuser means that you are not subject to access controls. For the purposes of this tutorial that is not important.

If you encounter problems starting`psql`then go back to the previous section. The diagnostics of`createdb`and`psql`are similar, and if the former worked the latter should work as well.

The last line printed out by`psql`is the prompt, and it indicates that`psql`is listening to you and that you can typeSQLqueries into a work space maintained by`psql`. Try out these commands:

```
mydb=
>
SELECT version();

                                         version
------------------------------------------------------------------------------------------
 PostgreSQL 10beta1 on x86_64-pc-linux-gnu, compiled by gcc (Debian 4.9.2-10) 4.9.2, 64-bit
(1 row)


mydb=
>
SELECT current_date;

    date
------------
 2016-01-07
(1 row)


mydb=
>
SELECT 2 + 2;

 ?column?
----------
        4
(1 row)

```

The`psql`program has a number of internal commands that are not SQL commands. They begin with the backslash character,“`\`”. For example, you can get help on the syntax of variousPostgreSQLSQLcommands by typing:

```
mydb=
>
\h
```

To get out of`psql`, type:

```
mydb=
>
\q
```

and`psql`will quit and return you to your command shell. \(For more internal commands, type`\?`at the`psql`prompt.\) The full capabilities of`psql`are documented in[psql](https://www.postgresql.org/docs/10/static/app-psql.html). In this tutorial we will not use these features explicitly, but you can use them yourself when it is helpful.

---



[^1]: [PostgreSQL: Documentation: 10: 1.4. Accessing a Database](https://www.postgresql.org/docs/10/static/tutorial-accessdb.html)

