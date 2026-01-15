from database.DB_connect import DBConnect
from model.rifugio import Rifugio
from model.connessione2 import Connessione2

class DAO:
    """
        Implementare tutte le funzioni necessarie a interrogare il database.
        """
    # TODO

    @staticmethod
    def get_all_rifugi(anno):
        """
        Restituisce il dizionario di tutti i rifugi collegati da almeno un sentiero fino
        all'anno specificato.
        :param year: anno massimo da considerare
        """

        conn = DBConnect.get_connection()
        rifugi = {}

        cursor = conn.cursor(dictionary=True)
        query = """
        SELECT r.id, r.nome, r.localita, r.altitudine, r.capienza, r.aperto
        FROM rifugio r, connessione c
        WHERE anno <= %s AND (r.id = c.id_rifugio1 or r.id = c.id_rifugio2)
        ORDER BY r.nome
        """

        cursor.execute(query,(anno,))

        for row in cursor:
            if rifugi.get(row["id"]) is None:
                rifugi[row["id"]] = Rifugio(**row)

        cursor.close()
        conn.close()
        return rifugi

    @staticmethod
    def get_connessioni_dict(anno, rifugi):
        """
        Restituisce tutte le connessioni tra rifugi fino all'ano specificato.
        :param year: anno massimo da considerare
        :param rifugi: dizionario {rifugio_id: Rifugio} per associare gli oggetti al loro id
        """

        conn = DBConnect.get_connection()
        connessioni = {}

        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT id_rifugio1, id_rifugio2, distanza, difficolta, durata
            FROM connessione 
            WHERE anno <= %s 
            """

        cursor.execute(query, (anno,))

        for row in cursor:
            h1, h2 = sorted((row["id_rifugio1"], row["id_rifugio2"]))
            key = (h1, h2)

            if h1 is not None and h2 is not None and (h1, h2) not in connessioni:
                connessioni[h1, h2] = Connessione2(h1, h2, row["distanza"], row["difficolta"], row["durata"])

        cursor.close()
        conn.close()
        return connessioni

    @staticmethod
    def get_connessioni(anno, rifugi):
        """
        Restituisce tutte le connessioni tra rifugi fino all'ano specificato.
        :param year: anno massimo da considerare
        :param rifugi: dizionario {rifugio_id: Rifugio} per associare gli oggetti al loro id
        """

        conn = DBConnect.get_connection()
        connessioni = []

        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT id_rifugio1, id_rifugio2, distanza, difficolta, durata
            FROM connessione 
            WHERE anno <= %s 
            """

        cursor.execute(query, (anno,))

        for row in cursor:
            r1 = rifugi.get(row["id_rifugio1"])
            r2 = rifugi.get(row["id_rifugio2"])

            if r1 is not None and r2 is not None:
                connessioni.append(
                    Connessione2(r1, r2, row["distanza"], row["difficolta"], row["durata"]))

        cursor.close()
        conn.close()
        return connessioni
