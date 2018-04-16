# 23. 語系

**Table of Contents**

[23.1. Locale Support](https://www.postgresql.org/docs/10/static/locale.html)

[23.1.1. Overview](https://www.postgresql.org/docs/10/static/locale.html#id-1.6.10.3.4)

[23.1.2. Behavior](https://www.postgresql.org/docs/10/static/locale.html#id-1.6.10.3.5)

[23.1.3. Problems](https://www.postgresql.org/docs/10/static/locale.html#id-1.6.10.3.6)

[23.2. Collation Support](https://www.postgresql.org/docs/10/static/collation.html)

[23.2.1. Concepts](https://www.postgresql.org/docs/10/static/collation.html#id-1.6.10.4.4)

[23.2.2. Managing Collations](https://www.postgresql.org/docs/10/static/collation.html#COLLATION-MANAGING)

[23.3. Character Set Support](https://www.postgresql.org/docs/10/static/multibyte.html)

[23.3.1. Supported Character Sets](https://www.postgresql.org/docs/10/static/multibyte.html#MULTIBYTE-CHARSET-SUPPORTED)

[23.3.2. Setting the Character Set](https://www.postgresql.org/docs/10/static/multibyte.html#id-1.6.10.5.6)

[23.3.3. Automatic Character Set Conversion Between Server and Client](https://www.postgresql.org/docs/10/static/multibyte.html#id-1.6.10.5.7)

[23.3.4. Further Reading](https://www.postgresql.org/docs/10/static/multibyte.html#id-1.6.10.5.8)

This chapter describes the available localization features from the point of view of the administrator.PostgreSQLsupports two localization facilities:

* Using the locale features of the operating system to provide locale-specific collation order, number formatting, translated messages, and other aspects. This is covered in[Section 23.1](https://www.postgresql.org/docs/10/static/locale.html)and[Section 23.2](https://www.postgresql.org/docs/10/static/collation.html).
* Providing a number of different character sets to support storing text in all kinds of languages, and providing character set translation between client and server. This is covered in[Section 23.3](https://www.postgresql.org/docs/10/static/multibyte.html).

