# 5.6. 權限[^1]

When an object is created, it is assigned an owner. The owner is normally the role that executed the creation statement. For most kinds of objects, the initial state is that only the owner \(or a superuser\) can do anything with the object. To allow other roles to use it,_privileges_must be granted.

There are different kinds of privileges:`SELECT`,`INSERT`,`UPDATE`,`DELETE`,`TRUNCATE`,`REFERENCES`,`TRIGGER`,`CREATE`,`CONNECT`,`TEMPORARY`,`EXECUTE`, and`USAGE`. The privileges applicable to a particular object vary depending on the object's type \(table, function, etc\). For complete information on the different types of privileges supported byPostgreSQL, refer to the[GRANT](https://www.postgresql.org/docs/10/static/sql-grant.html)reference page. The following sections and chapters will also show you how those privileges are used.

The right to modify or destroy an object is always the privilege of the owner only.

An object can be assigned to a new owner with an`ALTER`command of the appropriate kind for the object, e.g.[ALTER TABLE](https://www.postgresql.org/docs/10/static/sql-altertable.html). Superusers can always do this; ordinary roles can only do it if they are both the current owner of the object \(or a member of the owning role\) and a member of the new owning role.

To assign privileges, the`GRANT`command is used. For example, if`joe`is an existing role, and`accounts`is an existing table, the privilege to update the table can be granted with:

```
GRANT UPDATE ON accounts TO joe;

```

Writing`ALL`in place of a specific privilege grants all privileges that are relevant for the object type.

The special“role”name`PUBLIC`can be used to grant a privilege to every role on the system. Also,“group”roles can be set up to help manage privileges when there are many users of a database — for details see[Chapter 21](https://www.postgresql.org/docs/10/static/user-manag.html).

To revoke a privilege, use the fittingly named`REVOKE`command:

```
REVOKE ALL ON accounts FROM PUBLIC;

```

The special privileges of the object owner \(i.e., the right to do`DROP`,`GRANT`,`REVOKE`, etc.\) are always implicit in being the owner, and cannot be granted or revoked. But the object owner can choose to revoke their own ordinary privileges, for example to make a table read-only for themselves as well as others.

Ordinarily, only the object's owner \(or a superuser\) can grant or revoke privileges on an object. However, it is possible to grant a privilege“with grant option”, which gives the recipient the right to grant it in turn to others. If the grant option is subsequently revoked then all who received the privilege from that recipient \(directly or through a chain of grants\) will lose the privilege. For details see the[GRANT](https://www.postgresql.org/docs/10/static/sql-grant.html)and[REVOKE](https://www.postgresql.org/docs/10/static/sql-revoke.html)reference pages.

---



[^1]: [PostgreSQL: Documentation: 10: 5.6. Privileges](https://www.postgresql.org/docs/10/static/ddl-priv.html)

