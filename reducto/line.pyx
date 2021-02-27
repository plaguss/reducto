# distutils: language=c++
# cython: c_string_type=unicode, c_string_encoding=utf8
# cython: language_level=3


from line cimport Line


cdef class PyLine:
    cdef PyLine* thisptr

    def __cinit__(self, const string& line):
        self.thisptr = new Line(line)

    def __dealloc__(self):
        del self.thisptr

    def get_line(self):
        return self.thisptr.get_line()

    def indentation_level(self):
        return self.thisptr.indentation_level()

    def is_comment(self):
        return self.thisptr.is_comment()

    def is_blank_line(self):
        return self.thisptr.is_blank_line()

    def is_def_start(self):
        return self.thisptr.is_def_start()

    def is_def_end(self):
        return self.thisptr.is_def_end()

    def is_class_start(self):
        return self.thisptr.is_class_start()

    def is_docstring_start(self):
        return self.thisptr.is_docstring_start()

    def is_docstring_end(self):
        return self.thisptr.is_docstring_end()
