# distutils: language=c++
# cython: c_string_type=unicode, c_string_encoding=utf8
# cython: language_level=3


from cython.operator cimport dereference as deref
from libcpp.string cimport string
from libcpp.vector cimport vector


cdef extern from "_pyfile.h" namespace "Reducto":

    cdef cppclass FileStats:
        int number_of_lines
        int max_line_length
        int docstrings
        int comment_lines
        int blank_lines
        vector[int] functions

    cdef cppclass PyFileCpp:
        PyFileCpp() except +
        PyFileCpp(const string&) except +
        void collect()
        int number_of_functions()
        int number_of_lines()
        int number_of_comment_lines()
        int number_of_blank_lines()
        int number_of_docstring_lines()
        int get_max_line_length()
        void get_functions()
        # void grab_functions_info()
        # void print_functions_info()
        dict stats()
        # FileStats stats();  # TODO: Y este?


cdef class PyFile:
    cdef PyFileCpp* _thisptr

    def __cinit__(self, const string& f):
        self._thisptr = new PyFileCpp(f)

    def __dealloc__(self):
        if self._thisptr != NULL:
            del self._thisptr

    def collect(self):
        return self._thisptr.collect()

    def number_of_functions(self):
        return self._thisptr.number_of_functions()

    def number_of_lines(self):
        return self._thisptr.number_of_lines()

    def number_of_comment_lines(self):
        return self._thisptr.number_of_comment_lines()

    def number_of_blank_lines(self):
        return self._thisptr.number_of_blank_lines()

    def number_of_docstring_lines(self):
        return self._thisptr.number_of_docstring_lines()

    def get_max_line_length(self):
        return self._thisptr.get_max_line_length()

    cdef dict _stats(self):
        FileStats _stats = self._thisptr.stats()
        cdef dict results

        results = {
            "number_of_lines": _stats.number_of_lines,
            "max_line_length": _stats.max_line_length,
            "docstrings": _stats.docstrings,
            "comment_lines": _stats.comment_lines,
            "blank_lines": _stats.blank_lines,
            "function_lengths": _stats.funtions
        }

        return results

    def stats(self):
        # TODO: Ayuda con FileStats
        # Tendría que ser un cpdef para devolver Python/Cpp!
        # https://groups.google.com/g/cython-users/c/39Nwqsksdto
        # https://stackoverflow.com/questions/63570432/dectlaration-of-function-that-returns-dictionary-in-cython
        # https://stackoverflow.com/questions/9781572/c-struct-inheritance-in-cython
        return self._stats()
        # TODO: acceder a la info internamente y devolver dict
