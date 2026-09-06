## Chapter 39. The Rule System

**Table of Contents**

[39.1. The Query Tree](querytree.md)

[39.2. Views and the Rule System](rules-views.md)
:   [39.2.1. How `SELECT` Rules Work](rules-views.md#RULES-SELECT)

    [39.2.2. View Rules in Non-`SELECT` Statements](rules-views.md#RULES-VIEWS-NON-SELECT)

    [39.2.3. The Power of Views in PostgreSQL](rules-views.md#RULES-VIEWS-POWER)

    [39.2.4. Updating a View](rules-views.md#RULES-VIEWS-UPDATE)

[39.3. Materialized Views](rules-materializedviews.md)

[39.4. Rules on `INSERT`, `UPDATE`, and `DELETE`](rules-update.md)
:   [39.4.1. How Update Rules Work](rules-update.md#RULES-UPDATE-HOW)

    [39.4.2. Cooperation with Views](rules-update.md#RULES-UPDATE-VIEWS)

[39.5. Rules and Privileges](rules-privileges.md)

[39.6. Rules and Command Status](rules-status.md)

[39.7. Rules Versus Triggers](rules-triggers.md)

<a id="id-1.8.6.2"></a>

This chapter discusses the rule system in
PostgreSQL. Production rule systems
are conceptually simple, but there are many subtle points
involved in actually using them.

Some other database systems define active database rules, which
are usually stored procedures and triggers. In
PostgreSQL, these can be implemented
using functions and triggers as well.

The rule system (more precisely speaking, the query rewrite rule
system) is totally different from stored procedures and triggers.
It modifies queries to take rules into consideration, and then
passes the modified query to the query planner for planning and
execution. It is very powerful, and can be used for many things
such as query language procedures, views, and versions. The
theoretical foundations and the power of this rule system are
also discussed in [[ston90b]](../../bibliography.md#STON90B) and [[ong90]](../../bibliography.md#ONG90).

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/rules.html)（英文原文，待翻譯）
