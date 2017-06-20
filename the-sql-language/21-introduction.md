# 2.1. 簡介[^1]

This chapter provides an overview of how to useSQLto perform simple operations. This tutorial is only intended to give you an introduction and is in no way a complete tutorial onSQL. Numerous books have been written onSQL, including[\[melt93\]](https://www.postgresql.org/docs/10/static/biblio.html#melt93)and[\[date97\]](https://www.postgresql.org/docs/10/static/biblio.html#date97). You should be aware that somePostgreSQLlanguage features are extensions to the standard.

In the examples that follow, we assume that you have created a database named`mydb`, as described in the previous chapter, and have been able to startpsql.

Examples in this manual can also be found in thePostgreSQLsource distribution in the directory`src/tutorial/`. \(Binary distributions ofPostgreSQLmight not compile these files.\) To use those files, first change to that directory and runmake:

```
$
cd 
....
/src/tutorial
$
make
```

This creates the scripts and compiles the C files containing user-defined functions and types. Then, to start the tutorial, do the following:

```
$
cd 
....
/tutorial
$
psql -s mydb
...
mydb=
>
\i basics.sql
```

The`\i`command reads in commands from the specified file.`psql`'s`-s`option puts you in single step mode which pauses before sending each statement to the server. The commands used in this section are in the file`basics.sql`.

---

[^1]: [PostgreSQL: Documentation: 10: 2.1. Introduction](https://www.postgresql.org/docs/10/static/tutorial-sql-intro.html)

