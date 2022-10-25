# 45. PL/Python - Python Procedural Language

PL/Python 程序語言允許 PostgreSQL 函數以 [Python 語言](https://www.python.org/)撰寫。

要將 PL/Python 安裝在特定的資料庫中，請使用 `CREATE EXTENSION plpythonu`（另請參閱第 45.1 節）。

{% hint style="info" %}
如果將語言安裝到 template1 中，則所有隨後建立的資料庫將自動安裝該語言。
{% endhint %}

PL/Python is only available as an “untrusted” language, meaning it does not offer any way of restricting what users can do in it and is therefore named `plpythonu`. A trusted variant `plpython` might become available in the future if a secure execution mechanism is developed in Python. The writer of a function in untrusted PL/Python must take care that the function cannot be used to do anything unwanted, since it will be able to do anything that could be done by a user logged in as the database administrator. Only superusers can create functions in untrusted languages such as `plpythonu`.

{% hint style="info" %}
自行編譯原始碼的使用者必須在安裝程序中特別啟用 PL/Python 的編譯。（更多相關資訊，請參閱安裝說明。）使用預先編譯版本的使用者可以在單獨的套件中找到 PL/Python。
{% endhint %}
