## 35.1. The Schema [#](#INFOSCHEMA-SCHEMA)

The information schema itself is a schema named
`information_schema`. This schema automatically
exists in all databases. The owner of this schema is the initial
database user in the cluster, and that user naturally has all the
privileges on this schema, including the ability to drop it (but
the space savings achieved by that are minuscule).

By default, the information schema is not in the schema search
path, so you need to access all objects in it through qualified
names. Since the names of some of the objects in the information
schema are generic names that might occur in user applications, you
should be careful if you want to put the information schema in the
path.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/infoschema-schema.html)（英文原文，待翻譯）
