<a id="DDL-ROWSECURITY"></a>

## 5.9. 資料列安全政策 [#](#DDL-ROWSECURITY)

<a id="id-1.5.4.11.2"></a><a id="id-1.5.4.11.3"></a>

除了透過 [GRANT](../../reference/sql-commands/sql-grant.md) 使用的 SQL 標準[權限系統](ddl-priv.md)之外，資料表還可以有*資料列安全政策*（row security policy），以每個使用者為單位，限制哪些資料列可以被一般查詢回傳，或被資料修改命令插入、更新或刪除。這項功能也稱為*資料列層級安全性*（Row-Level Security）。預設情況下，資料表沒有任何政策，因此只要使用者依照 SQL 權限系統擁有某個資料表的存取權限，該資料表中的所有資料列就同樣可以被查詢或更新。

當資料表啟用了資料列安全性（使用 [ALTER TABLE ... ENABLE ROW LEVEL SECURITY](../../reference/sql-commands/sql-altertable.md)）時，所有為了選取或修改資料列而對該資料表進行的一般存取，都必須受到資料列安全政策的允許。（不過，資料表的擁有者通常不受資料列安全政策的約束。）如果該資料表沒有任何政策，就會使用預設拒絕政策，也就是沒有任何資料列可見或可被修改。適用於整個資料表的操作，例如 `TRUNCATE` 與 `REFERENCES`，不受資料列安全性的約束。

資料列安全政策可以針對特定命令、特定角色，或兩者兼具。政策可以指定為套用到 `ALL` 命令，或套用到 `SELECT`、`INSERT`、`UPDATE` 或 `DELETE`。一個政策可以指派給多個角色，並適用一般的角色成員資格與繼承規則。

要依據政策指定哪些資料列可見或可修改，需要一個回傳布林結果的運算式。這個運算式會在來自使用者查詢的任何條件或函式之前，針對每一筆資料列進行評估。（這項規則唯一的例外是 `leakproof` 函式，它們保證不會洩漏資訊；最佳化器可能會選擇在資料列安全性檢查之前套用這類函式。）運算式沒有回傳 `true` 的資料列不會被處理。可以指定不同的運算式，分別獨立控制哪些資料列可見、哪些資料列允許被修改。政策運算式會作為查詢的一部分，以執行該查詢之使用者的權限執行，不過可以使用安全性定義者（security definer）函式來存取呼叫者無法取得的資料。

超級使用者以及具有 `BYPASSRLS` 屬性的角色，在存取資料表時一律會略過資料列安全系統。資料表擁有者通常也會略過資料列安全性，不過資料表擁有者可以使用 [ALTER TABLE ... FORCE ROW LEVEL SECURITY](../../reference/sql-commands/sql-altertable.md) 選擇讓自己受資料列安全性約束。

啟用與停用資料列安全性，以及為資料表加入政策，一律只有資料表擁有者才有權限進行。

政策使用 [CREATE POLICY](../../reference/sql-commands/sql-createpolicy.md) 命令建立，使用 [ALTER POLICY](../../reference/sql-commands/sql-alterpolicy.md) 命令修改，並使用 [DROP POLICY](../../reference/sql-commands/sql-droppolicy.md) 命令刪除。要為特定資料表啟用或停用資料列安全性，請使用 [ALTER TABLE](../../reference/sql-commands/sql-altertable.md) 命令。

每個政策都有一個名稱，而一個資料表可以定義多個政策。由於政策是針對特定資料表的，同一個資料表的每個政策都必須有唯一的名稱。不同的資料表可以有同名的政策。

當多個政策適用於同一個查詢時，它們會以 `OR`（用於寬鬆政策，這是預設值）或以 `AND`（用於限制性政策）組合起來。`OR` 的行為類似於「一個角色擁有其所屬之所有角色的權限」這項規則。寬鬆政策與限制性政策的差別會在下面進一步討論。

舉一個簡單的例子，以下說明如何在 `account` 關聯上建立一個政策，只允許 `managers` 角色的成員存取資料列，而且只能存取他們自己帳戶的資料列：

```

CREATE TABLE accounts (manager text, company text, contact_email text);

ALTER TABLE accounts ENABLE ROW LEVEL SECURITY;

CREATE POLICY account_managers ON accounts TO managers
    USING (manager = current_user);
```

上面的政策隱含地提供了一個與其 `USING` 子句相同的 `WITH CHECK` 子句，因此這項限制同時適用於命令所選取的資料列（因此經理無法對屬於其他經理的現有資料列進行 `SELECT`、`UPDATE` 或 `DELETE`），也適用於命令所修改的資料列（因此無法透過 `INSERT` 或 `UPDATE` 建立屬於其他經理的資料列）。

如果沒有指定角色，或使用了特殊的使用者名稱 `PUBLIC`，那麼政策會套用到系統上的所有使用者。要讓所有使用者只能存取 `users` 資料表中他們自己的資料列，可以使用一個簡單的政策：

```

CREATE POLICY user_policy ON users
    USING (user_name = current_user);
```

這與前一個範例的運作方式類似。

若要讓加入資料表的資料列與可見的資料列使用不同的政策，可以組合多個政策。下面這一對政策會允許所有使用者查看 `users` 資料表中的所有資料列，但只能修改他們自己的資料列：

```

CREATE POLICY user_sel_policy ON users
    FOR SELECT
    USING (true);
CREATE POLICY user_mod_policy ON users
    USING (user_name = current_user);
```

在 `SELECT` 命令中，這兩個政策會以 `OR` 組合，最終的效果是所有資料列都可以被選取。在其他類型的命令中，只有第二個政策適用，因此效果與先前相同。

也可以使用 `ALTER TABLE` 命令停用資料列安全性。停用資料列安全性並不會移除資料表上定義的任何政策；它們只是被忽略而已。此時，資料表中的所有資料列都可見且可修改，只受標準 SQL 權限系統的約束。

下面是一個較大的範例，說明如何在正式環境中使用這項功能。資料表 `passwd` 模擬 Unix 的密碼檔：

```

-- Simple passwd-file based example
CREATE TABLE passwd (
  user_name             text UNIQUE NOT NULL,
  pwhash                text,
  uid                   int  PRIMARY KEY,
  gid                   int  NOT NULL,
  real_name             text NOT NULL,
  home_phone            text,
  extra_info            text,
  home_dir              text NOT NULL,
  shell                 text NOT NULL
);

CREATE ROLE admin;  -- Administrator
CREATE ROLE bob;    -- Normal user
CREATE ROLE alice;  -- Normal user

-- Populate the table
INSERT INTO passwd VALUES
  ('admin','xxx',0,0,'Admin','111-222-3333',null,'/root','/bin/dash');
INSERT INTO passwd VALUES
  ('bob','xxx',1,1,'Bob','123-456-7890',null,'/home/bob','/bin/zsh');
INSERT INTO passwd VALUES
  ('alice','xxx',2,1,'Alice','098-765-4321',null,'/home/alice','/bin/zsh');

-- Be sure to enable row-level security on the table
ALTER TABLE passwd ENABLE ROW LEVEL SECURITY;

-- Create policies
-- Administrator can see all rows and add any rows
CREATE POLICY admin_all ON passwd TO admin USING (true) WITH CHECK (true);
-- Normal users can view all rows
CREATE POLICY all_view ON passwd FOR SELECT USING (true);
-- Normal users can update their own records, but
-- limit which shells a normal user is allowed to set
CREATE POLICY user_mod ON passwd FOR UPDATE
  USING (current_user = user_name)
  WITH CHECK (
    current_user = user_name AND
    shell IN ('/bin/bash','/bin/sh','/bin/dash','/bin/zsh','/bin/tcsh')
  );

-- Allow admin all normal rights
GRANT SELECT, INSERT, UPDATE, DELETE ON passwd TO admin;
-- Users only get select access on public columns
GRANT SELECT
  (user_name, uid, gid, real_name, home_phone, extra_info, home_dir, shell)
  ON passwd TO public;
-- Allow users to update certain columns
GRANT UPDATE
  (pwhash, real_name, home_phone, extra_info, shell)
  ON passwd TO public;
```

與任何安全性設定一樣，測試並確保系統的行為符合預期是很重要的。使用上面的範例，下面展示了權限系統正常運作的情形。

```

-- admin can view all rows and fields
postgres=> set role admin;
SET
postgres=> table passwd;
 user_name | pwhash | uid | gid | real_name |  home_phone  | extra_info | home_dir    |   shell
-----------+--------+-----+-----+-----------+--------------+------------+-------------+-----------
 admin     | xxx    |   0 |   0 | Admin     | 111-222-3333 |            | /root       | /bin/dash
 bob       | xxx    |   1 |   1 | Bob       | 123-456-7890 |            | /home/bob   | /bin/zsh
 alice     | xxx    |   2 |   1 | Alice     | 098-765-4321 |            | /home/alice | /bin/zsh
(3 rows)

-- Test what Alice is able to do
postgres=> set role alice;
SET
postgres=> table passwd;
ERROR:  permission denied for table passwd
postgres=> select user_name,real_name,home_phone,extra_info,home_dir,shell from passwd;
 user_name | real_name |  home_phone  | extra_info | home_dir    |   shell
-----------+-----------+--------------+------------+-------------+-----------
 admin     | Admin     | 111-222-3333 |            | /root       | /bin/dash
 bob       | Bob       | 123-456-7890 |            | /home/bob   | /bin/zsh
 alice     | Alice     | 098-765-4321 |            | /home/alice | /bin/zsh
(3 rows)

postgres=> update passwd set user_name = 'joe';
ERROR:  permission denied for table passwd
-- Alice is allowed to change her own real_name, but no others
postgres=> update passwd set real_name = 'Alice Doe';
UPDATE 1
postgres=> update passwd set real_name = 'John Doe' where user_name = 'admin';
UPDATE 0
postgres=> update passwd set shell = '/bin/xx';
ERROR:  new row violates WITH CHECK OPTION for "passwd"
postgres=> delete from passwd;
ERROR:  permission denied for table passwd
postgres=> insert into passwd (user_name) values ('xxx');
ERROR:  permission denied for table passwd
-- Alice can change her own password; RLS silently prevents updating other rows
postgres=> update passwd set pwhash = 'abc';
UPDATE 1
```

到目前為止建立的所有政策都是寬鬆政策，也就是說，套用多個政策時，它們會以「OR」布林運算子組合。雖然可以建構寬鬆政策，只在預期的情況下允許存取資料列，但將寬鬆政策與限制性政策（資料列必須通過，且以「AND」布林運算子組合的政策）結合使用，可能會比較簡單。在上面的範例基礎上，我們加入一個限制性政策，要求管理員必須透過本機 Unix 通訊端連線，才能存取 `passwd` 資料表的記錄：

```

CREATE POLICY admin_local_only ON passwd AS RESTRICTIVE TO admin
    USING (pg_catalog.inet_client_addr() IS NULL);
```

接著我們可以看到，由於這個限制性政策，透過網路連線的管理員將看不到任何記錄：

```

=> SELECT current_user;
 current_user
--------------
 admin
(1 row)

=> select inet_client_addr();
 inet_client_addr
------------------
 127.0.0.1
(1 row)

=> TABLE passwd;
 user_name | pwhash | uid | gid | real_name | home_phone | extra_info | home_dir | shell
-----------+--------+-----+-----+-----------+------------+------------+----------+-------
(0 rows)

=> UPDATE passwd set pwhash = NULL;
UPDATE 0
```

參照完整性檢查，例如唯一或主鍵限制條件以及外鍵參照，一律會略過資料列安全性，以確保資料完整性得以維持。在開發綱要與資料列層級政策時必須小心，避免資訊透過這類參照完整性檢查以「隱蔽通道」（covert channel）的方式洩漏。

在某些情境下，確認沒有套用資料列安全性是很重要的。例如，在進行備份時，如果資料列安全性默默地導致某些資料列被排除在備份之外，後果可能不堪設想。在這種情況下，你可以將 [row_security](../../server-administration/runtime-config/runtime-config-client.md#GUC-ROW-SECURITY) 組態參數設為 `off`。這本身並不會略過資料列安全性；它的作用是，如果任何查詢的結果會被政策過濾，就引發錯誤。接著就可以調查並修正錯誤的原因。

在上面的範例中，政策運算式只考量要存取或更新之資料列中的目前值。這是最簡單、效能也最好的情況；可能的話，最好將資料列安全性應用設計成以這種方式運作。如果需要查閱其他資料列或其他資料表才能做出政策決定，可以在政策運算式中使用子 `SELECT`，或包含 `SELECT` 的函式來達成。不過請注意，這樣的存取可能會產生競爭條件，如果不小心，就可能導致資訊洩漏。舉例來說，考慮下面的資料表設計：

```

-- definition of privilege groups
CREATE TABLE groups (group_id int PRIMARY KEY,
                     group_name text NOT NULL);

INSERT INTO groups VALUES
  (1, 'low'),
  (2, 'medium'),
  (5, 'high');

GRANT ALL ON groups TO alice;  -- alice is the administrator
GRANT SELECT ON groups TO public;

-- definition of users' privilege levels
CREATE TABLE users (user_name text PRIMARY KEY,
                    group_id int NOT NULL REFERENCES groups);

INSERT INTO users VALUES
  ('alice', 5),
  ('bob', 2),
  ('mallory', 2);

GRANT ALL ON users TO alice;
GRANT SELECT ON users TO public;

-- table holding the information to be protected
CREATE TABLE information (info text,
                          group_id int NOT NULL REFERENCES groups);

INSERT INTO information VALUES
  ('barely secret', 1),
  ('slightly secret', 2),
  ('very secret', 5);

ALTER TABLE information ENABLE ROW LEVEL SECURITY;

-- a row should be visible to/updatable by users whose security group_id is
-- greater than or equal to the row's group_id
CREATE POLICY fp_s ON information FOR SELECT
  USING (group_id <= (SELECT group_id FROM users WHERE user_name = current_user));
CREATE POLICY fp_u ON information FOR UPDATE
  USING (group_id <= (SELECT group_id FROM users WHERE user_name = current_user));

-- we rely only on RLS to protect the information table
GRANT ALL ON information TO public;
```

現在假設 `alice` 想要變更「slightly secret」的資訊，但她決定不應該讓 `mallory` 看到該資料列的新內容，因此她執行：

```

BEGIN;
UPDATE users SET group_id = 1 WHERE user_name = 'mallory';
UPDATE information SET info = 'secret from mallory' WHERE group_id = 2;
COMMIT;
```

這看起來很安全；不存在任何 `mallory` 應該能看到「secret from mallory」字串的時間窗口。然而，這裡有一個競爭條件。如果 `mallory` 同時在執行，比方說，

```

SELECT * FROM information WHERE group_id = 2 FOR UPDATE;
```

而她的交易處於 `READ COMMITTED` 模式，那麼她就有可能看到「secret from mallory」。當她的交易在 `alice` 的交易之後才剛好到達 `information` 資料列時，就會發生這種情況。它會阻擋並等待 `alice` 的交易提交，然後由於 `FOR UPDATE` 子句的關係，擷取更新後的資料列內容。然而，它*不會*為對 `users` 的隱含 `SELECT` 擷取更新後的資料列，因為那個子 `SELECT` 沒有 `FOR UPDATE`；取而代之的是，`users` 資料列是以查詢開始時所取得的快照讀取的。因此，政策運算式檢驗的是 `mallory` 權限等級的舊值，於是允許她看到更新後的資料列。

有好幾種方法可以解決這個問題。一個簡單的答案是在資料列安全政策的子 `SELECT` 中使用 `SELECT ... FOR SHARE`。不過，這需要將被參照資料表（這裡是 `users`）的 `UPDATE` 權限授予受影響的使用者，而這可能並不理想。（但可以再套用另一個資料列安全政策，防止他們實際行使該權限；或者可以將子 `SELECT` 嵌入安全性定義者函式中。）此外，在被參照的資料表上大量並行使用資料列共享鎖定，可能會造成效能問題，特別是當它經常被更新時。另一種解決方法，在被參照資料表很少更新時很實用，就是在更新它時對它取得 `ACCESS EXCLUSIVE` 鎖定，使得沒有任何並行交易會檢視到舊的資料列值。或者，也可以在提交被參照資料表的更新之後、做出依賴新安全狀態的變更之前，等待所有並行交易結束。

更多細節請參閱 [CREATE POLICY](../../reference/sql-commands/sql-createpolicy.md) 與 [ALTER TABLE](../../reference/sql-commands/sql-altertable.md)。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ddl-rowsecurity.html)（原文版本：18.6；核對日期：2026-09-13）
