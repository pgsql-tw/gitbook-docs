# 2. PostgreSQL沿革

The object-relational database management system now known asPostgreSQLis derived from thePOSTGRESpackage written at the University of California at Berkeley. With over two decades of development behind it,PostgreSQLis now the most advanced open-source database available anywhere.

### 2.1. The BerkeleyPOSTGRESProject



ThePOSTGRESproject, led by Professor Michael Stonebraker, was sponsored by the Defense Advanced Research Projects Agency \(DARPA\), the Army Research Office \(ARO\), the National Science Foundation \(NSF\), and ESL, Inc. The implementation ofPOSTGRESbegan in 1986. The initial concepts for the system were presented in[\[ston86\]](https://www.postgresql.org/docs/10/static/biblio.html#ston86), and the definition of the initial data model appeared in[\[rowe87\]](https://www.postgresql.org/docs/10/static/biblio.html#rowe87). The design of the rule system at that time was described in[\[ston87a\]](https://www.postgresql.org/docs/10/static/biblio.html#ston87a). The rationale and architecture of the storage manager were detailed in[\[ston87b\]](https://www.postgresql.org/docs/10/static/biblio.html#ston87b).

POSTGREShas undergone several major releases since then. The first“demoware”system became operational in 1987 and was shown at the 1988ACM-SIGMODConference. Version 1, described in[\[ston90a\]](https://www.postgresql.org/docs/10/static/biblio.html#ston90a), was released to a few external users in June 1989. In response to a critique of the first rule system \([\[ston89\]](https://www.postgresql.org/docs/10/static/biblio.html#ston89)\), the rule system was redesigned \([\[ston90b\]](https://www.postgresql.org/docs/10/static/biblio.html#ston90b)\), and Version 2 was released in June 1990 with the new rule system. Version 3 appeared in 1991 and added support for multiple storage managers, an improved query executor, and a rewritten rule system. For the most part, subsequent releases untilPostgres95\(see below\) focused on portability and reliability.

POSTGREShas been used to implement many different research and production applications. These include: a financial data analysis system, a jet engine performance monitoring package, an asteroid tracking database, a medical information database, and several geographic information systems.POSTGREShas also been used as an educational tool at several universities. Finally, Illustra Information Technologies \(later merged into[Informix](http://www.informix.com/), which is now owned by[IBM](http://www.ibm.com/)\) picked up the code and commercialized it. In late 1992,POSTGRESbecame the primary data manager for the[Sequoia 2000 scientific computing project](http://meteora.ucsd.edu/s2k/s2k_home.html).

The size of the external user community nearly doubled during 1993. It became increasingly obvious that maintenance of the prototype code and support was taking up large amounts of time that should have been devoted to database research. In an effort to reduce this support burden, the BerkeleyPOSTGRESproject officially ended with Version 4.2.

### 2.2. Postgres95



In 1994, Andrew Yu and Jolly Chen added an SQL language interpreter toPOSTGRES. Under a new name,Postgres95was subsequently released to the web to find its own way in the world as an open-source descendant of the originalPOSTGRESBerkeley code.

Postgres95code was completely ANSI C and trimmed in size by 25%. Many internal changes improved performance and maintainability.Postgres95release 1.0.x ran about 30-50% faster on the Wisconsin Benchmark compared toPOSTGRES, Version 4.2. Apart from bug fixes, the following were the major enhancements:

* The query language PostQUEL was replaced withSQL\(implemented in the server\). \(Interface library[libpq](https://www.postgresql.org/docs/10/static/libpq.html)was named after PostQUEL.\) Subqueries were not supported untilPostgreSQL\(see below\), but they could be imitated inPostgres95with user-definedSQLfunctions. Aggregate functions were re-implemented. Support for the`GROUP BY`query clause was also added.

* A new program \(psql\) was provided for interactive SQL queries, which usedGNUReadline. This largely superseded the oldmonitorprogram.

* A new front-end library,`libpgtcl`, supportedTcl-based clients. A sample shell,`pgtclsh`, provided new Tcl commands to interfaceTclprograms with thePostgres95server.

* The large-object interface was overhauled. The inversion large objects were the only mechanism for storing large objects. \(The inversion file system was removed.\)

* The instance-level rule system was removed. Rules were still available as rewrite rules.

* A short tutorial introducing regularSQLfeatures as well as those ofPostgres95was distributed with the source code

* GNUmake \(instead ofBSDmake\) was used for the build. Also,Postgres95could be compiled with an unpatchedGCC\(data alignment of doubles was fixed\).

### 2.3. PostgreSQL

By 1996, it became clear that the name“Postgres95”would not stand the test of time. We chose a new name,PostgreSQL, to reflect the relationship between the originalPOSTGRESand the more recent versions withSQLcapability. At the same time, we set the version numbering to start at 6.0, putting the numbers back into the sequence originally begun by the BerkeleyPOSTGRESproject.

Many people continue to refer toPostgreSQLas“Postgres”\(now rarely in all capital letters\) because of tradition or because it is easier to pronounce. This usage is widely accepted as a nickname or alias.

The emphasis during development ofPostgres95was on identifying and understanding existing problems in the server code. WithPostgreSQL, the emphasis has shifted to augmenting features and capabilities, although work continues in all areas.

Details about what has happened inPostgreSQLsince then can be found in[Appendix E](https://www.postgresql.org/docs/10/static/release.html).

---

* [https://www.postgresql.org/docs/10/static/history.html](https://www.postgresql.org/docs/10/static/history.html)



