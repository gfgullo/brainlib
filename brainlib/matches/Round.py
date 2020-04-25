from .Time import Time


class Round:
    def __init__(self, raw: dict, time_object: Time = Time()):
        """
        Questa classe definisce uno dei tre  round, per uno dei due utenti del Match.

        un round è formato dalle seguenti componenti:

        - max_deadline  ->  corrisponde alla massima scadenza del round (24h)
        - deadline      ->  deadline calcolato dal momento dell'apertura del round.
        - time_end      ->  indica il tempo esatto in cui l'utente ha dato la risposta
                            questo tempo può essere 0, in tal caso l'utente non ha risposto.
        - time_start    ->  questo tempo rappresenta il momento di apertura del round
        - time_virew    ->  questo tempo rappresenta il momento esatto in cui l'utente
                            ha aperto il round
        - notification  ->  unboolean che indica se l'utente ha ricevuto notifica
                            per questo round nel caso di prossima scadenza (1 ora)
        - helps         -> dizzionario con gli aiuti
                            - suggestion
                            - remove
                            - reveals
                            sono tutte e tre chiavi con valore booleano e rappresenta il true
                            se l'aiuto è stato usato

        :param raw: Rappresentazione dizionario del Round
        """
        self.max_deadline = raw.get("max_deadline", 0)
        self.deadline = raw.get("deadline", 0)
        self.time_end = raw.get("time_end", 0)
        self.__time: Time = time_object
        self.time_start = raw.get("time_start", 0)
        self.notification = raw.get("notification", False)
        self.time_view = raw.get("time_view", 0)
        self.helps: dict = {
            "remove": raw.get("helps", {}).get("remove", False),
            "reveals": raw.get("helps", {}).get("reveals", False),
            "suggestion": raw.get("helps", {}).get("suggestion", False)
        }
        self.errors = raw.get("errors", 0)

    def to_dict(self) -> dict:
        return {
            "helps": self.helps,
            "max_deadline": self.max_deadline,
            "time_end": self.time_end,
            "time_start": self.time_start,
            "deadline": self.deadline,
            "errors": self.errors,
            "notification": self.notification,
            "time_view": self.time_view
        }

    def open(self, tick: int = None):
        if tick is None:
            tick = self.__time.now
        if self.time_start == 0:
            self.time_start = tick
            self.time_view = 0
            self.deadline = tick + self.__time.day

    def close(self, tick: int = None):
        if tick is None:
            tick = self.__time.now

        if self.time_end == 0:
            self.time_end = self.when_deadline()
            if self.time_start == 0:
                self.time_start = tick - self.__time.day
            if self.time_view == 0:
                self.time_view = tick - self.__time.day

    def is_close(self) -> bool:
        """
        riporta se il round è chiuso
        :return:
        """
        now = int(self.__time.now)
        if self.time_end > 0:
            return True
        if now > self.when_deadline():
            return True
        else:
            return False

    def when_deadline(self) -> int:
        """
        Questo metodo riporta l'esatta scadenza del round tra
        deadeolin || max_deadline
        :return: int
        """
        if self.deadline > 0:
            return self.deadline
        else:
            return self.max_deadline

    def get_time_start(self) -> int:
        if self.time_start > 0:
            return self.time_start
        else:
            return self.max_deadline - (3600*24)

    def resolved(self) -> bool:
        if self.time_end == 0:
            return False
        if 0 < self.time_end < self.when_deadline():
            return True

        return False

    def resolved_in(self) -> int:
        """
        Questa funzione ritorna un valore int, che rappresenta il tempo
        impiegato dall'utente per rispondere e completare il round
        nella casualità che il valore ritoranato da questa funzione sia 0
        questo indica che il round non è stato risolto.
        :return:
        """
        if self.resolved():
            if self.time_view == 0:
                self.time_view = self.when_deadline() - self.__time.day

            result = self.time_end - self.time_view
            if result < 0:
                # controllo se  il risultato è negativo per evitare tempi non corretti
                result = result * -1

            if result <= self.__time.day:
                # controllo che il tempo sia minore di un giorno (tempo massimo)
                return result
            else:
                # print("(Round) BrainLib -> Attenzione!: {}".format(self.to_dict()), file=sys.stderr)
                return self.__time.day
        else:
            return 0

    def time_remaining(self) -> int:
        """
        Ritorna il tempo rimanente del round
        :return:
        """
        c = self.when_deadline() - int(self.__time.now)
        if c > 0:
            return c
        else:
            return 0
