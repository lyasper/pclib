#include <Python.h>
#include <stdio.h>
#include <stdlib.h>

static PyObject* stdout_line(PyObject* self,  PyObject* args)
{
 
    int setvbuf_mode; 
    setvbuf_mode = _IOLBF;
    if (setvbuf (stdout, NULL, setvbuf_mode, 0) != 0)
    {
      fprintf (stderr, "could not set buffering of std to mode line\n");
    }
    Py_RETURN_NONE;
}
 
static PyMethodDef HelloMethods[] =
{
     {"stdout_line", stdout_line, METH_NOARGS, "make stdout line buffered"},
     {NULL, NULL, 0, NULL}
};
 
PyMODINIT_FUNC
 
initstdbuf(void)
{
     (void) Py_InitModule("stdbuf", HelloMethods);
}
