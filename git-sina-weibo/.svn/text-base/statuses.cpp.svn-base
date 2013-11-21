#include "statuses.h"
#include <QDebug>
#include <QDomComment>
#include <QDomNodeList>
#include <QtCore>
#include "sina.h"

Statuses::Statuses()
{

} 
const QString Statuses::m_key = "966880929";

void Statuses::sendRequest()
{
    m_manager = new QNetworkAccessManager;
    QString url = "http://api.t.sina.com.cn/statuses/friends_timeline.xml";
    QString requestUrl = url+"?source="+m_key+"&count=20&page=10";
    m_request.setUrl(QUrl(requestUrl));
    m_reply = m_manager->get(m_request);
    connect(m_reply,SIGNAL(readyRead()),this,SLOT(ReadyRead()));
    return ;

}
void Statuses::ReadyRead()
{

    QString xmlFile = m_reply->readAll();
    QDomDocument doc;
    doc.setContent(xmlFile);

    QDomNodeList screen_name = doc.elementsByTagName("screen_name");
    QDomNodeList favourites_count = doc.elementsByTagName("favourites_count");
    QDomNodeList text = doc.elementsByTagName("text");
    //QDomNodeList in_reply_to_status_id = doc.elementsByTagName("in_reply_to_status_id");
    //QDomNodeList in_reply_to_user_id = doc.elementsByTagName("in_reply_to_user_id");
    //QDomNodeList in_reply_to_screen_name = doc.elementsByTagName("in_reply_to_screen_name");
    //QDomNodeList retweeted_status = doc.elementsByTagName("retweeted_status");
    QDomNodeList location = doc.elementsByTagName("location");
    QDomNodeList description = doc.elementsByTagName("description");
    QDomNodeList url = doc.elementsByTagName("url");
    QDomNodeList profile_image_url = doc.elementsByTagName("profile_image_url");
    QDomNodeList gender = doc.elementsByTagName("gender");
    QDomNodeList followers_count = doc.elementsByTagName("followers_count");
    QDomNodeList friends_count = doc.elementsByTagName("friends_count");
    QDomNodeList status_count = doc.elementsByTagName("status_count");
    QDomNodeList verified = doc.elementsByTagName("verified");

    QStringList Info;
    int count = 20;
    for(int i = 0;i<=count;i++)
    {
        Info.append(screen_name.at(i).toElement().attribute(""));
        Info.append(verified.at(i).toElement().attribute(""));
        Info.append(": ");
        Info.append(text.at(i).toElement().attribute(""));
        Info.append(location.at(i).toElement().attribute(""));
        Info.append(description.at(i).toElement().attribute(""));
        Info.append(url.at(i).toElement().attribute(""));
        Info.append(profile_image_url.at(i).toElement().attribute(""));
        Info.append(gender.at(i).toElement().attribute(""));
        Info.append(followers_count.at(i).toElement().attribute(""));
        Info.append(friends_count.at(i).toElement().attribute(""));
        Info.append(status_count.at(i).toElement().attribute(""));
        Info.append(favourites_count.at(i).toElement().attribute(""));
    }
    return ;
}
void Statuses::netError(QNetworkReply::NetworkError error)
{

}
