#include "oauth.h"
#include "sina.h"
#include <QtCore>
#include "constData.h"

OAuth::OAuth()
{

}
const QString OAuth::consumerSecret = "consumer_secret";
const QString OAuth::OAuthconsumerKey = "oauth_consumer_key";
const QString OAuth::OAuthMethond = "oauth_signature_method";
const QString OAuth::OAuthTimeStemp = "oauth_timestamp";
const QString OAuth::OAuthNonce = "oauth_nonce";
const QString OAuth::OAuthVersion = "oauth_version";
const QString OAuth::OAuthCallback = "oauth_callback";
const QString OAuth::OAuthSignature = "oauth_signature";
const QString OAuth::OAuthToken = "oauth_token";
const QString OAuth::OAuthVerifier = "oauth_verifier";
QString OAuth::AccessToken = "";
QString OAuth::AccessTokenSecret = "";

QNetworkRequest OAuth::getRequestToken()
{

    QMap<QString, QString> params;
    params.insert(OAuth::OAuthCallback, "oob");
    params.insert(OAuth::OAuthconsumerKey,Sina::Source);
    params.insert(OAuth::OAuthNonce, this->createNonce());
    params.insert(OAuth::OAuthMethond, "HMAC-SHA1");
    params.insert(OAuth::OAuthTimeStemp, this->createTimeStemp());
    params.insert(OAuth::OAuthVersion, "1.0");



    QByteArray bytSignature = this->createSignature( GET,
                                                     REQUEST_TOKEN,
                                                     Sina::Secret+"&",
                                                     params);
    params.insert(OAuth::OAuthSignature, bytSignature.toPercentEncoding());
    QUrl url(REQUEST_TOKEN);
    QNetworkRequest request(url);
    this->setOAuthInfo(request, params);
    return request;

}
QNetworkRequest OAuth::getAuthorize()
{
    QString urlString = AUTHORIZE+
                       "?oauth%5Ftoken="+m_OAuthToken.toAscii().toPercentEncoding("&=",".-_~")+
                       "&oauth%5Fcallback=xml&userId="+m_passport.toAscii().toPercentEncoding("&=",".-_~")+
                       "&passwd="+m_password.toAscii().toPercentEncoding("&=",".-_~");
    QUrl url=QUrl::fromEncoded(urlString.toAscii(), QUrl::StrictMode);
    if(url.isValid())
    {
         QNetworkRequest request(url);
         return request;
    }

}
QNetworkRequest OAuth::getAccessToken()
{
    QMap<QString, QString> params;

    params.insert(OAuth::OAuthconsumerKey, Sina::Source);
    params.insert(OAuth::OAuthNonce, this->createNonce());
    params.insert(OAuth::OAuthMethond, "HMAC-SHA1");
    params.insert(OAuth::OAuthTimeStemp, this->createTimeStemp());
    params.insert(OAuth::OAuthVersion, "1.0");
    params.insert(OAuth::OAuthToken, m_OAuthToken);
    params.insert(OAuth::OAuthVerifier, m_verifierNumber);

    QByteArray tmp = this->createSignature( POST, ACCESS_TOKEN,
                                            Sina::Secret+"&"+m_OAuthTokenSecret, params);

    params.insert(OAuth::OAuthSignature, tmp.toPercentEncoding());

    QNetworkRequest request;
    request.setUrl(QUrl(ACCESS_TOKEN));
    this->setOAuthInfo(request, params);
    return request;


}

QNetworkRequest OAuth::getDataRequest(QUrl url, QMap<QString, QString> extendParams)
{
    QMap<QString,QString> oauthParams;
    QString key =  Sina::Secret+"&"+OAuth::AccessTokenSecret;
    QNetworkRequest request;
    request.setUrl(url);


    oauthParams.insert(OAuth::OAuthToken,OAuth::AccessToken);
    oauthParams.insert(OAuth::OAuthconsumerKey, Sina::Source);
    oauthParams.insert(OAuth::OAuthNonce, createNonce());
    oauthParams.insert(OAuth::OAuthMethond, "HMAC-SHA1");
    oauthParams.insert(OAuth::OAuthTimeStemp, createTimeStemp());
    oauthParams.insert(OAuth::OAuthVersion, "1.0");

    //添加扩展参数
    if(0 != extendParams.count()){
//        oauthParams.unite(extendParams);
        extendParams.unite(oauthParams);
        qDebug()<<"add unite";
    }
    //将带有扩展参数 map 制作成一个signature  此处的url为不带参数的
    QByteArray signature = createSignature( GET, url.toString(QUrl::RemoveQuery), key, extendParams);
    qDebug()<<"signature is"<<signature;
    oauthParams.insert(OAuth::OAuthSignature, signature.toPercentEncoding());
    setOAuthInfo(request, oauthParams);
    return request;

}

void OAuth::setOAuthInfo(QNetworkRequest &request, QMap<QString, QString> &params)
{
    QStringList paramsList;
    QString str = "%1=\"%2\"";
    QMapIterator<QString, QString> it(params);
    while(it.hasNext())
    {
        it.next();
        paramsList.append(str.arg(it.key()).arg(it.value()));
    }
    str = "OAuth " + paramsList.join(", ");
    qDebug()<<"str-----is ------"<<str;
    request.setRawHeader("Authorization", str.toAscii());


}

QByteArray OAuth::createSignature(eHttpMethond httpMethond,
                                  const QString &requestUrl,
                                  const QString key, QMap<QString,
                                  QString> &params)
{
    QString baseString;
    switch(httpMethond)
    {
    case GET:
        baseString.append("GET");
        break;
    case POST:
        baseString.append("POST");
        break;
    default:
        break;
    }
    qDebug()<< requestUrl <<"#url";
    baseString.append("&");
    baseString.append(requestUrl.toAscii().toPercentEncoding());
    baseString.append("&");
    QString tmp;
    QMapIterator< QString, QString> it(params);
    while(it.hasNext())
    {
        it.next();
        tmp.append(it.key()+"="+it.value()+"&");
    }
    tmp.remove(tmp.length()-1, 1);//remove last &
    baseString.append(tmp.toAscii().toPercentEncoding());
    return getHmacSha1Result(baseString, key);
}
QString OAuth::createTimeStemp()
{
   return QString::number(QDateTime::currentDateTime().toTime_t());
}
QString OAuth::createNonce()
{
    QString nonce;

    qsrand(QDateTime::currentDateTime().toTime_t());
    const char chars[37] = "0123456789abcdefghijklmnopqrstuvwxyz";
    for( int i=0; i<16; i++)
    {
        nonce.append( chars[ qrand()%36]);
    }
   qDebug("nonce is :"+nonce.toAscii());
    return nonce;
}

QByteArray OAuth::getHmacSha1Result(QString data, QString key)
{

    QByteArray ipadArray( 64, char(0x36));
    QByteArray opadArray( 64, char(0x5C));
    QByteArray temp;
    if( key.length() > 64 )
    {
        temp = QCryptographicHash::hash(key.toAscii(),
                                        QCryptographicHash::Sha1);
    }
    else
    {
        temp = key.toAscii();
    }
    temp.leftJustified( 64, (char) 0);
    for( int i=0; i<temp.length(); i++)
    {
        ipadArray[i] = ipadArray[i] ^ temp.at(i);
        opadArray[i] = opadArray[i] ^ temp.at(i);
    }
    temp = QCryptographicHash::hash( ipadArray.append( data.toAscii() ),
                                     QCryptographicHash::Sha1);
    temp = QCryptographicHash::hash( opadArray.append( temp ),
                                     QCryptographicHash::Sha1);
    return temp.toBase64();
}
void OAuth::startAuthorization(const QString &passport, const QString &password)
{
    m_passport = passport;
    m_password = password;
    setState(eREQUEST_TOKEN);
    nextStep();
}
void OAuth::getData(int state, QString str)
{
    switch(state)
    {
    case eREQUEST_TOKEN:
        parseRequestToken(str);
        setState(eUSER_AUTHORIZE);
        break;

    case eUSER_AUTHORIZE:
        parseAuthorize(str);
        setState(eACCESS_TOKEN);
        break;

    case eACCESS_TOKEN:
        parseAccessToken(str);
        setState(eSUCCESS);
        //测试用
        emit success();
        break;
    case eSUCCESS:

        break;
    default:
        setState(eREQUEST_TOKEN);
        break;
    }
    nextStep();
}
void OAuth::setState(States state)
{
    m_state = state;
}



void OAuth::nextStep()
{
    Thread * thread = new Thread();
    connect(thread,SIGNAL(readData(int,QString)),this,SLOT(getData(int,QString)));
    connect(thread,SIGNAL(finished()),thread,SLOT(deleteLater()));
    int state = m_state;
    switch(m_state)
    {
    case eREQUEST_TOKEN:
        thread->setGet(state,getRequestToken());
        break;

    case eUSER_AUTHORIZE:
        thread->setGet(state,getAuthorize());
        break;

    case eACCESS_TOKEN:
        thread->setPost(state,getAccessToken(),QByteArray());
        break;

    default:
        break;
    }

}

bool OAuth::parseRequestToken(QString &str)
{
    qDebug()<< "request Token is:"<< str;
    if(str.isEmpty() || str.isNull())
    {
        return false;
    }
    QStringList resultList = str.split("&");
    for( int i=0; i<resultList.length(); i++)
    {
        QString tmp = resultList.at(i);
        if(tmp.startsWith("oauth_token="))
            m_OAuthToken = tmp.replace("oauth_token=","");

        else if(tmp.startsWith("oauth_token_secret="))
            m_OAuthTokenSecret = tmp.replace("oauth_token_secret=","");
    }
    qDebug()<<"token is"<<m_OAuthToken;
    qDebug()<<"secret is"<<m_OAuthTokenSecret;
    return true;
}
bool OAuth::parseAuthorize(QString &str)
{
    QRegExp regExp("<oauth_verifier>(.+)</oauth_verifier>");
    if(regExp.indexIn(str)!=-1)
    {
        qDebug("found it");
         m_verifierNumber = regExp.cap(1);
         return true;
    }
    else
    {
        qDebug("not found!");
        return false;
    }
}
bool OAuth::parseAccessToken(QString &str)
{
    if(str.isEmpty() || str.isNull())
    {
        return false;
    }
    QStringList strList = str.split("&");
    for( int i=0; i<strList.length(); i++)
    {
        QString tmp = strList.at(i);
        if(tmp.startsWith("oauth_token="))
            AccessToken = tmp.replace("oauth_token=","");
        else if(tmp.startsWith("oauth_token_secret="))
            AccessTokenSecret = tmp.replace("oauth_token_secret=","");
    }

    return true;
}
void OAuth::netError(QNetworkReply::NetworkError)
{

}
