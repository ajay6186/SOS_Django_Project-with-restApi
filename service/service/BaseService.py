from abc import ABC, abstractmethod


class BaseService(ABC):
    def __init__(self):
        self.pageSize = 5

    def get(self, pk):
        try:
            m = self.get_model().objects.get(id=pk)
            return m
        except self.get_model().DoesNotExist:
            return None

    def preload(self, rid):
        try:
            r = self.get_model().objects.all()
            return r
        except self.get_model().DoesNotExist:
            return None

    def save(self, mObj):
        if mObj.id == 0:
            mObj.id = None
        mObj.save()

    def delete(self, mid):
        m = self.get(mid)
        m.delete()

    @abstractmethod
    def get_model(self):
        pass
