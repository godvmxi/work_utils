
#ifndef SINA_H
#define SINA_H
#include <QObject>
#include <QHash>
#include "parsexml.h"
#include <QNetworkRequest>
#include "oauth.h"
#include <QEventLoop>
#include <QTimer>
#include <QNetworkReply>


class Sina:public QObject
{
    Q_OBJECT
public:
    Sina(QObject *parent = 0);
    static Sina *getInstance();
    static QString myAccessToken;
    static QString myAccessTokenSecret;

    QString getSevice(QString key);
    void setSevice(const QString key,const QString value);
    void startOAuth();
    void startStatus();

    static QString Source;
    static QString Secret;


public slots: //获取数据接口

    //获取下行数据集(timeline)接口
   //

    //
    QList<Status *> friendsTimeline(int since_id = -1,
                                    int max_id = -1,
                                    int count = 20,
                                    int page = 1,
                                    int feature = 0);

    QList<Status *> userTimeline(int64_t user_id,
                                 int since_id = -1,
                                 int max_id = -1,
                                 int count = 20,
                                 int page = 1,
                                 int feature = 0);

    QList<Status *> mentions(int since_id, int max_id, int count, int page);
    QList<Comment *> commentsTimeline(int since_id, int max_id, int count, int page);
    QList<Comment *> commentsByMe(int since_id, int max_id, int count, int page);
    QList<Comment *> commentsToMe(int since_id, int max_id, int count, int page);
//    void comments();
//    void counts();
//    void repostTimeline();
//    void repostByMe();
//    void unread();
//    void resetCount();
//    void emotions();

//    //微博访问接口
//    void showId();
//    void userStatusesId();
//    void update();
//    void upload();
//    void destroy();
//    void repost();
//    void comment();
//    void commentDestroy();
//    void commentDestroyBatch();
//    void reply();

//    //用户接口
//    void usersShow();
//    void friends();
//    void followers();
//    void usersHot();
//    void updateRemark();
//    void suggestions();

//    //私信接口(高级,默认为限制级接口!
//    void directMessages();
//    void sent();
//    void New();
//    void destroyId();
//    void directMessagesDestroyBatch();

//     //关注接口
//    void friendshipsCreate();
//    void friendshipsDestroy();
//    void friendshipsShow();
//    void friendshipsExists();
//    void friendsIds();
//    void followersIds();

//    //话题接口
//    void trends();
//    void trendsStatuses();
//    void trendsFollow();
//    void trendsDestroy();
//    void trendsHourly();
//    void trendsDaily();
//    void trendsWeekly();

//    //隐私设置接口
//    void updatePrivacy();
//    void getPrivacy();

//    //黑名单接口
//    void blocksCreate();
//    void blocksDestroy();
//    void blocksExists();
//    void blocksBlocking();
//    void blocksBlockingIds();

//    //用户标签接口
//    void tags();
//    void tagsCreate();
//    void tagsDestroy();
//    void tagsSuggestions();
//    void tagsDestroyBatch();

//    //帐号接口
//    void verifyCredentials();
//    void rateLimitStatus();
//    void endSession();
//    void updateProfileImage();
//    void updateProfile();

//    //收藏接口
//    void favourites();
//    void favouritesCreate();
//    void favouritesDestroy();
//    void favouritesDestroyBatch();

//    //微博搜索
//    void suggestionsAtUsers();


private slots:
    void timeout();
    void getData(int,QString); //获取数据
signals :
    void sig_data(int, QString);
    void sig_networkErr(int, QNetworkReply::NetworkError);
private:

    void sendRequest();         //发送数据请求
    void addListParames(QUrl &url,
                        QMap<QString, QString> &map,
                        int since_id,
                        int max_id,
                        int count,
                        int page);

    void addFeatureParame(QUrl &url, QMap<QString, QString> &map, int feature);
    void addUserIdParame(QUrl &url, QMap<QString, QString> &map, int64_t user_id);

    QEventLoop *m_loop;
    OAuth *m_oauth;
    static Sina *m_instance;
    QHash<QString,QString> m_sevice;
    int m_iCurrentKey;
    QString m_sCurrentData;
    ParseXml *m_parseXml;
    QTimer *m_timer;

    void reqData(QNetworkRequest request);
};


#endif // SINA_H
