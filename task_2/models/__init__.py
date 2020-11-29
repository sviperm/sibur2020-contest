from abc import ABC, abstractmethod


class AbstractModel(ABC):
    @abstractmethod
    def load(self, *args, **kwargs):
        pass

    @abstractmethod
    def predict(self, name_1, name_2, *args, **kwargs):
        pass


class TensorflowModel(AbstractModel):
    """
    Tensorflow based classifier
    """

    def __init__(self) -> None:
        self.model = None

    def load(self, *args, **kwargs):
        """
        Load Tensorflow model
        """
        # TODO load model
        self.model = 'Tensorflow model'
        if ('debug' in kwargs) and (kwargs['debug']):
            print('tensorflow model loaded')

        return self

    def predict(self, name_1, name_2, *args, **kwargs):
        prediction = self.model.predict([name_1, name_2])
        return prediction
