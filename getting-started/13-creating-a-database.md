# 1.3. 建立一個資料庫[^1]

The first test to see whether you can access the database server is to try to create a database. A runningPostgreSQLserver can manage many databases. Typically, a separate database is used for each project or for each user.

Possibly, your site administrator has already created a database for your use. In that case you can omit this step and skip ahead to the next section.

To create a new database, in this example named`mydb`, you use the following command:

```
$
createdb mydb
```

If this produces no response then this step was successful and you can skip over the remainder of this section.

If you see a message similar to:

```
createdb: command not found

```

thenPostgreSQLwas not installed properly. Either it was not installed at all or your shell's search path was not set to include it. Try calling the command with an absolute path instead:

```
$
/usr/local/pgsql/bin/createdb mydb
```

The path at your site might be different. Contact your site administrator or check the installation instructions to correct the situation.

Another response could be this:

```
createdb: could not connect to database postgres: could not connect to server: No such file or directory
        Is the server running locally and accepting
        connections on Unix domain socket "/tmp/.s.PGSQL.5432"?

```

This means that the server was not started, or it was not started where`createdb`expected it. Again, check the installation instructions or consult the administrator.

Another response could be this:

```
createdb: could not connect to database postgres: FATAL:  role "joe" does not exist

```

where your own login name is mentioned. This will happen if the administrator has not created aPostgreSQLuser account for you. \(PostgreSQLuser accounts are distinct from operating system user accounts.\) If you are the administrator, see[Chapter 21](https://www.postgresql.org/docs/10/static/user-manag.html)for help creating accounts. You will need to become the operating system user under whichPostgreSQLwas installed \(usually`postgres`\) to create the first user account. It could also be that you were assigned aPostgreSQLuser name that is different from your operating system user name; in that case you need to use the`-U`switch or set the`PGUSER`environment variable to specify yourPostgreSQLuser name.

If you have a user account but it does not have the privileges required to create a database, you will see the following:

```
createdb: database creation failed: ERROR:  permission denied to create database

```

Not every user has authorization to create new databases. IfPostgreSQLrefuses to create databases for you then the site administrator needs to grant you permission to create databases. Consult your site administrator if this occurs. If you installedPostgreSQLyourself then you should log in for the purposes of this tutorial under the user account that you started the server as.[\[1\]](https://www.postgresql.org/docs/10/static/tutorial-createdb.html#ftn.idm46249860450640)

You can also create databases with other names.PostgreSQLallows you to create any number of databases at a given site. Database names must have an alphabetic first character and are limited to 63 bytes in length. A convenient choice is to create a database with the same name as your current user name. Many tools assume that database name as the default, so it can save you some typing. To create that database, simply type:

```
$
createdb
```

If you do not want to use your database anymore you can remove it. For example, if you are the owner \(creator\) of the database`mydb`, you can destroy it using the following command:

```
$
dropdb mydb
```

\(For this command, the database name does not default to the user account name. You always need to specify it.\) This action physically removes all files associated with the database and cannot be undone, so this should only be done with a great deal of forethought.

More about`createdb`and`dropdb`can be found in[createdb](https://www.postgresql.org/docs/10/static/app-createdb.html)and[dropdb](https://www.postgresql.org/docs/10/static/app-dropdb.html)respectively.

  


---

[\[1\]](https://www.postgresql.org/docs/10/static/tutorial-createdb.html#idm46249860450640)As an explanation for why this works:PostgreSQLuser names are separate from operating system user accounts. When you connect to a database, you can choose whatPostgreSQLuser name to connect as; if you don't, it will default to the same name as your current operating system account. As it happens, there will always be aPostgreSQLuser account that has the same name as the operating system user that started the server, and it also happens that that user always has permission to create databases. Instead of logging in as that user you can also specify the`-U`option everywhere to select aPostgreSQLuser name to connect as.

---



[^1]: [PostgreSQL: Documentation: 10: 1.3. Creating a Database](https://www.postgresql.org/docs/10/static/tutorial-createdb.html)

