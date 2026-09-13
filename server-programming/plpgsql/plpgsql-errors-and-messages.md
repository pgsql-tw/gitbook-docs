<a id="PLPGSQL-ERRORS-AND-MESSAGES"></a>

## 41.9. 錯誤與訊息 [#](#PLPGSQL-ERRORS-AND-MESSAGES)

[41.9.1. 回報錯誤與訊息](plpgsql-errors-and-messages.md#PLPGSQL-STATEMENTS-RAISE)

[41.9.2. 檢查斷言](plpgsql-errors-and-messages.md#PLPGSQL-STATEMENTS-ASSERT)

<a id="PLPGSQL-STATEMENTS-RAISE"></a>

### 41.9.1. 回報錯誤與訊息 [#](#PLPGSQL-STATEMENTS-RAISE)

<a id="id-1.8.8.11.2.2"></a><a id="id-1.8.8.11.2.3"></a>

使用 `RAISE` 陳述式來回報訊息並拋出錯誤。

```

RAISE [ level ] 'format' [, expression [, ... ]] [ USING option { = | := } expression [, ... ] ];
RAISE [ level ] condition_name [ USING option { = | := } expression [, ... ] ];
RAISE [ level ] SQLSTATE 'sqlstate' [ USING option { = | := } expression [, ... ] ];
RAISE [ level ] USING option { = | := } expression [, ... ];
RAISE ;
```

*`level`* 選項用來指定錯誤的嚴重程度。允許的層級有 `DEBUG`、`LOG`、`INFO`、`NOTICE`、`WARNING` 與 `EXCEPTION`，其中 `EXCEPTION` 為預設值。`EXCEPTION` 會拋出一個錯誤（通常會中止目前的交易）；其他層級則只會產生不同優先層級的訊息。特定優先層級的訊息是否回報給用戶端、寫入伺服器日誌或兩者皆是，由 [log_min_messages](../../server-administration/runtime-config/runtime-config-logging.md#GUC-LOG-MIN-MESSAGES) 與 [client_min_messages](../../server-administration/runtime-config/runtime-config-client.md#GUC-CLIENT-MIN-MESSAGES) 這兩個組態變數控制。更多資訊請參閱[第 19 章](../../server-administration/runtime-config/README.md)。

在第一種語法變體中，於 *`level`*（若有指定）之後，要寫一個 *`format`* 字串（必須是單純的字串常數，不能是運算式）。這個格式字串指定了要回報的錯誤訊息文字。格式字串後面可以接選擇性的引數運算式，這些運算式的值會被插入訊息中。在格式字串裡，`%` 會被下一個選擇性引數之值的字串表示法所取代。若要輸出字面的 `%`，請寫成 `%%`。引數的數量必須與格式字串中 `%` 佔位符的數量相符，否則在編譯該函式時就會拋出錯誤。

在這個例子中，`v_job_id` 的值會取代字串中的 `%`：

```

RAISE NOTICE 'Calling cs_create_job(%)', v_job_id;
```

在第二與第三種語法變體中，*`condition_name`* 與 *`sqlstate`* 分別用來指定錯誤條件名稱或五個字元的 SQLSTATE 代碼。有效的錯誤條件名稱與預先定義的 SQLSTATE 代碼請參閱[附錄 A](../../appendixes/errcodes-appendix/README.md)。

以下是使用 *`condition_name`* 與 *`sqlstate`* 的例子：

```

RAISE division_by_zero;
RAISE WARNING SQLSTATE '22012';
```

在上述任何一種語法變體中，你都可以在後面寫上 `USING`，再接著 *`option`* = *`expression`* 項目，藉此在錯誤報告中附加額外資訊。每個 *`expression`* 都可以是任何回傳字串值的運算式。允許的 *`option`* 關鍵字有：

<a id="RAISE-USING-OPTIONS"></a>

<a id="RAISE-USING-OPTION-MESSAGE"></a>

`MESSAGE` [#](#RAISE-USING-OPTION-MESSAGE)
:   設定錯誤訊息文字。這個選項不能用在第一種語法變體中，因為訊息在那裡已經提供過了。
<a id="RAISE-USING-OPTION-DETAIL"></a>

`DETAIL` [#](#RAISE-USING-OPTION-DETAIL)
:   提供錯誤的詳細訊息。
<a id="RAISE-USING-OPTION-HINT"></a>

`HINT` [#](#RAISE-USING-OPTION-HINT)
:   提供提示訊息。
<a id="RAISE-USING-OPTION-ERRCODE"></a>

`ERRCODE` [#](#RAISE-USING-OPTION-ERRCODE)
:   指定要回報的錯誤碼（SQLSTATE），可以用[附錄 A](../../appendixes/errcodes-appendix/README.md) 所列的條件名稱指定，也可以直接寫五個字元的 SQLSTATE 代碼。這個選項不能用在第二或第三種語法變體中，因為錯誤碼在那裡已經提供過了。
<a id="RAISE-USING-OPTION-COLUMN"></a>

`COLUMN`<br>`CONSTRAINT`<br>`DATATYPE`<br>`TABLE`<br>`SCHEMA` [#](#RAISE-USING-OPTION-COLUMN)
:   提供相關物件的名稱。

這個例子會以指定的錯誤訊息與提示中止交易：

```

RAISE EXCEPTION 'Nonexistent ID --> %', user_id
      USING HINT = 'Please check your user ID';
```

下面這兩個例子示範了設定 SQLSTATE 的兩種等價寫法：

```

RAISE 'Duplicate user ID: %', user_id USING ERRCODE = 'unique_violation';
RAISE 'Duplicate user ID: %', user_id USING ERRCODE = '23505';
```

另一種產生相同結果的方式是：

```

RAISE unique_violation USING MESSAGE = 'Duplicate user ID: ' || user_id;
```

如第四種語法變體所示，你也可以寫成 `RAISE USING` 或 `RAISE level USING`，把其餘所有內容都放進 `USING` 清單中。

`RAISE` 的最後一種變體完全不帶參數。這種形式只能用在 `BEGIN` 區塊的 `EXCEPTION` 子句內；它會使目前正在處理的錯誤被重新拋出。

### 注意

在 PostgreSQL 9.1 之前，不帶參數的 `RAISE` 會被解讀為重新拋出「包含該作用中例外處理常式的區塊」所發生的錯誤。因此，巢狀於該處理常式內的 `EXCEPTION` 子句無法攔截它，即使該 `RAISE` 就位於那個巢狀 `EXCEPTION` 子句的區塊之中也一樣。這個行為被認為相當出人意料，也與 Oracle 的 PL/SQL 不相容。

如果在 `RAISE EXCEPTION` 指令中沒有指定條件名稱或 SQLSTATE，預設會使用 `raise_exception`（`P0001`）。如果沒有指定訊息文字，預設會以條件名稱或 SQLSTATE 作為訊息文字。

### 注意

以 SQLSTATE 代碼指定錯誤碼時，你並不侷限於預先定義的錯誤碼，而是可以選用任何由五個數字與／或大寫 ASCII 字母組成、且不是 `00000` 的錯誤碼。建議你避免拋出結尾為三個零的錯誤碼，因為那些是類別代碼，只能透過攔截整個類別的方式來攔截。

<a id="PLPGSQL-STATEMENTS-ASSERT"></a>

### 41.9.2. 檢查斷言 [#](#PLPGSQL-STATEMENTS-ASSERT)

<a id="id-1.8.8.11.3.2"></a><a id="id-1.8.8.11.3.3"></a><a id="id-1.8.8.11.3.4"></a>

`ASSERT` 陳述式是一種方便的簡寫，可用來在 PL/pgSQL 函式中插入除錯用的檢查。

```

ASSERT condition [ , message ];
```

*`condition`* 是一個布林運算式，預期永遠會計算為真；如果為真，`ASSERT` 陳述式就不會再做任何事。如果結果為假或 NULL，就會拋出 `ASSERT_FAILURE` 例外。（如果在計算 *`condition`* 的過程中發生錯誤，該錯誤會以一般錯誤的方式回報。）

如果有提供選擇性的 *`message`*，它是一個運算式，其結果（若不為 NULL）會在 *`condition`* 不成立時，取代預設的錯誤訊息文字「assertion failed」。在斷言成立的一般情況下，並不會計算 *`message`* 運算式。

斷言的測試可以透過組態參數 `plpgsql.check_asserts` 來啟用或停用，此參數接受布林值，預設為 `on`。如果這個參數是 `off`，那麼 `ASSERT` 陳述式就不會有任何作用。

請注意，`ASSERT` 的用途是偵測程式的錯誤，而不是回報一般的錯誤狀況。那種情況請改用前面介紹的 `RAISE` 陳述式。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/plpgsql-errors-and-messages.html)（原文版本：18.6；核對日期：2026-09-12）
