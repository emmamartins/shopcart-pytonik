#!/Library/Frameworks/Python.framework/Versions/3.8/bin/python3
#print("Content-type:text/html\r\n")
try:

  from pytonik import Web

except Exception as err:
  exit(err)

App = Web.App()

App.runs()
