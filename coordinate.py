class Coordinate:
    def __init__(self,i,j):
        """
        init for coordinate object
        :param i: index i
        :param j: index j
        """
        self.__i = i
        self.__j = j

    def get_i(self):
        """
        get i
        :return: index i
        """
        return self.__i

    def get_j(self):
        """
        get j
        :return: index j
        """
        return self.__j
