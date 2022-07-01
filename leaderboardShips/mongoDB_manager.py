#MONGO IS NOT THE OPTIMAL CHOICE, IK, BUT IT'S FREE SO I'LL USE IT
import copy

from bson import ObjectId
from pymongo import MongoClient

class mongo_manager:

    client=None

    def __init__(self,conn_string):
        try:
            self.client = MongoClient(conn_string)
        except:
            print("Something went wrong with the database connection")

    def __get_leaderboard_coll__(self):
        try:
            mydb = self.client["db_leaderboard"]
            mycol = mydb["leaderboard"]
            return mycol
        except:
            print("Something went wrong with the database connection")

    def __get_collection__(self):
        try:
            mydb = self.client["db_leaderboard"]
            mycol = mydb["users_ship"]
            return mycol
        except:
            print("Something went wrong with the database connection")


    def insert_full_user_ships(self,dict_to_insert):
        try:
            self.__get_collection__().insert_one(dict_to_insert)
        except Exception as e:
            print(e)

    def get_drop_by_name(self,name):
        path="ships.ship.drops."+name
        return self.__get_collection__().find({path:{"$exists":1}})


    def get_full_from_eid(self,eid):
        try:
            return self.__get_collection__().find_one({'EID':eid})
        except Exception as e:
            print(e)

    def user_exists(self, encryptedEID):
        try:
            res= self.__get_collection__().find_one({'EID':encryptedEID})
            if res is None:
                return False
            else:
                return True
        except Exception as e:
            print(e)

    def get_all_encrypted_IDs(self):
        array_id = self.__get_collection__().find({}, {"EID": 1})
        return array_id

    def get_ID_ships_already_stored(self,encryptedEID):
        ships = self.__get_collection__().find({"EID": encryptedEID}, {"ships": 1})
        list_already_stored = []
        for el in ships:
            for i in range(len(el["ships"])):
                list_already_stored.append(el["ships"][i]["identifier"])
        return list_already_stored

    def update_and_return_user_ships(self, final_dict, encryptedEID):
        list_already_stored=self.get_ID_ships_already_stored(encryptedEID)
        to_append=[]
        for el in final_dict["ships"]:
            if el["identifier"] not in list_already_stored:
                to_append.append(el)
        if len(to_append) > 0:
            print("Inserting "+str(len(to_append))+" new ships to the database")
            #get old doc
            doc=self.get_full_from_eid(encryptedEID)
            #contains a dict of only the new ships
            to_return=copy.deepcopy(doc)
            to_return["ships"]=to_return["ships"].clear()
            to_return["ships"]=[]
            for el in to_append:
                doc["ships"].append(el)
                to_return["ships"].append(el)
            self.__get_collection__().delete_one({"EID":encryptedEID})
            self.__get_collection__().insert_one(doc)
            return to_return
        else:
            return None

    def get_leaderboard_stone_ingr(self):
        try:
            return self.__get_leaderboard_coll__().find_one({"_id":ObjectId("62bea7e7103e3eb4639db3ea")})
        except Exception as e:
            print(e)

    def load_updated_document(self, leaderboard_updated,id):
        try:
            self.__get_leaderboard_coll__().delete_one({"_id":id})
            self.__get_leaderboard_coll__().insert_one(leaderboard_updated)
            print("Leaderboard updated")
        except Exception as e:
            print(e)

    def get_leaderboard_full_ingredients(self):
        try:
            return self.__get_leaderboard_coll__().find_one({"_id": ObjectId("62bc1395103e3eb463ae2df6")})
        except Exception as e:
            print(e)

