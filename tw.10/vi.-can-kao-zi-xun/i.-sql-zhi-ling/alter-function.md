# ALTER FUNCTION

ALTER FUNCTION — 變更一個函數的定義

### 語法

```text
ALTER FUNCTION name [ ( [ [ argmode ] [ argname ] argtype [, ...] ] ) ]
    action [ ... ] [ RESTRICT ]
ALTER FUNCTION name [ ( [ [ argmode ] [ argname ] argtype [, ...] ] ) ]
    RENAME TO new_name
ALTER FUNCTION name [ ( [ [ argmode ] [ argname ] argtype [, ...] ] ) ]
    OWNER TO { new_owner | CURRENT_USER | SESSION_USER }
ALTER FUNCTION name [ ( [ [ argmode ] [ argname ] argtype [, ...] ] ) ]
    SET SCHEMA new_schema
ALTER FUNCTION name [ ( [ [ argmode ] [ argname ] argtype [, ...] ] ) ]
    DEPENDS ON EXTENSION extension_name

where action is one of:

    CALLED ON NULL INPUT | RETURNS NULL ON NULL INPUT | STRICT
    IMMUTABLE | STABLE | VOLATILE | [ NOT ] LEAKPROOF
    [ EXTERNAL ] SECURITY INVOKER | [ EXTERNAL ] SECURITY DEFINER
    PARALLEL { UNSAFE | RESTRICTED | SAFE }
    COST execution_cost
    ROWS result_rows
    SET configuration_parameter { TO | = } { value | DEFAULT }
    SET configuration_parameter FROM CURRENT
    RESET configuration_parameter
    RESET ALL
```

### 說明

`ALTER FUNCTION` 變更一個函數的定義。

您必須是函數擁有者才能使用 ALTER FUNCTION 功能。要變更函數的綱要，您還必須具有新綱要的 CREATE 權限。要變更擁有者，您還必須是新擁有角色的直接或間接成員，並且該角色必須對該函數的綱要具有 CREATE 權限。（這些限制強制改變擁有者不會做任何透過刪除和重新建立函數都無法做到的事情，但是超級用戶可以改變任何函數的所有權。）

### 參數

_`name`_

現有函數的名稱（可以加上綱要）。如果未指定參數列表，則該名稱在其綱要中必須是唯一的。

_`argmode`_

參數的模式：IN，OUT，INOUT 或 VARIADIC。如果省略，則預設為 IN。請注意，ALTER FUNCTION 實際上並不關心 OUT 參數，因為只需要輸入參數來確定函數的身份。所以列出 IN，INOUT 和 VARIADIC 參數就足夠了。

_`argname`_

參數的名稱。請注意，ALTER FUNCTION 實際上並不關心參數名稱，因為只需要參數資料型別來確定函數的身份。

_`argtype`_

如果有的話，函數參數的資料型別（可選用綱要修飾）。

_`new_name`_

函數的新名稱。

_`new_owner`_

函數的新擁有者。請注意，如果該函數被標記為 SECURITY DEFINER，隨後它將以新的擁有者執行。

_`new_schema`_

函數的新綱要。

_`extension_name`_

函數相依的延伸套件。

`CALLED ON NULL INPUT`  
`RETURNS NULL ON NULL INPUT`  
`STRICT`

CALLED ON NULL INPUT 變更此函數，以便在其某些或全部參數為空時呼叫此函數。回傳 NULL ON NULL INPUT 或 STRICT 變更該函數，以便在其任何參數為 null 時不呼叫此函數；相反地，則會自動假設空的結果。有關更多訊息，請參閱 [CREATE FUNCTION](create-function.md)。

`IMMUTABLE`  
`STABLE`  
`VOLATILE`

將函數的易變性變更為指定的設定。詳情請參閱 [CREATE FUNCTION](create-function.md)。

`[ EXTERNAL ] SECURITY INVOKER`  
`[ EXTERNAL ] SECURITY DEFINER`

變更該函數是否是安全性定義者。考慮到 SQL 標準的一致性，關鍵字 EXTERNAL 會被忽略。有關此功能的更多訊息，請參閱 [CREATE FUNCTION](create-function.md)。

`PARALLEL`

改變函數是否被認為是可以安全地平行運算。 詳情請參閱 [CREATE FUNCTION](create-function.md)。

`LEAKPROOF`

變更函數是否被認為是 leakproof。有關此功能的更多訊息，請參閱 [CREATE FUNCTION](create-function.md)。

`COST` _`execution_cost`_

變更函數估計的執行成本。有關更多訊息，請參閱 [CREATE FUNCTION](create-function.md)。

`ROWS` _`result_rows`_

變更由 set-returning 函數回傳的估計資料列數。有關更多訊息，請參閱 [CREATE FUNCTION](create-function.md)。

_`configuration_parameter`_  
_`value`_

呼叫函數時，增加或變更要對配置參數進行的指定方式。 如果值為 DEFAULT，或者等價地使用 RESET，那麼函數本地配置將被刪除，以便該函數執行其環境中存在的值。使用 RESET ALL 清除所有功能本地配置。SET FROM CURRENT 將執行 ALTER FUNCTION 時當下參數的值保存為輸入函數時所要應用的值。

有關允許的參數名稱和值相關更多訊息，請參閱 [SET](set.md) 和[第 19 章](../../iii.-xi-tong-guan-li/19.-fu-wu-zu-tai-she-ding/)。

`RESTRICT`

此語法會被忽略，它只為了符合 SQL 標準。

### 範例

要將 integer 型別的函數 sqrt 重新命名為 square\_root：

```text
ALTER FUNCTION sqrt(integer) RENAME TO square_root;
```

要將整數型別函數 sqrt 的擁有者變更為 joe，請執行以下操作：

```text
ALTER FUNCTION sqrt(integer) OWNER TO joe;
```

要將整數型別函數 sqrt 的綱要變更為 maths，請執行以下操作：

```text
ALTER FUNCTION sqrt(integer) SET SCHEMA maths;
```

要將 integer 型別的函數標記為相依於延伸套件 mathlib：

```text
ALTER FUNCTION sqrt(integer) DEPENDS ON EXTENSION mathlib;
```

自動以該函數調整搜尋路徑：

```text
ALTER FUNCTION check_password(text) SET search_path = admin, pg_temp;
```

要停用某個函數的 search\_path 自動設定，請執行以下操作：

```text
ALTER FUNCTION check_password(text) RESET search_path;
```

該函數現在將執行其呼叫者使用的任何搜尋路徑。

### 相容性

此語法與 SQL 標準中的 ALTER FUNCTION 語法部分相容。標準可以允許修改一個函數的更多屬性，但不能提供重新命名函數、使函數成為 security definer、將配置參數值附加到函數或變更函數的擁有者、綱要或易變性的設定。標準還需要 RESTRICT 關鍵字，這在 PostgreSQL 中是選用的。

### 參閱

[CREATE FUNCTION](create-function.md), [DROP FUNCTION](drop-function.md)

