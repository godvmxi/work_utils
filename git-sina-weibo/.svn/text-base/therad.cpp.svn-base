
#include "thread.h"
#include <QDebug>

Thread::Thread()
{
    //m_request = new QNetworkRequest;
    m_iType = 0;

}
//获取数据
void Thread::run()
{
    qDebug()<<"current thread id is :"<<this->currentThreadId();
    m_manager = new QNetworkAccessManager;
    m_reply = getData();
    connect(m_reply,SIGNAL(finished()),this,SLOT(readAll()),Qt::DirectConnection);
  //  connect(m_reply,SIGNAL(error(QNetworkReply::NetworkError)),this,SLOT(error(QNetworkReply::NetworkError)));
    exec();
    delete m_manager;
}
//初始化 request, type 表示读的是神马数据~
void Thread::setGet(int type, QNetworkRequest request)
{
    m_iType = type;
    m_methond = GET;
    m_request = request;
    start();
}
//此处的post的data 为空~
void Thread::setPost(int type, QNetworkRequest request, QByteArray data)
{
    m_iType = type;
    m_methond = POST;
    m_request = request;
    m_bytData = data;
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
    //log err code
    emit netError(error);
    exit();
}

//获取数据, 通过get 或者 post
QNetworkReply * Thread::getData()
{
    if(GET == m_methond)
    {
       m_manager->get(m_request);
    }
    else if(POST == m_methond)
    {
        m_manager->post(m_request, m_bytData);
    }
}
