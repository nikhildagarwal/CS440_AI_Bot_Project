from diagram import Diagram


class Generate:
    def __init__(self, sample_count):
        self.images = []
        self.labels = []
        for _ in range(sample_count):
            d = Diagram()
            self.images.append(d.image)
            self.labels.append(d.label)
