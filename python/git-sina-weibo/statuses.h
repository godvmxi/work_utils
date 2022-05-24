#ifndef STATUSES_H
#define STATUSES_H

#include <QNetworkReply>
#include <QNetworkAccessManager>
#include <QMap>
#include <QNetworkRequest>
#include "thread.h"

class Statuses:public QObject
{
    Q_OBJECT
public:
    enum eHttpMethond {
        GET,
        POST
    };
    Statuses();
    void sendRequest();
    QNetworkRequest getDataRequest(int type,QString str);
private slots:
    void ReadyRead(QString str);
    void netError(QNetworkReply::NetworkError error);
signals:
    void readReady();

private:
    static const QString m_key;
    static const QString m_Source;
    QNetworkRequest m_request;
    QNetworkReply *m_reply;
    QNetworkAccessManager *m_manager;
    eHttpMethond m_state;
};

#endif // BLOG_H
