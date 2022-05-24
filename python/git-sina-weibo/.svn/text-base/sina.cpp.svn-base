#include "sina.h"
#include "parsexml.h"
#include <QDebug>
#include "weibodata.h"
#include "constData.h"


QString Sina::myAccessToken = "myAccessToken";
QString Sina::myAccessTokenSecret = "myAccessTokenSecret";
Sina* Sina::m_instance = NULL;

Sina* Sina::getInstance()
{
    if(NULL == m_instance)
        m_instance = new Sina();
    return m_instance;
}


QString Sina::Source = "966880929";
QString Sina::Secret = "763f318c8a21e3fed8ba93fa6f75cbdb";

Sina::Sina(QObject *parent):QObject(parent){
    m_oauth = new OAuth;
    m_loop = new QEventLoop(this);
    m_timer = new QTimer(this);
    m_timer->setSingleShot(true);
    connect(m_timer,SIGNAL(timeout()),this,SLOT(timeout()));
}


//request 索取数据的request
void Sina::reqData(QNetworkRequest request){

    Thread *thread = new Thread();
    connect(thread,SIGNAL(readData(int,QString)),this,SLOT(getData(int,QString)));
    connect(thread,SIGNAL(finished()),this,SLOT(deleteLater()));
    connect(thread,SIGNAL(netError(int,QNetworkReply::NetworkError)),
            this,SIGNAL(sig_networkErr(int,QNetworkReply::NetworkError)));
    thread->setGet(-1,request);
    m_timer->start(6000);
    //防止有可能产生递归..
    m_loop->exec(QEventLoop::ExcludeUserInputEvents);

}

void Sina::timeout(){
    m_loop->exit();
    m_sCurrentData.clear();
    emit sig_networkErr(-1,QNetworkReply::TimeoutError);
}

void Sina::startOAuth()
{
    m_oauth = new OAuth();
    m_oauth->startAuthorization("15860821091","252173537");
    connect(m_oauth,SIGNAL(success()),this,SLOT(friendsTimeline()));
}

//get the thread
void Sina::getData(int type, QString str)
{
   qDebug()<<"Sina_getData is ==========";
   //qDebug()<<str;
   //emit sig_data(type, str);
   m_iCurrentKey = type;
   m_sCurrentData = str;
   m_loop->exit();
}
//void Sina::verifyCredentials()
//{
//    OAuth oauth;
//    Thread *thread = new Thread();
//    connect(thread,SIGNAL(readData(int,QString)),this,SLOT(getData(int,QString)));
//    connect(thread,SIGNAL(finished()),this,SLOT(deleteLater()));
//    thread->setGet(iVERIFY_CREDENTIALS,oauth.getDataRequest(VERIFY_CREDENTIALS));
//}

/******************************************************************
* since_id  获取statuss的最小id
* max_id    获取stauts的最大id
* count     获取status的条数
* page  以分页方式返回,指定返回的页码
*feature   指定获取status 的性质,图片,原创...等!
*
*
********************************************************************/
QList<Status *> Sina::friendsTimeline(int since_id,
                                      int max_id,
                                      int count,
                                      int page,
                                      int feature){
    qDebug()<<"friendsTimeline";

    QUrl url;
    QMap<QString, QString> map;
    url.setUrl(FRIENDS_TIMELINE);

    addListParames(url, map, since_id, max_id, count, page);
    addFeatureParame(url, map,feature);
    reqData(m_oauth->getDataRequest(url, map));

    return m_parseXml->parseFriendsTimeline(m_sCurrentData);
}

QList<Status *> Sina::userTimeline(int64_t user_id,
                                   int since_id,
                                   int max_id,
                                   int count,
                                   int page,
                                   int feature){

    QUrl url;
    QMap<QString, QString> map;
    url.setUrl(USER_TIMELINE);
    addUserIdParame(url,map, user_id);
    addListParames(url, map, since_id, max_id, count, page);
    addFeatureParame(url, map, feature);
    reqData(m_oauth->getDataRequest(url, map));
    return m_parseXml->parseUserTimeline(m_sCurrentData);
}

// @我的列表
QList<Status *> Sina::mentions(int since_id, int max_id, int count, int page){
    QUrl url;
    QMap<QString, QString> map;
    url.setUrl(MENTIONS);
    addListParames(url, map, since_id, max_id, count, page);
    reqData(m_oauth->getDataRequest(url, map));
    return m_parseXml->parseMentions(m_sCurrentData);

}

// 我的评论列表,包括我的评论,和给我的评论
  QList<Comment *> Sina::commentsTimeline(int since_id,
                                       int max_id,
                                       int count,
                                       int page){
    QUrl url;
    QMap<QString, QString> map;
    url.setUrl(COMMENTS_TIMELINE);
    addListParames(url, map, since_id, max_id, count, page);
    reqData(m_oauth->getDataRequest(url, map));
    return m_parseXml->parseCommentsTimeline(m_sCurrentData);
}

// 我发出的评论列表
QList<Comment *> Sina::commentsByMe(int since_id, int max_id, int count, int page){

    QUrl url;
    QMap<QString, QString> map;
    url.setUrl(COMMENTS_BY_ME);
    addListParames(url, map, since_id, max_id, count, page);
    reqData(m_oauth->getDataRequest(url, map));
    return m_parseXml->parseCommentsByMe(m_sCurrentData);
}

//我收到的评论列表
QList<Comment *> Sina::commentsToMe(int since_id, int max_id, int count, int page){
    QUrl url;
    QMap<QString, QString> map;
    url.setUrl(COMMENTS_TO_ME);
    addListParames(url, map, since_id, max_id, count, page);
    reqData(m_oauth->getDataRequest(url, map));
    return m_parseXml->parseCommentsToMe(m_sCurrentData);
}



void Sina::addListParames(QUrl &url,
                          QMap<QString, QString> &map,
                          int since_id,
                          int max_id,
                          int count,
                          int page){
    if(since_id > 0){
       map.insert("since_id", QString::number(since_id));
       url.addQueryItem("since_id", QString::number(since_id));
    }
    if(max_id > 0){
        map.insert("max_id", QString::number(max_id));
        url.addQueryItem("max_id", QString::number(max_id));
    }
    if(count > 0){
        map.insert("count", QString::number(count));
        url.addQueryItem("count", QString::number(count));
    }
    if(page > 0){
        map.insert("page", QString::number(page));
        url.addQueryItem("page", QString::number(page));
    }
}

void Sina::addFeatureParame(QUrl &url, QMap<QString, QString> &map, int feature){
    if(feature > 0 && feature < 5){
        map.insert("feature", QString::number(feature));
        url.addQueryItem("feature", QString::number(feature));
    }
}

void Sina::addUserIdParame(QUrl &url, QMap<QString, QString> &map, int64_t user_id){
     map.insert("user_id", QString::number(user_id));
     url.addQueryItem("user_id", QString::number(user_id));
}



