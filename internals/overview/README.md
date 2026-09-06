## Chapter 51. Overview of PostgreSQL Internals

**Table of Contents**

[51.1. The Path of a Query](query-path.md)

[51.2. How Connections Are Established](connect-estab.md)

[51.3. The Parser Stage](parser-stage.md)
:   [51.3.1. Parser](parser-stage.md#PARSER-STAGE-PARSER)

    [51.3.2. Transformation Process](parser-stage.md#PARSER-STAGE-TRANSFORMATION-PROCESS)

[51.4. The PostgreSQL Rule System](rule-system.md)

[51.5. Planner/Optimizer](planner-optimizer.md)
:   [51.5.1. Generating Possible Plans](planner-optimizer.md#PLANNER-OPTIMIZER-GENERATING-POSSIBLE-PLANS)

[51.6. Executor](executor.md)

### Author

This chapter originated as part of
[[sim98]](../../bibliography.md#SIM98) Stefan Simkovics'
Master's Thesis prepared at Vienna University of Technology under the direction
of O.Univ.Prof.Dr. Georg Gottlob and Univ.Ass. Mag. Katrin Seyr.

This chapter gives an overview of the internal structure of the
backend of PostgreSQL. After having
read the following sections you should have an idea of how a query
is processed. This chapter is intended to help the reader
understand the general sequence of operations that occur within the
backend from the point at which a query is received, to the point
at which the results are returned to the client.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/overview.html)（英文原文，待翻譯）
