from dataclasses import dataclass
import datetime
from model.rifugio import Rifugio

@dataclass
class Connessione2:
    r1 : Rifugio
    r2 : Rifugio
    distanza : float = 0.0
    difficolta : str = "facile"
    durata : datetime.time = datetime.time(0, 0, 0)

    def __str__(self):
        return (f'Connessione({self.r1.nome} - {self.r2.nome},'
                f' distanza: {self.distanza} km, difficoltà: {self.difficolta}, '
                f' tempo {self.durata})')
