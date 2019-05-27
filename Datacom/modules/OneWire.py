class OneWire:
    MASTER_NAME = 'w1_bus_master1'
    BASE_PATH = '/sys/bus/w1/devices'

    @classmethod
    def make_path(cls, name):
        return '{}/{}/{}'.format(cls.BASE_PATH, cls.MASTER_NAME, name)

    @classmethod
    def slave_count(cls):
        # Lees het bestand w1_master_slave_count in, zet de inhoud ervan om naar een int en return die
        fo = open(cls.make_path("w1_master_slave_count"), 'r')
        aantal = 0
        for line in fo:
            aantal += int(line)

        return aantal

    @classmethod
    def list_slaves(cls):
        # Lees het bestand w1_master_slaves in. Het bevat 1 slave ID per regel. Return een 'list' van slave ID's
        slaveID = []
        fo = open(cls.make_path("w1_master_slaves"), 'r')
        for line in fo:
            fo.readline()
            line = line[0:len(line) - 2]
            slaveID.append(line)

        return slaveID

    @classmethod
    def get_slave(cls, slave_id):
        # Check eerst of de slave wel bestaat a.d.h.v de methode list_slaves() die je net schreef.
        # Indien niet raise je een ValueError.
        try:
            if slave_id in cls.list_slaves():
                cls.make_path(slave_id)
        except:
            raise ValueError("De slave bestaat niet.")
        finally:
            return OneWire.Slave(cls.MASTER_NAME, slave_id)

    class Slave:
        def __init__(self, master, slave_id):
            self.master = master
            self.id = slave_id

        def get_data(self):
            path = '{base}/{master}/{id}/w1_slave'.format(base=OneWire.BASE_PATH, master=self.master, id=self.id) #Path maken
            naam = "t=" # Naam die we zoeken in de lijnen
            var = "" # Dit wordt de gevonden waarde
            with open(path, 'r') as file:
                for line in file:
                    try:
                        karakter = line.find(naam)
                        var = line[karakter+2:] # +2 zodat naam weg is
                    except:
                        raise ValueError("Variable {0} not found!".format(var))
            print(var)

'''
def main():
    one = OneWire()
    print(one.slave_count())
    print(one.list_slaves())
    one.get_slave("28-0416c0a80aff").get_data()


if __name__ == '__main__':
    main()
'''