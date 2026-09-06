## 35.5. `applicable_roles` [#](#INFOSCHEMA-APPLICABLE-ROLES)

The view `applicable_roles` identifies all roles
whose privileges the current user can use. This means there is
some chain of role grants from the current user to the role in
question. The current user itself is also an applicable role. The
set of applicable roles is generally used for permission checking.
<a id="id-1.7.6.9.2.2"></a>
<a id="id-1.7.6.9.2.3"></a>

<a id="id-1.7.6.9.3"></a>

**Table 35.3. `applicable_roles` Columns**

<table border="1" class="table" summary="applicable_roles Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">grantee</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the role to which this role membership was granted (can
       be the current user, or a different role in case of nested role
       memberships)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">role_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of a role
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">is_grantable</code> <code class="type">yes_or_no</code>
</p>
<p>
<code class="literal">YES</code> if the grantee has the admin option on
       the role, <code class="literal">NO</code> if not
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/infoschema-applicable-roles.html)（英文原文，待翻譯）
