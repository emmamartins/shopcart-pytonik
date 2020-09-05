from pytonik.Model import Model
from pytonik.Session import Session
from pytonik import Version
import ast

class Cart(Model):

    def __getattr__(self, item):
        return item

    def __init__(self):
        return None

    @staticmethod
    def find(item, key="", value=""):
        
        if Session().has(item) == True:
            
            try:
                d = Session().get(item)
                
                if key is "":
                    

                    k_dict, dict_kv= [],  {}
                    for nv in d:
                        fn = nv.items()
                        for k, v in fn:
                            dict_kv.update({k:v})
                        k_dict.append(dict_kv)
                    
                    return ast.literal_eval(k_dict)

                elif key != "" and value != "":
                    
                    bl = bool
                    for nv in d:

                        if Version.PYVERSION_MA >= 3:
                            fn = nv.items()
                        else:
                            fn = nv.iteritems()

                        for k, v in fn:
                            if key == k:
                                if value == v:
                                    bl=  True
                                else:
                                    bl =  False
                    return bl
                else:
                    
                    vals = []
                    for nv in d:
                        fn = nv.items()
                        for k, v in fn:
                            if key == k:
                                vals.append(v)
                        
                    return vals
            except Exception as err:
                return ""
        else:
            return ""

    @staticmethod
    def delete(item, key="", value=""):
        
        if Session().has(item) == True:
            list_item = Session().get(item)
            if key != "" and value != "":
                for i in range(len(list_item)):

                    if list_item[i][key] == value:
                        del list_item[i]
                        break
                if len(list_item) < 1:
                    Session().destroy(item)
                else:
                    Session().set(item, list_item)
                return True
            else:
                list_item.clear()
                if len(list_item) < 1:
                    Session().destroy(item)
                else:
                    Session().set(item, list_item)
                return True
        else:
            return ""
    @staticmethod
    def update(item, key= "", value="", newitem=""):

        if  Session().has(item) == True:
            itemv = Session().get(item)

            upnewitem = []
            for olditem in itemv:

                listnewitem = {}
                
                fn = olditem.items()
                
                for k, v in fn:

                    if k == key:
                        if olditem.get(k, '') == value:
                            olditem.update(newitem)
                    listnewitem.update(olditem)

                upnewitem.append(listnewitem)

            Session().set(item, upnewitem)
            return True

        else:
            return ""
