#include <stdio.h>


void display_ascii_art(int n)
{
    printf("  _   _      _ _         __        __         _     _ _ \n");
    printf(" | | | | ___| | | ___    \\ \\      / /__  _ __| | __| | |\n");
    printf(" | |_| |/ _ \\ | |/ _ \\    \\ \\ /\\ / / _ \\| '__| |/ _` | |\n");
    printf(" |  _  |  __/ | | (_) |    \\ V  V / (_) | |  | | (_| |_|\n");
    printf(" |_| |_|\\___|_|_|\\___( )    \\_/\\_/ \\___/|_|  |_|\\__,_(_)\n");
    printf("                     |/                                 \n");
}
 
int main()
{
    int n = 9;
    display_ascii_art(n);
    return 0;
}
