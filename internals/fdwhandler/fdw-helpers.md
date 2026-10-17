<a id="FDW-HELPERS"></a>

## 58.3. 外部資料包裝器輔助函式 [#](#FDW-HELPERS)

核心伺服器匯出了數個輔助函式，讓
外部資料包裝器的作者可以輕鬆存取
FDW 相關物件的屬性，例如 FDW 選項。
要使用其中任何一個函式，你需要在原始檔中引入標頭檔
`foreign/foreign.h`。
該標頭檔也定義了這些函式所傳回的
結構型別。

```

ForeignDataWrapper *
GetForeignDataWrapperExtended(Oid fdwid, bits16 flags);
```

此函式傳回具有給定 OID 之外部資料包裝器的 `ForeignDataWrapper`
物件。
`ForeignDataWrapper` 物件包含該 FDW 的屬性
（詳情請參閱 `foreign/foreign.h`）。
`flags` 是以位元 OR 組合而成的位元遮罩，表示
一組額外的選項。它可以取值
`FDW_MISSING_OK`，此時對於未定義的物件，
會向呼叫者傳回 `NULL`
結果，而不是擲出錯誤。

```

ForeignDataWrapper *
GetForeignDataWrapper(Oid fdwid);
```

此函式傳回具有給定 OID 之外部資料包裝器的 `ForeignDataWrapper`
物件。
`ForeignDataWrapper` 物件包含該 FDW 的屬性
（詳情請參閱 `foreign/foreign.h`）。

```

ForeignServer *
GetForeignServerExtended(Oid serverid, bits16 flags);
```

此函式傳回具有給定 OID 之外部伺服器的 `ForeignServer` 物件。
`ForeignServer` 物件包含該伺服器的屬性
（詳情請參閱 `foreign/foreign.h`）。
`flags` 是以位元 OR 組合而成的位元遮罩，表示
一組額外的選項。它可以取值
`FSV_MISSING_OK`，此時對於未定義的物件，
會向呼叫者傳回 `NULL`
結果，而不是擲出錯誤。

```

ForeignServer *
GetForeignServer(Oid serverid);
```

此函式傳回具有給定 OID 之外部伺服器的 `ForeignServer` 物件。
`ForeignServer` 物件包含該伺服器的屬性
（詳情請參閱 `foreign/foreign.h`）。

```

UserMapping *
GetUserMapping(Oid userid, Oid serverid);
```

此函式傳回給定角色在給定伺服器上之使用者對應的 `UserMapping` 物件。
（若該特定使用者沒有對應，它會傳回
`PUBLIC` 的對應；若連該對應也不存在，則擲出錯誤。）
`UserMapping` 物件包含該使用者對應的屬性
（詳情請參閱 `foreign/foreign.h`）。

```

ForeignTable *
GetForeignTable(Oid relid);
```

此函式傳回具有給定 OID 之外部資料表的 `ForeignTable` 物件。
`ForeignTable` 物件包含該外部資料表的屬性
（詳情請參閱 `foreign/foreign.h`）。

```

List *
GetForeignColumnOptions(Oid relid, AttrNumber attnum);
```

此函式傳回由給定外部資料表 OID 與屬性編號所指定之欄位的逐欄 FDW 選項，
形式為 `DefElem` 的串列。若該欄位沒有
選項，則傳回 NIL。

除了以 OID 為基礎的查詢函式之外，某些物件類型還有以名稱為基礎的查詢函式：

```

ForeignDataWrapper *
GetForeignDataWrapperByName(const char *name, bool missing_ok);
```

此函式傳回具有給定名稱之外部資料包裝器的 `ForeignDataWrapper`
物件。若找不到該包裝器，
則在 missing_ok 為 true 時傳回 NULL，否則擲出
錯誤。

```

ForeignServer *
GetForeignServerByName(const char *name, bool missing_ok);
```

此函式傳回具有給定名稱之外部伺服器的 `ForeignServer` 物件。
若找不到該伺服器，
則在 missing_ok 為 true 時傳回 NULL，否則擲出錯誤。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/fdw-helpers.html)（原文版本：18.6；核對日期：2026-10-17）
