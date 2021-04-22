# -*- coding: utf-8 -*-
class _const:
    class ConstError(TypeError): pass

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError("Can't rebind const (%s)" % name)
        self.__dict__[name] = value


const = _const()
const.PI = 3
const.PI1 = 3.14
print(type(const.PI))
print(type(const.PI1))
