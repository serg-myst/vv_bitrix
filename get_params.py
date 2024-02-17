class Params:
    def __init__(self, fields: list, params: dict):
        self.fields = fields
        self.params = params

    def add_select(self):
        self.params = dict((f'select[{ind}]', value) for ind, value in enumerate(self.fields))

    def add_filter(self, field: str, value: int | str):
        self.params[f"filter[{field}]"] = value

    def add_order(self, field: str, value: int | str):
        self.params[f"order[{field}]"] = value

    def get_params(self):
        return self.params


if __name__ == '__main__':
    ...
