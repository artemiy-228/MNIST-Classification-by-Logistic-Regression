from joblib import load
from sklearn.ensemble import RandomForestClassifier
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt


class Predictor:
    model: RandomForestClassifier

    def __init__(self, model_name: str):
        self.model = load(model_name)

    @staticmethod
    def normalize(X: np.array) -> np.array:
        return (X - X.min()) / (X.max() - X.min())

    def guess_number_by_tree(self, image) -> str:
        image = image.convert('L')

        temp_image = np.array(image).reshape(1, 784)
        temp_image = self.normalize(temp_image)


        number = self.model.predict(temp_image)[0]

        return f"This number is {number}"


