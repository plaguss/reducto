# distutils: language=c++
# cython: c_string_type=unicode, c_string_encoding=utf8
# cython: language_level=3


# TODO: Should work with cimport
# from reducto.ext.line_wrap cimport Line

from libcpp.string cimport string
from libcpp cimport bool


# cdef extern from "_line.cpp":
#     pass


cdef extern from "_line.h" namespace "Reducto":
    cdef cppclass Line:
        Line(const string&) except +
        string get_line()
        int indentation_level()
        bool is_comment()
        bool is_blank_line()
        bool is_def_start()
        bool is_def_end()
        bool is_class_start()
        bool is_docstring_start()
        bool is_docstring_end()


cdef class PyLine:
    cdef Line* _thisptr

    def __cinit__(self, const string& l):
        self._thisptr = new Line(l)

    def __dealloc__(self):
        if self._thisptr != NULL:
            del self._thisptr

    def get_line(self):
        return self._thisptr.get_line()

    def indentation_level(self):
        return self._thisptr.indentation_level()

    def is_comment(self):
        return self._thisptr.is_comment()

    def is_blank_line(self):
        return self._thisptr.is_blank_line()

    def is_def_start(self):
        return self._thisptr.is_def_start()

    def is_def_end(self):
        return self._thisptr.is_def_end()

    def is_class_start(self):
        return self._thisptr.is_class_start()

    def is_docstring_start(self):
        return self._thisptr.is_docstring_start()

    def is_docstring_end(self):
        return self._thisptr.is_docstring_end()
