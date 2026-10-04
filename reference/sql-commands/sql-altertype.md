<a id="SQL-ALTERTYPE"></a><a id="id-1.9.3.42.1"></a>

## ALTER TYPE

ALTER TYPE — 變更型別的定義

<a id="id-1.9.3.42.4"></a>

## 語法

```

ALTER TYPE name OWNER TO { new_owner | CURRENT_ROLE | CURRENT_USER | SESSION_USER }
ALTER TYPE name RENAME TO new_name
ALTER TYPE name SET SCHEMA new_schema
ALTER TYPE name RENAME ATTRIBUTE attribute_name TO new_attribute_name [ CASCADE | RESTRICT ]
ALTER TYPE name action [, ... ]
ALTER TYPE name ADD VALUE [ IF NOT EXISTS ] new_enum_value [ { BEFORE | AFTER } neighbor_enum_value ]
ALTER TYPE name RENAME VALUE existing_enum_value TO new_enum_value
ALTER TYPE name SET ( property = value [, ... ] )

where action is one of:

    ADD ATTRIBUTE attribute_name data_type [ COLLATE collation ] [ CASCADE | RESTRICT ]
    DROP ATTRIBUTE [ IF EXISTS ] attribute_name [ CASCADE | RESTRICT ]
    ALTER ATTRIBUTE attribute_name [ SET DATA ] TYPE data_type [ COLLATE collation ] [ CASCADE | RESTRICT ]
```

<a id="id-1.9.3.42.5"></a>

## 說明

`ALTER TYPE` 會變更現有型別的定義。它有以下幾種子形式：

`OWNER`
:   此形式會變更型別的擁有者。

`RENAME`
:   此形式會變更型別的名稱。

`SET SCHEMA`
:   此形式會將型別移到另一個綱要。

`RENAME ATTRIBUTE`
:   此形式只能用於複合型別。它會變更型別中個別屬性的名稱。

`ADD ATTRIBUTE`
:   此形式會在複合型別中新增屬性，使用的語法與 [`CREATE TYPE`](sql-createtype.md) 相同。

`DROP ATTRIBUTE [ IF EXISTS ]`
:   此形式會從複合型別中移除屬性。若指定了 `IF EXISTS` 而該屬性不存在，則不擲出錯誤；此情況改為發出 notice。

`ALTER ATTRIBUTE ... SET DATA TYPE`
:   此形式會變更複合型別中某個屬性的型別。

`ADD VALUE [ IF NOT EXISTS ] [ BEFORE | AFTER ]`
:   此形式會在列舉型別中新增值。新值在列舉排序中的位置，可以指定為位於某個現有值的 `BEFORE`（之前）或 `AFTER`（之後）。否則，新項目會加在值清單的末端。

    若指定了 `IF NOT EXISTS`，則型別已包含新值時不視為錯誤：會發出 notice，但不採取其他動作。否則，若新值已存在，就會發生錯誤。

`RENAME VALUE`
:   此形式會重新命名列舉型別的某個值。該值在列舉排序中的位置不受影響。若指定的值不存在，或新名稱已存在，就會發生錯誤。

`SET ( property = value [, ... ] )`
:   此形式只適用於基本型別。它允許調整可在 `CREATE
    TYPE` 中設定之基本型別屬性的一部分。具體而言，可以變更下列屬性：

    * `RECEIVE` 可以設定為二進位輸入函式的名稱，或設定為 `NONE` 以移除型別的二進位輸入函式。使用此選項需要超級使用者權限。
    * `SEND` 可以設定為二進位輸出函式的名稱，或設定為 `NONE` 以移除型別的二進位輸出函式。使用此選項需要超級使用者權限。
    * `TYPMOD_IN` 可以設定為型別修飾詞輸入函式的名稱，或設定為 `NONE` 以移除型別的型別修飾詞輸入函式。使用此選項需要超級使用者權限。
    * `TYPMOD_OUT` 可以設定為型別修飾詞輸出函式的名稱，或設定為 `NONE` 以移除型別的型別修飾詞輸出函式。使用此選項需要超級使用者權限。
    * `ANALYZE` 可以設定為型別專屬之統計資料收集函式的名稱，或設定為 `NONE` 以移除型別的統計資料收集函式。使用此選項需要超級使用者權限。
    * `SUBSCRIPT` 可以設定為型別專屬之下標處理函式的名稱，或設定為 `NONE` 以移除型別的下標處理函式。使用此選項需要超級使用者權限。
    * `STORAGE`<a id="id-1.9.3.42.5.2.2.10.2.1.2.7.1.2"></a>
      可以設定為 `plain`、`extended`、`external` 或 `main`（這些設定的意義請參閱[第 66.2 節](../../internals/storage/storage-toast.md)）。不過，從 `plain` 變更為其他設定需要超級使用者權限（因為這要求該型別的 C 函式全都支援 TOAST），而從其他設定變更為 `plain` 則完全不允許（因為資料庫中可能已經存在該型別經過 TOAST 處理的值）。請注意，變更此選項本身並不會變更任何已儲存的資料，它只是設定未來建立之資料表欄位所使用的預設 TOAST 策略。要變更現有資料表欄位的 TOAST 策略，請參閱 [ALTER TABLE](sql-altertable.md)。

    關於這些型別屬性的更多細節，請參閱 [CREATE TYPE](sql-createtype.md)。請注意，在適當的情況下，基本型別上這些屬性的變更會自動傳播到以該型別為基礎的網域。

`ADD ATTRIBUTE`、`DROP
ATTRIBUTE` 與 `ALTER ATTRIBUTE` 動作可以組合成一份包含多項變更的清單，一併套用。例如，可以在單一命令中新增數個屬性，以及（或）變更數個屬性的型別。

你必須擁有該型別才能使用 `ALTER TYPE`。若要變更型別的綱要，你還必須在新綱要上具有 `CREATE` 權限。若要變更擁有者，你必須能夠 `SET ROLE` 成為新的擁有者角色，且該角色必須在型別所屬的綱要上具有 `CREATE` 權限。（這些限制確保變更擁有者不會做到任何你無法藉由移除並重新建立該型別而做到的事。不過，超級使用者無論如何都可以變更任何型別的擁有權。）若要新增屬性或變更屬性的型別，你還必須在該屬性的資料型別上具有 `USAGE` 權限。

<a id="id-1.9.3.42.6"></a>

## 參數

*`name`*
:   要變更之現有型別的名稱（可能以綱要限定）。

*`new_name`*
:   型別的新名稱。

*`new_owner`*
:   型別之新擁有者的使用者名稱。

*`new_schema`*
:   型別的新綱要。

*`attribute_name`*
:   要新增、變更或移除之屬性的名稱。

*`new_attribute_name`*
:   要重新命名之屬性的新名稱。

*`data_type`*
:   要新增之屬性的資料型別，或要變更之屬性的新型別。

*`new_enum_value`*
:   要加入列舉型別之值清單的新值，或要賦予現有值的新名稱。如同所有列舉常值，它需要加上引號。

*`neighbor_enum_value`*
:   一個現有的列舉值；在列舉型別的排序中，新值應該緊接著加在它之前或之後。如同所有列舉常值，它需要加上引號。

*`existing_enum_value`*
:   應該重新命名的現有列舉值。如同所有列舉常值，它需要加上引號。

*`property`*
:   要修改之基本型別屬性的名稱；可能的值請參閱上文。

`CASCADE`
:   自動將此操作傳播到以所變更之型別為型別的型別化資料表（typed table）及其後代。

`RESTRICT`
:   若所變更的型別是某個型別化資料表的型別，則拒絕此操作。這是預設行為。

<a id="id-1.9.3.42.7"></a>

## 注意事項

若在交易區塊內執行 `ALTER TYPE ... ADD VALUE`（在列舉型別中新增值的形式），則必須等到交易提交之後，才能使用新值。

涉及新增之列舉值的比較，有時會比只涉及列舉型別原有成員的比較更慢。通常只有在使用 `BEFORE` 或 `AFTER` 將新值的排序位置設在清單末端以外的某處時，才會發生這種情況。不過，有時即使新值加在末端也會發生這種情況（若 OID 計數器自列舉型別最初建立以來已經「繞回」，就會發生）。這種變慢通常微不足道；但若有影響，可以藉由移除並重新建立該列舉型別，或藉由傾印並還原資料庫，來恢復最佳效能。

<a id="id-1.9.3.42.8"></a>

## 範例

重新命名資料型別：

```

ALTER TYPE electronic_mail RENAME TO email;
```

將型別 `email` 的擁有者變更為 `joe`：

```

ALTER TYPE email OWNER TO joe;
```

將型別 `email` 的綱要變更為 `customers`：

```

ALTER TYPE email SET SCHEMA customers;
```

在複合型別中新增屬性：

```

ALTER TYPE compfoo ADD ATTRIBUTE f3 int;
```

在列舉型別的特定排序位置新增值：

```

ALTER TYPE colors ADD VALUE 'orange' AFTER 'red';
```

重新命名列舉值：

```

ALTER TYPE colors RENAME VALUE 'purple' TO 'mauve';
```

為現有的基本型別建立二進位 I/O 函式：

```

CREATE FUNCTION mytypesend(mytype) RETURNS bytea ...;
CREATE FUNCTION mytyperecv(internal, oid, integer) RETURNS mytype ...;
ALTER TYPE mytype SET (
    SEND = mytypesend,
    RECEIVE = mytyperecv
);
```

<a id="id-1.9.3.42.9"></a>

## 相容性

新增與移除屬性的形式是 SQL 標準的一部分；其他形式則是 PostgreSQL 的擴充語法。

<a id="SQL-ALTERTYPE-SEE-ALSO"></a>

## 另請參閱

[CREATE TYPE](sql-createtype.md), [DROP TYPE](sql-droptype.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-altertype.html)（原文版本：18.6；核對日期：2026-10-04）
