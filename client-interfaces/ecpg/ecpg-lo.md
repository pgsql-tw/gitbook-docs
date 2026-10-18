<a id="ECPG-LO"></a>

## 34.12. 大型物件 [#](#ECPG-LO)

ECPG 並未直接支援大型物件，但 ECPG 應用程式可以透過 libpq 的大型物件函式來操作大型物件，所需的 `PGconn` 物件可藉由呼叫 `ECPGget_PGconn()` 函式取得。（不過，使用 `ECPGget_PGconn()` 函式以及直接操作 `PGconn` 物件時應非常謹慎，而且最好不要與其他 ECPG 資料庫存取呼叫混用。）

關於 `ECPGget_PGconn()` 的更多細節，請參閱[第 34.11 節](ecpg-library.md)。關於大型物件函式介面的資訊，請參閱[第 33 章](../largeobjects/README.md)。

大型物件函式必須在交易區塊中呼叫，因此在自動提交關閉時，必須明確發出 `BEGIN` 命令。

[範例 34.2](ecpg-lo.md#ECPG-LO-EXAMPLE) 是一個範例程式，示範如何在 ECPG 應用程式中建立、寫入及讀取大型物件。

<a id="ECPG-LO-EXAMPLE"></a>

**範例 34.2. 存取大型物件的 ECPG 程式**

```

#include <stdio.h>
#include <stdlib.h>
#include <libpq-fe.h>
#include <libpq/libpq-fs.h>

EXEC SQL WHENEVER SQLERROR STOP;

int
main(void)
{
    PGconn     *conn;
    Oid         loid;
    int         fd;
    char        buf[256];
    int         buflen = 256;
    char        buf2[256];
    int         rc;

    memset(buf, 1, buflen);

    EXEC SQL CONNECT TO testdb AS con1;
    EXEC SQL SELECT pg_catalog.set_config('search_path', '', false); EXEC SQL COMMIT;

    conn = ECPGget_PGconn("con1");
    printf("conn = %p\n", conn);

    /* create */
    loid = lo_create(conn, 0);
    if (loid &lt; 0)
        printf("lo_create() failed: %s", PQerrorMessage(conn));

    printf("loid = %d\n", loid);

    /* write test */
    fd = lo_open(conn, loid, INV_READ|INV_WRITE);
    if (fd &lt; 0)
        printf("lo_open() failed: %s", PQerrorMessage(conn));

    printf("fd = %d\n", fd);

    rc = lo_write(conn, fd, buf, buflen);
    if (rc &lt; 0)
        printf("lo_write() failed\n");

    rc = lo_close(conn, fd);
    if (rc &lt; 0)
        printf("lo_close() failed: %s", PQerrorMessage(conn));

    /* read test */
    fd = lo_open(conn, loid, INV_READ);
    if (fd &lt; 0)
        printf("lo_open() failed: %s", PQerrorMessage(conn));

    printf("fd = %d\n", fd);

    rc = lo_read(conn, fd, buf2, buflen);
    if (rc &lt; 0)
        printf("lo_read() failed\n");

    rc = lo_close(conn, fd);
    if (rc &lt; 0)
        printf("lo_close() failed: %s", PQerrorMessage(conn));

    /* check */
    rc = memcmp(buf, buf2, buflen);
    printf("memcmp() = %d\n", rc);

    /* cleanup */
    rc = lo_unlink(conn, loid);
    if (rc &lt; 0)
        printf("lo_unlink() failed: %s", PQerrorMessage(conn));

    EXEC SQL COMMIT;
    EXEC SQL DISCONNECT ALL;
    return 0;
}
```

譯註：上方程式碼依原樣保留，僅在此說明四點：

- 程式碼中的「&amp;lt;」是文件轉換時殘留的 HTML 實體，實際原始碼為小於符號「&lt;」，例如 loid &lt; 0 與 fd &lt; 0。
- lo_create 的傳回型別 Oid 是無號整數，因此 loid &lt; 0 這項檢查永遠不會成立；lo_create 失敗時傳回的是 InvalidOid（0），正確的檢查方式是比較 loid == InvalidOid。
- 本節說明大型物件函式必須在交易區塊中呼叫，但範例在 EXEC SQL COMMIT 之後就直接呼叫 lo_create，沒有先開始交易。實際使用時，應在第一次呼叫大型物件函式之前先執行 EXEC SQL BEGIN（或以其他方式開始交易）。
- 範例使用了 memset 與 memcmp，但沒有引入宣告這兩個函式的標頭檔 &lt;string.h&gt;。實際編譯時應加上 #include &lt;string.h&gt;，以取得正確的函式宣告。

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ecpg-lo.html)（原文版本：18.6；核對日期：2026-10-18）
