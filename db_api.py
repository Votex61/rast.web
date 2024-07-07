import sqlite3

db = None
cursor = None

def db_open():
    global db, cursor
    db = sqlite3.connect("skins.db")
    cursor = db.cursor()
    cursor.execute("""PRAGMA foreign_keys=on""")

def db_close():
    db.commit()
    cursor.close()
    db.close()

def db_create():
    db_open()
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS user(
                        id INTEGER PRIMARY KEY,
                        name VARCHAR,
                        login VARCHAR,
                        password VARCHAR,
                        mail VARCHAR
                   )""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS category(
                        id INTEGER PRIMARY KEY,
                        title VARCHAR
                   )""")
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS skin(
                        id INTEGER PRIMARY KEY,
                        title VARCHAR,
                        info VARCHAR,
                        prise VARCHAR,
                        id_category INTEGER,
                        url_image VARCHAR,
                        FOREIGN KEY (id_category) REFERENCES category(id)
                   )""")
    
    db_close()
 
def db_del():
    db_open()
    cursor.execute("""DROP TABLE user""")
    cursor.execute("""DROP TABLE skin""")
    cursor.execute("""DROP TABLE category""")
    db_close()

#===================================== user =====================================================
def reg_user(name:str, login:str, password:str, mail:str):
    """login_user -> [id]"""
    last_id = None

    db_open()
    
    cursor.execute("""SELECT login, mail
                        FROM user
                        WHERE login == ? 
                            OR mail == ?
                    """,(login, mail))
    data = cursor.fetchall()

    if data == None or len(data) == 0:
        cursor.execute("""INSERT INTO user(name, login, password, mail)
                            VALUES (?, ?, ?, ?) 
                        """,(name, login, password, mail))
        last_id = cursor.lastrowid

    db_close()
    
    return last_id

def login_user(login:str, password:str):
    """login_user -> [id]"""
    db_open()
    cursor.execute("""SELECT id
                        FROM user
                        WHERE login == ? 
                            AND password == ?
                    """,(login,password))
    data = cursor.fetchone()
    db_close()
    return data

def get_user(id:int):
    """get_user -> [name, login, mail]"""
    db_open()
    cursor.execute("""SELECT name, login, mail
                        FROM user
                        WHERE id == ? 
                    """,(id,))
    data = cursor.fetchone()
    db_close()
    return data
#===================================== category =================================================
def add_category(title:str):
    "return id"
    db_open()
    cursor.execute("""INSERT INTO category(title)
                            VALUES (?)  
                   """,(title,))
    last_id = cursor.lastrowid
    db_close()
    return last_id

def get_category(id:int):
    "id, title"
    db_open()
    cursor.execute("""SELECT id, title
                        FROM category
                        WHERE id == ?  
                   """,(id,))
    data = cursor.fetchone()
    db_close()
    return data

def get_all_category():
    "id, title"
    db_open()
    cursor.execute("""SELECT id, title
                        FROM category
                   """)
    data = cursor.fetchall()
    db_close()
    return data
#===================================== skin ==================================================
def add_skin(title:str, info:str, prise:float, id_category:int,url_image:str):
    "add_skin -> id"
    db_open()
    cursor.execute("""INSERT INTO skin(title, info, prise, id_category, url_image)
                            VALUES (?,?,?,?,?) 
                   """,(title, info, prise, id_category, url_image))
    last_id = cursor.lastrowid
    db_close()
    return last_id

def get_skin(id:int):
    " get_skin -> [skin.id, skin.title, skin.info, skin.prise, category.title, skin.url_image] "
    db_open()
    cursor.execute("""SELECT skin.id, skin.title, skin.info, skin.prise, category.title, skin.url_image
                        FROM skin, category
                        WHERE skin.id_category == category.id 
                            AND  skin.id == ?  
                   """,(id,))
    data = cursor.fetchone()
    db_close()
    return data

def get_all_skin():
    " get_all_skin -> [(id, title, info, prise, id_category, url_image), ...] "
    db_open()
    cursor.execute("""SELECT id, title, info, prise, id_category, url_image
                        FROM skin
                   """)
    data = cursor.fetchall()
    db_close()
    return data

def get_form_category_skin(id_category:int):
    "get_form_category_skin -> [(id, title, info, prise, id_category, url_image), ...] "
    db_open()
    cursor.execute("""SELECT id, title, info, prise, id_category, url_image
                        FROM skin
                        WHERE id_category == ?  
                   """,(id_category,))
    data = cursor.fetchall()
    db_close()
    return data

#===================================== create ===================================================
if __name__ == "__main__":
    # db_del()
    db_create()
    if True:
        reg_user("Voter1", "Votex1", "1337", "Voter@gmail.com")
        reg_user("Voter2", "Votex2", "1337", "Voter@gmail.com")
        reg_user("Voter3", "Votex3", "1337", "Voter@gmail.com")

        add_category("Weapons") # id = 1
        add_category("Deployable") # id = 2
        add_category("Clothing") # id = 3


        add_skin("""Apocalyptic Roadsign Gloves""",
                 """This is a skin for the Roadsign Gloves item. You will be able to apply this skin at a repair bench or when you craft the item in game.""",
                 """0.99$""",
                 3,
                 "https://rustlabs.com/img/skins/324/59107.png")
        add_skin("""Royal Safari AR""",
                 """This is a skin for the Assault Rifle item. You will be able to apply this skin at a repair bench or when you craft the item in game.""",
                 """3.49$""",
                 1,
                 """https://rustlabs.com/img/skins/324/59108.png""")
        add_skin("""Stone Pick Axe from Hell""",
                 """This skin glows in the dark

                This is a skin for the Stone Pickaxe item. You will be able to apply this skin at a repair bench or when you craft the item in game.""",
                 """2.49$""",
                 1,
                 """https://rustlabs.com/img/skins/324/59105.png""")


        add_skin("""Black Diamond Thompson""","""This is a skin for the Thompson item. You will be able to apply this skin at a repair bench or when you craft the item in game.""",
                 """"2.20$""",
                 1,
                 """https://wiki.rustclash.com/img/skins/324/58709.png """)
        
        add_skin("""Abyss Boots""","""This is a skin for the Boots item. You will be able to apply this skin at a repair bench or when you craft the item in game.""",
                 """1.62$""", 
                 3,
                 """https://wiki.rustclash.com/img/skins/324/58604.png""")
        
        add_skin("""Toxic Armored Double Door""","""This skin glows in the dark
                This is a skin for the Armored Double Door item. You will be able to apply this skin at a repair bench or when you craft the item in game.""",
                "$2.90",
                2,
                 """ https://wiki.rustclash.com/img/skins/324/58601.png""")
        
        add_skin("""Quarantine Garage Door""",
                """This is a skin for the Garage Door item. You will be able to apply this skin at a repair bench or when you craft the item in game.""",
                """1.59$""",
                2,
                """https://wiki.rustclash.com/img/skins/324/58902.png""")
        
        add_skin("""Blackguard Facemask""",
                 """ This is a skin for the Metal Facemask item. You will be able to apply this skin at a repair bench or when you craft the item in game.""",
                 """0.96$""",
                 3,
                 """https://wiki.rustclash.com/img/skins/324/58509.png""")
        
        add_skin("""Ice Eye Hatchet""",
                 """This is a skin for the Hatchet item. You will be able to apply this skin at a repair bench or when you craft the item in game.""",
                 """ 1.19$""",
                 1,
                 """https://wiki.rustclash.com/img/skins/324/58800.png""")
        
        add_skin("""Blinds Rug""",
                 """This is a skin for the Rug item. You will be able to apply this skin at a repair bench or when you craft the item in game. """,
                 """2.49$""",
                 2,
                 """https://wiki.rustclash.com/img/skins/324/58503.png
                 """)
        
        add_skin("""Watcher of Doom Metal Door""",
                 """This is a skin for the Sheet Metal Door item. You will be able to apply this skin at a repair bench or when you craft the item in game.""",
                 """1,07$""",
                 2,
                 """https://wiki.rustclash.com/img/skins/324/58408.png""")
        
        add_skin("""Bullseye LR300""",
                """Breaks down into 1 x Metal""",
                """0.91$""",
                1,
                """"https://wiki.rustclash.com/img/skins/324/58302.png""")
        
        add_skin("""Mr.Craboo Bandana""","""This is a skin for the Bandana Mask item. You will be able to apply this skin at a repair bench or when you craft the item in game.""",
                 """0.64$""",
                 3,
                 """https://wiki.rustclash.com/img/skins/324/58107.png""")
        
        add_skin("""Mr.Craboo Poncho""",
                 """ This is a skin for the Hide Poncho item. You will be able to apply this skin at a repair bench or when you craft the item in game.""",
                 """0.92$""",
                 3,
                 """https://wiki.rustclash.com/img/skins/324/58106.png""")
        
        add_skin("""Red Armored Container Door""",
                 """This is a skin for the Armored Door item. You will be able to apply this skin at a repair bench or when you craft the item in game. """,
                 """1.06$""",
                 2,
                 """https://wiki.rustclash.com/img/skins/324/56800.png""",) 
        
        add_skin("""Serpent AR""",""""This is a skin for the Assault Rifle item. You will be able to apply this skin at a repair bench or when you craft the item in game.""",
                 
        """0.99$""",
        1,
        """https://wiki.rustclash.com/img/skins/324/57407.png""")

        add_skin("""Valentine's Gift Sleeping Bag""","""This is a skin for the Sleeping Bag item. You will be able to apply this skin at a repair bench or when you craft the item in game.""",
                 
        """1.36$""",
        2,
        """https://wiki.rustclash.com/img/skins/324/57111.png""")

        add_skin("""Abyss Roadsign Gloves""","""This is a skin for the Roadsign Gloves item. You will be able to apply this skin at a repair bench or when you craft the item in game.""",
                 
        """4.58$""",
        3,
        """https://wiki.rustclash.com/img/skins/324/56710.png""")

        add_skin("""Pirate Large Box""","""This is a skin for the Large Wood Box item. You will be able to apply this skin at a repair bench or when you craft the item in game.""",
                 
        """1.60$""",
        2,
        """https://wiki.rustclash.com/img/skins/324/56604.png""")

        add_skin("""Pirate Facemask""","""This is a skin for the Metal Facemask item. You will be able to apply this skin at a repair bench or when you craft the item in game.""",
                 
        """1.87$""",
        3,
        """https://wiki.rustclash.com/img/skins/324/53505.png""")

        add_skin("""Pirate Chestplate""","""This is a skin for the Metal Chest Plate item. You will be able to apply this skin at a repair bench or when you craft the item in game.""",
                 
        """1.08$""",
        3,
        """https://wiki.rustclash.com/img/skins/324/53504.png""")

        add_skin("""Abyss Facemask""","""This is a skin for the Metal Facemask item. You will be able to apply this skin at a repair bench or when you craft the item in game.""",
                 
        """1.08$""",
        3,
        """https://wiki.rustclash.com/img/skins/324/54301.png""")

        add_skin("""Prototype 7164 Thompson""","""This is a skin for the Thompson item. You will be able to apply this skin at a repair bench or when you craft the item in game.""",
                 
        """1.68$""",
        1,
        """https://wiki.rustclash.com/img/skins/324/59000.png""")

        
        add_skin("""Prototype 7164 Thompson""","""This is a skin for the Thompson item. You will be able to apply this skin at a repair bench or when you craft the item in game.""",
                 
        """1.68$""",
        1,
        """https://wiki.rustclash.com/img/skins/324/59000.png""")



        









        











                      
        
        
        
        

        
        







        
        

                

         