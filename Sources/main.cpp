#include <iostream>
#include <Windows.h>

using namespace std;

int main()
{

    ShowWindow(GetConsoleWindow(), SW_HIDE);
    // Start project
    system("python -m PLM");
    ShowWindow(GetConsoleWindow(), SW_RESTORE);

};
