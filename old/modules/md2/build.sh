swig -c++ -python md2.i
g++ -c -fPIC md2Model.cpp
g++ -c -fPIC md2Object.cpp
g++ -c -fPIC md2_wrap.cxx -I/usr/include/python2.5
ld -shared md2Model.o md2Object.o md2_wrap.o -o _md2.so

