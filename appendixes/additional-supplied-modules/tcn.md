<a id="TCN"></a>

# F.44. tcn

<a id="id-1.11.7.53.2"></a><a id="id-1.11.7.53.3"></a>

`tcn` 模組提供一個觸發程序函式，用於通知接聽者其所附加的任何資料表發生變更。它必須作為 `AFTER` 觸發程序並使用 `FOR EACH ROW`。

此模組被視為「受信任」，也就是說，對目前資料庫具有 `CREATE` 權限的非超級使用者可以安裝它。

在 `CREATE TRIGGER` 陳述式中，此函式最多只能提供一個可選參數。若提供，該參數將作為通知的頻道名稱；若省略，則使用 `tcn` 作為頻道名稱。

通知的酬載由資料表名稱、表示執行作業類型的字母，以及主鍵欄位的欄位名稱／值配對所組成。各部分以逗號分隔。為便於使用正規表示式剖析，資料表和欄位名稱一律以雙引號括住，資料值一律以單引號括住；內嵌的引號會重複一次。

以下為使用此擴充功能的簡短範例。

```

test=# create table tcndata
test-#   (
test(#     a int not null,
test(#     b date not null,
test(#     c text,
test(#     primary key (a, b)
test(#   );
CREATE TABLE
test=# create trigger tcndata_tcn_trigger
test-#   after insert or update or delete on tcndata
test-#   for each row execute function triggered_change_notification();
CREATE TRIGGER
test=# listen tcn;
LISTEN
test=# insert into tcndata values (1, date '2012-12-22', 'one'),
test-#                            (1, date '2012-12-23', 'another'),
test-#                            (2, date '2012-12-23', 'two');
INSERT 0 3
Asynchronous notification "tcn" with payload ""tcndata",I,"a"='1',"b"='2012-12-22'" received from server process with PID 22770.
Asynchronous notification "tcn" with payload ""tcndata",I,"a"='1',"b"='2012-12-23'" received from server process with PID 22770.
Asynchronous notification "tcn" with payload ""tcndata",I,"a"='2',"b"='2012-12-23'" received from server process with PID 22770.
test=# update tcndata set c = 'uno' where a = 1;
UPDATE 2
Asynchronous notification "tcn" with payload ""tcndata",U,"a"='1',"b"='2012-12-22'" received from server process with PID 22770.
Asynchronous notification "tcn" with payload ""tcndata",U,"a"='1',"b"='2012-12-23'" received from server process with PID 22770.
test=# delete from tcndata where a = 1 and b = date '2012-12-22';
DELETE 1
Asynchronous notification "tcn" with payload ""tcndata",D,"a"='1',"b"='2012-12-22'" received from server process with PID 22770.
```

---

原文：[PostgreSQL 15.19 Documentation](https://www.postgresql.org/docs/15/tcn.html)
