## H.1. Client Interfaces [#](#EXTERNAL-INTERFACES)

<a id="id-1.11.9.3.2"></a>

There are only two client interfaces included in the base
PostgreSQL distribution:

* [libpq](../../client-interfaces/libpq/README.md) is included because it is the
  primary C language interface, and because many other client interfaces
  are built on top of it.
* [ECPG](../../client-interfaces/ecpg/README.md) is included because it depends on the
  server-side SQL grammar, and is therefore sensitive to changes in
  PostgreSQL itself.

All other language interfaces are external projects and are distributed
separately. A
[list of language interfaces](https://wiki.postgresql.org/wiki/List_of_drivers)
is maintained on the PostgreSQL wiki. Note that some of these packages are
not released under the same license as PostgreSQL.
For more information on each language interface, including licensing terms,
refer to its website and documentation.

<https://wiki.postgresql.org/wiki/List_of_drivers>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/external-interfaces.html)（英文原文，待翻譯）
