#include <QtGui/QApplication>
#include <QtCore>
#include <QTextCodec>
#include "oauth.h"
#include "sina.h"


int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
   QTextCodec *encoding = QTextCodec::codecForName("utf-8");
   QTextCodec::setCodecForCStrings(encoding);
   QTextCodec::setCodecForLocale(encoding);
   QTextCodec::setCodecForTr(encoding);
   Sina sina;
   sina.startOAuth();

    return a.exec();
    qDebug()<<"i m leave.....";
}
