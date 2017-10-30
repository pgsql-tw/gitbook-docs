# 5. 問題回報指南[^1]

> 本篇談的是如何回報問題到 PostgreSQL 官方組織，而本手冊並非由官方手冊提供，所以如果你希望指出的問題是本手冊的相關問題，請透過[討論區](https://www.gitbook.com/book/pgsql-tw/documents/discussions)，或[台灣 PostgreSQL 使用者社群](https://pgsql-tw.github.io/)所提供的聯絡資訊回報。

如果你在 PostgreSQL 中發現了問題，我們會很希望可以得到通知。你的問題回報可以讓 PostgreSQL 變得更值得信任，因為百密仍有一疏，PostgreSQL 無法保證在任何平台或任何情況下，都一定是完美無缺的。

下面的建議提供你在回報問題時能夠更有效率。你不一定要完全遵照下面的方式，但如果你試著遵循的話，對大家都有幫助。

我們無法保證可以立即修正所有的錯誤。但如果那個問題是明顯的、關鍵的、或是有重大影響的，那就會有人進行瞭解。也可能會回覆你更新你的資料庫版本，如果是因為版本問題的話。我們也可能會判定該錯誤不會被修正，在我們進行重大修改之前；又也許它不容易簡單處理，而且有其他更重要的需求排程已經在進行中。如果你需要立即性的支援，請接洽當地的商業服務。

### 5.1. 確認錯誤

在報告錯誤之前，請再三閱讀文件，以確認你真的在進行你正在嘗試的事情。 如果從文件中不清楚是否可以做某事，請回報；這是屬於文件的一個錯誤。如果確實證明一個程式與文件所描述地不同，那就是一個錯誤。這可能包括但不限於以下情況：

* 程式以致命信號（fatal signal）或程式中某個問題造成作業系統錯誤訊息而終止。（反例可能是“磁盤已滿”的訊息，因為您必須自己修復。）

* 程式對於任何輸入都產生錯誤輸出結果。

* 程式拒絕接受有效的輸入 （如文件中所定義的）。

* 程式接受了無效的輸入，卻沒有警告或錯誤消息。但請記住，您對於無效輸入的認知可能來自於我們對傳統做法的延伸或相容性。

* PostgreSQL 在支援的平台上，按照指示進行編譯，構建或安裝卻失敗了。

這裡的「程式」是指任何可執行文件，不僅僅是後端執行的程序。

緩慢或資源匱乏不一定是一個錯誤。閱讀文件或在某個郵件列表中提問，可以幫助你調整應用程式。不符合 SQL 標準不代表是錯誤，除非明確聲明相容某個特定的功能。

在繼續之前，請檢查 TODO 列表和常見問題解答，看看您的錯誤是否已知。 如果您無法瞭解 TODO 列表中的資訊，請報告你的問題。 我們至少可以做的是使 TODO 列表更清楚。

### 5.2. What to Report

The most important thing to remember about bug reporting is to state all the facts and only facts. Do not speculate what you think went wrong, what“it seemed to do”, or which part of the program has a fault. If you are not familiar with the implementation you would probably guess wrong and not help us a bit. And even if you are, educated explanations are a great supplement to but no substitute for facts. If we are going to fix the bug we still have to see it happen for ourselves first. Reporting the bare facts is relatively straightforward \(you can probably copy and paste them from the screen\) but all too often important details are left out because someone thought it does not matter or the report would be understood anyway.

The following items should be contained in every bug report:

* The exact sequence of steps\_from program start-up\_necessary to reproduce the problem. This should be self-contained; it is not enough to send in a bare`SELECT`statement without the preceding`CREATE TABLE`and`INSERT`statements, if the output should depend on the data in the tables. We do not have the time to reverse-engineer your database schema, and if we are supposed to make up our own data we would probably miss the problem.

  The best format for a test case for SQL-related problems is a file that can be run through thepsqlfrontend that shows the problem. \(Be sure to not have anything in your`~/.psqlrc`start-up file.\) An easy way to create this file is to usepg\_dumpto dump out the table declarations and data needed to set the scene, then add the problem query. You are encouraged to minimize the size of your example, but this is not absolutely necessary. If the bug is reproducible, we will find it either way.

  If your application uses some other client interface, such asPHP, then please try to isolate the offending queries. We will probably not set up a web server to reproduce your problem. In any case remember to provide the exact input files; do not guess that the problem happens for“large files”or“midsize databases”, etc. since this information is too inexact to be of use.

* The output you got. Please do not say that it“didn't work”or“crashed”. If there is an error message, show it, even if you do not understand it. If the program terminates with an operating system error, say which. If nothing at all happens, say so. Even if the result of your test case is a program crash or otherwise obvious it might not happen on our platform. The easiest thing is to copy the output from the terminal, if possible.

  ### Note

  If you are reporting an error message, please obtain the most verbose form of the message. Inpsql, say`\set VERBOSITY verbose`beforehand. If you are extracting the message from the server log, set the run-time parameter[log\_error\_verbosity](https://www.postgresql.org/docs/10/static/runtime-config-logging.html#guc-log-error-verbosity)to`verbose`so that all details are logged.

  ### Note

  In case of fatal errors, the error message reported by the client might not contain all the information available. Please also look at the log output of the database server. If you do not keep your server's log output, this would be a good time to start doing so.

* The output you expected is very important to state. If you just write“This command gives me that output.”or“This is not what I expected.”, we might run it ourselves, scan the output, and think it looks OK and is exactly what we expected. We should not have to spend the time to decode the exact semantics behind your commands. Especially refrain from merely saying that“This is not what SQL says/Oracle does.”Digging out the correct behavior fromSQLis not a fun undertaking, nor do we all know how all the other relational databases out there behave. \(If your problem is a program crash, you can obviously omit this item.\)

* Any command line options and other start-up options, including any relevant environment variables or configuration files that you changed from the default. Again, please provide exact information. If you are using a prepackaged distribution that starts the database server at boot time, you should try to find out how that is done.

* Anything you did at all differently from the installation instructions.

* ThePostgreSQLversion. You can run the command`SELECT version();`to find out the version of the server you are connected to. Most executable programs also support a`--version`option; at least`postgres --version`and`psql --version`should work. If the function or the options do not exist then your version is more than old enough to warrant an upgrade. If you run a prepackaged version, such as RPMs, say so, including any subversion the package might have. If you are talking about a Git snapshot, mention that, including the commit hash.

  If your version is older than 10beta1 we will almost certainly tell you to upgrade. There are many bug fixes and improvements in each new release, so it is quite possible that a bug you have encountered in an older release ofPostgreSQLhas already been fixed. We can only provide limited support for sites using older releases ofPostgreSQL; if you require more than we can provide, consider acquiring a commercial support contract.

* Platform information. This includes the kernel name and version, C library, processor, memory information, and so on. In most cases it is sufficient to report the vendor and version, but do not assume everyone knows what exactly“Debian”contains or that everyone runs on i386s. If you have installation problems then information about the toolchain on your machine \(compiler,make, and so on\) is also necessary.

Do not be afraid if your bug report becomes rather lengthy. That is a fact of life. It is better to report everything the first time than us having to squeeze the facts out of you. On the other hand, if your input files are huge, it is fair to ask first whether somebody is interested in looking into it. Here is an[article](http://www.chiark.greenend.org.uk/~sgtatham/bugs.html)that outlines some more tips on reporting bugs.

Do not spend all your time to figure out which changes in the input make the problem go away. This will probably not help solving it. If it turns out that the bug cannot be fixed right away, you will still have time to find and share your work-around. Also, once again, do not waste your time guessing why the bug exists. We will find that out soon enough.

When writing a bug report, please avoid confusing terminology. The software package in total is called“PostgreSQL”, sometimes“Postgres”for short. If you are specifically talking about the backend process, mention that, do not just say“PostgreSQL crashes”. A crash of a single backend process is quite different from crash of the parent“postgres”process; please don't say“the server crashed”when you mean a single backend process went down, nor vice versa. Also, client programs such as the interactive frontend“psql”are completely separate from the backend. Please try to be specific about whether the problem is on the client or server side.

### 5.3. Where to Report Bugs

In general, send bug reports to the bug report mailing list at`<`[`pgsql-bugs@postgresql.org`](mailto:pgsql-bugs@postgresql.org)`>`. You are requested to use a descriptive subject for your email message, perhaps parts of the error message.

Another method is to fill in the bug report web-form available at the project's[web site](http://www.postgresql.org/). Entering a bug report this way causes it to be mailed to the`<`[`pgsql-bugs@postgresql.org`](mailto:pgsql-bugs@postgresql.org)`>`mailing list.

If your bug report has security implications and you'd prefer that it not become immediately visible in public archives, don't send it to`pgsql-bugs`. Security issues can be reported privately to`<`[`security@postgresql.org`](mailto:security@postgresql.org)`>`.

Do not send bug reports to any of the user mailing lists, such as`<`[`pgsql-sql@postgresql.org`](mailto:pgsql-sql@postgresql.org)`>`or`<`[`pgsql-general@postgresql.org`](mailto:pgsql-general@postgresql.org)`>`. These mailing lists are for answering user questions, and their subscribers normally do not wish to receive bug reports. More importantly, they are unlikely to fix them.

Also, please do\_not\_send reports to the developers' mailing list`<`[`pgsql-hackers@postgresql.org`](mailto:pgsql-hackers@postgresql.org)`>`. This list is for discussing the development ofPostgreSQL, and it would be nice if we could keep the bug reports separate. We might choose to take up a discussion about your bug report on`pgsql-hackers`, if the problem needs more review.

If you have a problem with the documentation, the best place to report it is the documentation mailing list`<`[`pgsql-docs@postgresql.org`](mailto:pgsql-docs@postgresql.org)`>`. Please be specific about what part of the documentation you are unhappy with.

If your bug is a portability problem on a non-supported platform, send mail to`<`[`pgsql-hackers@postgresql.org`](mailto:pgsql-hackers@postgresql.org)`>`, so we \(and you\) can work on portingPostgreSQLto your platform.

### Note

Due to the unfortunate amount of spam going around, all of the above email addresses are closed mailing lists. That is, you need to be subscribed to a list to be allowed to post on it. \(You need not be subscribed to use the bug-report web form, however.\) If you would like to send mail but do not want to receive list traffic, you can subscribe and set your subscription option to`nomail`. For more information send mail to`<`[`majordomo@postgresql.org`](mailto:majordomo@postgresql.org)`>`with the single word`help`in the body of the message.

---

[^1]: [PostgreSQL: Documentation: 10: 5. Bug Reporting Guidelines](https://www.postgresql.org/docs/10/static/bug-reporting.html)

