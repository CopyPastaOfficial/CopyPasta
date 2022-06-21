from ast import literal_eval
from os import startfile
from requests import get


startfile("C:/")


print(literal_eval(get("https://api.github.com/repos/CopyPastaOfficial/CopyPasta/tags").text)[0]['name'])