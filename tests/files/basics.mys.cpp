// This file was generated by mys. DO NOT EDIT!!!

#include "basics.mys.hpp"

/* mys-embedded-c++-before-namespace start */

#include <before>

/* mys-embedded-c++-before-namespace stop */

namespace mys::basics

{

Tuple<i32, String> func_1(i32 a);

std::shared_ptr<Dict<i64, std::shared_ptr<List<f64>>>> func_3(i32 a);

void func_4(void);

std::shared_ptr<List<i64>> func_5(void);

void main(int __argc, const char *__argv[]);

;

/* mys-embedded-c++ start */

#include <not-before>

/* mys-embedded-c++ stop */;

Tuple<i32, String> func_1(i32 a)
{
    return Tuple<i32, String>({(2 * a), "Bar"});
}

std::shared_ptr<Dict<i64, std::shared_ptr<List<f64>>>> func_3(i32 a)
{
    return std::make_shared<Dict<todo>>({});
}

void func_4(void)
{
    try {
        throw GeneralError();
    } catch (std::exception& e) {
        std::cout << "func_4():      An exception occurred." << std::endl;
    }
}

std::shared_ptr<List<i64>> func_5(void)
{
    std::shared_ptr<List<i64>> small = std::make_shared<List<i64>>(std::initializer_list<i64>{});
    auto items_2 = std::make_shared<List<i64>>(std::initializer_list<i64>{3, 1, 5, 7, 2});
    for (auto i_3 = 0; i_3 < items_2->__len__(); i_3++) {
        auto v = items_2->get(i_3);
        if ((v < 5)) {
            small->append(v);
        }
    }
    small->sort();
    small->reverse();
    return small;
}

class Calc : public Object {

public:

    i32 value;

    void triple(void)
    {
        this->value *= 3;
    }

    Calc(i32 value)
    {
        this->value = value;
    }

    virtual ~Calc() {}

    String __str__() const
    {
        std::stringstream ss;
        ss << "Calc(";
        ss << "value=" << this->value;
        ss << ")";
        return String(ss.str().c_str());
    }

};

void main(int __argc, const char *__argv[])
{
    auto argv = create_args(__argc, __argv);
    i32 value = i32(argv->get(1));
    std::cout << "func_1(value):" << " " << func_1(value) << std::endl;
    std::cout << "func_3(value):" << " " << func_3(value) << std::endl;
    func_4();
    std::cout << "func_5():     " << " " << func_5() << std::endl;
    std::shared_ptr<Calc> calc = std::make_shared<Calc>(value);
    calc->triple();
    std::cout << "calc:         " << " " << calc << std::endl;
}

}



void package_main(int argc, const char *argv[])
{
    mys::basics::main(argc, argv);
}
