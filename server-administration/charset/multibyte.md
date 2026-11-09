<a id="MULTIBYTE"></a>

## 23.3. 字元集支援 [#](#multibyte) <a href="#multibyte" id="multibyte"></a>

[23.3.1. 支援的字元集](multibyte/multibyte-charset-supported.md#multibyte-charset-supported)

[23.3.2. 設定字元集](multibyte.md#multibyte-setting)

[23.3.3. 伺服器與用戶端間的自動字元集轉換](multibyte.md#multibyte-automatic-conversion)

[23.3.4. 可用的字元集轉換](multibyte/multibyte-conversions-supported.md#multibyte-conversions-supported)

[23.3.5. 延伸閱讀](multibyte.md#multibyte-further-reading)

<a id="id-1.6.10.5.2"></a>

PostgreSQL 的字元集支援
讓你可以用多種字元集（也稱為
編碼）來儲存文字，包括
單位元組字元集（例如 ISO 8859 系列）以及
多位元組字元集（例如 EUC（Extended Unix
Code）、UTF-8 及 Mule 內部編碼）。所有支援的字元集
都可以被用戶端透明地使用，但其中少數幾種不支援
在伺服器內部使用（也就是不能作為伺服器端編碼）。
預設字元集會在使用 `initdb` 初始化
PostgreSQL 資料庫
叢集時選定。建立資料庫時可以覆寫此設定，因此你可以讓多個
資料庫各自使用不同的字元集。

不過，這裡有一項重要的限制：每個資料庫的字元集
必須與該資料庫的 `LC_CTYPE`（字元
分類）以及 `LC_COLLATE`（字串排序順序）區域設定
相容。對於 `C` 或
`POSIX` 區域設定，可以使用任何字元集，但對於其他
由 libc 提供的區域設定，只有一種字元集能正確
運作。
（不過在 Windows 上，UTF-8 編碼可以搭配任何區域設定使用。）
若你已設定了 ICU 支援，ICU 所提供的區域設定可以搭配大部分（但非全部）伺服器端編碼使用。

### 23.3.1. 支援的字元集 [#](#multibyte-charset-supported) <a href="#multibyte-charset-supported" id="multibyte-charset-supported"></a>

完整內容請見 [23.3.1. 支援的字元集](multibyte/multibyte-charset-supported.md#multibyte-charset-supported)。

<a id="MULTIBYTE-SETTING"></a>

### 23.3.2. 設定字元集 [#](#multibyte-setting) <a href="#multibyte-setting" id="multibyte-setting"></a>

`initdb` 定義了
PostgreSQL 叢集的預設字元集（編碼）。例如，

```

initdb -E EUC_JP
```

會將預設字元集設定為
`EUC_JP`（日文的 Extended Unix Code）。若你偏好較長的選項字串，
可以使用 `--encoding`
取代 `-E`。
如果未指定 `-E` 或 `--encoding` 選項，
`initdb` 會嘗試根據所指定或預設的區域設定，
判斷應使用的適當編碼。

你可以在建立資料庫時指定非預設的編碼，
前提是該編碼必須與所選擇的區域設定相容：

```

createdb -E EUC_KR -T template0 --lc-collate=ko_KR.euckr --lc-ctype=ko_KR.euckr korean
```

這會建立一個名為 `korean` 的資料庫，
使用字元集 `EUC_KR`，區域設定為 `ko_KR`。
要達成此目的，另一種方式是使用以下 SQL 指令：

```

CREATE DATABASE korean WITH ENCODING 'EUC_KR' LC_COLLATE='ko_KR.euckr' LC_CTYPE='ko_KR.euckr' TEMPLATE=template0;
```

請注意，上述指令都指定要複製 `template0`
資料庫。當複製其他任何資料庫時，編碼與區域設定
都無法變更為與來源資料庫不同的設定，因為這樣
可能導致資料損毀。詳情請參閱
[第 22.3 節](../managing-databases/manage-ag-templatedbs.md)。

資料庫的編碼會儲存在系統目錄
`pg_database` 中。你可以使用
`psql` 的 `-l` 選項，或
`\l` 指令來查看。

```

$ psql -l
                                         List of databases
   Name    |  Owner   | Encoding  |  Collation  |    Ctype    |          Access Privileges
-----------+----------+-----------+-------------+-------------+-------------------------------------
 clocaledb | hlinnaka | SQL_ASCII | C           | C           |
 englishdb | hlinnaka | UTF8      | en_GB.UTF8  | en_GB.UTF8  |
 japanese  | hlinnaka | UTF8      | ja_JP.UTF8  | ja_JP.UTF8  |
 korean    | hlinnaka | EUC_KR    | ko_KR.euckr | ko_KR.euckr |
 postgres  | hlinnaka | UTF8      | fi_FI.UTF8  | fi_FI.UTF8  |
 template0 | hlinnaka | UTF8      | fi_FI.UTF8  | fi_FI.UTF8  | {=c/hlinnaka,hlinnaka=CTc/hlinnaka}
 template1 | hlinnaka | UTF8      | fi_FI.UTF8  | fi_FI.UTF8  | {=c/hlinnaka,hlinnaka=CTc/hlinnaka}
(7 rows)
```

### 重要

在大多數現代作業系統上，PostgreSQL
可以判斷 `LC_CTYPE` 設定所隱含的字元集，
並會強制要求只能使用相符的資料庫編碼。在較舊的系統上，
確保所使用的編碼與所選區域設定相符便是你的責任。在這方面若有失誤，
很可能導致依賴區域設定的操作（例如排序）出現異常行為。

即使 `LC_CTYPE` 不是 `C` 或 `POSIX`，
PostgreSQL 仍會允許超級使用者建立
使用 `SQL_ASCII` 編碼的資料庫。如上所述，
`SQL_ASCII` 並不會強制要求資料庫中儲存的資料具有任何特定編碼，
因此這項選擇會帶來依賴區域設定而產生異常行為的風險。這種組合設定
已不建議使用，未來某天可能會被完全禁止。

<a id="MULTIBYTE-AUTOMATIC-CONVERSION"></a>

### 23.3.3. 伺服器與用戶端間的自動字元集轉換 [#](#multibyte-automatic-conversion) <a href="#multibyte-automatic-conversion" id="multibyte-automatic-conversion"></a>

PostgreSQL 支援在許多字元
集組合之間，於伺服器與用戶端之間進行自動字元集轉換
（[第 23.3.4 節](multibyte/multibyte-conversions-supported.md#multibyte-conversions-supported)
顯示了具體有哪些組合）。

若要啟用自動字元集轉換，你必須
告知 PostgreSQL 你想在用戶端使用的字元集
（編碼）。有幾種方式可以達成此目的：

* 在 psql 中使用
  `\encoding` 指令。
  `\encoding` 讓你可以即時變更用戶端
  編碼。例如，
  若要將編碼變更為 `SJIS`，請輸入：

  ```

  \encoding SJIS
  ```
* libpq（[第 32.11 節](../../client-interfaces/libpq/libpq-control.md)）提供了控制用戶端編碼的函式。
* 使用 `SET client_encoding TO`。
  可以使用以下 SQL 指令設定用戶端編碼：

  ```

  SET CLIENT_ENCODING TO 'value';
  ```

  你也可以使用標準 SQL 語法 `SET NAMES`
  來達成同樣的目的：

  ```

  SET NAMES 'value';
  ```

  若要查詢目前的用戶端編碼：

  ```

  SHOW client_encoding;
  ```

  若要回復為預設編碼：

  ```

  RESET client_encoding;
  ```
* 使用 `PGCLIENTENCODING`。若用戶端
  環境中定義了環境變數
  `PGCLIENTENCODING`，則在連線到伺服器時，
  會自動選用該用戶端編碼。（後續仍可
  使用上述任一其他方法覆寫此設定。）
* 使用組態變數 [client_encoding](../runtime-config/runtime-config-client.md#GUC-CLIENT-ENCODING)。若設定了
  `client_encoding` 變數，則在連線到
  伺服器時，會自動選用該用戶端編碼。（後續仍可
  使用上述任一其他方法覆寫此設定。）

若無法轉換某個特定字元——
假設你為伺服器選用了 `EUC_JP`，
而用戶端選用 `LATIN1`，且回傳了某些
在 `LATIN1` 中沒有對應表示法的
日文字元——則會回報錯誤。

若用戶端字元集被定義為 `SQL_ASCII`，
則無論伺服器的字元集為何，都會停用編碼轉換。
（不過，若伺服器的字元集
不是 `SQL_ASCII`，伺服器仍會檢查
傳入的資料對該編碼而言是否有效；因此實際效果
就如同用戶端字元集與伺服器相同一樣。）
與伺服器端的情況相同，除非你要處理的是全 ASCII 資料，
否則使用 `SQL_ASCII` 並非明智之舉。

### 23.3.4. 可用的字元集轉換 [#](#multibyte-conversions-supported) <a href="#multibyte-conversions-supported" id="multibyte-conversions-supported"></a>

完整內容請見 [23.3.4. 可用的字元集轉換](multibyte/multibyte-conversions-supported.md#multibyte-conversions-supported)。

<a id="MULTIBYTE-FURTHER-READING"></a>

### 23.3.5. 延伸閱讀 [#](#multibyte-further-reading) <a href="#multibyte-further-reading" id="multibyte-further-reading"></a>

以下是開始學習各種編碼系統的優良參考資料。

*CJKV Information Processing: Chinese, Japanese, Korean & Vietnamese Computing*
:   內含 `EUC_JP`、
    `EUC_CN`、`EUC_KR`、
    `EUC_TW` 的詳細說明。

<https://www.unicode.org/>
:   Unicode 協會的網站。

[RFC 3629](https://datatracker.ietf.org/doc/html/rfc3629)
:   UTF-8（8 位元 UCS／Unicode 轉換
    格式）即定義於此。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/multibyte.html)（原文版本：18.6；核對日期：2026-10-23）
