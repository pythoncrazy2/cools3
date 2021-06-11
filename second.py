strs="hello"
from google_trans_new import google_translator  
g=google_translator()

a=g.translate(strs,"es")
a=g.translate(a,"en")
print(a)