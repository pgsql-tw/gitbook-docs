<a id="ECPG-IFDEF"></a>

## 34.9.3. ifdef、ifndef、elif、else 與 endif 指令 [#](#ecpg-ifdef) <a href="#ecpg-ifdef" id="ecpg-ifdef"></a>

你可以使用下列指令有條件地編譯程式碼區段：

<a id="ECPG-IFDEF-IFDEF"></a>

### `EXEC SQL ifdef name;` [#](#ecpg-ifdef-ifdef) <a href="#ecpg-ifdef-ifdef" id="ecpg-ifdef-ifdef"></a>

檢查 *`name`*，若 *`name`* 已透過 `EXEC SQL define
    name` 定義，則處理後續各行。

<a id="ECPG-IFDEF-IFNDEF"></a>

### `EXEC SQL ifndef name;` [#](#ecpg-ifdef-ifndef) <a href="#ecpg-ifdef-ifndef" id="ecpg-ifdef-ifndef"></a>

檢查 *`name`*，若 *`name`* *尚未*透過 `EXEC SQL define name` 定義，則處理後續各行。

<a id="ECPG-IFDEF-ELIF"></a>

### `EXEC SQL elif name;` [#](#ecpg-ifdef-elif) <a href="#ecpg-ifdef-elif" id="ecpg-ifdef-elif"></a>

在 `EXEC SQL ifdef name` 或 `EXEC SQL ifndef name` 指令之後，開始一個選用的替代區段。`elif` 區段可以出現任意多個。若 *`name`* 已定義，*而且*同一個 `ifdef`/`ifndef`...`endif` 結構中先前沒有任何區段被處理過，則會處理 `elif` 之後的各行。

<a id="ECPG-IFDEF-ELSE"></a>

### `EXEC SQL else;` [#](#ecpg-ifdef-else) <a href="#ecpg-ifdef-else" id="ecpg-ifdef-else"></a>

在 `EXEC SQL ifdef name` 或 `EXEC SQL ifndef name` 指令之後，開始一個選用的最終替代區段。若同一個 `ifdef`/`ifndef`...`endif` 結構中先前沒有任何區段被處理過，則會處理後續各行。

<a id="ECPG-IFDEF-ENDIF"></a>

### `EXEC SQL endif;` [#](#ecpg-ifdef-endif) <a href="#ecpg-ifdef-endif" id="ecpg-ifdef-endif"></a>

結束一個 `ifdef`/`ifndef`...`endif` 結構。後續各行會照常處理。

`ifdef`/`ifndef`...`endif` 結構可以巢狀使用，最多 127 層。

此範例會在三個 `SET
TIMEZONE` 命令中恰好編譯其中一個：

```

EXEC SQL ifdef TZVAR;
EXEC SQL SET TIMEZONE TO TZVAR;
EXEC SQL elif TZNAME;
EXEC SQL SET TIMEZONE TO TZNAME;
EXEC SQL else;
EXEC SQL SET TIMEZONE TO 'GMT';
EXEC SQL endif;
```

[返回 34.9. 前置處理器指令](ecpg-preproc.md#ecpg-preproc)。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ecpg-preproc.html)（原文版本：18.6；核對日期：2026-10-18）
