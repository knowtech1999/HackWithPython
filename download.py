import requests

def download(url):
    get_request = requests.get(url)

    imagefile = open("image.jpg","wb")
    imagefile.write(get_request.content)
    imagefile.close()


download("https://cdn.pixabay.com/photo/2015/04/23/22/00/tree-736885_960_720.jpg")


