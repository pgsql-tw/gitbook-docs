## H.1. 用戶端介面 [#](#EXTERNAL-INTERFACES)

<a id="id-1.11.9.3.2"></a>

PostgreSQL 基本發行版只包含兩種用戶端介面：

* [libpq](../../client-interfaces/libpq/README.md) 是主要的 C 語言介面，而且許多其他用戶端介面都以它為基礎，因此納入發行版。
* [ECPG](../../client-interfaces/ecpg/README.md) 依賴伺服器端的 SQL 語法，因此容易受到 PostgreSQL 本身變更的影響，所以也納入發行版。

所有其他語言介面都是外部專案，並各自發行。PostgreSQL wiki 維護了一份[語言介面清單](https://wiki.postgresql.org/wiki/List_of_drivers)。請注意，其中部分套件採用的授權條款與 PostgreSQL 不同。各語言介面的更多資訊（包括授權條款），請參閱其網站與文件。

<https://wiki.postgresql.org/wiki/List_of_drivers>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/external-interfaces.html)（原文版本：18.6；核對日期：2026-09-07）
