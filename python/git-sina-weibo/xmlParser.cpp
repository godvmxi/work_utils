#include "xmlParser.h"
#include <QDomDocument>
#include <QDebug>
QList<Status*> XmlParser::parseFriendsTimeLine(const QString &data){
    QList<Status*> listStatus;
    QDomDocument doc;
     doc.setContent(data);
     if(!doc.isNull()){
        QDomNodeList nodeList = doc.elementsByTagName("status");
        for(int i = 0; i != nodeList.size(); i++){
          // Status *status = new Status;
           Status *status = parseStatus(nodeList.at(i));
           listStatus.append(status);
        }
     }
     return listStatus;
}
Status * XmlParser::parseStatus(const QDomNode &node){
    Status *status = new Status;
    QDomNode child = node.firstChild();
    while(!child.isNull()){
        QDomElement element = child.toElement();
        qDebug()<<"element.tagName() is"<<element.tagName();
        if("created_at" == element.tagName()){
            status->m_sCreatedAt = element.text();
        }else if("id" == element.tagName()){
            status->m_iId = element.text().toInt();
        }else if("text" == element.tagName()){
            status->m_sText = element.text();
            qDebug()<<status->m_sText;
        }else if("source" == element.tagName()){
            //status->m_sSource = parseSource(element);
        }else if("favorited" == element.tagName()){
            if("false" == element.text()){
                status->m_bFavorited = false;
            }else if("true" == element.text()){
                status->m_bFavorited = true;
            }
        }else if("user" == element.tagName()){
            //status->m_user = parseUser(element);
        }
        child = child.nextSibling();
    }
    return status;
}

QString XmlParser::parseSource(const QDomElement &element){

}

User XmlParser::parseUser(const QDomElement &node){

}
