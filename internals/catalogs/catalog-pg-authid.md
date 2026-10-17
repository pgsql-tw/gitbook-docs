<a id="CATALOG-PG-AUTHID"></a>

## 52.8. `pg_authid` [#](#CATALOG-PG-AUTHID)

<a id="id-1.10.4.10.2"></a>

系統目錄 `pg_authid` 包含資料庫授權識別碼（角色）的相關資訊。
角色涵蓋了「使用者」與「群組」的概念。使用者本質上就只是
設定了 `rolcanlogin` 旗標的角色。任何角色（無論是否設定
`rolcanlogin`）都可以有其他角色作為成員；請參閱
[`pg_auth_members`](catalog-pg-auth-members.md)。

由於此系統目錄包含密碼，它不得開放公開讀取。
[`pg_roles`](../views/view-pg-roles.md)
是建立在 `pg_authid` 上、可公開讀取的檢視表，
它會將密碼欄位遮蔽為空白。

[第 21 章](../../server-administration/user-manag/README.md)包含使用者與
權限管理的詳細資訊。

由於使用者身分是整個叢集通用的，
`pg_authid`
由叢集中的所有資料庫共用：每個叢集只有一份
`pg_authid`，而不是每個資料庫各一份。

<a id="id-1.10.4.10.7"></a>

**表 52.8. `pg_authid` 欄位**

<table border="1" class="table" summary="表 52.8. pg_authid 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">oid</code> <code class="type">oid</code>
</p>
<p>
       資料列識別碼
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">rolname</code> <code class="type">name</code>
</p>
<p>
       角色名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">rolsuper</code> <code class="type">bool</code>
</p>
<p>
       角色具有超級使用者權限
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">rolinherit</code> <code class="type">bool</code>
</p>
<p>
       角色自動繼承它身為成員之各角色的權限
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">rolcreaterole</code> <code class="type">bool</code>
</p>
<p>
       角色可以建立更多角色
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">rolcreatedb</code> <code class="type">bool</code>
</p>
<p>
       角色可以建立資料庫
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">rolcanlogin</code> <code class="type">bool</code>
</p>
<p>
       角色可以登入。也就是說，此角色可以作為初始的工作階段
       授權識別碼。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">rolreplication</code> <code class="type">bool</code>
</p>
<p>
       角色是複寫角色。複寫角色可以發起複寫連線，
       並建立及移除複寫插槽。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">rolbypassrls</code> <code class="type">bool</code>
</p>
<p>
       角色會略過所有資料列層級安全性政策，詳細資訊請參閱
       <a class="xref" href="../../the-sql-language/ddl/ddl-rowsecurity.md">第 5.9 節</a>。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">rolconnlimit</code> <code class="type">int4</code>
</p>
<p>
       對於可以登入的角色，此值設定此角色可建立的最大同時
       連線數。-1 表示沒有限制。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">rolpassword</code> <code class="type">text</code>
</p>
<p>
       加密後的密碼；若無則為 null。其格式取決於
       所使用的加密形式。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">rolvaliduntil</code> <code class="type">timestamptz</code>
</p>
<p>
       密碼到期時間（僅用於密碼認證）；
       若不會到期則為 null
      </p></td></tr></tbody></table>

<br>

對於 MD5 加密的密碼，`rolpassword`
欄位會以字串 `md5` 開頭，後接
32 個字元的十六進位 MD5 雜湊值。此 MD5 雜湊值是對使用者的
密碼串接其使用者名稱後計算而得。例如，若使用者
`joe` 的密碼是 `xyzzy`，PostgreSQL
會存放 `xyzzyjoe` 的 MD5 雜湊值。

### 警告

MD5 加密密碼的支援已被棄用，並將在 PostgreSQL 的未來版本中移除。
關於遷移到其他密碼類型的詳細資訊，請參閱
[第 20.5 節](../../server-administration/client-authentication/auth-password.md)。

若密碼以 SCRAM-SHA-256 加密，其格式為：

```

SCRAM-SHA-256$<iteration count>:<salt>$<StoredKey>:<ServerKey>
```

其中 *`salt`*、*`StoredKey`* 與
*`ServerKey`* 採用 Base64 編碼格式。此格式
與 [RFC 5803](https://datatracker.ietf.org/doc/html/rfc5803) 所規定的格式相同。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-authid.html)（原文版本：18.6；核對日期：2026-10-17）
