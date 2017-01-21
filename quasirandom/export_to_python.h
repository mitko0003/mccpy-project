#pragma once

#include <Python.h>
#include <math.h>

#define STRING(x) #x
#define JOIN(x, y) x##y

#define EXPORT_TO_PYTHON(name, function) \
\
static PyObject *JOIN(name, Error); \
static int s_nSeed = 766993126; \
 \
static PyObject* seed(PyObject *self, PyObject *args) \
{ \
    int seed = 0; \
 \
    if (!PyArg_ParseTuple(args, "i", &seed)) \
    { \
        PyErr_SetString(JOIN(name, Error), "Invalid function arguments"); \
        return nullptr; \
    } \
 \
    s_nSeed = seed; \
 \
    Py_RETURN_NONE; \
} \
 \
static PyObject* random(PyObject *self, PyObject *args) \
{ \
    int dim_num = 0; \
 \
    if (!PyArg_ParseTuple(args, "i", &dim_num)) \
    { \
        PyErr_SetString(JOIN(name, Error), "Invalid function arguments"); \
        return nullptr; \
    } \
 \
    if (dim_num < 2) \
    { \
        PyErr_SetString(JOIN(name, Error), "Invalid dimensions number (>= 2)"); \
        return nullptr; \
    } \
 \
    double* pVector = new double[dim_num];     \
    if (pVector == nullptr) \
    { \
        PyErr_SetString(JOIN(name, Error), "Failed to allocate memory for random vector generation"); \
        return nullptr; \
    } \
 \
    function(dim_num, &s_nSeed, pVector); \
 \
    PyObject* pResult = PyTuple_New(dim_num); \
    if (!pResult) \
    { \
        delete[] pVector; \
        PyErr_SetString(JOIN(name, Error), "Failed to create output tuple"); \
	return nullptr; \
    } \
    for (int i = 0; i < dim_num; ++i)  \
    { \
	PyObject *pFloat = PyFloat_FromDouble(fabs(pVector[i])); \
	if (!pFloat)  \
        { \
            delete[] pVector; \
	    Py_DECREF(pResult); \
            PyErr_SetString(JOIN(name, Error), "Failed to create output float"); \
	    return nullptr; \
	} \
	PyTuple_SET_ITEM(pResult, i, pFloat); \
    } \
 \
    delete[] pVector; \
 \
    return pResult; \
} \
 \
static PyMethodDef JOIN(name, _methods)[] = { \
    { "random", random, METH_VARARGS, "Generate N dimensional random vector" }, \
    { "seed", seed, METH_VARARGS, "Seed the random generator" }, \
    { nullptr, nullptr, 0, nullptr } \
}; \
 \
static struct PyModuleDef JOIN(name, module) = { \
    PyModuleDef_HEAD_INIT, \
    #name, \
    nullptr, \
    -1, \
    JOIN(name, _methods) \
}; \
 \
PyMODINIT_FUNC JOIN(PyInit_, name)(void) \
{ \
    PyObject *pmodule = PyModule_Create(&JOIN(name, module)); \
 \
    if (pmodule == nullptr) \
        return nullptr; \
 \
    JOIN(name, Error) = PyErr_NewException(STRING(JOIN(faure, .error)), NULL, NULL); \
    Py_INCREF(JOIN(name, Error)); \
    PyModule_AddObject(pmodule, "error", JOIN(name, Error)); \
 \
    return pmodule; \
} \
