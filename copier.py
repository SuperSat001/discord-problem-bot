import pickle
from replit import db
from copy import deepcopy

x = deepcopy(db)

with open('filename.pickle', 'wb') as handle:
    pickle.dump(x, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('filename.pickle', 'rb') as handle:
    b = pickle.load(handle)

print(b.keys())