## Chapter 23. Localization

**Table of Contents**

[23.1. Locale Support](locale.md)
:   [23.1.1. Overview](locale.md#LOCALE-OVERVIEW)

    [23.1.2. Behavior](locale.md#LOCALE-BEHAVIOR)

    [23.1.3. Selecting Locales](locale.md#LOCALE-SELECTING-LOCALES)

    [23.1.4. Locale Providers](locale.md#LOCALE-PROVIDERS)

    [23.1.5. ICU Locales](locale.md#ICU-LOCALES)

    [23.1.6. Problems](locale.md#LOCALE-PROBLEMS)

[23.2. Collation Support](collation.md)
:   [23.2.1. Concepts](collation.md#COLLATION-CONCEPTS)

    [23.2.2. Managing Collations](collation.md#COLLATION-MANAGING)

    [23.2.3. ICU Custom Collations](collation.md#ICU-CUSTOM-COLLATIONS)

[23.3. Character Set Support](multibyte.md)
:   [23.3.1. Supported Character Sets](multibyte.md#MULTIBYTE-CHARSET-SUPPORTED)

    [23.3.2. Setting the Character Set](multibyte.md#MULTIBYTE-SETTING)

    [23.3.3. Automatic Character Set Conversion Between Server and Client](multibyte.md#MULTIBYTE-AUTOMATIC-CONVERSION)

    [23.3.4. Available Character Set Conversions](multibyte.md#MULTIBYTE-CONVERSIONS-SUPPORTED)

    [23.3.5. Further Reading](multibyte.md#MULTIBYTE-FURTHER-READING)

This chapter describes the available localization features from the
point of view of the administrator.
PostgreSQL supports two localization
facilities:

* Using the locale features of the operating system to provide
  locale-specific collation order, number formatting, translated
  messages, and other aspects.
  This is covered in [Section 23.1](locale.md) and
  [Section 23.2](collation.md).
* Providing a number of different character sets to support storing text
  in all kinds of languages, and providing character set translation
  between client and server.
  This is covered in [Section 23.3](multibyte.md).

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/charset.html)（英文原文，待翻譯）
