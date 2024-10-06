from row_names import Groups


class NewEnumerator:
    # sub_enumerators = {}

    def __init__(self):
        self.sub_enumerators = {}



    def get_nr(self, type_name, group):
        if group not in self.sub_enumerators:
            self.sub_enumerators[group] = SubEnumerator()
        return self.sub_enumerators[group].get_nr(type_name)


    def get_nr_extract_group(self, type_name, type_key, gb, kb, rb, jf):
        tmp = -1

        if type_key=='KP' and ((gb and kb)or(gb and rb)or(kb and rb)):
            return self.get_nr(type_name, "X_ALL")
        if not gb and not kb and not rb and not jf:
            return self.get_nr(type_name, "X_ALL")
        if type_key == 'SAN':
            return self.get_nr(type_name, "X_ALL")

        if gb:
            tmp = self.get_nr(type_name, Groups.GB.value)
        if kb:
            tmpx = self.get_nr(type_name, Groups.KB.value)
            if tmp == -1 or tmp == tmpx:
                tmp = tmpx
            else:
                raise ValueError("Inconsistent numbering")
        if rb:
            tmpx = self.get_nr(type_name, Groups.RB.value)
            if tmp == -1 or tmp == tmpx:
                tmp = tmpx
            else:
                raise ValueError("Inconsistent numbering")
        if jf:
            tmpx = self.get_nr(type_name, Groups.JF.value)
            if tmp == -1 or tmp == tmpx:
                tmp = tmpx
            else:
                raise ValueError("Inconsistent numbering")

        return tmp


class SubEnumerator:

    def __init__(self):
        self.typeEnumerators = {}

    def get_nr(self, type_name):
        if type_name not in self.typeEnumerators:
            self.typeEnumerators[type_name] = 0
        self.typeEnumerators[type_name] += 1
        return self.typeEnumerators[type_name]