if __name__ == '__main__':
    data =""
    with open("videos.json", "r+") as fp:
         data+=fp.read()
    last_open = data.rindex("{")
    data = data[:data.rindex("{")]
    data = data[:data.rindex(",")]
    data +="]"

    with open("videos.json", "w+") as fp:
        fp.write(data)


