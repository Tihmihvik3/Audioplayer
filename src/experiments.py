abc = None


def aa():
    print("aaaaaaaaaaaa")
    print("aaaaaaaaaaaa")
    print("aaaaaaaaaaaa")
    def bb():
        print("Hello")
        print("Hello")
        print("Hello")

    global abc
    abc = bb


aa()
abc()
