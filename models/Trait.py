from abc import abstractclassmethod


class Trait:
    __slots__ = ("_domain", "name")

    def __init__(self, domain: str):
        self._domain = domain
        self.name = self._domain.split(".")[-1]

    @abstractclassmethod
    def domain(cls):
        pass


class ConnectivityTrait(Trait):
    __slots__ = "_status"

    def __init__(self, data):
        if not data:
            self._status = "OFFLINE"
        else:
            self._status = data.get("status")
        super().__init__(self.domain)

    @classmethod
    def domain(cls):
        return "sdm.devices.traits.Connectivity"

    @property
    def status(self):
        return self._status

    @property
    def is_connected(self):
        return self._status == "ONLINE"
