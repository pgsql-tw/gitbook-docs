<a id="EVENT-TRIGGER-TABLE-REWRITE-EXAMPLE"></a>
## 38.4. 資料表重寫事件觸發程序範例 [#](#EVENT-TRIGGER-TABLE-REWRITE-EXAMPLE)

由於 `table_rewrite` 事件，可以實作一套資料表重寫策略，僅允許在維護時段內進行重寫。

以下是實作這樣一套策略的範例。

```

CREATE OR REPLACE FUNCTION no_rewrite()
 RETURNS event_trigger
 LANGUAGE plpgsql AS
$$
---
--- Implement local Table Rewriting policy:
---   public.foo is not allowed rewriting, ever
---   other tables are only allowed rewriting between 1am and 6am
---   unless they have more than 100 blocks
---
DECLARE
  table_oid oid := pg_event_trigger_table_rewrite_oid();
  current_hour integer := extract('hour' from current_time);
  pages integer;
  max_pages integer := 100;
BEGIN
  IF pg_event_trigger_table_rewrite_oid() = 'public.foo'::regclass
  THEN
        RAISE EXCEPTION 'you''re not allowed to rewrite the table %',
                        table_oid::regclass;
  END IF;

  SELECT INTO pages relpages FROM pg_class WHERE oid = table_oid;
  IF pages > max_pages
  THEN
        RAISE EXCEPTION 'rewrites only allowed for table with less than % pages',
                        max_pages;
  END IF;

  IF current_hour NOT BETWEEN 1 AND 6
  THEN
        RAISE EXCEPTION 'rewrites only allowed between 1am and 6am';
  END IF;
END;
$$;

CREATE EVENT TRIGGER no_rewrite_allowed
                  ON table_rewrite
   EXECUTE FUNCTION no_rewrite();
```

> 譯者註：上列範例程式碼開頭註解提及「超過 100 blocks」可作為維護時段限制的例外，但實際程式邏輯是只要區塊數（pages）超過 max_pages（100）就一律拒絕重寫，與是否落在維護時段（凌晨 1 點至 6 點）無關；兩項檢查彼此獨立。此為 PostgreSQL 官方文件範例本身註解與程式碼的既有不一致之處，非翻譯所致，程式碼區塊維持原文逐字呈現。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/event-trigger-table-rewrite-example.html)（原文版本：18.6；核對日期：2026-09-22）
