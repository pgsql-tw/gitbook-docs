<a id="XFUNC-OVERLOAD"></a>
## 36.6. 函式多載 [#](#XFUNC-OVERLOAD)

<a id="id-1.8.3.9.2"></a>

只要引數不同，就可以用相同的 SQL 名稱定義多個函式。換句話說，函式名稱可以*多載*。不論你是否使用這項功能，當資料庫中有些使用者不信任其他使用者時，呼叫函式就會牽涉到安全上的預防措施；見[第 10.3 節](../../the-sql-language/typeconv/typeconv-func.md)。執行查詢時，伺服器會依據所提供引數的資料型別與數量，來判斷要呼叫哪一個函式。多載也可以用來模擬引數個數可變（但有一個有限的最大值）的函式。

在建立一系列多載函式時，應該小心避免造成歧義。舉例來說，給定下列函式：

```

CREATE FUNCTION test(int, real) RETURNS ...
CREATE FUNCTION test(smallint, double precision) RETURNS ...
```

對於像 `test(1, 1.5)` 這種簡單的輸入，並不能立即看出會呼叫哪一個函式。目前實作的解析規則說明於[第 10 章](../../the-sql-language/typeconv/README.md)，但設計一套會微妙地依賴這種行為的系統，並不是明智之舉。

接受單一複合型別引數的函式，通常不應該與該型別的任何屬性（欄位）同名。回想一下，`attribute(table)` 會被視為等同於 `table.attribute`。如果複合型別上的函式與該複合型別的某個屬性發生歧義，系統一律會使用該屬性。你可以透過以綱要限定函式名稱（也就是 `schema.func(table)`）來覆寫這個選擇，不過更好的做法是一開始就避免選用互相衝突的名稱，以避免這個問題。

另一種可能的衝突，發生在可變引數函式與非可變引數函式之間。舉例來說，你可以同時建立 `foo(numeric)` 與 `foo(VARIADIC numeric[])`。在這種情況下，並不清楚提供單一數值引數的呼叫（例如 `foo(10.1)`）應該比對到哪一個函式。規則是：會使用在搜尋路徑中較早出現的函式；如果兩個函式位於同一個綱要中，則偏好非可變引數的那一個。

對 C 語言函式進行多載時，還有一項額外的限制：一系列多載函式中，每個函式的 C 名稱，都必須與所有其他函式（不論是內部函式還是動態載入的函式）的 C 名稱不同。如果違反這項規則，其行為就不具可攜性。你可能會遇到執行期連結器錯誤，或是其中一個函式會被呼叫（通常是內部函式）。SQL `CREATE FUNCTION` 命令中 `AS` 子句的另一種形式，可以把 SQL 函式名稱與 C 原始碼中的函式名稱分開。例如：

```

CREATE FUNCTION test(int) RETURNS int
    AS 'filename', 'test_1arg'
    LANGUAGE C;
CREATE FUNCTION test(int, int) RETURNS int
    AS 'filename', 'test_2arg'
    LANGUAGE C;
```

這裡的 C 函式名稱，反映了眾多可能命名慣例中的一種。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/xfunc-overload.html)（原文版本：18.6；核對日期：2026-09-15）
