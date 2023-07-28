thedict = [
    {"name": "item1", "price": 10},
    {"name": "item2", "price": 5},
    {"name": "item3", "price": 10},
    {"name": "item4", "price": 12},
    {"name": "item5", "price": 12},
    {"name": "item6", "price": 5}
 ]
 
 
d = {}
 
for item in thedict:
    d.setdefault(item['price'], []).append(item)
 
# list(d.values())
 
print(d)