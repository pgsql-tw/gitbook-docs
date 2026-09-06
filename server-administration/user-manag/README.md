## Chapter 21. Database Roles

**Table of Contents**

[21.1. Database Roles](database-roles.md)

[21.2. Role Attributes](role-attributes.md)

[21.3. Role Membership](role-membership.md)

[21.4. Dropping Roles](role-removal.md)

[21.5. Predefined Roles](predefined-roles.md)

[21.6. Function Security](perm-functions.md)

PostgreSQL manages database access permissions
using the concept of *roles*. A role can be thought of as
either a database user, or a group of database users, depending on how
the role is set up. Roles can own database objects (for example, tables
and functions) and can assign privileges on those objects to other roles to
control who has access to which objects. Furthermore, it is possible
to grant *membership* in a role to another role, thus
allowing the member role to use privileges assigned to another role.

The concept of roles subsumes the concepts of “users” and
“groups”. In PostgreSQL versions
before 8.1, users and groups were distinct kinds of entities, but now
there are only roles. Any role can act as a user, a group, or both.

This chapter describes how to create and manage roles.
More information about the effects of role privileges on various
database objects can be found in [Section 5.8](../../the-sql-language/ddl/ddl-priv.md).

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/user-manag.html)（英文原文，待翻譯）
