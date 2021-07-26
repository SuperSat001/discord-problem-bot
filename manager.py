from replit import db

# for i in db["physics"].keys():
#     print(i, db["physics"][i])


print(db.keys())

k = ["saveChannelId", "postChannelId", "leadMessageId"]
phy = [869079873560408075, 869079899393105930, 869081077044617277]
maths = [869079922377900043, 869079941122236426, 869081098095841290]

for i in range(3):
    db["physics"][k[i]] = phy[i]
    db["maths"][k[i]] = maths[i]


for i in range(3):
    print(k[i], db["physics"][k[i]])
    print(k[i], db["maths"][k[i]])

print(db["physics"]["leadChannelId"])
print(db["maths"]["leadChannelId"])
db["physics"]["leadChannelId"] = 869079961724682301
db["maths"]["leadChannelId"] = 869079961724682301