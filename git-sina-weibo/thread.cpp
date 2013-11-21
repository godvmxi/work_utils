#include "thread.h"
//#include "ui_thread.h"
#include <QDebug>

Thread::Thread()
{
    m_iType = 0;
}
void Thread::run()
{
    qDebug()<<"current thread id is :"<<this->currentThreadId();
    m_manager = new QNetworkAccessManager;
    m_reply = getData();
    connect(m_reply,SIGNAL(finished()),this,SLOT(readAll()),Qt::DirectConnection);
    connect(m_reply,SIGNAL(error(QNetworkReply::NetworkError)),
                this,SLOT(error(QNetworkReply::NetworkError)));
    exec();
    delete m_manager;

}
void Thread::setGet(int type, QNetworkRequest request)
{
    m_iType = type;
    m_methond = GET;
    m_request = request;
    start();
}
void Thread::setPost(int type, QNetworkRequest request, QByteArray data)
{
    m_iType = type;
    m_request = request;
    m_methond = POST;
    m_data = data;
    start();
}
void Thread::readAll()
{
   QString strData = m_reply->readAll();
   emit readData(m_iType,strData);
   exit();
}
void Thread::error(QNetworkReply::NetworkError error)
{
    emit netError(m_iType, error);
    exit();
}

QNetworkReply * Thread::getData()
{
    if(GET == m_methond)
    {
       return m_manager->get(m_request);
    }
    else if(POST == m_methond)
    {
        return m_manager->post(m_request, m_data);
    }
}
