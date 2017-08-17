# 9.13. 文字檢索函式及運算子[^1]

[Table 9.40](https://www.postgresql.org/docs/10/static/functions-textsearch.html#textsearch-operators-table),[Table 9.41](https://www.postgresql.org/docs/10/static/functions-textsearch.html#textsearch-functions-table)and[Table 9.42](https://www.postgresql.org/docs/10/static/functions-textsearch.html#textsearch-functions-debug-table)summarize the functions and operators that are provided for full text searching. See[Chapter 12](https://www.postgresql.org/docs/10/static/textsearch.html)for a detailed explanation ofPostgreSQL's text search facility.

**Table 9.40. Text Search Operators**

| Operator | Return Type | Description | Example | Result |
| :--- | :--- | :--- | :--- | :--- |
| `@@` | `boolean` | `tsvector`matches`tsquery`? | `to_tsvector('fat cats ate rats') @@ to_tsquery('cat & rat')` | `t` |
| `@@@` | `boolean` | deprecated synonym for`@@` | `to_tsvector('fat cats ate rats') @@@ to_tsquery('cat & rat')` | `t` |
| `||` | `tsvector` | concatenate`tsvector`s | `'a:1 b:2'::tsvector || 'c:1 d:2 b:3'::tsvector` | `'a':1 'b':2,5 'c':3 'd':4` |
| `&&` | `tsquery` | AND`tsquery`s together | `'fat | rat'::tsquery && 'cat'::tsquery` | `( 'fat' | 'rat' ) & 'cat'` |
| `||` | `tsquery` | OR`tsquery`s together | `'fat | rat'::tsquery || 'cat'::tsquery` | `( 'fat' | 'rat' ) | 'cat'` |
| `!!` | `tsquery` | negate a`tsquery` | `!! 'cat'::tsquery` | `!'cat'` |
| `<->` | `tsquery` | `tsquery`followed by`tsquery` | `to_tsquery('fat') <-> to_tsquery('rat')` | `'fat' <-> 'rat'` |
| `@>` | `boolean` | `tsquery`contains another ? | `'cat'::tsquery @> 'cat & rat'::tsquery` | `f` |
| `<@` | `boolean` | `tsquery`is contained in ? | `'cat'::tsquery <@ 'cat & rat'::tsquery` | `t` |

  


### Note

The`tsquery`containment operators consider only the lexemes listed in the two queries, ignoring the combining operators.

In addition to the operators shown in the table, the ordinary B-tree comparison operators \(`=`,`<`, etc\) are defined for types`tsvector`and`tsquery`. These are not very useful for text searching but allow, for example, unique indexes to be built on columns of these types.

**Table 9.41. Text Search Functions**

| Function | Return Type | Description | Example | Result |
| :--- | :--- | :--- | :--- | :--- |
| `array_to_tsvector(text[]`\) | `tsvector` | convert array of lexemes to`tsvector` | `array_to_tsvector('{fat,cat,rat}'::text[])` | `'cat' 'fat' 'rat'` |
| `get_current_ts_config()` | `regconfig` | get default text search configuration | `get_current_ts_config()` | `english` |
| `length(tsvector`\) | `integer` | number of lexemes in`tsvector` | `length('fat:2,4 cat:3 rat:5A'::tsvector)` | `3` |
| `numnode(tsquery`\) | `integer` | number of lexemes plus operators in`tsquery` | `numnode('(fat & rat) | cat'::tsquery)` | `5` |
| `plainto_tsquery([`_`config`_`regconfig`,\]_`query`_`text`\) | `tsquery` | produce`tsquery`ignoring punctuation | `plainto_tsquery('english', 'The Fat Rats')` | `'fat' & 'rat'` |
| `phraseto_tsquery([`_`config`_`regconfig`,\]_`query`_`text`\) | `tsquery` | produce`tsquery`that searches for a phrase, ignoring punctuation | `phraseto_tsquery('english', 'The Fat Rats')` | `'fat' <-> 'rat'` |
| `querytree(`_`query`_`tsquery`\) | `text` | get indexable part of a`tsquery` | `querytree('foo & ! bar'::tsquery)` | `'foo'` |
| `setweight(`_`vector`_`tsvector`,_`weight`_`"char"`\) | `tsvector` | assign_`weight`_to each element of_`vector`_ | `setweight('fat:2,4 cat:3 rat:5B'::tsvector, 'A')` | `'cat':3A 'fat':2A,4A 'rat':5A` |
| `setweight(`_`vector`_`tsvector`,_`weight`_`"char"`,_`lexemes`_`text[]`\) | `tsvector` | assign_`weight`_to elements of_`vector`_that are listed in_`lexemes`_ | `setweight('fat:2,4 cat:3 rat:5B'::tsvector, 'A', '{cat,rat}')` | `'cat':3A 'fat':2,4 'rat':5A` |
| `strip(tsvector`\) | `tsvector` | remove positions and weights from`tsvector` | `strip('fat:2,4 cat:3 rat:5A'::tsvector)` | `'cat' 'fat' 'rat'` |
| `to_tsquery([`_`config`_`regconfig`,\]_`query`_`text`\) | `tsquery` | normalize words and convert to`tsquery` | `to_tsquery('english', 'The & Fat & Rats')` | `'fat' & 'rat'` |
| `to_tsvector([`_`config`_`regconfig`,\]_`document`_`text`\) | `tsvector` | reduce document text to`tsvector` | `to_tsvector('english', 'The Fat Rats')` | `'fat':2 'rat':3` |
| `to_tsvector([`_`config`_`regconfig`,\]_`document`_`json(b)`\) | `tsvector` | reduce each string value in the document to a`tsvector`, and then concatentate those in document order to produce a single`tsvector` | `to_tsvector('english', '{"a": "The Fat Rats"}'::json)` | `'fat':2 'rat':3` |
| `ts_delete(`_`vector`_`tsvector`,_`lexeme`_`text`\) | `tsvector` | remove given_`lexeme`_from_`vector`_ | `ts_delete('fat:2,4 cat:3 rat:5A'::tsvector, 'fat')` | `'cat':3 'rat':5A` |
| `ts_delete(`_`vector`_`tsvector`,_`lexemes`_`text[]`\) | `tsvector` | remove any occurrence of lexemes in_`lexemes`_from_`vector`_ | `ts_delete('fat:2,4 cat:3 rat:5A'::tsvector, ARRAY['fat','rat'])` | `'cat':3` |
| `ts_filter(`_`vector`_`tsvector`,_`weights`_`"char"[]`\) | `tsvector` | select only elements with given_`weights`_from_`vector`_ | `ts_filter('fat:2,4 cat:3b rat:5A'::tsvector, '{a,b}')` | `'cat':3B 'rat':5A` |
| `ts_headline([`_`config`_`regconfig`,\]_`document`_`text`,_`query`_`tsquery`\[,_`options`_`text`\]\) | `text` | display a query match | `ts_headline('x y z', 'z'::tsquery)` | `x y <b>z</b>` |
| `ts_headline([`_`config`_`regconfig`,\]_`document`_`json(b)`,_`query`_`tsquery`\[,_`options`_`text`\]\) | `text` | display a query match | `ts_headline('{"a":"x y z"}'::json, 'z'::tsquery)` | `{"a":"x y <b>z</b>"}` |
| `ts_rank([`_`weights`_`float4[]`,\]_`vector`_`tsvector`,_`query`_`tsquery`\[,_`normalization`_`integer`\]\) | `float4` | rank document for query | `ts_rank(textsearch, query)` | `0.818` |
| `ts_rank_cd([`_`weights`_`float4[]`,\]_`vector`_`tsvector`,_`query`_`tsquery`\[,_`normalization`_`integer`\]\) | `float4` | rank document for query using cover density | `ts_rank_cd('{0.1, 0.2, 0.4, 1.0}', textsearch, query)` | `2.01317` |
| `ts_rewrite(`_`query`_`tsquery`,_`target`_`tsquery`,_`substitute`_`tsquery`\) | `tsquery` | replace_`target`_with_`substitute`_within query | `ts_rewrite('a & b'::tsquery, 'a'::tsquery, 'foo|bar'::tsquery)` | `'b' & ( 'foo' | 'bar' )` |
| `ts_rewrite(`_`query`_`tsquery`,_`select`_`text`\) | `tsquery` | replace using targets and substitutes from a`SELECT`command | `SELECT ts_rewrite('a & b'::tsquery, 'SELECT t,s FROM aliases')` | `'b' & ( 'foo' | 'bar' )` |
| `tsquery_phrase(`_`query1`_`tsquery`,_`query2`_`tsquery`\) | `tsquery` | make query that searches for_`query1`_followed by_`query2`_\(same as`<->`operator\) | `tsquery_phrase(to_tsquery('fat'), to_tsquery('cat'))` | `'fat' <-> 'cat'` |
| `tsquery_phrase(`_`query1`_`tsquery`,_`query2`_`tsquery`,_`distance`_`integer`\) | `tsquery` | make query that searches for_`query1`_followed by_`query2`_at distance_`distance`_ | `tsquery_phrase(to_tsquery('fat'), to_tsquery('cat'), 10)` | `'fat' <10> 'cat'` |
| `tsvector_to_array(tsvector`\) | `text[]` | convert`tsvector`to array of lexemes | `tsvector_to_array('fat:2,4 cat:3 rat:5A'::tsvector)` | `{cat,fat,rat}` |
| `tsvector_update_trigger()` | `trigger` | trigger function for automatic`tsvector`column update | `CREATE TRIGGER ... tsvector_update_trigger(tsvcol, 'pg_catalog.swedish', title, body)` |  |
| `tsvector_update_trigger_column()` | `trigger` | trigger function for automatic`tsvector`column update | `CREATE TRIGGER ... tsvector_update_trigger_column(tsvcol, configcol, title, body)` |  |
| `unnest(tsvector`, OUT_`lexeme`_`text`, OUT_`positions`_`smallint[]`, OUT_`weights`_`text`\) | `setof record` | expand a tsvector to a set of rows | `unnest('fat:2,4 cat:3 rat:5A'::tsvector)` | `(cat,{3},{D}) ...` |

  


### Note

All the text search functions that accept an optional`regconfig`argument will use the configuration specified by[default\_text\_search\_config](https://www.postgresql.org/docs/10/static/runtime-config-client.html#guc-default-text-search-config)when that argument is omitted.

The functions in[Table 9.42](https://www.postgresql.org/docs/10/static/functions-textsearch.html#textsearch-functions-debug-table)are listed separately because they are not usually used in everyday text searching operations. They are helpful for development and debugging of new text search configurations.

**Table 9.42. Text Search Debugging Functions**

| Function | Return Type | Description | Example | Result |
| :--- | :--- | :--- | :--- | :--- |
| `ts_debug([`_`config`_`regconfig`,\]_`document`_`text`, OUT_`alias`_`text`, OUT_`description`_`text`, OUT_`token`_`text`, OUT_`dictionaries`_`regdictionary[]`, OUT_`dictionary`_`regdictionary`, OUT_`lexemes`_`text[]`\) | `setof record` | test a configuration | `ts_debug('english', 'The Brightest supernovaes')` | `(asciiword,"Word, all ASCII",The,{english_stem},english_stem,{}) ...` |
| `ts_lexize(`_`dict`_`regdictionary`,_`token`_`text`\) | `text[]` | test a dictionary | `ts_lexize('english_stem', 'stars')` | `{star}` |
| `ts_parse(`_`parser_name`_`text`,_`document`_`text`, OUT_`tokid`_`integer`, OUT_`token`_`text`\) | `setof record` | test a parser | `ts_parse('default', 'foo - bar')` | `(1,foo) ...` |
| `ts_parse(`_`parser_oid`_`oid`,_`document`_`text`, OUT_`tokid`_`integer`, OUT_`token`_`text`\) | `setof record` | test a parser | `ts_parse(3722, 'foo - bar')` | `(1,foo) ...` |
| `ts_token_type(`_`parser_name`_`text`, OUT_`tokid`_`integer`, OUT_`alias`_`text`, OUT_`description`_`text`\) | `setof record` | get token types defined by parser | `ts_token_type('default')` | `(1,asciiword,"Word, all ASCII") ...` |
| `ts_token_type(`_`parser_oid`_`oid`, OUT_`tokid`_`integer`, OUT_`alias`_`text`, OUT_`description`_`text`\) | `setof record` | get token types defined by parser | `ts_token_type(3722)` | `(1,asciiword,"Word, all ASCII") ...` |
| `ts_stat(`_`sqlquery`_`text`, \[_`weights`_`text`,\] OUT_`word`_`text`, OUT_`ndoc`_`integer`, OUT_`nentry`_`integer`\) | `setof record` | get statistics of a`tsvector`column | `ts_stat('SELECT vector from apod')` | `(foo,10,15) ...` |

---

  


[^1]:  [PostgreSQL: Documentation: 10: 9.13. Text Search Functions and Operators](https://www.postgresql.org/docs/10/static/functions-textsearch.html)

