<a id="PLPERL-TRIGGERS"></a>

## 43.6. PL/Perl 觸發程序 [#](#PLPERL-TRIGGERS)

PL/Perl 可以用來撰寫觸發程序函式。在觸發程序函式中，hash（雜湊）參照 `$_TD` 含有關於目前觸發程序事件的資訊。`$_TD` 是一個全域變數，它在觸發程序的每一次呼叫中都會取得各自獨立的區域值。`$_TD` hash 參照的各欄位如下：

`$_TD->{new}{foo}`
:   欄位 `foo` 的 `NEW` 值

`$_TD->{old}{foo}`
:   欄位 `foo` 的 `OLD` 值

`$_TD->{name}`
:   被呼叫的觸發程序名稱

`$_TD->{event}`
:   觸發程序事件：`INSERT`、`UPDATE`、`DELETE`、`TRUNCATE` 或 `UNKNOWN`

`$_TD->{when}`
:   觸發程序何時被呼叫：`BEFORE`、`AFTER`、`INSTEAD OF` 或 `UNKNOWN`

`$_TD->{level}`
:   觸發程序層級：`ROW`、`STATEMENT` 或 `UNKNOWN`

`$_TD->{relid}`
:   觸發該觸發程序之資料表的 OID

`$_TD->{table_name}`
:   觸發該觸發程序之資料表的名稱

`$_TD->{relname}`
:   觸發該觸發程序之資料表的名稱。這已經被棄用，未來的版本中可能會移除。請改用 $_TD->{table_name}。

`$_TD->{table_schema}`
:   觸發該觸發程序之資料表所在綱要的名稱

`$_TD->{argc}`
:   觸發程序函式的引數數量

`@{$_TD->{args}}`
:   觸發程序函式的引數。如果 `$_TD->{argc}` 為 0，則不存在。

資料列層級的觸發程序可以回傳下列其中之一：

`return;`
:   執行該操作

`"SKIP"`
:   不要執行該操作

`"MODIFY"`
:   表示 `NEW` 資料列已被觸發程序函式修改過

以下是一個觸發程序函式的範例，說明了上述的部分內容：

```

CREATE TABLE test (
    i int,
    v varchar
);

CREATE OR REPLACE FUNCTION valid_id() RETURNS trigger AS $$
    if (($_TD->{new}{i} >= 100) || ($_TD->{new}{i} <= 0)) {
        return "SKIP";    # skip INSERT/UPDATE command
    } elsif ($_TD->{new}{v} ne "immortal") {
        $_TD->{new}{v} .= "(modified by trigger)";
        return "MODIFY";  # modify row and execute INSERT/UPDATE command
    } else {
        return;           # execute INSERT/UPDATE command
    }
$$ LANGUAGE plperl;

CREATE TRIGGER test_valid_id_trig
    BEFORE INSERT OR UPDATE ON test
    FOR EACH ROW EXECUTE FUNCTION valid_id();
```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/plperl-triggers.html)（原文版本：18.6；核對日期：2026-09-13）
