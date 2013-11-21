#-------------------------------------------------
#
# Project created by QtCreator 2011-04-25T23:38:01
#
#-------------------------------------------------

QT       += core gui
QT       += network
QT       += xml
QT       += webkit
TARGET = sinaWeibo
TEMPLATE = app


SOURCES += main.cpp\
    thread.cpp \
    sina.cpp \
    oauth.cpp \
    parsexml.cpp \
    weibodata.cpp

HEADERS  += \
    thread.h \
    sina.h \
    oauth.h \
    parsexml.h \
    weibodata.h \
    constData.h

FORMS    += \
    thread.ui \
    sina.ui \
    oauth.ui \
    parsexml.ui \
    weibodata.ui

CONFIG += mobility
MOBILITY = 

symbian {
    TARGET.UID3 = 0xecba04dc
    # TARGET.CAPABILITY += 
    TARGET.EPOCSTACKSIZE = 0x14000
    TARGET.EPOCHEAPSIZE = 0x020000 0x800000
}
