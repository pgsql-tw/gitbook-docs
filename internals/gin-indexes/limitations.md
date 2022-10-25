# 66.6. 限制

GIN 假定可索引運算子是嚴格的。這意味著將根本不對 null 值呼叫 extractValue（相反地，將自動建立 placeholder 索引項目），並且也將不對 null 查詢值呼叫 extractQuery（相反地，假定查詢將無法滿足要求） 。 但是請注意，支援包含在非 null 組合項目或查詢值中的 null 鍵值。
