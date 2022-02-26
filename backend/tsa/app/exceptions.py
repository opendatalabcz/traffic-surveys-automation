class NotFoundError(Exception):
    def __init__(self, table_name: str, record_id: int):
        self.args = ("Record not found.", table_name, record_id)
