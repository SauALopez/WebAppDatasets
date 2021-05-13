class Sensors():
    def __init__(self, keys =["temperature","humidity","light", "voltage"]):

        self.metadata=0
        self.ids =[]

        self.keys =keys
        self.n_keys =len(keys)


        self.sensors =[]

    def create_sensor(self,id):            #CREATE A BASE DICTIONARY PEER id
        data = {}
        data["id"] =id
        for x in range(self.n_keys):        
            data[self.keys[x]]=  []
        return data

    def new_sensor(self,id):
        self.ids.append(id)
        self.sensors.append(self.create_sensor(id))

    def check(self,values):
        if len(values) == self.n_keys:
            return True
        else:
            return False

    def data_input(self,id,values):
        if self.check(values):
            self.metadata +=1
            if id in self.ids:
                data = self.sensors[self.ids.index(id)]                            #CHOIDE DICTIONARY FOR THE CORRECT 
                for k,v in values.items():
                    data[k].append(v)
            else:
                self.new_sensor(id)
                self.data_input(id,values)  

    def media(self,id, key):
        data = self.sensors[self.ids.index(id)]
        values = data[key]
        suma = sum(values)
        n = len(values)
        return round(suma/n,2)

    def mediana(self,id,key):
        data = self.sensors[self.ids.index(id)]
        values= data[key]
        values.sort()
        midle = int((len(values)-1)/2)
        return round(values[midle],2)

    def moda(self,id, key):
        data = self.sensors[self.ids.index(id)]
        values= data[key]
        count ={}
        values.sort()
        for v in values:
            if(count.get(v)==None):
                count[v]=1
            else:
                count[v]= count.get(v) +1
        m = (max(count,key=count.get))
        return round(m,2)
    
    def info(self,key):
        txt_ids = []
        modas = []
        medianas = []
        medias = []
        self.ids.sort()
        for id in self.ids:
            txt_ids.append("Sensor "+str(id))
            modas.append(self.moda(id,key))
            medianas.append(self.mediana(id,key))
            medias.append(self.media(id,key))

        return {"KEY":key, "IDS":txt_ids,"moda": modas, "mediana": medianas,"media": medias, "keys":self.keys}
