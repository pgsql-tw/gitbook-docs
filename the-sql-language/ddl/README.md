## Chapter 5. Data Definition

**Table of Contents**

[5.1. Table Basics](ddl-basics.md)

[5.2. Default Values](ddl-default.md)

[5.3. Identity Columns](ddl-identity-columns.md)

[5.4. Generated Columns](ddl-generated-columns.md)

[5.5. Constraints](ddl-constraints.md)
:   [5.5.1. Check Constraints](ddl-constraints.md#DDL-CONSTRAINTS-CHECK-CONSTRAINTS)

    [5.5.2. Not-Null Constraints](ddl-constraints.md#DDL-CONSTRAINTS-NOT-NULL)

    [5.5.3. Unique Constraints](ddl-constraints.md#DDL-CONSTRAINTS-UNIQUE-CONSTRAINTS)

    [5.5.4. Primary Keys](ddl-constraints.md#DDL-CONSTRAINTS-PRIMARY-KEYS)

    [5.5.5. Foreign Keys](ddl-constraints.md#DDL-CONSTRAINTS-FK)

    [5.5.6. Exclusion Constraints](ddl-constraints.md#DDL-CONSTRAINTS-EXCLUSION)

[5.6. System Columns](ddl-system-columns.md)

[5.7. Modifying Tables](ddl-alter.md)
:   [5.7.1. Adding a Column](ddl-alter.md#DDL-ALTER-ADDING-A-COLUMN)

    [5.7.2. Removing a Column](ddl-alter.md#DDL-ALTER-REMOVING-A-COLUMN)

    [5.7.3. Adding a Constraint](ddl-alter.md#DDL-ALTER-ADDING-A-CONSTRAINT)

    [5.7.4. Removing a Constraint](ddl-alter.md#DDL-ALTER-REMOVING-A-CONSTRAINT)

    [5.7.5. Changing a Column's Default Value](ddl-alter.md#DDL-ALTER-COLUMN-DEFAULT)

    [5.7.6. Changing a Column's Data Type](ddl-alter.md#DDL-ALTER-COLUMN-TYPE)

    [5.7.7. Renaming a Column](ddl-alter.md#DDL-ALTER-RENAMING-COLUMN)

    [5.7.8. Renaming a Table](ddl-alter.md#DDL-ALTER-RENAMING-TABLE)

[5.8. Privileges](ddl-priv.md)

[5.9. Row Security Policies](ddl-rowsecurity.md)

[5.10. Schemas](ddl-schemas.md)
:   [5.10.1. Creating a Schema](ddl-schemas.md#DDL-SCHEMAS-CREATE)

    [5.10.2. The Public Schema](ddl-schemas.md#DDL-SCHEMAS-PUBLIC)

    [5.10.3. The Schema Search Path](ddl-schemas.md#DDL-SCHEMAS-PATH)

    [5.10.4. Schemas and Privileges](ddl-schemas.md#DDL-SCHEMAS-PRIV)

    [5.10.5. The System Catalog Schema](ddl-schemas.md#DDL-SCHEMAS-CATALOG)

    [5.10.6. Usage Patterns](ddl-schemas.md#DDL-SCHEMAS-PATTERNS)

    [5.10.7. Portability](ddl-schemas.md#DDL-SCHEMAS-PORTABILITY)

[5.11. Inheritance](ddl-inherit.md)
:   [5.11.1. Caveats](ddl-inherit.md#DDL-INHERIT-CAVEATS)

[5.12. Table Partitioning](ddl-partitioning.md)
:   [5.12.1. Overview](ddl-partitioning.md#DDL-PARTITIONING-OVERVIEW)

    [5.12.2. Declarative Partitioning](ddl-partitioning.md#DDL-PARTITIONING-DECLARATIVE)

    [5.12.3. Partitioning Using Inheritance](ddl-partitioning.md#DDL-PARTITIONING-USING-INHERITANCE)

    [5.12.4. Partition Pruning](ddl-partitioning.md#DDL-PARTITION-PRUNING)

    [5.12.5. Partitioning and Constraint Exclusion](ddl-partitioning.md#DDL-PARTITIONING-CONSTRAINT-EXCLUSION)

    [5.12.6. Best Practices for Declarative Partitioning](ddl-partitioning.md#DDL-PARTITIONING-DECLARATIVE-BEST-PRACTICES)

[5.13. Foreign Data](ddl-foreign-data.md)

[5.14. Other Database Objects](ddl-others.md)

[5.15. Dependency Tracking](ddl-depend.md)

This chapter covers how one creates the database structures that
will hold one's data. In a relational database, the raw data is
stored in tables, so the majority of this chapter is devoted to
explaining how tables are created and modified and what features are
available to control what data is stored in the tables.
Subsequently, we discuss how tables can be organized into
schemas, and how privileges can be assigned to tables. Finally,
we will briefly look at other features that affect the data storage,
such as inheritance, table partitioning, views, functions, and
triggers.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ddl.html)（英文原文，待翻譯）
