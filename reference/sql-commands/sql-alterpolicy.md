<a id="SQL-ALTERPOLICY"></a><a id="id-1.9.3.23.1"></a>

## ALTER POLICY

ALTER POLICY — 變更資料列層級安全性政策的定義

<a id="id-1.9.3.23.4"></a>

## 語法

```

ALTER POLICY name ON table_name RENAME TO new_name

ALTER POLICY name ON table_name
    [ TO { role_name | PUBLIC | CURRENT_ROLE | CURRENT_USER | SESSION_USER } [, ...] ]
    [ USING ( using_expression ) ]
    [ WITH CHECK ( check_expression ) ]
```

<a id="id-1.9.3.23.5"></a>

## 說明

`ALTER POLICY` 會變更現有資料列層級安全性政策的定義。請注意，`ALTER POLICY` 只允許修改政策所套用的角色集合，以及 `USING` 與 `WITH CHECK` 運算式。若要變更政策的其他屬性，例如政策所套用的命令，或政策是寬鬆政策還是限制性政策，則必須先移除該政策再重新建立。

要使用 `ALTER POLICY`，你必須是該政策所套用之資料表的擁有者。

在 `ALTER POLICY` 的第二種形式中，若有指定角色清單、*`using_expression`* 與 *`check_expression`*，會各自獨立地被取代。省略其中某個子句時，政策中對應的部分維持不變。

<a id="id-1.9.3.23.6"></a>

## 參數

*`name`*
:   要修改的現有政策名稱。

*`table_name`*
:   政策所在之資料表的名稱（可選擇以綱要限定）。

*`new_name`*
:   政策的新名稱。

*`role_name`*
:   政策所套用的角色。可以一次指定多個角色。若要將政策套用於所有角色，請使用 `PUBLIC`。

*`using_expression`*
:   政策的 `USING` 運算式。詳情請參閱 [CREATE POLICY](sql-createpolicy.md)。

*`check_expression`*
:   政策的 `WITH CHECK` 運算式。詳情請參閱 [CREATE POLICY](sql-createpolicy.md)。

<a id="id-1.9.3.23.7"></a>

## 相容性

`ALTER POLICY` 是 PostgreSQL 的擴充語法。

<a id="id-1.9.3.23.8"></a>

## 另請參閱

[CREATE POLICY](sql-createpolicy.md), [DROP POLICY](sql-droppolicy.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-alterpolicy.html)（原文版本：18.6；核對日期：2026-10-05）
