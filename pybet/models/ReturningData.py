class ReturningData:
    def __init__(self, ok:bool = True, data: any = None, error:any = None) -> None:
        self.ok = ok
        self.data:any = data
        self.error:any = error