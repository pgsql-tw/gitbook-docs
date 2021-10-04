# 50. PostgreSQL 的內部架構

{% hint style="info" %}
#### Author

This chapter originated as part of [\[sim98\]](../../bibliography.md#sim-98-enhancement-of-the-ansi-sql-implementation-of-postgresql-stefan-simkovics-department-of-information-systems-vienna-university-of-technology-vienna-austria-november-29-1998), Stefan Simkovics' Master's Thesis prepared at Vienna University of Technology under the direction of O.Univ.Prof.Dr. Georg Gottlob and Univ.Ass. Mag. Katrin Seyr.
{% endhint %}

本章概述了 PostgreSQL 的內部架構。閱讀以下各節後，你應該可以了解一個查詢是如何被處理的。本章的目的不是詳細描述 PostgreSQL 的內部操作，因為那樣的說明太過於詳盡。本章旨在幫助讀者理解資料庫後端內部發生的一些操作程序，從接收查詢的開始到將結果回傳給用戶端之間所發生的事。  


