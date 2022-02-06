
class FileReader:

    def __init__(self, path):
        self.path = path

    def read(self):
        try:
            with open(self.path, 'r') as f:
                return f.read()
        except FileNotFoundError:
            return ''


# reader = FileReader('not_exist_file.txt')
# text = reader.read()
# print(text)
# # ''
# with open('some_file.txt', 'w') as file:
#     file.write('some text')
#
# reader = FileReader('some_file.txt')
# text = reader.read()
# print(text)
# # 'some text'
# print(type(reader))
# # <class 'solution.FileReader'>