

class Result:
    def __init__(self, data, success):
        self.data = data
        self.success = success

    @staticmethod
    def failed(data):
        return Result(data, False)

    @staticmethod
    def success(data):
        return Result(data, True)

    def is_success(self):
        return self.success
