// This file was generated by mys. DO NOT EDIT!!!

#include "generics/main.mys.hpp"

namespace mys::generics::main

{

void echo(String& message);

void echo(i32 message);

void echo(f32 message);

int main(int __argc, const char *__argv[]);

void echo(String& message)
{
    std::cout << "String: " << " " << message << std::endl;
}

void echo(i32 message)
{
    std::cout << "Integer:" << " " << message << std::endl;
}

void echo(f32 message)
{
    std::cout << "Float:  " << " " << message << std::endl;
}

int main(int __argc, const char *__argv[])
{
    (void)__argc;
    (void)__argv;
    auto message = String("foo");
    echo(message);
    echo(5);
    echo(5.3f);

    return 0;
}

}



int package_main(int argc, const char *argv[])
{
    return mys::generics::main::main(argc, argv);
}