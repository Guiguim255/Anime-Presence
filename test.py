def soundex(val: str):
  val = val.upper()
  soundex = val[0]
  databse = [ "BP", "CKQ", "DT", "L", "MN", "R", "GJ", "XZS", "FV"]
  for char in val[1:]:
    for key in databse:
      if char in key and str(databse.index(key)+1) != soundex[-1]: soundex += str(databse.index(key)+1)
  return soundex

def soundex(val: str):
  val = val.upper()
  soundex = val[0]
  databse = {k:str(v+1) for v,k in enumerate(["BP", "CKQ", "DT", "L", "MN", "R", "GJ", "XZS", "FV"])}
  for char in val[1:]:
    for key in databse:
      if char in key and databse[key] != soundex[-1]: soundex += databse[key]
  return soundex