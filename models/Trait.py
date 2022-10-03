class Trait:

    def __init__(self, domain: str, value: [str, dict]):
        self._domain = domain
        self.value = value
        self.name = self._domain.split('.')[-1]
