import hashlib

class Data():

    def __init__(self, private_key="", data1="", data2=""):
        self.public_key = hashlib.sha256(private_key.encode()).hexdigest()
        self.data1 = data1
        self.data2 = data2

    def serialize(self):
        return {
            'public_key': self.public_key,
            'data1': self.data1,
            'data2': self.data2,
        }

    def required(self):
        return ['private_key', 'data1', 'data2']

if __name__ == "__main__":
    d = Data(data1='please', data2='help')
    print(d.__dict__)
    print(Data().__dict__.keys())