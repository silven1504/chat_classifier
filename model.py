import utils

MODEL_PATH = 'tf_model.h5'


class Model:
    def __init__(self):
        self.model = utils.load_model(MODEL_PATH)

    def predict(self, data):
        tf_input = utils.make_batch(data)
        return (self.model.predict(tf_input) > 0.5).astype("int32")

    def predict_proba(self, data):
        tf_input = utils.make_batch(data)
        return self.model.predict(tf_input)
