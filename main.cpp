#include <iostream>
#include <Windows.h>
#include <string>
#include <cstring>
#include <cstdlib>
#include <typeinfo>

using namespace std;


std::string ExePath()
{

    char buffer[MAX_PATH];
    GetModuleFileName( NULL, buffer, MAX_PATH );
    string::size_type pos = string( buffer ).find_last_of( "\\/" );
    //return string( buffer ).substr( 0, pos);
    return std::string(buffer);

}


std::string get_env_var( std::string key )
    {
        char * val;
        val = getenv( key.c_str() );
        std::string retval = "";
        if (val != NULL) {
            retval = val;
    }
    return retval;
}


main()
{

    ShowWindow(GetConsoleWindow(), SW_HIDE);
    system("python -m PLM");

};
