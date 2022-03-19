import re
import requests


if __name__ == '__main__':
    text = "M-AA1223"
    pattern = "^[A-Z]{1,3}-[A-Z]{1,2}([1-9]{1}[0-9]{0,3}|[8]{0})$"

    data = {"plate": text}
    response = requests.get(" http://192.168.1.50:5000/plate", json=data)
    print(response.json())
