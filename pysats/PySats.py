import os

class PySats:
    __instance = None

    @staticmethod 
    def getInstance():
        """ Static access method. """
        if PySats.__instance == None:
            PySats()
        return PySats.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if PySats.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            import jnius_config
            jnius_config.set_classpath(
                '.', os.path.join('lib', '*'))
            PySats.__instance = self
    
    def create_lsvm(self, seed=None, number_of_national_bidders=1, number_of_regional_bidders=5):
        from Lsvm import _Lsvm
        return _Lsvm(seed, number_of_national_bidders, number_of_regional_bidders)
