from database.DB_connect import DBConnect
from model.attore import DTO

class DAO():
    def __init__(self):
        pass

    #valori per riempire DPD
    @staticmethod
    def getallratings():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        res = []

        query="""select distinct r.avg_rating as rating
                    from ratings r
                    order by r.avg_rating """

        cursor.execute(query)

        for row in cursor.fetchall():
            res.append(row["rating"])

        cursor.close()
        cnx.close()

        return res

    #NODI
    @staticmethod
    def getnodes(input):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        res = []

        query = """ """

        cursor.execute(query, (input))

        for row in cursor.fetchall():
            res.append(DTO(**row))

        cursor.close()
        cnx.close()

        return res

    #ARCHI
    @staticmethod
    def getedges(input):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        res = []

        query = """ """

        cursor.execute(query, (input))

        for row in cursor.fetchall():
            res.append({"id1": row["id1"], "id2": row["id2"], "weight": row["weight"]})

        cursor.close()
        cnx.close()

        return res
