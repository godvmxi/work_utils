#ifndef OAUTH_H
#define OAUTH_H

#include <QByteArray>
#include <QMap>
#include <QNetworkRequest>
#include "thread.h"

class OAuth:public QObject
{
    Q_OBJECT
public:
    OAuth();
    enum eHttpMethond {
        GET,
        POST
    };
    enum States {
        eREQUEST_TOKEN = 100,
        eUSER_AUTHORIZE,
        eACCESS_TOKEN,

        eNET_ERR = 200,
        eSUCCESS
    };
    static OAuth* oauth;
    OAuth instance();
    QNetworkRequest getDataRequest(QUrl url, QMap<QString, QString> extendParams = QMap<QString, QString>());
    void startAuthorization(const QString &passport,const QString &password);

   static QString AccessToken;
   static QString AccessTokenSecret;

private slots:
   void netError(QNetworkReply::NetworkError);
   void getData(int state,QString str);
signals:
   void success();
private:
   QByteArray getHmacSha1Result(QString data, QString key);
   QNetworkRequest getRequestToken();
   QNetworkRequest getAuthorize();
   QNetworkRequest getAccessToken();

   QByteArray createSignature(eHttpMethond httpMethond,
                              const QString &requestUrl,
                              const QString key,
                              QMap<QString,QString> &parmas);


   QString createTimeStemp();
   QString createNonce();

   void setOAuthInfo(QNetworkRequest &request, QMap<QString, QString> &params);

   static const QString OAuthCallback;
   static const QString OAuthNonce;
   static const QString OAuthSignature;
   static const QString OAuthTimeStemp;
   static const QString OAuthVersion;
   static const QString OAuthVerifier;
   static const QString OAuthconsumerKey;
   static const QString consumerSecret;
   static const QString OAuthToken;
   static const QString OAuthMethond;

   QString m_verifierNumber;
   QString m_OAuthToken;
   QString m_OAuthTokenSecret;

   QString m_passport;
   QString m_password;

   bool parseAccessToken(QString &str);
   bool parseRequestToken(QString &str);
   bool parseAuthorize(QString &str);

   States m_state;
   void setState(States state);
   void nextStep();

};



#endif // OAUTH_H
