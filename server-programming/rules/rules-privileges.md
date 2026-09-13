<a id="RULES-PRIVILEGES"></a>

## 39.5. 規則與權限 [#](#RULES-PRIVILEGES)

<a id="id-1.8.6.10.2"></a><a id="id-1.8.6.10.3"></a>

由於 PostgreSQL 規則系統會重寫查詢，因此原始查詢中沒有用到的其他資料表／檢視表也會被存取到。當使用更新規則時，這甚至可能包含對資料表的寫入存取。

重寫規則沒有獨立的擁有者。關聯（資料表或檢視表）的擁有者自動就是為它所定義之重寫規則的擁有者。PostgreSQL 規則系統改變了預設存取控制系統的行為。除了與 security invoker 檢視表相關的 `SELECT` 規則之外（參閱 [`CREATE VIEW`](../../reference/sql-commands/sql-createview.md)），所有因為規則而被使用到的關聯，都是依照規則擁有者的權限來檢查，而不是依照呼叫該規則的使用者。這表示除了 security invoker 檢視表之外，使用者只需要對自己查詢中明確指名的那些資料表／檢視表擁有必要的權限即可。

舉例來說：某位使用者有一份電話號碼清單，其中有些是私人的，其他的則是辦公室助理會需要用到的。這位使用者可以這樣建構：

```

CREATE TABLE phone_data (person text, phone text, private boolean);
CREATE VIEW phone_number AS
    SELECT person, CASE WHEN NOT private THEN phone END AS phone
    FROM phone_data;
GRANT SELECT ON phone_number TO assistant;
```

除了該使用者（以及資料庫超級使用者）以外，沒有人能夠存取 `phone_data` 資料表。但是因為有了 `GRANT`，助理可以對 `phone_number` 檢視表執行 `SELECT`。規則系統會把對 `phone_number` 的 `SELECT` 重寫成對 `phone_data` 的 `SELECT`。由於這位使用者是 `phone_number` 的擁有者，因此也是該規則的擁有者，所以對 `phone_data` 的讀取存取現在是依照這位使用者的權限來檢查，於是這個查詢被允許。存取 `phone_number` 的檢查同樣會執行，但這項檢查是針對呼叫的使用者進行，所以除了這位使用者和助理之外，沒有人能夠使用它。

權限是一條規則一條規則地檢查。所以目前助理是唯一能夠看到公開電話號碼的人。但是助理可以另外建立一個檢視表，並把存取權授予所有人。這麼一來，任何人都可以透過助理的檢視表看到 `phone_number` 的資料。助理辦不到的是建立一個直接存取 `phone_data` 的檢視表。（實際上助理可以建立，但它不會有作用，因為每一次存取都會在權限檢查時被拒絕。）而只要這位使用者一發現助理把他的 `phone_number` 檢視表公開出去，就可以撤銷助理的存取權。立刻地，任何對助理那個檢視表的存取都會失敗。

有人可能會認為這種逐條規則檢查的方式是個安全漏洞，但事實上並不是。因為如果不是這樣運作，助理大可以建立一個和 `phone_number` 有相同欄位的資料表，然後每天把資料複製過去一次。那樣一來資料就是助理自己的，助理想授權給誰都行。`GRANT` 指令的意思就是「我信任你」。如果你信任的人做了上述的事，那就該重新考慮一下，然後使用 `REVOKE`。

請注意，雖然檢視表可以用上面示範的技巧來隱藏特定欄位的內容，但除非設定了 `security_barrier` 旗標，否則它們無法可靠地隱藏未顯示資料列中的資料。例如，下面這個檢視表就是不安全的：

```

CREATE VIEW phone_number AS
    SELECT person, phone FROM phone_data WHERE phone NOT LIKE '412%';
```

這個檢視表看起來似乎很安全，因為規則系統會把任何對 `phone_number` 的 `SELECT` 重寫成對 `phone_data` 的 `SELECT`，並加上只取 `phone` 不是以 412 開頭之項目的限定條件。但如果使用者可以建立自己的函式，要說服規劃器在 `NOT LIKE` 運算式之前先執行這個使用者定義的函式並不困難。例如：

```

CREATE FUNCTION tricky(text, text) RETURNS bool AS $$
BEGIN
    RAISE NOTICE '% => %', $1, $2;
    RETURN true;
END;
$$ LANGUAGE plpgsql COST 0.0000000000000000000001;

SELECT * FROM phone_number WHERE tricky(person, phone);
```

`phone_data` 資料表中的每一個人與電話號碼都會以 `NOTICE` 的形式印出來，因為規劃器會選擇先執行成本低廉的 `tricky` 函式，再執行成本較高的 `NOT LIKE`。即使使用者被禁止定義新的函式，內建函式也可以用於類似的攻擊。（例如，大多數的型別轉換函式都會把輸入值包含在它們所產生的錯誤訊息中。）

類似的考量也適用於更新規則。在前一節的範例中，範例資料庫裡那些資料表的擁有者可以把 `shoelace` 檢視表的 `SELECT`、`INSERT`、`UPDATE` 與 `DELETE` 權限授予別人，但對 `shoelace_log` 只授予 `SELECT`。寫入日誌項目的規則動作仍然會成功執行，而那位使用者也能看到日誌項目。但是他們無法建立假的項目，也無法竄改或移除既有的項目。在這個案例中，不可能藉由說服規劃器改變操作順序來破壞規則，因為唯一參照到 `shoelace_log` 的規則是一個沒有限定條件的 `INSERT`。在更複雜的情境下，這一點可能就不成立了。

當檢視表有必要提供資料列層級的安全性時，應該為該檢視表套用 `security_barrier` 屬性。這可以防止在檢視表完成它的工作之前，就把資料列的值傳遞給惡意挑選的函式與運算子。例如，如果上面所示的檢視表是像這樣建立的，它就會是安全的：

```

CREATE VIEW phone_number WITH (security_barrier) AS
    SELECT person, phone FROM phone_data WHERE phone NOT LIKE '412%';
```

以 `security_barrier` 建立的檢視表，效能可能遠遠不如沒有使用這個選項所建立的檢視表。一般來說，這是無法避免的：如果最快的執行計畫可能危及安全性，就必須捨棄它。基於這個原因，這個選項預設並未啟用。

在處理沒有副作用的函式時，查詢規劃器有較大的彈性。這類函式被稱為 `LEAKPROOF`，其中包含許多簡單且常用的運算子，例如許多相等運算子。查詢規劃器可以安全地允許這類函式在查詢執行過程中的任何時間點被求值，因為把它們套用在使用者看不到的資料列上，並不會洩漏關於那些未顯示資料列的任何資訊。此外，不接受引數、或是不會從 security barrier 檢視表被傳入任何引數的函式，不需要被標記為 `LEAKPROOF` 也可以被下推，因為它們永遠不會收到來自檢視表的資料。相對地，可能會依據所收到的引數值而拋出錯誤的函式（例如在發生溢位或除以零時拋出錯誤的函式）就不是 leakproof 的，而且如果在安全檢視表的資料列篩選之前被套用，就可能提供關於未顯示資料列的重要資訊。

例如，對於 security barrier 檢視表（或具有資料列層級安全性原則的資料表）的查詢，如果 `WHERE` 子句中使用的某個運算子雖然屬於某個索引的運算子家族，但其底層函式並未標記為 `LEAKPROOF`，那麼就無法選用索引掃描。[psql](../../reference/reference-client/app-psql.md) 程式的 `\dAo+` 中介指令很適合用來列出運算子家族，並判斷其中哪些運算子被標記為 leakproof。

有一點很重要必須瞭解：即使是以 `security_barrier` 選項建立的檢視表，其安全性也僅限於一個有限的意義，也就是不可見 tuple（值組）的內容不會被傳遞給可能不安全的函式。使用者仍然很可能有其他方法可以推論出未顯示的資料；例如，他們可以使用 `EXPLAIN` 看到查詢計畫，或是測量針對該檢視表所做查詢的執行時間。惡意的攻擊者或許能夠推論出未顯示資料的數量，甚至取得一些關於資料分佈或最常見值的資訊（因為這些東西可能會影響執行計畫的執行時間；甚至由於它們也反映在最佳化器的統計資訊中，還會影響執行計畫的選擇）。如果你在意這類「隱蔽通道」（covert channel）攻擊，那麼最好完全不要授予任何存取這些資料的權限。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/rules-privileges.html)（原文版本：18.6；核對日期：2026-09-12）
