/* Coded with C Grammar for MSVC in Windows
   This Source uses UTF-8-BOM encoding & CRLF (Windows) line endings
   Alias : WinAPI.c & Last Modded : 2021.04.14.
   Windows NT API 함수를 정의 Coded by IRACK
*/

#include <Windows.h>

#ifndef WINAPI_H
  #define WINAPI_H

  #define SHOW 0 // hideConsoleCursor 함수의 콘솔 커서 보이기 옵션
  #define HIDE 1 // hideConsoleCursor 함수의 콘솔 커서 숨기기 옵션
#endif

void gotoXY(int x, int y); // 콘솔창 커서 좌표 이동 함수
int wrIsX(void); // 콘솔창 커서 X축(가로) 좌표 리턴 함수
int wrIsY(void); // 콘솔창 커서 Y축(세로) 좌표 리턴 함수
void changeTxtColor(int const color); // 콘솔창 글자 색 변경 함수
void hideConsoleCursor(_Bool const hide_flag); // 콘솔창 커서 깜박임 제거 함수

void gotoXY(int x, int y) {
  COORD position = {x, y};
  SetConsoleCursorPosition(GetStdHandle(STD_OUTPUT_HANDLE), position); // Windows API 사용
}

int wrIsX(void) {
  CONSOLE_SCREEN_BUFFER_INFO presentCur;
  GetConsoleScreenBufferInfo(GetStdHandle(STD_OUTPUT_HANDLE), &presentCur); // Windows API 사용
  return presentCur.dwCursorPosition.X;
}

int wrIsY(void) {
  CONSOLE_SCREEN_BUFFER_INFO presentCur;
  GetConsoleScreenBufferInfo(GetStdHandle(STD_OUTPUT_HANDLE), &presentCur); // Windows API 사용
  return presentCur.dwCursorPosition.Y;

}

void changeTxtColor(int const color) {
  /* 0 = 검정색, 1 = 파란색, 2 = 초록색, 3 = 옥색, 4 = 빨간색, 5 = 자주색,
     6 = 노란색, 7 = 흰색, 8 = 회색, 9 = 연한 파란색, 10 = 연한 초록색,
     11 = 연한 옥색, 12 = 연한 빨간색, 13 = 연한 자주색, 14 = 연한 노란색, 15 = 진한 흰색
  */
  SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), color); // Windows API 사용
}

void hideConsoleCursor(_Bool const hide_flag) {
  // 커서 제거 - https://kkikkodev.tistory.com/27
  CONSOLE_CURSOR_INFO cursorInfo = {0};
  cursorInfo.dwSize = 1; // 커서 크기 설정
  cursorInfo.bVisible = !hide_flag; // 커서를 보이려면 TRUE, 그렇지 않으려면 FALSE
  SetConsoleCursorInfo(GetStdHandle(STD_OUTPUT_HANDLE), &cursorInfo); // Windows API 사용
}
