# distutils: language=c++
# cython: c_string_type=unicode, c_string_encoding=utf8
# cython: language_level=3


from cython.operator cimport dereference as deref
from libcpp.string cimport string
from libcpp.vector cimport vector


cdef extern from "_pyfile.h" namespace "Reducto":

    cdef cppclass FileStats:
        FileStats() except +

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

        # FileStats stats();  # TODO: Y este?

# cdef


cdef class PyFile:
    cdef PyFileCpp* _thisptr

    def __cinit__(self, const string& l):
        self._thisptr = new PyFileCpp(l)

    def __dealloc__(self):
        if self._thisptr != NULL:
            del self._thisptr

    property name:
        def __get__(self):
            return deref(self._thisptr).filename

        def __set__(self, _name):
            deref(self._thisptr).filename = _name

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

    def stats(self):
        # TODO: Ayuda con FileStats
        # Tendría que ser un cpdef para devolver Python/Cpp!
        # https://groups.google.com/g/cython-users/c/39Nwqsksdto
        cdef FileStats _stats = self._thisptr.stats()
        # TODO: acceder a la info internamente y devolver dict
