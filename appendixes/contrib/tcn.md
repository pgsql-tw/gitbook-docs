<a id="TCN"></a>

## F.44. tcn — 通知監聽者資料表內容變更的觸發程序函式 [#](#tcn) <a href="#tcn" id="tcn"></a>

<a id="id-1.11.7.54.2"></a><a id="id-1.11.7.54.3"></a>

`tcn` 模組提供一個觸發程序函式，會將其所附加之任何資料表的內容變更通知監聽者。它必須作為 `FOR EACH ROW` 的 `AFTER` 觸發程序使用。

此模組被視為「受信任」，亦即具有目前資料庫 `CREATE` 權限的非超級使用者可以安裝它。

在 `CREATE TRIGGER` 陳述式中只能為此函式提供一個參數，而且該參數是選用的。若有提供，它會作為通知的通道名稱；若省略，則以 `tcn` 作為通道名稱。

通知的承載由資料表名稱、表示所執行操作類型的字母，以及主鍵欄位的欄位名稱／值配對組成，各部分之間以逗號分隔。為了方便以正規表示式剖析，資料表與欄位名稱一律以雙引號包圍，資料值一律以單引號包圍。內嵌的引號會重複為兩個。

以下是使用此擴充功能的簡短範例。

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

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/tcn.html)（原文版本：18.6；核對日期：2026-10-22）
