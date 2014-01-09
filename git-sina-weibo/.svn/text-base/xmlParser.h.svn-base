#ifndef XMLPARSER_H
#define XMLPARSER_H
#include <QString>
#include <weiBoData.h>
#include <QDomNode>

class XmlParser{
public:
    QList<Status*> parseFriendsTimeLine(const QString &data);
private:
    Status *parseStatus(const QDomNode &node);
    User parseUser(const QDomElement &element);
    QString parseSource(const QDomElement &element);
};

#endif // XMLPARSER_H
