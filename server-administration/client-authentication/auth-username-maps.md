<a id="AUTH-USERNAME-MAPS"></a>

## 20.2. 使用者名稱對應 [#](#AUTH-USERNAME-MAPS)

<a id="id-1.6.7.9.2"></a>

當使用 Ident 或 GSSAPI 等外部驗證系統時，發起連線的作業系統
使用者名稱，可能與要使用的資料庫使用者（角色）不同。
在這種情況下，可以套用使用者名稱對應，將作業系統
使用者名稱對應到資料庫使用者。若要使用使用者名稱對應，請在
`pg_hba.conf` 的選項欄位中指定
`map`=*`map-name`*。所有能接收外部使用者名稱的驗證方法
都支援這個選項。由於不同的連線可能需要不同的對應，
因此要使用的對應名稱，是在
`pg_hba.conf` 中的 *`map-name`* 參數裡指定，
以表明每個連線各自要使用哪個對應。

使用者名稱對應是定義在 ident 對應檔中，該檔案預設名為
`pg_ident.conf`<a id="id-1.6.7.9.4.2"></a>
並儲存在
叢集的資料目錄下。（不過，你也可以把對應檔放在其他位置；請參見
[ident_file](../runtime-config/runtime-config-file-locations.md#GUC-IDENT-FILE)
這個組態參數。）
ident 對應檔包含以下這種一般形式的行：

```

map-name system-username database-username
include file
include_if_exists file
include_dir directory
```

註解、空白字元與跨行接續的處理方式，與
`pg_hba.conf` 中相同。
*`map-name`* 是一個任意名稱，會用來在 `pg_hba.conf` 中
參照此對應。其餘
兩個欄位則分別指定一個作業系統使用者名稱與一個
相符的資料庫使用者名稱。同一個 *`map-name`* 可以
重複使用，以便在單一對應中指定多組使用者對應。

如同 `pg_hba.conf` 一樣，這個檔案中的
行也可以是 include 指令，並遵循相同的規則。

`pg_ident.conf` 檔案會在啟動時，以及
主要伺服器程序收到
SIGHUP<a id="id-1.6.7.9.6.3"></a>
訊號時被讀取。如果你在運作中的系統上編輯這個檔案，
就需要向 postmaster 送出訊號
（使用 `pg_ctl reload`、呼叫 SQL 函式
`pg_reload_conf()`，或使用 `kill
-HUP`），才能讓它重新讀取檔案。

系統檢視表
[`pg_ident_file_mappings`](../../internals/views/view-pg-ident-file-mappings.md)
有助於在正式套用前，先行測試對
`pg_ident.conf` 檔案所做的變更，或是在
載入檔案後未達到預期效果時，用來診斷問題。若檢視表中某列的
`error` 欄位不是 null，就表示該檔案中
對應的那一行存在問題。

對於一個給定的作業系統使用者可以對應到多少個資料庫使用者，
或反過來一個資料庫使用者可以對應到多少個作業系統使用者，並沒有任何限制。因此，對應檔中的項目
應該被理解為「這個作業系統
使用者被允許以這個資料庫使用者的身分連線」，而不是
暗示兩者是等價的。只要存在任何一筆對應項目，能將外部驗證系統所取得的
使用者名稱，與使用者要求連線所用的資料庫
使用者名稱配對成功，該連線就會被允許。你可以將值 `all`
用作 *`database-username`*，用來指定只要
*`system-username`* 相符，該使用者就被允許以任何一個現有的資料庫使用者
身分登入。將 `all` 加上引號，會讓這個關鍵字失去其特殊意義。

如果 *`database-username`* 以
`+` 字元開頭，則該作業系統使用者可以以屬於該角色的任何使用者身分登入，
這與 `pg_hba.conf`
中以 `+` 開頭的使用者名稱的處理方式類似。
因此，`+` 符號代表「符合直接或間接
屬於此角色成員的任何角色」，而沒有
`+` 符號的名稱則只會符合該特定角色。將以 `+` 開頭的
使用者名稱加上引號，會讓 `+`
失去其特殊意義。

如果 *`system-username`* 欄位以斜線（`/`）開頭，
該欄位其餘的部分就會被視為正規表示式。
（PostgreSQL 正規表示式語法的細節，請參見
[Section 9.7.3.1](../../the-sql-language/functions/functions-matching.md#POSIX-SYNTAX-DETAILS)。）
該正規表示式可以包含一個擷取（capture），也就是括號括住的
子表示式。系統使用者名稱中符合該擷取的部分，
之後就可以在 *`database-username`*
欄位中以 `\1`（反斜線加一）來參照。這使得
在單一行中對應多個使用者名稱成為可能，對於
簡單的語法代換特別有用。舉例來說，以下這些項目

```

mymap   /^(.*)@mydomain\.com$      \1
mymap   /^(.*)@otherdomain\.com$   guest
```

會移除系統使用者名稱以
`@mydomain.com` 結尾的使用者的網域部分，並允許系統名稱以
`@otherdomain.com` 結尾的任何使用者，以 `guest` 的身分登入。
將包含 `\1` 的 *`database-username`*
加上引號，*並不會*讓
`\1` 失去其特殊意義。

如果 *`database-username`* 欄位以
斜線（`/`）開頭，該欄位其餘的部分就會被視為
正規表示式。
當 *`database-username`* 欄位是正規表示式時，就
無法在其中使用 `\1` 來參照來自
*`system-username`* 欄位的擷取內容。

### 提示

請記得，依預設，正規表示式可以只符合字串的一部分。
如上例所示，通常明智的做法是使用 `^` 與
`$`，強制要求比對必須符合整個
系統使用者名稱。

可以搭配[範例 20.1](auth-pg-hba-conf.md#EXAMPLE-PG-HBA.CONF) 中
`pg_hba.conf` 檔案一起使用的
`pg_ident.conf` 檔案，如[範例 20.2](auth-username-maps.md#EXAMPLE-PG-IDENT.CONF) 所示。在這個範例中，
任何登入 192.168 網路上某台機器、但作業系統使用者名稱不是
`bryanh`、`ann` 或
`robert` 的人，都不會被授予存取權限。Unix 使用者
`robert` 只有在嘗試以 PostgreSQL 使用者 `bob`
的身分連線時才會被允許存取，而不能以
`robert` 或其他任何身分連線。`ann` 則只被
允許以 `ann` 的身分連線。使用者
`bryanh` 則被允許以 `bryanh` 或 `guest1`
的身分連線。

<a id="EXAMPLE-PG-IDENT.CONF"></a>

**範例 20.2. 一個 `pg_ident.conf` 檔案範例**

```

# MAPNAME       SYSTEM-USERNAME         PG-USERNAME

omicron         bryanh                  bryanh
omicron         ann                     ann
# bob has user name robert on these machines
omicron         robert                  bob
# bryanh can also connect as guest1
omicron         bryanh                  guest1
```

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/auth-username-maps.html)（原文版本：18.6；核對日期：2026-09-24）
