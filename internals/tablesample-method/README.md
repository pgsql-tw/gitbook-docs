<a id="TABLESAMPLE-METHOD"></a>

## 第 59 章 撰寫資料表取樣方法

**目錄**

[59.1. 取樣方法支援函式](tablesample-support-functions.md)

<a id="id-1.10.11.2"></a><a id="id-1.10.11.3"></a>

PostgreSQL 對 `TABLESAMPLE`
子句的實作，除了 SQL 標準所要求的
`BERNOULLI` 與 `SYSTEM` 方法之外，還支援自訂的資料表取樣方法。取樣方法決定了使用 `TABLESAMPLE` 子句時，會選取資料表中的哪些資料列。

在 SQL 層級，資料表取樣方法以單一 SQL
函式表示，該函式通常以 C 實作，其簽章為

```

method_name(internal) RETURNS tsm_handler
```

函式的名稱就是出現在
`TABLESAMPLE` 子句中的方法名稱。`internal` 引數是一個虛設引數
（其值永遠為零），作用只是防止此函式直接從 SQL 命令中被呼叫。
函式的結果必須是以 palloc 配置、型別為 `TsmRoutine` 的結構，其中包含指向該取樣方法各支援函式的指標。這些支援函式是一般的 C 函式，在 SQL 層級既不可見，也無法呼叫。支援函式描述於[第 59.1 節](tablesample-support-functions.md)。

除了函式指標之外，`TsmRoutine` 結構還必須提供下列額外欄位：

`List *parameterTypes`
:   這是一個 OID 清單，包含使用此取樣方法時
    `TABLESAMPLE` 子句所接受之參數的資料型別 OID。例如，對於內建方法，此清單只包含一個值為 `FLOAT4OID` 的項目，代表取樣百分比。自訂取樣方法可以有更多或不同的參數。

`bool repeatable_across_queries`
:   若為 `true`，則只要每次都提供相同的參數與
    `REPEATABLE` 種子值，且資料表內容沒有變更，取樣方法就可以在連續的多個查詢中提供相同的樣本。當此值為 `false` 時，
    此取樣方法不接受搭配使用 `REPEATABLE` 子句。

`bool repeatable_across_scans`
:   若為 `true`，取樣方法可以在同一個查詢的連續多次掃描中提供相同的樣本（假設參數、種子值與快照都不變）。
    當此值為 `false` 時，規劃器不會選擇需要掃描受取樣資料表超過一次的計畫，因為那可能導致查詢輸出不一致。

`TsmRoutine` 結構型別宣告於
`src/include/access/tsmapi.h`，更多細節請參閱該檔案。

在嘗試撰寫自己的資料表取樣方法時，標準發行版中所包含的取樣方法是很好的參考。內建的取樣方法請查看原始碼樹中的
`src/backend/access/tablesample` 子目錄，附加的方法則請查看 `contrib`
子目錄。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/tablesample-method.html)（原文版本：18.6；核對日期：2026-10-12）
