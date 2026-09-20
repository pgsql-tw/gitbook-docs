<a id="TRIGGER-INTERFACE"></a>
## 37.3. 以 C 撰寫觸發程序函式 [#](#TRIGGER-INTERFACE)

<a id="id-1.8.4.7.2"></a><a id="id-1.8.4.7.3"></a>

本節說明觸發程序函式介面的低階細節。只有在以 C 撰寫觸發程序函式時，才需要這項資訊。若您使用較高階的語言，這些細節都會為您處理好。在大多數情況下，於以 C 撰寫觸發程序之前，應先考慮使用某種程序語言。每種程序語言的文件，都說明了如何以該語言撰寫觸發程序。

觸發程序函式必須使用「第 1 版」函式管理員介面。

當觸發程序管理員呼叫某個函式時，並不會傳入任何一般引數，而是會傳入一個指向 `TriggerData` 結構的「情境（context）」指標。C
函式可以透過執行以下巨集，檢查自己是否是由觸發程序管理員所呼叫：

```

CALLED_AS_TRIGGER(fcinfo)
```

其展開後為：

```

((fcinfo)->context != NULL && IsA((fcinfo)->context, TriggerData))
```

若此式傳回 true，便可安全地將
`fcinfo->context` 轉型為 `TriggerData
*` 型別，並使用其所指向的
`TriggerData` 結構。函式*不得*變更該
`TriggerData` 結構，或其所指向的任何資料。

`struct TriggerData` 定義於
`commands/trigger.h` 中：

```

typedef struct TriggerData
{
    NodeTag          type;
    TriggerEvent     tg_event;
    Relation         tg_relation;
    HeapTuple        tg_trigtuple;
    HeapTuple        tg_newtuple;
    Trigger         *tg_trigger;
    TupleTableSlot  *tg_trigslot;
    TupleTableSlot  *tg_newslot;
    Tuplestorestate *tg_oldtable;
    Tuplestorestate *tg_newtable;
    const Bitmapset *tg_updatedcols;
} TriggerData;
```

其成員定義如下：

`type`
:   固定為 `T_TriggerData`。

`tg_event`
:   描述呼叫此函式的事件。您可以使用下列巨集來檢查 `tg_event`：

    `TRIGGER_FIRED_BEFORE(tg_event)`
    :   若觸發程序是在操作之前觸發，則傳回 true。

    `TRIGGER_FIRED_AFTER(tg_event)`
    :   若觸發程序是在操作之後觸發，則傳回 true。

    `TRIGGER_FIRED_INSTEAD(tg_event)`
    :   若觸發程序是用以取代該操作而觸發，則傳回 true。

    `TRIGGER_FIRED_FOR_ROW(tg_event)`
    :   若觸發程序是針對資料列層級事件而觸發，則傳回 true。

    `TRIGGER_FIRED_FOR_STATEMENT(tg_event)`
    :   若觸發程序是針對陳述式層級事件而觸發，則傳回 true。

    `TRIGGER_FIRED_BY_INSERT(tg_event)`
    :   若觸發程序是由 `INSERT` 命令觸發，則傳回 true。

    `TRIGGER_FIRED_BY_UPDATE(tg_event)`
    :   若觸發程序是由 `UPDATE` 命令觸發，則傳回 true。

    `TRIGGER_FIRED_BY_DELETE(tg_event)`
    :   若觸發程序是由 `DELETE` 命令觸發，則傳回 true。

    `TRIGGER_FIRED_BY_TRUNCATE(tg_event)`
    :   若觸發程序是由 `TRUNCATE` 命令觸發，則傳回 true。

`tg_relation`
:   指向描述該觸發程序所觸發之關聯（relation）的結構之指標。
    關於此結構的詳情，請參閱 `utils/rel.h`。其中
    最值得留意的是
    `tg_relation->rd_att`（該關聯資料列的描述子）與
    `tg_relation->rd_rel->relname`
    （關聯名稱；其型別並非 `char*`，而是
    `NameData`；若您需要該名稱的副本，請使用
    `SPI_getrelname(tg_relation)` 來取得 `char*`）。

`tg_trigtuple`
:   指向觸發程序所觸發之資料列的指標。這是
    正在被新增、更新或刪除的資料列。若此觸發程序
    是因 `INSERT` 或
    `DELETE` 而觸發，且您不想以另一列取代此列
    （在 `INSERT` 的情況下）或略過此操作，那麼這就是您應該從函式中
    傳回的內容。對於外部資料表上的觸發程序，其中系統
    欄位的值並未定義。

`tg_newtuple`
:   指向該資料列新版本的指標，適用於觸發程序是因
    `UPDATE` 而觸發的情況；若是因
    `INSERT` 或
    `DELETE` 而觸發，則為 `NULL`。若事件為
    `UPDATE`，且您不想以另一列取代此列
    或略過此操作，這就是您必須從函式中傳回的內容。對於外部資料表上的觸發程序，其中系統
    欄位的值並未定義。

`tg_trigger`
:   指向型別為 `Trigger` 之結構的指標，
    定義於 `utils/reltrigger.h` 中：

    ```

    typedef struct Trigger
    {
        Oid         tgoid;
        char       *tgname;
        Oid         tgfoid;
        int16       tgtype;
        char        tgenabled;
        bool        tgisinternal;
        bool        tgisclone;
        Oid         tgconstrrelid;
        Oid         tgconstrindid;
        Oid         tgconstraint;
        bool        tgdeferrable;
        bool        tginitdeferred;
        int16       tgnargs;
        int16       tgnattr;
        int16      *tgattr;
        char      **tgargs;
        char       *tgqual;
        char       *tgoldtable;
        char       *tgnewtable;
    } Trigger;
    ```

    其中 `tgname` 是觸發程序的名稱，
    `tgnargs` 是 `tgargs` 中引數的數量，
    而 `tgargs` 則是一個陣列，其中每個元素都是指向 `CREATE
    TRIGGER` 陳述式中所指定引數的指標。其餘成員僅供
    內部使用。

`tg_trigslot`
:   包含 `tg_trigtuple` 的插槽（slot），
    若沒有這樣的資料列，則為 `NULL` 指標。

`tg_newslot`
:   包含 `tg_newtuple` 的插槽，
    若沒有這樣的資料列，則為 `NULL` 指標。

`tg_oldtable`
:   指向型別為 `Tuplestorestate` 之結構的指標，
    其中包含零筆或多筆、格式由
    `tg_relation` 指定的資料列；若沒有
    `OLD TABLE` 轉換關聯，則為 `NULL` 指標。

`tg_newtable`
:   指向型別為 `Tuplestorestate` 之結構的指標，
    其中包含零筆或多筆、格式由
    `tg_relation` 指定的資料列；若沒有
    `NEW TABLE` 轉換關聯，則為 `NULL` 指標。

`tg_updatedcols`
:   對於 `UPDATE` 觸發程序，這是一個位元映射集合，指出
    觸發此命令所更新的欄位。通用的觸發程序函式可利用此資訊來最佳化動作，不必處理
    未變更的欄位。

    舉例來說，若要判斷屬性編號（1 起始）為
    `attnum` 的欄位是否為此位元映射集合的成員，
    可呼叫 `bms_is_member(attnum -
    FirstLowInvalidHeapAttributeNumber,
    trigdata->tg_updatedcols))`。

    對於非 `UPDATE` 觸發程序而言，此值將
    為 `NULL`。

若要讓透過 SPI 發出的查詢能夠參照轉換資料表，請見
[SPI_register_trigger_data](../spi/spi-spi-register-trigger-data.md)。

觸發程序函式必須傳回
`HeapTuple` 指標或 `NULL` 指標
（*而非* SQL 的 null 值，也就是說，請勿將 *`isNull`* 設為 true）。
若您不想修改正在操作中的資料列，請小心地依情況傳回
`tg_trigtuple` 或 `tg_newtuple`。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/trigger-interface.html)（原文版本：18.6；核對日期：2026-09-15）
