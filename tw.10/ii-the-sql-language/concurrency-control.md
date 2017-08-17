# 13. 一致性管理[^1]

This chapter describes the behavior of the

PostgreSQL

database system when two or more sessions try to access the same data at the same time. The goals in that situation are to allow efficient access for all sessions while maintaining strict data integrity. Every developer of database applications should be familiar with the topics covered in this chapter.

---



[^1]:  [PostgreSQL: Documentation: 10: Chapter 13. Concurrency Control](https://www.postgresql.org/docs/10/static/mvcc.html)

