## 36.9. 內部函式 [#](#XFUNC-INTERNAL)

<a id="id-1.8.3.12.2"></a>

內部函式是以 C 撰寫並靜態連結至 PostgreSQL 伺服器的函式。函式定義的「主體」會指定函式的 C 語言名稱，無須與宣告供 SQL 使用的名稱相同。（為維持向後相容，空白主體表示 C 語言函式名稱與 SQL 名稱相同。）

通常伺服器中的所有內部函式都會在初始化資料庫叢集時宣告（請參閱[第 18.2 節](../../server-administration/runtime/creating-cluster.md)），但使用者可用 `CREATE FUNCTION` 為內部函式建立額外別名。內部函式會在 `CREATE FUNCTION` 中以 `internal` 作為語言名稱宣告。舉例來說，若要為 `sqrt` 函式建立別名：

```

CREATE FUNCTION square_root(double precision) RETURNS double precision
    AS 'dsqrt'
    LANGUAGE internal
    STRICT;
```

（大多數內部函式預期宣告為「strict」。）

### 注意

並非所有「預先定義」函式都是上述意義的「內部」函式；有些預先定義函式以 SQL 撰寫。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/xfunc-internal.html)（原文版本：18.6；核對日期：2026-09-10）
