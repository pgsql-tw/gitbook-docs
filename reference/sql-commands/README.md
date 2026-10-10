<a id="SQL-COMMANDS"></a>

# SQL 命令

---

<a id="id-1.9.3.2"></a>

本部分包含 PostgreSQL 所支援之 SQL 命令的參考資訊。這裡所說的「SQL」是泛指這個語言；關於各命令的標準符合程度與相容性資訊，可以在各自的參考頁面中找到。

**目錄**

[ABORT](sql-abort.md) — 中止目前的交易

[ALTER AGGREGATE](sql-alteraggregate.md) — 變更彙總函式的定義

[ALTER COLLATION](sql-altercollation.md) — 變更定序的定義

[ALTER CONVERSION](sql-alterconversion.md) — 變更轉換的定義

[ALTER DATABASE](sql-alterdatabase.md) — 變更資料庫

[ALTER DEFAULT PRIVILEGES](sql-alterdefaultprivileges.md) — 定義預設存取權限

[ALTER DOMAIN](sql-alterdomain.md) — 變更網域的定義

[ALTER EVENT TRIGGER](sql-altereventtrigger.md) — 變更事件觸發程序的定義

[ALTER EXTENSION](sql-alterextension.md) — 變更擴充功能的定義

[ALTER FOREIGN DATA WRAPPER](sql-alterforeigndatawrapper.md) — 變更外部資料包裝器的定義

[ALTER FOREIGN TABLE](sql-alterforeigntable.md) — 變更外部資料表的定義

[ALTER FUNCTION](sql-alterfunction.md) — 變更函式的定義

[ALTER GROUP](sql-altergroup.md) — 變更角色名稱或成員資格

[ALTER INDEX](sql-alterindex.md) — 變更索引的定義

[ALTER LANGUAGE](sql-alterlanguage.md) — 變更程序語言的定義

[ALTER LARGE OBJECT](sql-alterlargeobject.md) — 變更大型物件的定義

[ALTER MATERIALIZED VIEW](sql-altermaterializedview.md) — 變更具體化檢視表的定義

[ALTER OPERATOR](sql-alteroperator.md) — 變更運算子的定義

[ALTER OPERATOR CLASS](sql-alteropclass.md) — 變更運算子類別的定義

[ALTER OPERATOR FAMILY](sql-alteropfamily.md) — 變更運算子家族的定義

[ALTER POLICY](sql-alterpolicy.md) — 變更資料列層級安全性政策的定義

[ALTER PROCEDURE](sql-alterprocedure.md) — 變更程序的定義

[ALTER PUBLICATION](sql-alterpublication.md) — 變更發佈的定義

[ALTER ROLE](sql-alterrole.md) — 變更資料庫角色

[ALTER ROUTINE](sql-alterroutine.md) — 變更常式的定義

[ALTER RULE](sql-alterrule.md) — 變更規則的定義

[ALTER SCHEMA](sql-alterschema.md) — 變更綱要的定義

[ALTER SEQUENCE](sql-altersequence.md) — 變更序列產生器的定義

[ALTER SERVER](sql-alterserver.md) — 變更外部伺服器的定義

[ALTER STATISTICS](sql-alterstatistics.md) — 變更擴充統計資訊物件的定義

[ALTER SUBSCRIPTION](sql-altersubscription.md) — 變更訂閱的定義

[ALTER SYSTEM](sql-altersystem.md) — 變更伺服器設定參數

[ALTER TABLE](sql-altertable.md) — 變更資料表的定義

[ALTER TABLESPACE](sql-altertablespace.md) — 變更資料表空間的定義

[ALTER TEXT SEARCH CONFIGURATION](sql-altertsconfig.md) — 變更文字搜尋設定的定義

[ALTER TEXT SEARCH DICTIONARY](sql-altertsdictionary.md) — 變更文字搜尋字典的定義

[ALTER TEXT SEARCH PARSER](sql-altertsparser.md) — 變更文字搜尋剖析器的定義

[ALTER TEXT SEARCH TEMPLATE](sql-altertstemplate.md) — 變更文本搜尋模板的定義

[ALTER TRIGGER](sql-altertrigger.md) — 變更觸發程序的定義

[ALTER TYPE](sql-altertype.md) — 變更型別的定義

[ALTER USER](sql-alteruser.md) — 變更資料庫角色

[ALTER USER MAPPING](sql-alterusermapping.md) — 變更使用者對應的定義

[ALTER VIEW](sql-alterview.md) — 變更檢視表的定義

[ANALYZE](sql-analyze.md) — 收集資料庫的統計資訊

[BEGIN](sql-begin.md) — 開始一個交易區塊

[CALL](sql-call.md) — 呼叫程序

[CHECKPOINT](sql-checkpoint.md) — 強制執行預寫式日誌檢查點

[CLOSE](sql-close.md) — 關閉游標

[CLUSTER](sql-cluster.md) — 依據索引將資料表叢集化

[COMMENT](sql-comment.md) — 定義或變更物件的註解

[COMMIT](sql-commit.md) — 提交目前的交易

[COMMIT PREPARED](sql-commit-prepared.md) — 提交先前已為兩階段提交而準備的交易

[COPY](sql-copy.md) — 在檔案與資料表之間複製資料

[CREATE ACCESS METHOD](sql-create-access-method.md) — 定義新的存取方法

[CREATE AGGREGATE](sql-createaggregate.md) — 定義新的彙總函式

[CREATE CAST](sql-createcast.md) — 定義新的型別轉換

[CREATE COLLATION](sql-createcollation.md) — 定義新的定序

[CREATE CONVERSION](sql-createconversion.md) — 定義新的編碼轉換

[CREATE DATABASE](sql-createdatabase.md) — 建立新的資料庫

[CREATE DOMAIN](sql-createdomain.md) — 定義新的網域

[CREATE EVENT TRIGGER](sql-createeventtrigger.md) — 定義新的事件觸發程序

[CREATE EXTENSION](sql-createextension.md) — 安裝擴充功能

[CREATE FOREIGN DATA WRAPPER](sql-createforeigndatawrapper.md) — 定義新的外部資料包裝器

[CREATE FOREIGN TABLE](sql-createforeigntable.md) — 定義新的外部資料表

[CREATE FUNCTION](sql-createfunction.md) — 定義新的函式

[CREATE GROUP](sql-creategroup.md) — 定義新的資料庫角色

[CREATE INDEX](sql-createindex.md) — 定義新的索引

[CREATE LANGUAGE](sql-createlanguage.md) — 定義新的程序語言

[CREATE MATERIALIZED VIEW](sql-creatematerializedview.md) — 定義新的具體化檢視表

[CREATE OPERATOR](sql-createoperator.md) — 定義新的運算子

[CREATE OPERATOR CLASS](sql-createopclass.md) — 定義新的運算子類別

[CREATE OPERATOR FAMILY](sql-createopfamily.md) — 定義新的運算子家族

[CREATE POLICY](sql-createpolicy.md) — 為資料表定義新的資料列層級安全性政策

[CREATE PROCEDURE](sql-createprocedure.md) — 定義新的程序

[CREATE PUBLICATION](sql-createpublication.md) — 定義新的發佈

[CREATE ROLE](sql-createrole.md) — 定義新的資料庫角色

[CREATE RULE](sql-createrule.md) — 定義新的重寫規則

[CREATE SCHEMA](sql-createschema.md) — 定義新的綱要

[CREATE SEQUENCE](sql-createsequence.md) — 定義新的序列產生器

[CREATE SERVER](sql-createserver.md) — 定義新的外部伺服器

[CREATE STATISTICS](sql-createstatistics.md) — 定義擴充統計資訊

[CREATE SUBSCRIPTION](sql-createsubscription.md) — 定義新的訂閱

[CREATE TABLE](sql-createtable.md) — 定義新的資料表

[CREATE TABLE AS](sql-createtableas.md) — 以查詢的結果定義新的資料表

[CREATE TABLESPACE](sql-createtablespace.md) — 定義新的資料表空間

[CREATE TEXT SEARCH CONFIGURATION](sql-createtsconfig.md) — 定義新的文字搜尋設定

[CREATE TEXT SEARCH DICTIONARY](sql-createtsdictionary.md) — 定義新的文字搜尋字典

[CREATE TEXT SEARCH PARSER](sql-createtsparser.md) — 定義新的文字搜尋剖析器

[CREATE TEXT SEARCH TEMPLATE](sql-createtstemplate.md) — 定義新的文字搜尋範本

[CREATE TRANSFORM](sql-createtransform.md) — 定義新的轉換

[CREATE TRIGGER](sql-createtrigger.md) — 定義新的觸發程序

[CREATE TYPE](sql-createtype.md) — 定義新的資料型別

[CREATE USER](sql-createuser.md) — 定義新的資料庫角色

[CREATE USER MAPPING](sql-createusermapping.md) — 定義使用者到外部伺服器的新對應

[CREATE VIEW](sql-createview.md) — 定義新的檢視表

[DEALLOCATE](sql-deallocate.md) — 釋放預備陳述式

[DECLARE](sql-declare.md) — 定義游標

[DELETE](sql-delete.md) — 刪除資料表中的資料列

[DISCARD](sql-discard.md) — 捨棄工作階段狀態

[DO](sql-do.md) — 執行匿名程式碼區塊

[DROP ACCESS METHOD](sql-drop-access-method.md) — 移除存取方法

[DROP AGGREGATE](sql-dropaggregate.md) — 移除彙總函式

[DROP CAST](sql-dropcast.md) — 移除型別轉換

[DROP COLLATION](sql-dropcollation.md) — 移除定序

[DROP CONVERSION](sql-dropconversion.md) — 移除轉換

[DROP DATABASE](sql-dropdatabase.md) — 移除資料庫

[DROP DOMAIN](sql-dropdomain.md) — 移除網域

[DROP EVENT TRIGGER](sql-dropeventtrigger.md) — 移除事件觸發器

[DROP EXTENSION](sql-dropextension.md) — 移除擴充功能

[DROP FOREIGN DATA WRAPPER](sql-dropforeigndatawrapper.md) — 移除外部資料包裝器

[DROP FOREIGN TABLE](sql-dropforeigntable.md) — 移除外部資料表

[DROP FUNCTION](sql-dropfunction.md) — 移除函式

[DROP GROUP](sql-dropgroup.md) — 移除資料庫角色

[DROP INDEX](sql-dropindex.md) — 移除索引

[DROP LANGUAGE](sql-droplanguage.md) — 移除程序語言

[DROP MATERIALIZED VIEW](sql-dropmaterializedview.md) — 移除具體化檢視表

[DROP OPERATOR](sql-dropoperator.md) — 移除運算子

[DROP OPERATOR CLASS](sql-dropopclass.md) — 移除運算子類別

[DROP OPERATOR FAMILY](sql-dropopfamily.md) — 移除運算子家族

[DROP OWNED](sql-drop-owned.md) — 移除資料庫角色所擁有的資料庫物件

[DROP POLICY](sql-droppolicy.md) — 從資料表移除資料列層級安全性政策

[DROP PROCEDURE](sql-dropprocedure.md) — 移除程序

[DROP PUBLICATION](sql-droppublication.md) — 移除發佈物件

[DROP ROLE](sql-droprole.md) — 移除資料庫角色

[DROP ROUTINE](sql-droproutine.md) — 移除常式

[DROP RULE](sql-droprule.md) — 移除重寫規則

[DROP SCHEMA](sql-dropschema.md) — 移除綱要

[DROP SEQUENCE](sql-dropsequence.md) — 移除序列

[DROP SERVER](sql-dropserver.md) — 移除外部伺服器描述器

[DROP STATISTICS](sql-dropstatistics.md) — 移除擴充統計資訊

[DROP SUBSCRIPTION](sql-dropsubscription.md) — 移除訂閱

[DROP TABLE](sql-droptable.md) — 移除資料表

[DROP TABLESPACE](sql-droptablespace.md) — 移除資料表空間

[DROP TEXT SEARCH CONFIGURATION](sql-droptsconfig.md) — 移除文字搜尋設定

[DROP TEXT SEARCH DICTIONARY](sql-droptsdictionary.md) — 移除文字搜尋字典

[DROP TEXT SEARCH PARSER](sql-droptsparser.md) — 移除文字搜尋剖析器

[DROP TEXT SEARCH TEMPLATE](sql-droptstemplate.md) — 移除文字搜尋範本

[DROP TRANSFORM](sql-droptransform.md) — 移除轉換

[DROP TRIGGER](sql-droptrigger.md) — 移除觸發程序

[DROP TYPE](sql-droptype.md) — 移除資料型別

[DROP USER](sql-dropuser.md) — 移除資料庫角色

[DROP USER MAPPING](sql-dropusermapping.md) — 移除外部伺服器的使用者對應

[DROP VIEW](sql-dropview.md) — 移除檢視表

[END](sql-end.md) — 提交目前的交易

[EXECUTE](sql-execute.md) — 執行預備陳述式

[EXPLAIN](sql-explain.md) — 顯示陳述式的執行計畫

[FETCH](sql-fetch.md) — 使用游標從查詢中取回資料列

[GRANT](sql-grant.md) — 定義存取權限

[IMPORT FOREIGN SCHEMA](sql-importforeignschema.md) — 從外部伺服器匯入資料表定義

[INSERT](sql-insert.md) — 在資料表中建立新的資料列

[LISTEN](sql-listen.md) — 監聽通知

[LOAD](sql-load.md) — 載入共享函式庫檔案

[LOCK](sql-lock.md) — 鎖定一個資料表

[MERGE](sql-merge.md) — 依條件插入、更新或刪除資料表中的資料列

[MOVE](sql-move.md) — 定位游標

[NOTIFY](sql-notify.md) — 產生通知

[PREPARE](sql-prepare.md) — 準備一則陳述式以供執行

[PREPARE TRANSACTION](sql-prepare-transaction.md) — 為兩階段提交準備目前的交易

[REASSIGN OWNED](sql-reassign-owned.md) — 變更某資料庫角色所擁有的資料庫物件之擁有權

[REFRESH MATERIALIZED VIEW](sql-refreshmaterializedview.md) — 取代一個具體化檢視表的內容

[REINDEX](sql-reindex.md) — 重建索引

[RELEASE SAVEPOINT](sql-release-savepoint.md) — 釋放先前定義的一個儲存點

[RESET](sql-reset.md) — 將某個執行期參數的值還原為預設值

[REVOKE](sql-revoke.md) — 移除存取權限

[ROLLBACK](sql-rollback.md) — 中止目前的交易

[ROLLBACK PREPARED](sql-rollback-prepared.md) — 取消一個先前已為兩階段提交而準備的交易

[ROLLBACK TO SAVEPOINT](sql-rollback-to.md) — 回復到某個儲存點

[SAVEPOINT](sql-savepoint.md) — 在目前交易中定義一個新的儲存點

[SECURITY LABEL](sql-security-label.md) — 定義或變更套用於某個物件的安全性標籤

[SELECT](sql-select.md) — 從資料表或檢視表擷取資料列

[SELECT INTO](sql-selectinto.md) — 從查詢結果定義一個新資料表

[SET](sql-set.md) — 變更一個執行期參數

[SET CONSTRAINTS](sql-set-constraints.md) — 設定目前交易中限制條件的檢查時機

[SET ROLE](sql-set-role.md) — 設定目前工作階段的目前使用者識別碼

[SET SESSION AUTHORIZATION](sql-set-session-authorization.md) — 設定目前工作階段的工作階段使用者識別碼與目前使用者識別碼

[SET TRANSACTION](sql-set-transaction.md) — 設定目前交易的特性

[SHOW](sql-show.md) — 顯示執行期參數的值

[START TRANSACTION](sql-start-transaction.md) — 開始一個交易區塊

[TRUNCATE](sql-truncate.md) — 清空一個資料表或一組資料表

[UNLISTEN](sql-unlisten.md) — 停止接聽某個通知頻道

[UPDATE](sql-update.md) — 更新資料表的資料列

[VACUUM](sql-vacuum.md) — 資料庫的垃圾回收，並可選擇進行分析

[VALUES](sql-values.md) — 計算一組資料列

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-commands.html)（原文版本：18.6；核對日期：2026-10-10）
