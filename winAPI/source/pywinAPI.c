/* Coded with C Grammar for MSVC in Windows
   This Source uses UTF-8-BOM encoding & CRLF (Windows) line endings
   Alias : WinAPI.c & Last Modded : 2021.04.16.
   Windows NT API 함수를 정의한 파이썬 C 모듈 Coded by IRACK
*/

#include "C:\Program Files\Python39\include\Python.h"
#include <Windows.h>

// 참고 : https://choiseokwon.tistory.com/250?category=247927
// 참고 : https://docs.python.org/ko/3/c-api/arg.html#c.PyArg_UnpackTuple

static PyObject *gotoXY(PyObject *self, PyObject *arg); // 콘솔창 커서 좌표 이동 함수
static PyObject *wrIsX(PyObject *self, PyObject *arg); // 콘솔창 커서 X축(가로) 리턴 함수
static PyObject *wrIsY(PyObject *self, PyObject *arg); // 콘솔창 커서 Y축(세로) 리턴 함수
static PyObject *changeTxtColor(PyObject *self, PyObject *arg); // 콘솔창 글자 색 변경 함수
static PyObject *hideConsoleCursor(PyObject *self, PyObject *arg); // 콘솔창 커서 깜박임 제거 함수

static PyObject *gotoXY(PyObject *self, PyObject *arg) {
  PyObject *x;
  PyObject *y;
  if (!PyArg_UnpackTuple(arg, "i", 1, 2, &x, &y)) {
    PyErr_SetString(PyExc_ValueError, "Argument is not integers.");
    return NULL;
  } else {
    COORD position = {PyLong_AsLong(x), PyLong_AsLong(y)};
    SetConsoleCursorPosition(GetStdHandle(STD_OUTPUT_HANDLE), position); // Windows API 사용
  }
  return arg;
}

static PyObject *wrIsX(PyObject *self, PyObject *arg) {
  CONSOLE_SCREEN_BUFFER_INFO presentCur;
  GetConsoleScreenBufferInfo(GetStdHandle(STD_OUTPUT_HANDLE), &presentCur); // Windows API 사용
  return PyLong_FromLong(presentCur.dwCursorPosition.X);
}

static PyObject *wrIsY(PyObject *self, PyObject *arg) {
  CONSOLE_SCREEN_BUFFER_INFO presentCur;
  GetConsoleScreenBufferInfo(GetStdHandle(STD_OUTPUT_HANDLE), &presentCur); // Windows API 사용
  return PyLong_FromLong(presentCur.dwCursorPosition.Y);
}

static PyObject *changeTxtColor(PyObject *self, PyObject *arg) {
  if (!PyLong_CheckExact(arg)) {
    PyErr_SetString(PyExc_ValueError, "Argument is not an integer.");
    return NULL;
  } else {
    long ordinal = PyLong_AsLong(arg);
    /* 0 = 검정색, 1 = 파란색, 2 = 초록색, 3 = 옥색, 4 = 빨간색, 5 = 자주색,
       6 = 노란색, 7 = 흰색, 8 = 회색, 9 = 연한 파란색, 10 = 연한 초록색,
       11 = 연한 옥색, 12 = 연한 빨간색, 13 = 연한 자주색, 14 = 연한 노란색, 15 = 진한 흰색
    */
    SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), ordinal); // Windows API 사용
  }
  return arg;
}

static PyObject *hideConsoleCursor(PyObject *self, PyObject *arg) {
  if (!PyLong_CheckExact(arg)) {
    PyErr_SetString(PyExc_ValueError, "Argument is not an integer.");
    return NULL;
  }
  long ordinal = PyLong_AsLong(arg);
  // 커서 제거 - https://kkikkodev.tistory.com/27
  CONSOLE_CURSOR_INFO cursorInfo = {0};
  cursorInfo.dwSize = 1; // 커서 크기 설정
  cursorInfo.bVisible = !ordinal;
  SetConsoleCursorInfo(GetStdHandle(STD_OUTPUT_HANDLE), &cursorInfo); // Windows API 사용
  return arg;
}

static PyMethodDef methods[] = {
    {"gotoXY", gotoXY, METH_VARARGS, "Move cursor to (x, y)."},
    {"wrIsX", wrIsX, METH_NOARGS, "Change text color to N."},
    {"wrIsY", wrIsY, METH_NOARGS, "Change text color to N."},
    {"changeTxtColor", changeTxtColor, METH_O, "Change text color to N."},
    {"hideConsoleCursor", hideConsoleCursor, METH_O, "Hide console cursor."},
    {NULL, NULL, 0, NULL}
    /* {실제 사용할 메소드 명, C 함수 명, 매개변수 타입, "설명"} */
};

#if PY_MAJOR_VERSION >= 3
PyDoc_STRVAR(module_doc, "Windows Console API.");

static struct PyModuleDef pycmathExt = {
    PyModuleDef_HEAD_INIT,
    "winAPI",  // 모듈 이름
    module_doc,
    -1,
    methods,
    NULL,
    NULL,
    NULL,
    NULL};

PyMODINIT_FUNC PyInit_winAPI(void) {
  return PyModule_Create(&pycmathExt);
}
#endif
