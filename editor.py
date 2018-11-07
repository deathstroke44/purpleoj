import abc


class Editor(object):
    languages = ["Java", "C", "Python"]
    __metaclass__ = abc.ABCMeta

    # @abc.abstractmethod
