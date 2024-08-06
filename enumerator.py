class Enumerator:
    kp = 0
    mat = 0
    jf = 0
    akvk = 0
    asi = 0
    f = 0
    of = 0
    fu = 0
    kad = 0
    sp = 0
    b = 0

    def get_kp(self):
        self.kp += 1
        return ' ' + str(self.kp)

    def get_mat(self):
        self.mat += 1
        return ' ' + str(self.mat)

    def get_jf(self):
        self.jf += 1
        return ' ' + str(self.jf)

    def get_akvk(self):
        self.akvk += 1
        return ' ' + str(self.akvk)

    def get_asi(self):
        self.asi += 1
        return ' ' + str(self.asi)

    def get_f(self):
        self.f += 1
        return ' ' + str(self.f)

    def get_of(self):
        self.of += 1
        return ' ' + str(self.of)

    def get_fu(self):
        self.fu += 1
        return ' ' + str(self.fu)

    def get_kad(self):
        self.kad += 1
        return ' ' + str(self.kad)

    def get_sp(self):
        self.sp += 1
        return ' ' + str(self.sp)

    def get_b(self):
        self.b += 1
        return ' ' + str(self.b)

class GroupesEnumerator:
    enumerators = {
        'rb': Enumerator(),
        'kb': Enumerator(),
        'gb': Enumerator(),
        'jf': Enumerator(),
    }

    def get_kp(self,group):
        return self.enumerators[group].get_kp()

    def get_mat(self,group):
        return self.enumerators[group].get_mat()

    def get_jf(self,group):
        return self.enumerators[group].get_jf()

    def get_akvk(self,group):
        return self.enumerators[group].get_akvk()

    def get_asi(self,group):
        return self.enumerators[group].get_asi()

    def get_f(self,group):
        return self.enumerators[group].get_f()

    def get_of(self,group):
        return self.enumerators[group].get_of()

    def get_fu(self,group):
        return self.enumerators[group].get_fu()

    def get_kad(self,group):
        return self.enumerators[group].get_kad()

    def get_sp(self,group):
        return self.enumerators[group].get_sp()

    def get_b(self,group):
        return self.enumerators[group].get_b()
