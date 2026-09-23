<a id="ROLE-REMOVAL"></a>

## 21.4. 移除角色 [#](#ROLE-REMOVAL)

由於角色可以擁有資料庫物件，也可以持有存取其他物件的權限，
因此移除角色，通常不只是單純執行一次
[`DROP ROLE`](../../reference/sql-commands/sql-droprole.md) 那麼簡單。
必須先移除該角色所擁有的所有物件，或將其轉移給其他擁有者；
並且必須撤銷授予該角色的所有權限。

物件的擁有權，可以透過 `ALTER` 指令逐一轉移，例如：

```

ALTER TABLE bobs_table OWNER TO alice;
```

或者，也可以使用
[`REASSIGN OWNED`](../../reference/sql-commands/sql-reassign-owned.md) 指令，
將即將被移除角色所擁有的所有物件，一次全部轉移給另一個
指定角色。由於 `REASSIGN OWNED` 無法存取其他資料庫中的物件，
因此必須在包含該角色所擁有物件的每一個資料庫中，
分別執行一次此指令。（請注意，第一次執行這樣的
`REASSIGN OWNED`，就會變更該即將被移除角色所擁有、
跨資料庫共用之物件——也就是資料庫或資料表空間——的擁有權。）

一旦任何有價值的物件都已轉移給新的擁有者，
即將被移除角色所擁有的任何剩餘物件，就可以透過
[`DROP OWNED`](../../reference/sql-commands/sql-drop-owned.md) 指令來移除。
同樣地，此指令也無法存取其他資料庫中的物件，
因此必須在包含該角色所擁有物件的每一個資料庫中，
分別執行一次。此外，`DROP OWNED`
不會移除整個資料庫或資料表空間，因此若該角色擁有
任何尚未轉移給新擁有者的資料庫或資料表空間，
就必須手動處理。

`DROP OWNED` 也會一併處理：移除目標角色對於
不屬於自己之物件所被授予的任何權限。由於
`REASSIGN OWNED` 不會處理這類物件，因此通常必須
同時執行 `REASSIGN OWNED` 與
`DROP OWNED`（且依此順序！），
才能完全移除即將被移除角色的所有相依關係。

簡而言之，移除一個曾用來擁有物件之角色的最通用做法是：

```

REASSIGN OWNED BY doomed_role TO successor_role;
DROP OWNED BY doomed_role;
-- repeat the above commands in each database of the cluster
DROP ROLE doomed_role;
```

若並非所有被擁有的物件，都要轉移給同一個後繼擁有者，
最好的做法是手動處理這些例外狀況，然後再執行
上述步驟收尾。

若在仍有相依物件存在的情況下，嘗試執行 `DROP ROLE`，
系統就會發出訊息，指出哪些物件需要轉移擁有權或移除。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/role-removal.html)（原文版本：18.6；核對日期：2026-09-22）
