from ast import literal_eval
from requests import get
print(literal_eval(get("https://api.github.com/repos/CopyPastaOfficial/CopyPasta/tags").text)[0]['name'] == "1.3")