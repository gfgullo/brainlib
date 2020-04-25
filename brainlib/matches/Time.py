import time


class Time:

    def __init__(self, t=None):
        """
        Questa classe controlla il tempo, fornisce delle proprietà già
        settate che corrispondono al tempo: Giorni, ore, minuti e secondi
        inoltre fornisce un "now" che riporta il tempo attuale (time.time())
        in questo costruttore si può definire il parametro "t"
        che indica una cifra in secondi di un tempo arbitrario

        Time ritornerà quel numero al posto di Now.
        Questa funzionalità è usata solo in fase di Test per avere pieno
        controllo del tempo.
        :param t: Tempo in secondi
        """
        self.__time = t

    @property
    def day(self):
        return self.hour * 24

    @property
    def second(self):
        return 1

    @property
    def minute(self):
        return self.second * 60

    @property
    def hour(self):
        return self.minute * 60

    __time = 0

    @property
    def now(self) -> int:
        if self.__time is not None:
            return self.__time
        return int(time.time())

    def set__time(self, value: int):
        self.__time = value
