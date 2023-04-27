import os
import pathlib


class PySats:
    __instance = None

    @staticmethod
    def getInstance():
        """
        Static access method.

        If you're getting a java.lang.NoClassDefFoundError, make sure you set the PYJNIUS_CLASSPATH variable correctly according to the README.
        """
        if PySats.__instance == None:
            PySats()
        return PySats.__instance

    def __init__(self):
        """Virtually private constructor."""
        if PySats.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            import jnius_config

            classpath = os.getenv(
                "PYJNIUS_CLASSPATH", pathlib.Path(__file__).parent.parent / "lib"
            )
            jnius_config.set_classpath(os.path.join(classpath, "*"))
            PySats.__instance = self

    def create_lsvm(
        self,
        seed=None,
        number_of_national_bidders=1,
        number_of_regional_bidders=5,
        isLegacyLSVM=False,
        store_files=False,
    ):
        from .lsvm import _Lsvm

        return _Lsvm(
            seed,
            number_of_national_bidders,
            number_of_regional_bidders,
            isLegacyLSVM,
            store_files,
        )

    def create_gsvm(
        self,
        seed=None,
        number_of_national_bidders=1,
        number_of_regional_bidders=6,
        isLegacyGSVM=False,
        store_files=False,
    ):
        from .gsvm import _Gsvm

        return _Gsvm(
            seed,
            number_of_national_bidders,
            number_of_regional_bidders,
            isLegacyGSVM,
            store_files,
        )

    def create_mrvm(
        self,
        seed=None,
        number_of_national_bidders=3,
        number_of_regional_bidders=4,
        number_of_local_bidders=3,
        store_files=False,
    ):
        from .mrvm import _Mrvm

        return _Mrvm(
            seed,
            number_of_national_bidders,
            number_of_regional_bidders,
            number_of_local_bidders,
            store_files,
        )

    def create_srvm(
        self,
        seed=None,
        number_of_small_bidders=2,
        number_of_high_frequency_bidders=1,
        number_of_secondary_bidders=2,
        number_of_primary_bidders=2,
        store_files=False,
    ):
        from .srvm import _Srvm

        return _Srvm(
            seed,
            number_of_small_bidders,
            number_of_high_frequency_bidders,
            number_of_secondary_bidders,
            number_of_primary_bidders,
            store_files,
        )
