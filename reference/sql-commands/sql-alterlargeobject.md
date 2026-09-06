<a id="id-1.9.3.18.1"></a>

## ALTER LARGE OBJECT

ALTER LARGE OBJECT — 變更大型物件的定義

## 語法

```

ALTER LARGE OBJECT large_object_oid OWNER TO { new_owner | CURRENT_ROLE | CURRENT_USER | SESSION_USER }
```

<a id="id-1.9.3.18.5"></a>

## 說明

`ALTER LARGE OBJECT` 會變更大型物件的定義。

你必須擁有該大型物件，才能使用 `ALTER LARGE OBJECT`。若要變更擁有者，還必須能以 `SET ROLE` 切換至新的擁有者角色。（不過，超級使用者可以變更任何大型物件。）目前唯一的功能是指定新擁有者，因此這兩項限制一律適用。

<a id="id-1.9.3.18.6"></a>

## 參數

*`large_object_oid`*
:   要變更的大型物件 OID

*`new_owner`*
:   大型物件的新擁有者

<a id="id-1.9.3.18.7"></a>

## 相容性

SQL 標準中沒有 `ALTER LARGE OBJECT` 陳述式。

<a id="id-1.9.3.18.8"></a>

## 另請參閱

[第 33 章](../../client-interfaces/largeobjects/README.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-alterlargeobject.html)（原文版本：18.6；核對日期：2026-09-07）
