# file: userServiceDb.py
import psycopg2
from abc import ABC, abstractmethod
from models.dbAcessService import * 
import bcrypt

#when adding to DB
class UserAuthDataStructure():
    def __init__(self, name, email, uuid, isAdmin , password_hash) -> None:
        self.uuid = uuid
        self.name = name
        self.email = email
        self.isAdmin:bool = isAdmin
        self.password_hash:str = password_hash

    def printUserAuthDataStructure(self):
        return (print(f'{self.name} - {self.uuid} - {self.email} -{self.isAdmin}'))

#when returning data from db 
class UserAuthDBStructure(UserAuthDataStructure):
    def __init__(self, id, uuid, name, email, isAdmin, password_hash ) -> None:
        self.id = id
        super().__init__(name, email, uuid, isAdmin, password_hash)
        

#usser database interface -> calls on db access instance. 

class UserAuthDbLinkInterface(ABC):

    @abstractmethod
    def addUserAuth():
        None

    @abstractmethod
    def getUserAuthByEmail():
        None

    @abstractmethod
    def getUserAuthById():
        None

    @abstractmethod
    def updateUserAuth():
        None
        

class UserAuthDbLink(UserAuthDbLinkInterface):
    def __init__(self) -> None:
        self.dbAccessServiceInstance: DatabaseAcessInterface = PGDBAcessService()
  
    def addUserAuth(self, data:UserAuthDataStructure):
        self.dbAcessInstance:DatabaseAcessInterface = PGDBAcessService()
        command = f""" 
                    INSERT INTO userauth
                    (uuid, name, email, isAdmin, password_hash)
                    values
                    (%s, %s, %s, %s, %s)
                    """
        args = (data.uuid, data.name, data.email, data.isAdmin)
        self.dbAcessInstance.dbAdd(command, args)
        return True
    
    def createUserAuthTable(self, tableName:str):
        self.dbAcessInstance:DatabaseAcessInterface = PGDBAcessService()
        command = f"""
                    CREATE TABLE {tableName} (
                        id SERIAL PRIMARY KEY,
                        uuid TEXT NOT NULL,
                        name TEXT NOT NULL,
                        email TEXT NOT NULL,
                        isAdmin BOOLEAN, 
                        password_hash TEXT
                    );"""
        self.dbAcessInstance.dbCreateTable(command)
        return True

    def getUserAuthByEmail(self, emailId):
        searchQuery = f"SELECT * FROM userdata WHERE email = '{emailId}'"
        results:UserAuthDBStructure = UserAuthDBStructure(*self.dbAccessServiceInstance.dbReadRecord(searchQuery)[0])
        return results
    
    def getUserAuthById(self, id):
        searchQuery = f"SELECT * FROM userdata WHERE id = '{id}'"
        results:UserAuthDBStructure = UserAuthDBStructure(*self.dbAccessServiceInstance.dbReadRecord(searchQuery)[0])
        return results
    
    def updateUserAuth(self, data:UserAuthDBStructure):
        command = """
                        UPDATE userauth
                        SET 
                        name = %s,
                        email = %s,
                        isAdmin = %s,
                        password_hash = %s  
                        where id = %s       
                    """
        args = (data.name, data.email, data.isAdmin, data.password_hash, data.id)
        self.dbAccessServiceInstance.dbUpdateRecord(command, args)


#updatemain:UserAuthDBStructure = UserAuthDBStructure(1, '123', 'nikhil', 'nik.m1992@gmail.com', )., True)
# bcrypt.hashpw('test'.encode(), bcrypt.gensalt().decode()

__all__ = ['UserAuthDbLink','UserAuthDbLinkInterface', 'UserAuthDBStructure', 'UserAuthDataStructure']



