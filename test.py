#import MyIn

#tags = []
#session = goScrap()
#session.start(tags, likes)
class Test:
    def __init__(self):
        print('start')

    def start(self, tags, likes_per_tag):
        self.tags = tags
        self.likes_per_tag = likes_per_tag
        print(self.tags)
        print(self.likes_per_tag)

session = Test()
session.start(['111', 'dsfa'], 88)