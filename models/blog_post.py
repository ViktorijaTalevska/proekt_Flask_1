class BlogPost:
    def __init__(self, name, title, content):
        self.name = name
        self.title = title
        self.content = content

    def __str__(self):
        return f"NAME = {self.name}\nTITLE = {self.title}\nCONTENT = {self.content}"