# 40. The Rule System[^1]

**Table of Contents**

[40.1. The Query Tree](https://www.postgresql.org/docs/10/static/querytree.html)

[40.2. Views and the Rule System](https://www.postgresql.org/docs/10/static/rules-views.html)

[40.2.1. How`SELECT`Rules Work](https://www.postgresql.org/docs/10/static/rules-views.html#rules-select)

[40.2.2. View Rules in Non-`SELECT`Statements](https://www.postgresql.org/docs/10/static/rules-views.html#idm45262084437216)

[40.2.3. The Power of Views inPostgreSQL](https://www.postgresql.org/docs/10/static/rules-views.html#idm45262084404432)

[40.2.4. Updating a View](https://www.postgresql.org/docs/10/static/rules-views.html#rules-views-update)

[40.3. Materialized Views](https://www.postgresql.org/docs/10/static/rules-materializedviews.html)

[40.4. Rules on`INSERT`,`UPDATE`, and`DELETE`](https://www.postgresql.org/docs/10/static/rules-update.html)

[40.4.1. How Update Rules Work](https://www.postgresql.org/docs/10/static/rules-update.html#idm45262084318800)

[40.4.2. Cooperation with Views](https://www.postgresql.org/docs/10/static/rules-update.html#rules-update-views)

[40.5. Rules and Privileges](https://www.postgresql.org/docs/10/static/rules-privileges.html)

[40.6. Rules and Command Status](https://www.postgresql.org/docs/10/static/rules-status.html)

[40.7. Rules Versus Triggers](https://www.postgresql.org/docs/10/static/rules-triggers.html)



This chapter discusses the rule system inPostgreSQL. Production rule systems are conceptually simple, but there are many subtle points involved in actually using them.

Some other database systems define active database rules, which are usually stored procedures and triggers. InPostgreSQL, these can be implemented using functions and triggers as well.

The rule system \(more precisely speaking, the query rewrite rule system\) is totally different from stored procedures and triggers. It modifies queries to take rules into consideration, and then passes the modified query to the query planner for planning and execution. It is very powerful, and can be used for many things such as query language procedures, views, and versions. The theoretical foundations and the power of this rule system are also discussed in[\[ston90b\]](https://www.postgresql.org/docs/10/static/biblio.html#ston90b)and[\[ong90\]](https://www.postgresql.org/docs/10/static/biblio.html#ong90).

---



[^1]:  [PostgreSQL: Documentation: 10: Chapter 40. The Rule System](https://www.postgresql.org/docs/10/static/rules.html)

