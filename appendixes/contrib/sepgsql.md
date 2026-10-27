<a id="SEPGSQL"></a>

## F.40. sepgsql — 以 SELinux 標籤為基礎的強制存取控制（MAC）安全模組 [#](#sepgsql) <a href="#sepgsql" id="sepgsql"></a>

[F.40.1. 概觀](sepgsql.md#sepgsql-overview)

[F.40.2. 安裝](sepgsql.md#sepgsql-installation)

[F.40.3. 迴歸測試](sepgsql.md#sepgsql-regression)

[F.40.4. GUC 參數](sepgsql.md#sepgsql-parameters)

[F.40.5. 功能](sepgsql.md#sepgsql-features)

[F.40.6. sepgsql 函式](sepgsql.md#sepgsql-functions)

[F.40.7. 限制](sepgsql.md#sepgsql-limitations)

[F.40.8. 外部資源](sepgsql.md#sepgsql-resources)

[F.40.9. 作者](sepgsql.md#sepgsql-author)

<a id="id-1.11.7.50.2"></a>

`sepgsql` 是一個可載入模組，依據 SELinux 安全政策，支援以標籤為基礎的強制存取控制（MAC）。

### 警告

目前的實作有重大限制，並未對所有動作強制執行強制存取控制。請參閱
[第 F.40.7 節](sepgsql.md#sepgsql-limitations)。

<a id="SEPGSQL-OVERVIEW"></a>

### F.40.1. 概觀 [#](#sepgsql-overview) <a href="#sepgsql-overview" id="sepgsql-overview"></a>

此模組與 SELinux 整合，在 PostgreSQL 通常提供的安全檢查之外，再額外提供一層安全檢查。從
SELinux 的角度來看，此模組讓
PostgreSQL 能作為使用者空間的物件管理器運作。由 DML 查詢發起的每一次資料表或函式存取，都會依據系統安全政策進行檢查。這項檢查是在
PostgreSQL 執行的一般 SQL 權限檢查之外額外進行的。

SELinux 的存取控制決策是使用安全標籤做出的，安全標籤以字串表示，例如
`system_u:object_r:sepgsql_table_t:s0`。每項存取控制決策都涉及兩個標籤：嘗試執行動作之主體的標籤，以及要對其執行操作之物件的標籤。由於這些標籤可以套用到任何種類的物件，因此資料庫內所儲存物件的存取控制決策，可以（而且使用此模組時確實會）採用與其他任何類型物件（例如檔案）相同的一般準則。此設計的目的，是讓集中式的安全政策能夠保護資訊資產，而與這些資產的儲存細節無關。

[`SECURITY LABEL`](../../reference/sql-commands/sql-security-label.md) 陳述式可以為資料庫物件指定安全標籤。

<a id="SEPGSQL-INSTALLATION"></a>

### F.40.2. 安裝 [#](#sepgsql-installation) <a href="#sepgsql-installation" id="sepgsql-installation"></a>

`sepgsql` 只能在已啟用 SELinux 的 Linux
2.6.28 或更新版本上使用，在其他任何平台上都無法使用。你還需要
libselinux 2.1.10 或更新版本，以及
selinux-policy 3.9.13 或更新版本（不過有些發行版可能會將必要的規則向後移植到較舊的政策版本中）。

`sestatus` 命令可讓你檢查
SELinux 的狀態。典型的顯示如下：

```

$ sestatus
SELinux status:                 enabled
SELinuxfs mount:                /selinux
Current mode:                   enforcing
Mode from config file:          enforcing
Policy version:                 24
Policy from config file:        targeted
```

若 SELinux 已停用或尚未安裝，你必須先設定好該產品，才能安裝此模組。

要建置此模組，請指定 [`--with-selinux`](../../server-administration/installation/install-make.md#CONFIGURE-OPTION-WITH-SEPGSQL)（使用 [make 與 autoconf](../../server-administration/installation/install-make.md) 時）或 [`-Dselinux={ auto | enabled | disabled }`](../../server-administration/installation/install-meson.md#CONFIGURE-WITH-SEPGSQL-MESON)（使用 [meson](../../server-administration/installation/install-meson.md) 時）。
請確認建置時已安裝 `libselinux-devel` RPM。

要使用此模組，你必須在
`postgresql.conf` 的 [shared_preload_libraries](../../server-administration/runtime-config/runtime-config-client.md#GUC-SHARED-PRELOAD-LIBRARIES) 參數中加入 `sepgsql`。若以其他任何方式載入，此模組將無法正確運作。模組載入後，你應該在每個資料庫中執行
`sepgsql.sql`。
這會安裝管理安全標籤所需的函式，並指定初始的安全標籤。

以下範例說明如何初始化一個全新的資料庫叢集，並安裝
`sepgsql` 函式與安全標籤。
請依你的安裝情況適當調整所示路徑：

```

$ export PGDATA=/path/to/data/directory
$ initdb
$ vi $PGDATA/postgresql.conf
  change
    #shared_preload_libraries = ''                # (change requires restart)
  to
    shared_preload_libraries = 'sepgsql'          # (change requires restart)
$ for DBNAME in template0 template1 postgres; do
    postgres --single -F -c exit_on_error=true $DBNAME \
      </usr/local/pgsql/share/contrib/sepgsql.sql >/dev/null
  done
```

請注意，依你所使用的
libselinux 與 selinux-policy 版本而定，你可能會看到下列部分或全部通知訊息：

```

/etc/selinux/targeted/contexts/sepgsql_contexts:  line 33 has invalid object type db_blobs
/etc/selinux/targeted/contexts/sepgsql_contexts:  line 36 has invalid object type db_language
/etc/selinux/targeted/contexts/sepgsql_contexts:  line 37 has invalid object type db_language
/etc/selinux/targeted/contexts/sepgsql_contexts:  line 38 has invalid object type db_language
/etc/selinux/targeted/contexts/sepgsql_contexts:  line 39 has invalid object type db_language
/etc/selinux/targeted/contexts/sepgsql_contexts:  line 40 has invalid object type db_language
```

這些訊息無害，應予忽略。

若安裝過程完成且沒有錯誤，現在就可以正常啟動伺服器。

<a id="SEPGSQL-REGRESSION"></a>

### F.40.3. 迴歸測試 [#](#sepgsql-regression) <a href="#sepgsql-regression" id="sepgsql-regression"></a>

若 `PG_TEST_EXTRA` 包含 `sepgsql`，就會執行
`sepgsql` 測試套件（請參閱
[第 31.1.3 節](../../server-administration/regress/regress-run.md#regress-additional)）。這種方法適用於
PostgreSQL 的開發期間。另外，也有一種執行測試的方式，可用來檢查資料庫執行個體是否已為
`sepgsql` 正確設定。

由於 SELinux 的特性，執行
`sepgsql` 的迴歸測試需要幾個額外的設定步驟，其中有些必須以 root 身分執行。

手動測試必須在已完成組態設定的 PostgreSQL 建置樹之 `contrib/sepgsql` 目錄中執行。雖然需要建置樹，但這些測試是設計為針對已安裝的伺服器執行，也就是說，它們相當於 `make installcheck`，而不是
`make check`。

首先，依照[第 F.40.2 節](sepgsql.md#sepgsql-installation)的說明，在運作中的資料庫裡設定 `sepgsql`。
請注意，目前的作業系統使用者必須能夠不經密碼驗證，以超級使用者身分連線到資料庫。

其次，建置並安裝迴歸測試用的政策套件。
`sepgsql-regtest` 政策是一個特殊用途的政策套件，提供一組在迴歸測試期間允許的規則。
它應該從政策原始檔
`sepgsql-regtest.te` 建置，建置方式是以 SELinux 提供的 Makefile 執行
`make`。
你需要在系統上找到適當的
Makefile；下方所示的路徑只是一個範例。
（此 Makefile 通常由
`selinux-policy-devel` 或
`selinux-policy` RPM 提供。）
建置完成後，使用
`semodule` 命令安裝此政策套件，該命令會將提供的政策套件載入核心。若套件安裝正確，
`semodule -l` 應會將 `sepgsql-regtest` 列為可用的政策套件：

```

$ cd .../contrib/sepgsql
$ make -f /usr/share/selinux/devel/Makefile
$ sudo semodule -u sepgsql-regtest.pp
$ sudo semodule -l | grep sepgsql
sepgsql-regtest 1.07
```

第三，開啟 `sepgsql_regression_test_mode`。
基於安全理由，`sepgsql-regtest` 中的規則預設不會啟用；
`sepgsql_regression_test_mode` 參數會啟用執行迴歸測試所需的規則。
可以使用 `setsebool` 命令開啟它：

```

$ sudo setsebool sepgsql_regression_test_mode on
$ getsebool sepgsql_regression_test_mode
sepgsql_regression_test_mode --> on
```

第四，確認你的 shell 是在 `unconfined_t`
網域（domain）中運作：

```

$ id -Z
unconfined_u:unconfined_r:unconfined_t:s0-s0:c0.c1023
```

若有必要調整你的工作網域，詳細資訊請參閱[第 F.40.8 節](sepgsql.md#sepgsql-resources)。

最後，執行迴歸測試指令稿：

```

$ ./test_sepgsql
```

此指令稿會嘗試驗證你是否已正確完成所有設定步驟，然後執行
`sepgsql` 模組的迴歸測試。

完成測試後，建議你停用
`sepgsql_regression_test_mode` 參數：

```

$ sudo setsebool sepgsql_regression_test_mode off
```

你也可以選擇完全移除 `sepgsql-regtest` 政策：

```

$ sudo semodule -r sepgsql-regtest
```

<a id="SEPGSQL-PARAMETERS"></a>

### F.40.4. GUC 參數 [#](#sepgsql-parameters) <a href="#sepgsql-parameters" id="sepgsql-parameters"></a>

<a id="GUC-SEPGSQL-PERMISSIVE"></a>

`sepgsql.permissive` (`boolean`) <a id="id-1.11.7.50.8.2.1.1.3"></a> [#](#GUC-SEPGSQL-PERMISSIVE)
:   此參數讓 `sepgsql` 不論系統設定為何，都以寬鬆（permissive）模式運作。
    預設為關閉。
    此參數只能在 `postgresql.conf`
    檔案中或伺服器命令列上設定。

    此參數開啟時，即使 SELinux 整體是以強制（enforcing）模式運作，`sepgsql`
    仍會以寬鬆模式運作。此參數主要用於測試目的。
<a id="GUC-SEPGSQL-DEBUG-AUDIT"></a>

`sepgsql.debug_audit` (`boolean`) <a id="id-1.11.7.50.8.2.2.1.3"></a> [#](#GUC-SEPGSQL-DEBUG-AUDIT)
:   此參數讓稽核訊息不論系統政策設定為何都會輸出。
    預設為關閉，表示訊息會依系統設定輸出。

    SELinux 的安全政策也有規則，用來控制特定存取是否要記錄。
    預設情況下，存取違規會被記錄，但允許的存取不會。

    此參數會強制開啟所有可能的記錄，而不論系統政策為何。

<a id="SEPGSQL-FEATURES"></a>

### F.40.5. 功能 [#](#sepgsql-features) <a href="#sepgsql-features" id="sepgsql-features"></a>

<a id="SEPGSQL-FEATURES-CONTROLLED-OBJ-CLASSES"></a>

#### F.40.5.1. 受控制的物件類別 [#](#SEPGSQL-FEATURES-CONTROLLED-OBJ-CLASSES)

SELinux 的安全模型將所有存取控制規則描述為主體實體（通常是資料庫的用戶端）與客體實體（例如資料庫物件）之間的關係，兩者各自由一個安全標籤識別。若嘗試存取未加標籤的物件，該物件會被視為已被指定標籤
`unlabeled_t`。

目前，`sepgsql` 允許將安全標籤指定給綱要、資料表、欄位、序列、檢視表與函式。
使用 `sepgsql` 時，系統會在支援的資料庫物件建立時自動為其指定安全標籤。
此標籤稱為預設安全標籤，依據系統安全政策決定；該政策的輸入包括建立者的標籤、指定給新物件之父物件的標籤，以及（選擇性地）所建立物件的名稱。

新的資料庫物件基本上會繼承父物件的安全標籤，但若安全政策有稱為型別轉換（type-transition）規則的特殊規則，則可能套用不同的標籤。
對綱要而言，父物件是目前的資料庫；對資料表、序列、檢視表與函式而言，父物件是其所屬的綱要；對欄位而言，父物件是其所屬的資料表。

<a id="SEPGSQL-FEATURES-DML-PERMISSIONS"></a>

#### F.40.5.2. DML 權限 [#](#SEPGSQL-FEATURES-DML-PERMISSIONS)

對資料表而言，會依陳述式的種類，對所有被參照的目標資料表檢查 `db_table:select`、`db_table:insert`、
`db_table:update` 或 `db_table:delete`；此外，對於所有包含在
`WHERE` 或 `RETURNING` 子句中被參照之欄位的資料表、作為
`UPDATE` 資料來源的資料表等，也會檢查 `db_table:select`。

也會對每個被參照的欄位檢查欄位層級的權限。
`db_column:select` 不僅會對使用 `SELECT` 讀取的欄位進行檢查，也會對其他 DML
陳述式中被參照的欄位進行檢查；對於被 `UPDATE` 或
`INSERT` 修改的欄位，也會檢查 `db_column:update` 或 `db_column:insert`。

例如，考慮以下陳述式：

```

UPDATE t1 SET x = 2, y = func1(y) WHERE z = 100;
```

此處，會對
`t1.x` 檢查 `db_column:update`，因為它被更新；會對
`t1.y` 檢查 `db_column:{select update}`，因為它既被更新也被參照；並對 `t1.z` 檢查
`db_column:select`，因為它只被參照。
在資料表層級也會檢查 `db_table:{select update}`。

對序列而言，使用 `SELECT` 參照序列物件時會檢查 `db_sequence:get_value`；不過請注意，目前並不會在執行對應的函式（例如
`lastval()`）時檢查權限。

對檢視表而言，會檢查 `db_view:expand`，然後再對從該檢視表展開的物件分別檢查其他任何所需的權限。

對函式而言，當使用者嘗試在查詢中執行函式，或透過快速路徑（fast-path）呼叫執行函式時，會檢查 `db_procedure:{execute}`。若此函式是受信任程序，還會檢查
`db_procedure:{entrypoint}` 權限，以確認它是否可以作為受信任程序的進入點。

要存取任何綱要物件，都需要具有其所屬綱要的 `db_schema:search`
權限。當參照物件而未以綱要限定時，不會搜尋沒有此權限的綱要（就如同使用者沒有該綱要的
`USAGE` 權限一樣）。若有明確的綱要限定，而使用者沒有所指名綱要的必要權限，就會發生錯誤。

用戶端必須被允許存取所有被參照的資料表與欄位，即使它們來自之後被展開的檢視表也一樣，如此一來，不論以何種方式參照資料表內容，都會套用一致的存取控制規則。

預設的資料庫權限系統允許資料庫超級使用者使用 DML 命令修改系統目錄，以及參照或修改
TOAST 資料表。啟用 `sepgsql` 時，這些操作會被禁止。

<a id="SEPGSQL-FEATURES-DDL-PERMISSIONS"></a>

#### F.40.5.3. DDL 權限 [#](#SEPGSQL-FEATURES-DDL-PERMISSIONS)

SELinux 為每種物件類型定義了數種權限，用來控制常見的操作，例如建立、修改、刪除，以及重新標記安全標籤。此外，有幾種物件類型具有特殊權限，用來控制其特有的操作，例如在特定綱要內新增或刪除名稱項目。

建立新的資料庫物件需要 `create` 權限。
SELinux 會依據用戶端的安全標籤與新物件的擬定安全標籤，授與或拒絕此權限。在某些情況下，還需要額外的權限：

* [`CREATE DATABASE`](../../reference/sql-commands/sql-createdatabase.md) 還需要對來源資料庫或範本資料庫具有
  `getattr` 權限。
* 建立綱要物件還需要對父綱要具有 `add_name`
  權限。
* 建立資料表還需要建立每個個別資料表欄位的權限，就如同每個資料表欄位都是獨立的頂層物件一樣。
* 建立標記為 `LEAKPROOF` 的函式還需要
  `install` 權限。（為既有函式設定 `LEAKPROOF` 時，
  也會檢查此權限。）

執行 `DROP` 命令時，會對被移除的物件檢查 `drop`。對於透過 `CASCADE`
間接刪除的物件也會檢查權限。刪除特定綱要內所含的物件（資料表、檢視表、序列與程序）時，還需要該綱要的 `remove_name`。

執行 `ALTER` 命令時，對每種物件類型，都會對被修改的物件檢查 `setattr`；但資料表的索引或觸發程序等附屬物件除外，對它們改為檢查父物件的權限。在某些情況下，還需要額外的權限：

* 將物件移到新的綱要，還需要對舊綱要具有
  `remove_name` 權限，以及對新綱要具有
  `add_name` 權限。
* 為函式設定 `LEAKPROOF` 屬性需要
  `install` 權限。
* 對物件使用 [`SECURITY LABEL`](../../reference/sql-commands/sql-security-label.md)，還需要該物件搭配其舊安全標籤的
  `relabelfrom` 權限，以及該物件搭配其新安全標籤的 `relabelto`
  權限。
  （在安裝了多個標籤提供者、而使用者嘗試設定的安全標籤並非由
  SELinux 管理的情況下，此處應該只檢查 `setattr`。
  由於實作上的限制，目前並未這樣做。）

<a id="SEPGSQL-FEATURES-TRUSTED-PROCEDURES"></a>

#### F.40.5.4. 受信任程序 [#](#SEPGSQL-FEATURES-TRUSTED-PROCEDURES)

受信任程序類似於安全性定義者（security definer）函式或 setuid
命令。SELinux 提供一項功能，允許受信任的程式碼使用與用戶端不同的安全標籤執行，通常是為了對敏感資料提供高度受控的存取（例如，可能省略某些資料列，或降低所儲存值的精確度）。函式是否作為受信任程序運作，由其安全標籤與作業系統安全政策控制。例如：

```

postgres=# CREATE TABLE customer (
               cid     int primary key,
               cname   text,
               credit  text
           );
CREATE TABLE
postgres=# SECURITY LABEL ON COLUMN customer.credit
               IS 'system_u:object_r:sepgsql_secret_table_t:s0';
SECURITY LABEL
postgres=# CREATE FUNCTION show_credit(int) RETURNS text
             AS 'SELECT regexp_replace(credit, ''-[0-9]+$'', ''-xxxx'', ''g'')
                        FROM customer WHERE cid = $1'
           LANGUAGE sql;
CREATE FUNCTION
postgres=# SECURITY LABEL ON FUNCTION show_credit(int)
               IS 'system_u:object_r:sepgsql_trusted_proc_exec_t:s0';
SECURITY LABEL
```

上述操作應由管理用途的使用者執行。

```

postgres=# SELECT * FROM customer;
ERROR:  SELinux: security policy violation
postgres=# SELECT cid, cname, show_credit(cid) FROM customer;
 cid | cname  |     show_credit
-----+--------+---------------------
   1 | taro   | 1111-2222-3333-xxxx
   2 | hanako | 5555-6666-7777-xxxx
(2 rows)
```

在此情況下，一般使用者無法直接參照 `customer.credit`，但受信任程序 `show_credit`
讓使用者能夠印出部分數字已遮蔽的顧客信用卡號碼。

<a id="SEPGSQL-FEATURES-DYNAMIC-DOMAIN-TRANSITIONS"></a>

#### F.40.5.5. 動態網域轉換 [#](#SEPGSQL-FEATURES-DYNAMIC-DOMAIN-TRANSITIONS)

若安全政策允許，可以使用 SELinux 的動態網域轉換功能，將用戶端程序的安全標籤（即用戶端網域）切換到新的上下文（context）。
用戶端網域需要 `setcurrent` 權限，以及從舊網域到新網域的
`dyntransition` 權限。

動態網域轉換應審慎考量，因為它讓使用者能夠依自己的選擇切換其標籤，進而切換其權限，而不是（如受信任程序的情況）由系統強制決定。
因此，只有在用來切換到權限集合比原本更小的網域時，`dyntransition` 權限才被視為安全。例如：

```

regression=# select sepgsql_getcon();
                    sepgsql_getcon
-------------------------------------------------------
 unconfined_u:unconfined_r:unconfined_t:s0-s0:c0.c1023
(1 row)

regression=# SELECT sepgsql_setcon('unconfined_u:unconfined_r:unconfined_t:s0-s0:c1.c4');
 sepgsql_setcon
----------------
 t
(1 row)

regression=# SELECT sepgsql_setcon('unconfined_u:unconfined_r:unconfined_t:s0-s0:c1.c1023');
ERROR:  SELinux: security policy violation
```

在上述範例中，我們被允許從較大的 MCS
範圍 `c1.c1023` 切換到較小的範圍 `c1.c4`，但切換回去則被拒絕。（譯註：依範例中 sepgsql_getcon() 的輸出，切換前的範圍實為 c0.c1023；c1.c1023 是最後一次嘗試、被拒絕的目標範圍。）

結合動態網域轉換與受信任程序，可以實現一種有趣的使用情境，符合連線池軟體典型的程序生命週期。
即使你的連線池軟體不被允許執行大部分的 SQL 命令，你仍可允許它在受信任程序內使用 `sepgsql_setcon()` 函式切換用戶端的安全標籤；該程序應接受某種憑據，以授權切換用戶端標籤的要求。
之後，此工作階段將擁有目標使用者的權限，而不是連線池程式的權限。
連線池程式之後可以再次以
`NULL` 引數使用 `sepgsql_setcon()`，還原安全標籤的變更；這同樣是在具有適當權限檢查的受信任程序內呼叫。
重點在於，只有受信任程序實際具有變更有效安全標籤的權限，而且只有在獲得適當憑據時才會這麼做。當然，為了安全運作，必須保護憑據的儲存處（資料表、程序定義或其他任何形式）免於未經授權的存取。

<a id="SEPGSQL-FEATURES-MISC"></a>

#### F.40.5.6. 其他 [#](#SEPGSQL-FEATURES-MISC)

我們一律拒絕 [`LOAD`](../../reference/sql-commands/sql-load.md) 命令，因為任何被載入的模組都可以輕易規避安全政策的強制執行。

<a id="SEPGSQL-FUNCTIONS"></a>

### F.40.6. sepgsql 函式 [#](#sepgsql-functions) <a href="#sepgsql-functions" id="sepgsql-functions"></a>

[表 F.32](sepgsql.md#SEPGSQL-FUNCTIONS-TABLE) 列出可用的函式。

<a id="SEPGSQL-FUNCTIONS-TABLE"></a>

**表 F.32. sepgsql 函式**

<table border="1" class="table" summary="sepgsql 函式"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">sepgsql_getcon</code> ()
        → <code class="returnvalue">text</code>
</p>
<p>
        傳回用戶端網域，也就是用戶端目前的安全標籤。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">sepgsql_setcon</code> ( <code class="type">text</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        若安全政策允許，將目前工作階段的用戶端網域切換到新的網域。
        它也接受 <code class="literal">NULL</code> 輸入，作為轉換回用戶端原本網域的要求。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">sepgsql_mcstrans_in</code> ( <code class="type">text</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        若 mcstrans 常駐程式正在執行，將給定的限定格式 MLS/MCS 範圍轉換為原始格式。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">sepgsql_mcstrans_out</code> ( <code class="type">text</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        若 mcstrans 常駐程式正在執行，將給定的原始格式 MLS/MCS 範圍轉換為限定格式。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">sepgsql_restorecon</code> ( <code class="type">text</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        為目前資料庫內的所有物件設定初始安全標籤。引數可以是 <code class="literal">NULL</code>，或是用來取代系統預設值的 specfile 名稱。
       </p></td></tr></tbody></table>

<br>

<a id="SEPGSQL-LIMITATIONS"></a>

### F.40.7. 限制 [#](#sepgsql-limitations) <a href="#sepgsql-limitations" id="sepgsql-limitations"></a>

資料定義語言（DDL）權限
:   由於實作上的限制，有些 DDL 操作不會檢查權限。

資料控制語言（DCL）權限
:   由於實作上的限制，DCL 操作不會檢查權限。

資料列層級存取控制
:   PostgreSQL 支援資料列層級的存取，但
    `sepgsql` 不支援。

隱蔽通道（covert channel）
:   即使使用者不被允許參照某個物件，`sepgsql` 也不會嘗試隱藏該物件的存在。
    例如，即使我們無法取得物件的內容，仍可從主鍵衝突、外部鍵違規等結果推斷出不可見物件的存在。極機密資料表的存在無法隱藏；我們只希望能隱藏其內容。

<a id="SEPGSQL-RESOURCES"></a>

### F.40.8. 外部資源 [#](#sepgsql-resources) <a href="#sepgsql-resources" id="sepgsql-resources"></a>

[SE-PostgreSQL 簡介](https://wiki.postgresql.org/wiki/SEPostgreSQL_Introduction)
:   此 wiki 頁面提供簡要概觀，以及安全設計、架構、管理與即將推出的功能。

[SELinux 使用者與管理員指南](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/selinux_users_and_administrators_guide/index)
:   此文件提供在你的系統上管理 SELinux 所需的廣泛知識。
    它主要著重於 Red Hat 作業系統，但並不限於這些系統。

[Fedora SELinux FAQ](https://fedoraproject.org/wiki/SELinux_FAQ)
:   此文件回答關於 SELinux 的常見問題。
    它主要著重於 Fedora，但並不限於 Fedora。

<a id="SEPGSQL-AUTHOR"></a>

### F.40.9. 作者 [#](#sepgsql-author) <a href="#sepgsql-author" id="sepgsql-author"></a>

KaiGai Kohei `<kaigai@ak.jp.nec.com>`

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sepgsql.html)（原文版本：18.6；核對日期：2026-10-22）
