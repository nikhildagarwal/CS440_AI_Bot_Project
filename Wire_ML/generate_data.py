from diagram import Diagram
from unsafe_diagram import UnsafeDiagram


class Generate:
    """
    Class to generate diagrams for task 1
    """
    def __init__(self, sample_count):
        """
        Takes an input of the sample count and generates that many diagrams
        :param sample_count: integer number of samples
        """
        self.images = []
        self.labels = []
        self.intersections = []
        for _ in range(sample_count):
            d = Diagram() # generate diagram
            self.images.append(d.image)
            self.labels.append(d.label)
            self.intersections.append(d.intersections)


class GenerateUnsafe:
    """
    Class to generate unsafe diagrams for task2
    """
    def __init__(self, sample_count):
        """
        Takes an input of the number of samples we want to generate
        :param sample_count: integer number of samples
        """
        self.images = []
        self.labels = []
        self.intersection_list = []
        self.answer = []
        for _ in range(sample_count):
            d = UnsafeDiagram() # generate unsafe diagram
            self.images.append(d.image)
            self.labels.append(d.label)
            self.intersection_list.append(d.intersections)
            self.answer.append(d.ans)
