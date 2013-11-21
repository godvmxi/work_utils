#ifndef THREAD_H
#define THREAD_H

#include <QThread>
#include <QNetworkAccessManager>
#include <QNetworkRequest>
#include <QNetworkReply>

class Thread:public QThread
{
    Q_OBJECT
public:
    Thread();
    void setGet(int type,QNetworkRequest request);
    void setPost(int type,QNetworkRequest request,QByteArray data);

    enum eMethond {
        GET,
        POST
    };
private slots:
    void readAll();
    void error(QNetworkReply::NetworkError);
signals:
    void netError(int, QNetworkReply::NetworkError);
    void readData(int type,QString str);
protected:
    void run();
private:
    QNetworkRequest m_request;
    QNetworkReply *m_reply;
    QNetworkAccessManager *m_manager;
    QByteArray m_data;
    int m_iType;
    eMethond m_methond;
    QNetworkReply *getData();

};

#endif // THREAD_H
