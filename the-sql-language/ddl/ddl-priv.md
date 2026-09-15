<a id="DDL-PRIV"></a>

## 5.8. 權限 [#](#DDL-PRIV)

<a id="id-1.5.4.10.2"></a><a id="id-1.5.4.10.3"></a><a id="id-1.5.4.10.4"></a><a id="id-1.5.4.10.5"></a><a id="id-1.5.4.10.6"></a><a id="id-1.5.4.10.7"></a><a id="id-1.5.4.10.8"></a>

物件建立時，會被指派一個擁有者。擁有者通常是執行建立陳述式的角色。對大多數種類的物件而言，初始狀態是只有擁有者（或超級使用者）能對該物件做任何事。要讓其他角色能使用它，就必須授予*權限*（privilege）。

權限有不同的種類：`SELECT`、`INSERT`、`UPDATE`、`DELETE`、`TRUNCATE`、`REFERENCES`、`TRIGGER`、`CREATE`、`CONNECT`、`TEMPORARY`、`EXECUTE`、`USAGE`、`SET`、`ALTER SYSTEM` 與 `MAINTAIN`。適用於特定物件的權限，會依物件的類型（資料表、函式等）而有所不同。關於這些權限之意義的更多細節如下所述。後續各節與各章也會說明如何使用這些權限。

修改或銷毀物件的權利是身為物件擁有者所固有的，其本身無法被授予或撤銷。（不過，就像所有權限一樣，擁有者角色的成員可以繼承這項權利；請參閱[第 21.3 節](../../server-administration/user-manag/role-membership.md)。）

可以使用適用於該物件種類的 `ALTER` 命令，將物件指派給新的擁有者，例如

```

ALTER TABLE table_name OWNER TO new_owner;
```

超級使用者一律可以這麼做；一般角色只有在同時是物件的目前擁有者（或繼承擁有者角色的權限），並且能夠 `SET ROLE` 成為新的擁有者角色時，才能這麼做。舊擁有者的所有物件權限，都會隨著擁有權一併轉移給新的擁有者。

要指派權限，請使用 [GRANT](../../reference/sql-commands/sql-grant.md) 命令。例如，如果 `joe` 是一個現有的角色，而 `accounts` 是一個現有的資料表，就可以用下列命令授予更新該資料表的權限：

```

GRANT UPDATE ON accounts TO joe;
```

以 `ALL` 取代特定的權限，會授予與該物件類型相關的所有權限。

特殊的「角色」名稱 `PUBLIC` 可以用來將權限授予系統上的每一個角色。此外，當資料庫有許多使用者時，可以設定「群組」角色來協助管理權限——詳情請參閱[第 21 章](../../server-administration/user-manag/README.md)。

要撤銷先前授予的權限，請使用名稱恰如其分的 [REVOKE](../../reference/sql-commands/sql-revoke.md) 命令：

```

REVOKE ALL ON accounts FROM PUBLIC;
```

一般而言，只有物件的擁有者（或超級使用者）能夠授予或撤銷物件上的權限。不過，可以「附帶授權選項」（with grant option）授予權限，讓接收者有權再將它授予其他人。如果之後撤銷了授權選項，那麼所有從該接收者（直接或透過一連串的授權）取得該權限的人，都會失去該權限。詳情請參閱 [GRANT](../../reference/sql-commands/sql-grant.md) 與 [REVOKE](../../reference/sql-commands/sql-revoke.md) 參考頁面。

物件的擁有者可以選擇撤銷自己的一般權限，例如讓某個資料表對自己和其他人都是唯讀的。但擁有者一律被視為持有所有授權選項，因此他們隨時可以重新授予自己的權限。

可用的權限如下：

<a id="DDL-PRIV-SELECT"></a>

`SELECT` [#](#DDL-PRIV-SELECT)
:   允許從資料表、檢視表、具體化檢視表或其他類似資料表之物件的任何欄位或特定欄位進行 `SELECT`。也允許使用 `COPY TO`。在 `UPDATE`、`DELETE` 或 `MERGE` 中參照現有的欄位值，也需要這項權限。對於序列，這項權限也允許使用 `currval` 函式。對於大型物件，這項權限允許讀取該物件。
<a id="DDL-PRIV-INSERT"></a>

`INSERT` [#](#DDL-PRIV-INSERT)
:   允許將新的資料列 `INSERT` 到資料表、檢視表等之中。可以針對特定欄位授予，在這種情況下，`INSERT` 命令中只能指派這些欄位（因此其他欄位會取得預設值）。也允許使用 `COPY FROM`。
<a id="DDL-PRIV-UPDATE"></a>

`UPDATE` [#](#DDL-PRIV-UPDATE)
:   允許對資料表、檢視表等的任何欄位或特定欄位進行 `UPDATE`。（在實務上，任何稍微複雜的 `UPDATE` 命令也都需要 `SELECT` 權限，因為它必須參照資料表欄位來決定要更新哪些資料列，和／或計算欄位的新值。）`SELECT ... FOR UPDATE` 與 `SELECT ... FOR SHARE` 除了 `SELECT` 權限之外，也需要至少一個欄位上的這項權限。對於序列，這項權限允許使用 `nextval` 與 `setval` 函式。對於大型物件，這項權限允許寫入或截斷該物件。
<a id="DDL-PRIV-DELETE"></a>

`DELETE` [#](#DDL-PRIV-DELETE)
:   允許從資料表、檢視表等之中 `DELETE` 資料列。（在實務上，任何稍微複雜的 `DELETE` 命令也都需要 `SELECT` 權限，因為它必須參照資料表欄位來決定要刪除哪些資料列。）
<a id="DDL-PRIV-TRUNCATE"></a>

`TRUNCATE` [#](#DDL-PRIV-TRUNCATE)
:   允許對資料表進行 `TRUNCATE`。
<a id="DDL-PRIV-REFERENCES"></a>

`REFERENCES` [#](#DDL-PRIV-REFERENCES)
:   允許建立參照某個資料表或資料表之特定欄位的外鍵限制條件。授予這項權限時應該非常小心，因為建立外鍵的使用者可以安排在強制執行該外鍵時呼叫任意函式（例如型別轉換函式），而這類函式會以資料表擁有者的權限被呼叫。
<a id="DDL-PRIV-TRIGGER"></a>

`TRIGGER` [#](#DDL-PRIV-TRIGGER)
:   允許在資料表、檢視表等之上建立觸發程序。授予這項權限時應該非常小心，因為加入到資料表或檢視表上的任何觸發程序，都會以修改它之使用者的權限執行。
<a id="DDL-PRIV-CREATE"></a>

`CREATE` [#](#DDL-PRIV-CREATE)
:   對於資料庫，允許在該資料庫中建立新的綱要與發佈物件，並允許在該資料庫中安裝受信任的擴充功能。

    對於綱要，允許在該綱要中建立新的物件。要重新命名現有的物件，你必須擁有該物件，*而且*擁有其所屬綱要的這項權限。

    對於資料表空間，允許在該資料表空間中建立資料表、索引與暫存檔，並允許建立以該資料表空間作為預設資料表空間的資料庫。

    請注意，撤銷這項權限並不會改變現有物件的存在或位置。
<a id="DDL-PRIV-CONNECT"></a>

`CONNECT` [#](#DDL-PRIV-CONNECT)
:   允許被授權者連線到該資料庫。這項權限會在連線啟動時檢查（此外也會檢查 `pg_hba.conf` 所施加的任何限制）。
<a id="DDL-PRIV-TEMPORARY"></a>

`TEMPORARY` [#](#DDL-PRIV-TEMPORARY)
:   允許在使用該資料庫時建立暫存資料表。
<a id="DDL-PRIV-EXECUTE"></a>

`EXECUTE` [#](#DDL-PRIV-EXECUTE)
:   允許呼叫函式或程序，包括使用任何建立在該函式之上的運算子。這是唯一適用於函式與程序的權限類型。
<a id="DDL-PRIV-USAGE"></a>

`USAGE` [#](#DDL-PRIV-USAGE)
:   對於程序式語言，允許使用該語言來建立以該語言撰寫的函式。這是唯一適用於程序式語言的權限類型。

    對於綱要，允許存取綱要中包含的物件（假設這些物件本身的權限要求也已滿足）。基本上，這允許被授權者在綱要中「查找」物件。沒有這項權限，仍然可以看到物件名稱，例如藉由查詢系統目錄。此外，在撤銷這項權限之後，現有的工作階段中可能有先前已經進行過這項查找的陳述式，因此這並不是防止存取物件的完全安全方法。

    對於序列，允許使用 `currval` 與 `nextval` 函式。

    對於型別與網域，允許在建立資料表、函式及其他綱要物件時使用該型別或網域。（請注意，這項權限並不控制對該型別的所有「使用」，例如出現在查詢中的該型別值。它只會防止建立依賴於該型別的物件。這項權限的主要目的，是控制哪些使用者可以建立對某個型別的依賴關係，因為這可能會妨礙擁有者之後更改該型別。）

    對於外部資料包裝器，允許使用該外部資料包裝器建立新的伺服器。

    對於外部伺服器，允許使用該伺服器建立外部資料表。被授權者也可以建立、修改或刪除自己與該伺服器相關聯的使用者對應。
<a id="DDL-PRIV-SET"></a>

`SET` [#](#DDL-PRIV-SET)
:   允許在目前的工作階段中將伺服器組態參數設為新值。（雖然這項權限可以授予任何參數，但除了那些通常需要超級使用者權限才能設定的參數之外，它都沒有意義。）
<a id="DDL-PRIV-ALTER-SYSTEM"></a>

`ALTER SYSTEM` [#](#DDL-PRIV-ALTER-SYSTEM)
:   允許使用 [ALTER SYSTEM](../../reference/sql-commands/sql-altersystem.md) 命令將伺服器組態參數設定為新值。
<a id="DDL-PRIV-MAINTAIN"></a>

`MAINTAIN` [#](#DDL-PRIV-MAINTAIN)
:   允許對關聯執行 `VACUUM`、`ANALYZE`、`CLUSTER`、`REFRESH MATERIALIZED VIEW`、`REINDEX`、`LOCK TABLE`，以及資料庫物件統計資訊操作函式（請參閱[表 9.105](../functions/functions-admin.md#FUNCTIONS-ADMIN-STATSMOD)）。

其他命令所需的權限，列在各命令的參考頁面中。

<a id="DDL-PRIV-DEFAULT"></a>

PostgreSQL 在建立某些類型的物件時，預設會將這些物件上的權限授予 `PUBLIC`。對於資料表、資料表欄位、序列、外部資料包裝器、外部伺服器、大型物件、綱要、資料表空間或組態參數，預設不會將任何權限授予 `PUBLIC`。對於其他類型的物件，預設授予 `PUBLIC` 的權限如下：資料庫的 `CONNECT` 與 `TEMPORARY`（建立暫存資料表）權限；函式與程序的 `EXECUTE` 權限；以及語言與資料型別（包括網域）的 `USAGE` 權限。物件擁有者當然可以 `REVOKE` 預設授予的權限與明確授予的權限。（為了獲得最高的安全性，請在建立物件的同一個交易中執行 `REVOKE`；這樣就不會有其他使用者可以使用該物件的時間窗口。）此外，這些預設權限設定可以使用 [ALTER DEFAULT PRIVILEGES](../../reference/sql-commands/sql-alterdefaultprivileges.md) 命令覆寫。

[表 5.1](ddl-priv.md#PRIVILEGE-ABBREVS-TABLE) 列出了在 *ACL* 值中用於這些權限類型的單一字母縮寫。你會在下面所列的 [psql](../../reference/reference-client/app-psql.md) 命令的輸出中，或在查看系統目錄的 ACL 欄位時看到這些字母。

<a id="PRIVILEGE-ABBREVS-TABLE"></a>

**表 5.1. ACL 權限縮寫**

<table border="1" class="table" summary="ACL Privilege Abbreviations"><colgroup><col class="col1"/><col class="col2"/><col class="col3"/></colgroup><thead><tr><th>權限</th><th>縮寫</th><th>適用的物件類型</th></tr></thead><tbody><tr><td><code class="literal">SELECT</code></td><td><code class="literal">r</code> (<span class="quote">“<span class="quote">read</span>”</span>)</td><td>
<code class="literal">LARGE OBJECT</code>,
       <code class="literal">SEQUENCE</code>,
       <code class="literal">TABLE</code>（以及類似資料表的物件）,
       資料表欄位
      </td></tr><tr><td><code class="literal">INSERT</code></td><td><code class="literal">a</code> (<span class="quote">“<span class="quote">append</span>”</span>)</td><td><code class="literal">TABLE</code>, 資料表欄位</td></tr><tr><td><code class="literal">UPDATE</code></td><td><code class="literal">w</code> (<span class="quote">“<span class="quote">write</span>”</span>)</td><td>
<code class="literal">LARGE OBJECT</code>,
       <code class="literal">SEQUENCE</code>,
       <code class="literal">TABLE</code>,
       資料表欄位
      </td></tr><tr><td><code class="literal">DELETE</code></td><td><code class="literal">d</code></td><td><code class="literal">TABLE</code></td></tr><tr><td><code class="literal">TRUNCATE</code></td><td><code class="literal">D</code></td><td><code class="literal">TABLE</code></td></tr><tr><td><code class="literal">REFERENCES</code></td><td><code class="literal">x</code></td><td><code class="literal">TABLE</code>, 資料表欄位</td></tr><tr><td><code class="literal">TRIGGER</code></td><td><code class="literal">t</code></td><td><code class="literal">TABLE</code></td></tr><tr><td><code class="literal">CREATE</code></td><td><code class="literal">C</code></td><td>
<code class="literal">DATABASE</code>,
       <code class="literal">SCHEMA</code>,
       <code class="literal">TABLESPACE</code>
</td></tr><tr><td><code class="literal">CONNECT</code></td><td><code class="literal">c</code></td><td><code class="literal">DATABASE</code></td></tr><tr><td><code class="literal">TEMPORARY</code></td><td><code class="literal">T</code></td><td><code class="literal">DATABASE</code></td></tr><tr><td><code class="literal">EXECUTE</code></td><td><code class="literal">X</code></td><td><code class="literal">FUNCTION</code>, <code class="literal">PROCEDURE</code></td></tr><tr><td><code class="literal">USAGE</code></td><td><code class="literal">U</code></td><td>
<code class="literal">DOMAIN</code>,
       <code class="literal">FOREIGN DATA WRAPPER</code>,
       <code class="literal">FOREIGN SERVER</code>,
       <code class="literal">LANGUAGE</code>,
       <code class="literal">SCHEMA</code>,
       <code class="literal">SEQUENCE</code>,
       <code class="literal">TYPE</code>
</td></tr><tr><td><code class="literal">SET</code></td><td><code class="literal">s</code></td><td><code class="literal">PARAMETER</code></td></tr><tr><td><code class="literal">ALTER SYSTEM</code></td><td><code class="literal">A</code></td><td><code class="literal">PARAMETER</code></td></tr><tr><td><code class="literal">MAINTAIN</code></td><td><code class="literal">m</code></td><td><code class="literal">TABLE</code></td></tr></tbody></table>

<br>

[表 5.2](ddl-priv.md#PRIVILEGES-SUMMARY-TABLE) 使用上面所示的縮寫，彙整了每種 SQL 物件可用的權限。它也列出了可用來檢查每種物件類型之權限設定的 psql 命令。

<a id="PRIVILEGES-SUMMARY-TABLE"></a>

**表 5.2. 存取權限摘要**

<table border="1" class="table" summary="Summary of Access Privileges"><colgroup><col class="col1"/><col class="col2"/><col class="col3"/><col class="col4"/></colgroup><thead><tr><th>物件類型</th><th>所有權限</th><th>預設的 <code class="literal">PUBLIC</code> 權限</th><th><span class="application">psql</span> 命令</th></tr></thead><tbody><tr><td><code class="literal">DATABASE</code></td><td><code class="literal">CTc</code></td><td><code class="literal">Tc</code></td><td><code class="literal">\l</code></td></tr><tr><td><code class="literal">DOMAIN</code></td><td><code class="literal">U</code></td><td><code class="literal">U</code></td><td><code class="literal">\dD+</code></td></tr><tr><td><code class="literal">FUNCTION</code> 或 <code class="literal">PROCEDURE</code></td><td><code class="literal">X</code></td><td><code class="literal">X</code></td><td><code class="literal">\df+</code></td></tr><tr><td><code class="literal">FOREIGN DATA WRAPPER</code></td><td><code class="literal">U</code></td><td>無</td><td><code class="literal">\dew+</code></td></tr><tr><td><code class="literal">FOREIGN SERVER</code></td><td><code class="literal">U</code></td><td>無</td><td><code class="literal">\des+</code></td></tr><tr><td><code class="literal">LANGUAGE</code></td><td><code class="literal">U</code></td><td><code class="literal">U</code></td><td><code class="literal">\dL+</code></td></tr><tr><td><code class="literal">LARGE OBJECT</code></td><td><code class="literal">rw</code></td><td>無</td><td><code class="literal">\dl+</code></td></tr><tr><td><code class="literal">PARAMETER</code></td><td><code class="literal">sA</code></td><td>無</td><td><code class="literal">\dconfig+</code></td></tr><tr><td><code class="literal">SCHEMA</code></td><td><code class="literal">UC</code></td><td>無</td><td><code class="literal">\dn+</code></td></tr><tr><td><code class="literal">SEQUENCE</code></td><td><code class="literal">rwU</code></td><td>無</td><td><code class="literal">\dp</code></td></tr><tr><td><code class="literal">TABLE</code>（以及類似資料表的物件）</td><td><code class="literal">arwdDxtm</code></td><td>無</td><td><code class="literal">\dp</code></td></tr><tr><td>資料表欄位</td><td><code class="literal">arwx</code></td><td>無</td><td><code class="literal">\dp</code></td></tr><tr><td><code class="literal">TABLESPACE</code></td><td><code class="literal">C</code></td><td>無</td><td><code class="literal">\db+</code></td></tr><tr><td><code class="literal">TYPE</code></td><td><code class="literal">U</code></td><td><code class="literal">U</code></td><td><code class="literal">\dT+</code></td></tr></tbody></table>

<br>

<a id="id-1.5.4.10.24.1"></a>
已授予特定物件的權限，會以一串 `aclitem` 項目顯示，每個項目的格式為：

```

grantee=privilege-abbreviation[*].../grantor
```

每個 `aclitem` 列出由某個特定授權者授予某一位被授權者的所有權限。個別權限以[表 5.1](ddl-priv.md#PRIVILEGE-ABBREVS-TABLE) 中的單一字母縮寫表示；如果該權限是附帶授權選項授予的，後面就會加上 `*`。例如，`calvin=r*w/hobbes` 表示角色 `calvin` 擁有附帶授權選項（`*`）的 `SELECT`（`r`）權限，以及不可再授予的 `UPDATE`（`w`）權限，兩者都是由角色 `hobbes` 授予的。如果 `calvin` 在同一個物件上還有由另一位授權者授予的某些權限，這些權限會顯示為另一個獨立的 `aclitem` 項目。`aclitem` 中空白的被授權者欄位代表 `PUBLIC`。

舉例來說，假設使用者 `miriam` 建立了資料表 `mytable`，並執行：

```

GRANT SELECT ON mytable TO PUBLIC;
GRANT SELECT, UPDATE, INSERT ON mytable TO admin;
GRANT SELECT (col1), UPDATE (col1) ON mytable TO miriam_rw;
```

那麼 psql 的 `\dp` 命令會顯示：

```

=> \dp mytable
                                  Access privileges
 Schema |  Name   | Type  |   Access privileges    |   Column privileges   | Policies
--------+---------+-------+------------------------+-----------------------+----------
 public | mytable | table | miriam=arwdDxtm/miriam+| col1:                +|
        |         |       | =r/miriam             +|   miriam_rw=rw/miriam |
        |         |       | admin=arw/miriam       |                       |
(1 row)
```

如果某個物件的「Access privileges」（存取權限）欄位是空的，就表示該物件擁有預設權限（也就是它在相關系統目錄中的權限項目為 null）。預設權限一律包含擁有者的所有權限，並且依物件類型的不同，可能包含 `PUBLIC` 的某些權限，如上所述。對物件進行的第一次 `GRANT` 或 `REVOKE`，會先將預設權限實體化（例如產生 `miriam=arwdDxt/miriam`），然後再依照所指定的要求修改它們。同樣地，只有具有非預設權限的欄位，才會在「Column privileges」（欄位權限）中顯示項目。（注意：就這個目的而言，「預設權限」一律指該物件類型的內建預設權限。權限受到 `ALTER DEFAULT PRIVILEGES` 命令影響的物件，一律會以包含該 `ALTER` 之效果的明確權限項目顯示。）

請注意，擁有者隱含的授權選項並不會標示在存取權限的顯示中。只有在明確將授權選項授予某人時，才會出現 `*`。

當物件的權限項目非 null 但為空時，「Access privileges」欄位會顯示 `(none)`。這表示完全沒有授予任何權限，連物件的擁有者也沒有——這是很少見的情況。（在這種情況下，擁有者仍然具有隱含的授權選項，因此可以重新授予自己的權限；但她目前沒有任何權限。）

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ddl-priv.html)（原文版本：18.6；核對日期：2026-09-13）
