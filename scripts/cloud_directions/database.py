import sqlite3

class Database():
    name = "cloud_directions_database.db"
    connection = None
    debug = False

    def __init__(self, debug) -> None:
        self.debug = debug
        if (self.debug):
            print ("### Opening the database connection ###")
        self.connection = sqlite3.connect(self.name)

    def close(self) -> None:
        if (self.debug):
            print ("### Closing the database connection ###")
        self.connection.close()

    def dropTable(self, tableName):
        if (self.debug):
            print ("### Droping the table "+tableName+"")
        self.connection.execute("DROP TABLE "+tableName)
        self.connection.commit()

    def selectClouds(self, iteration):
        if (self.debug):
            print ("### Selecting clouds - iteration "+str(iteration)+" ###")
        return self.connection.execute("SELECT id, x, y, width, height, cloud_cover, iteration_id, parent_id "+
        " FROM cloud WHERE iteration_id = "+str(iteration)+" ORDER BY id")

    def selectAllClouds(self):
        if (self.debug):
            print ("### Selecting all clouds ###")
        return self.connection.execute("SELECT id, x, y, width, height, cloud_cover, iteration_id, parent_id "+
        " FROM cloud ORDER BY id")

    def updateCloud(self, cloudId, parentId) -> None:
        if (self.debug):
            print ("### Updating cloud - "+str(cloudId)+" ###")
        self.connection.execute("UPDATE cloud SET parent_id = "+str(parentId)+" WHERE id = "+str(cloudId)+" ")
        self.connection.commit()

    def createCloud(self, cloud) -> None:
        if (self.debug):
            print ("### Creating the cloud ###")

        self.connection.execute("INSERT INTO cloud (x, y, width, height, cloud_cover, iteration_id, parent_id)"+
        "VALUES ("+str(cloud.x)+", "+str(cloud.y)+", "+str(cloud.width)+", "+str(cloud.height)+", "+str(cloud.cloudCover)+", "+str(cloud.iterationId)+", "+str(cloud.parentId)+")");
        self.connection.commit()

    def initialize(self):
        if (self.debug):
            print ("### Creating the tables ###")
        self.connection.execute("CREATE TABLE cloud (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,"+
                                                    "x INTEGER NOT NULL,"+
                                                    "y INTEGER NOT NULL,"+
                                                    "width INTEGER NOT NULL,"+
                                                    "height INTEGER NOT NULL,"+
                                                    "cloud_cover INTEGER NOT NULL,"+
                                                    "iteration_id INTEGER NOT NULL,"+
                                                    "parent_id INTEGER);")