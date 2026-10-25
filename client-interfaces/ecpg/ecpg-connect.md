<a id="ECPG-CONNECT"></a>

## 34.2. 管理資料庫連線 [#](#ecpg-connect) <a href="#ecpg-connect" id="ecpg-connect"></a>

[34.2.1. 連線到資料庫伺服器](ecpg-connect.md#ecpg-connecting)

[34.2.2. 選擇連線](ecpg-connect.md#ecpg-set-connection)

[34.2.3. 關閉連線](ecpg-connect.md#ecpg-disconnect)

本節說明如何開啟、關閉與切換資料庫連線。

<a id="ECPG-CONNECTING"></a>

### 34.2.1. 連線到資料庫伺服器 [#](#ecpg-connecting) <a href="#ecpg-connecting" id="ecpg-connecting"></a>

使用下列陳述式連線到資料庫：

```

EXEC SQL CONNECT TO target [AS connection-name] [USER user-name];
```

*`target`* 可以用下列方式指定：

* `dbname[@hostname][:port]`
* `tcp:postgresql://hostname[:port][/dbname][?options]`
* `unix:postgresql://localhost[:port][/dbname][?options]`
* 內容為上述任一形式的 SQL 字串常數
* 內容為上述任一形式之字元變數的參照（請參閱範例）
* `DEFAULT`

連線目標 `DEFAULT` 會以預設使用者名稱連線到預設資料庫。在這種情況下，不能另外指定使用者名稱或連線名稱。

若直接指定連線目標（也就是不以字串常數或變數參照的形式指定），目標的各個組成部分會經過一般的 SQL 剖析；這表示，舉例來說，*`hostname`* 必須看起來像是以點號分隔的一個或多個 SQL 識別字，而且除非加上雙引號，這些識別字會經過大小寫轉換。任何 *`options`* 的值都必須是 SQL 識別字、整數或變數參照。當然，只要加上雙引號，幾乎任何內容都可以放進 SQL 識別字中。實務上，使用（以單引號括住的）字串常數或變數參照，可能比直接寫出連線目標更不容易出錯。

指定使用者名稱的方式也有好幾種：

* `username`
* `username/password`
* `username IDENTIFIED BY password`
* `username USING password`

與上述相同，參數 *`username`* 與 *`password`* 可以是 SQL 識別字、SQL 字串常數，或字元變數的參照。

若連線目標包含任何 *`options`*，它們由以 & 符號（`&`）分隔的 `keyword=value` 設定組成。允許的關鍵字與 libpq 所認得的關鍵字相同（請參閱[第 32.1.2 節](../libpq/libpq-paramkeywords.md#libpq-paramkeywords)）。任何 *`keyword`* 或 *`value`* 之前的空白都會被忽略，但其中或其後的空白則不會。請注意，沒有任何方法可以在 *`value`* 中寫入 `&`。

請注意，指定通訊端連線（使用 `unix:` 前綴）時，主機名稱必須正好是 `localhost`。若要選擇非預設的通訊端目錄，請在目標的 *`options`* 部分中，將該目錄的路徑名稱寫成 `host` 選項的值。

*`connection-name`* 用於在一個程式中處理多個連線。若程式只使用一個連線，可以省略它。最近開啟的連線會成為目前連線，要執行 SQL 陳述式時，預設會使用目前連線（請參閱本章後面的說明）。

以下是幾個 `CONNECT` 陳述式的範例：

```

EXEC SQL CONNECT TO mydb@sql.mydomain.com;

EXEC SQL CONNECT TO tcp:postgresql://sql.mydomain.com/mydb AS myconnection USER john;

EXEC SQL BEGIN DECLARE SECTION;
const char *target = "mydb@sql.mydomain.com";
const char *user = "john";
const char *passwd = "secret";
EXEC SQL END DECLARE SECTION;
 ...
EXEC SQL CONNECT TO :target USER :user USING :passwd;
/* or EXEC SQL CONNECT TO :target USER :user/:passwd; */
```

最後一個範例使用了上文所稱的字元變數參照功能。在後面的章節中，你會看到 C 變數加上冒號前綴後，如何在 SQL 陳述式中使用。

請注意，SQL 標準並未規範連線目標的格式。因此，若你想要開發可攜的應用程式，可能會想以類似上面最後一個範例的方式，把連線目標字串封裝在某個地方。

若不受信任的使用者可以存取尚未採用[安全的綱要使用模式](../../the-sql-language/ddl/ddl-schemas.md#DDL-SCHEMAS-PATTERNS)的資料庫，請在每個工作階段開始時，從 `search_path` 中移除可供公開寫入的綱要。例如，在 `options` 中加入 `options=-c search_path=`，或在連線後發出 `EXEC SQL SELECT pg_catalog.set_config('search_path', '',
false);`。這項考量並非 ECPG 所特有；它適用於所有可執行任意 SQL 命令的介面。

<a id="ECPG-SET-CONNECTION"></a>

### 34.2.2. 選擇連線 [#](#ecpg-set-connection) <a href="#ecpg-set-connection" id="ecpg-set-connection"></a>

嵌入式 SQL 程式中的 SQL 陳述式預設會在目前連線上執行，也就是最近開啟的那一個連線。若應用程式需要管理多個連線，有三種處理方式。

第一種做法是為每個 SQL 陳述式明確選擇連線，例如：

```

EXEC SQL AT connection-name SELECT ...;
```

若應用程式需要以交錯的順序使用多個連線，這種做法特別合適。

若你的應用程式使用多個執行緒，這些執行緒不能同時共用同一個連線。你必須明確控制對連線的存取（使用互斥鎖），或者讓每個執行緒各自使用一個連線。

第二種做法是執行一個陳述式來切換目前連線。該陳述式為：

```

EXEC SQL SET CONNECTION connection-name;
```

若有許多陳述式要在同一個連線上執行，這種做法特別方便。

以下是管理多個資料庫連線的範例程式：

```

#include <stdio.h>

EXEC SQL BEGIN DECLARE SECTION;
    char dbname[1024];
EXEC SQL END DECLARE SECTION;

int
main()
{
    EXEC SQL CONNECT TO testdb1 AS con1 USER testuser;
    EXEC SQL SELECT pg_catalog.set_config('search_path', '', false); EXEC SQL COMMIT;
    EXEC SQL CONNECT TO testdb2 AS con2 USER testuser;
    EXEC SQL SELECT pg_catalog.set_config('search_path', '', false); EXEC SQL COMMIT;
    EXEC SQL CONNECT TO testdb3 AS con3 USER testuser;
    EXEC SQL SELECT pg_catalog.set_config('search_path', '', false); EXEC SQL COMMIT;

    /* This query would be executed in the last opened database "testdb3". */
    EXEC SQL SELECT current_database() INTO :dbname;
    printf("current=%s (should be testdb3)\n", dbname);

    /* Using "AT" to run a query in "testdb2" */
    EXEC SQL AT con2 SELECT current_database() INTO :dbname;
    printf("current=%s (should be testdb2)\n", dbname);

    /* Switch the current connection to "testdb1". */
    EXEC SQL SET CONNECTION con1;

    EXEC SQL SELECT current_database() INTO :dbname;
    printf("current=%s (should be testdb1)\n", dbname);

    EXEC SQL DISCONNECT ALL;
    return 0;
}
```

此範例會產生下列輸出：

```

current=testdb3 (should be testdb3)
current=testdb2 (should be testdb2)
current=testdb1 (should be testdb1)
```

第三種做法是宣告一個與該連線相連結的 SQL 識別字，例如：

```

EXEC SQL AT connection-name DECLARE statement-name STATEMENT;
EXEC SQL PREPARE statement-name FROM :dyn-string;
```

一旦將 SQL 識別字連結到某個連線，你就可以不使用 AT 子句來執行動態 SQL。請注意，這種做法的行為類似前置處理器指令，因此這個連結只在該檔案中有效。

以下是使用這種做法的範例程式：

```

#include <stdio.h>

EXEC SQL BEGIN DECLARE SECTION;
char dbname[128];
char *dyn_sql = "SELECT current_database()";
EXEC SQL END DECLARE SECTION;

int main(){
  EXEC SQL CONNECT TO postgres AS con1;
  EXEC SQL CONNECT TO testdb AS con2;
  EXEC SQL AT con1 DECLARE stmt STATEMENT;
  EXEC SQL PREPARE stmt FROM :dyn_sql;
  EXEC SQL EXECUTE stmt INTO :dbname;
  printf("%s\n", dbname);

  EXEC SQL DISCONNECT ALL;
  return 0;
}
```

即使預設連線是 testdb，此範例也會產生下列輸出：

```

postgres
```

<a id="ECPG-DISCONNECT"></a>

### 34.2.3. 關閉連線 [#](#ecpg-disconnect) <a href="#ecpg-disconnect" id="ecpg-disconnect"></a>

使用下列陳述式關閉連線：

```

EXEC SQL DISCONNECT [connection];
```

*`connection`* 可以用下列方式指定：

* `connection-name`
* `CURRENT`
* `ALL`

若未指定連線名稱，則會關閉目前連線。

良好的寫法是，應用程式一律明確中斷它所開啟的每一個連線。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ecpg-connect.html)（原文版本：18.6；核對日期：2026-10-22）
