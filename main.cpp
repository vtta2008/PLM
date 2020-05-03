#include <iostream>
#include <Windows.h>
#include <string>

using namespace std;


string ExePath()
{

    char buffer[MAX_PATH];
    GetModuleFileName( NULL, buffer, MAX_PATH );
    string::size_type pos = string( buffer ).find_last_of( "\\/" );
    return string( buffer ).substr( 0, pos);

}

int main()
{

    //ShowWindow(GetConsoleWindow(), SW_HIDE);
    cout << ExePath() << "\n";
    system("python -m PLM");

};
