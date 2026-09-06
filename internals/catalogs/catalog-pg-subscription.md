## 52.54. `pg_subscription` [#](#CATALOG-PG-SUBSCRIPTION)

<a id="id-1.10.4.56.2"></a>

The catalog `pg_subscription` contains all existing
logical replication subscriptions. For more information about logical
replication see [Chapter 29](../../server-administration/logical-replication/README.md).

Unlike most system catalogs, `pg_subscription` is
shared across all databases of a cluster: there is only one copy
of `pg_subscription` per cluster, not one per
database.

Access to the column `subconninfo` is revoked from
normal users, because it could contain plain-text passwords.

<a id="id-1.10.4.56.6"></a>

**Table 52.54. `pg_subscription` Columns**

<table border="1" class="table" summary="pg_subscription Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">oid</code> <code class="type">oid</code>
</p>
<p>
       Row identifier
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">subdbid</code> <code class="type">oid</code>
       (references <a class="link" href="catalog-pg-database.md"><code class="structname">pg_database</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       OID of the database that the subscription resides in
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">subskiplsn</code> <code class="type">pg_lsn</code>
</p>
<p>
       Finish LSN of the transaction whose changes are to be skipped, if a valid
       LSN; otherwise <code class="literal">0/0</code>.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">subname</code> <code class="type">name</code>
</p>
<p>
       Name of the subscription
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">subowner</code> <code class="type">oid</code>
       (references <a class="link" href="catalog-pg-authid.md"><code class="structname">pg_authid</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       Owner of the subscription
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">subenabled</code> <code class="type">bool</code>
</p>
<p>
       If true, the subscription is enabled and should be replicating
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">subbinary</code> <code class="type">bool</code>
</p>
<p>
       If true, the subscription will request that the publisher send data
       in binary format
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">substream</code> <code class="type">char</code>
</p>
<p>
       Controls how to handle the streaming of in-progress transactions:
       <code class="literal">f</code> = disallow streaming of in-progress transactions,
       <code class="literal">t</code> = spill the changes of in-progress transactions to
       disk and apply at once after the transaction is committed on the
       publisher and received by the subscriber,
       <code class="literal">p</code> = apply changes directly using a parallel apply
       worker if available (same as <code class="literal">t</code> if no worker is
       available)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">subtwophasestate</code> <code class="type">char</code>
</p>
<p>
       State codes for two-phase mode:
       <code class="literal">d</code> = disabled,
       <code class="literal">p</code> = pending enablement,
       <code class="literal">e</code> = enabled
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">subdisableonerr</code> <code class="type">bool</code>
</p>
<p>
       If true, the subscription will be disabled if one of its workers
       detects an error
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">subpasswordrequired</code> <code class="type">bool</code>
</p>
<p>
       If true, the subscription will be required to specify a password
       for authentication
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">subrunasowner</code> <code class="type">bool</code>
</p>
<p>
       If true, the subscription will be run with the permissions
       of the subscription owner
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">subfailover</code> <code class="type">bool</code>
</p>
<p>
       If true, the associated replication slots (i.e. the main slot and the
       table synchronization slots) in the upstream database are enabled to be
       synchronized to the standbys
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">subconninfo</code> <code class="type">text</code>
</p>
<p>
       Connection string to the upstream database
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">subslotname</code> <code class="type">name</code>
</p>
<p>
       Name of the replication slot in the upstream database (also used
       for the local replication origin name);
       null represents <code class="literal">NONE</code>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">subsynccommit</code> <code class="type">text</code>
</p>
<p>
       The <code class="varname">synchronous_commit</code>
       setting for the subscription's workers to use
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">subpublications</code> <code class="type">text[]</code>
</p>
<p>
       Array of subscribed publication names. These reference
       publications defined in the upstream database. For more on publications
       see <a class="xref" href="../../server-administration/logical-replication/logical-replication-publication.md">Section 29.1</a>.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">suborigin</code> <code class="type">text</code>
</p>
<p>
       The origin value must be either <code class="literal">none</code> or
       <code class="literal">any</code>. The default is <code class="literal">any</code>.
       If <code class="literal">none</code>, the subscription will request the publisher
       to only send changes that don't have an origin. If
       <code class="literal">any</code>, the publisher sends changes regardless of their
       origin.
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-subscription.html)（英文原文，待翻譯）
