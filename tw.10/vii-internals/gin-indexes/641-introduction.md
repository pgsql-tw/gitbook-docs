# 64.1. Introduction[^1]

GINstands for Generalized Inverted Index.GINis designed for handling cases where the items to be indexed are composite values, and the queries to be handled by the index need to search for element values that appear within the composite items. For example, the items could be documents, and the queries could be searches for documents containing specific words.

We use the word_item_to refer to a composite value that is to be indexed, and the word_key_to refer to an element value.GINalways stores and searches for keys, not item values per se.

AGINindex stores a set of \(key, posting list\) pairs, where a_posting list_is a set of row IDs in which the key occurs. The same row ID can appear in multiple posting lists, since an item can contain more than one key. Each key value is stored only once, so aGINindex is very compact for cases where the same key appears many times.

GINis generalized in the sense that theGINaccess method code does not need to know the specific operations that it accelerates. Instead, it uses custom strategies defined for particular data types. The strategy defines how keys are extracted from indexed items and query conditions, and how to determine whether a row that contains some of the key values in a query actually satisfies the query.

One advantage ofGINis that it allows the development of custom data types with the appropriate access methods, by an expert in the domain of the data type, rather than a database expert. This is much the same advantage as usingGiST.

TheGINimplementation inPostgreSQLis primarily maintained by Teodor Sigaev and Oleg Bartunov. There is more information aboutGINon their[website](http://www.sai.msu.su/~megera/wiki/Gin).

---



[^1]:  [PostgreSQL: Documentation: 10: 64.1. Introduction](https://www.postgresql.org/docs/10/static/gin-intro.html)

