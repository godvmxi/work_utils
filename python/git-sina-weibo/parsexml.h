#ifndef PARSEXML_H
#define PARSEXML_H
#include "weibodata.h"
#include <QString>
#include <QList>
#include <QDomNode>
//#include "sina.h"

class ParseXml
{
public:
    QList<Status*> parseFriendsTimeline(const QString &data);
    QList<Status*> parseUserTimeline(const QString &data);
    QList<Status*> parseMentions(const QString &data);
    QList<Comment*> parseCommentsTimeline(const QString &data);
    QList<Comment*> parseCommentsByMe(const QString &data);
    QList<Comment*> parseCommentsToMe(const QString &data);
    QList<Comment*> parseComments(const QString &data);
    QList<Count*> parseCounts(const QString &data);
    QList<Status*> parseRepostTimeline(const QString &data);
    QList<Status*> parseRepostByMe(const QString &data);
    Count parseUnRead(const QString &data);
    bool parseResetCount(const QString &data);
    QList<Emtion*> parseEmotions(const QString &data);

    QList<Status*> parseShow(const QString &data);
    Status* parseUpDate(const QString &data);
    Status* parseUpLoad(const QString &data);
    Status* parseDestroy(const QString &data);
    Status* parseRepost(const QString &data);
    Comment* ParseComment(const QString &data);
    Comment* parseCommentDestroy(const QString &data);
    QList<Comment*> parseCommentDestroyBatch(const QString &data);
    Comment* parseReply(const QString &data);

    User parseUserShow(const QString &data);
    QList<User> parseStatusFriends(const QString &data);
    QList<User> parseFollowers(const QString &data);
    QList<User> parseUsersHot(const QString &data);
    User parseUpDateRemark(const QString &data);
    QList<User> parseSuggestions(const QString &data);

    QList<DirectMessage*> parseDirectmessages(const QString &data);
    QList<DirectMessage*> parseMessageSent(const QString &data);
    DirectMessage* parseMessage(const QString &data);
    DirectMessage* parseMessageDestroy(const QString &data);
    QList<DirectMessage*> parseMessageDestroyBatch(const QString &data);
    User parseFriendshipCreate(const QString &data);
    User parseFriendshipDestroy(const QString &data);
    bool parseFriendshipexists(const QString &data);
    Relationship parseFriendshipShow(const QString &data);
    QList<Trend> ParseTrends(const QString &data);
    QList<Status*> parseTrendStatus(const QString &data);
    QList<int> parseTrendsFollow(const QString &data);
    bool parseTrendDestroy(const QString &data);
    QList<Trends*> parseTrendsHourly(const QString &data);
    QList<Trends*> parseTrendsDaily(const QString &data);
    QList<Trends*> parseTrendsWeekly(const QString &data);
    IdList* parseFriendIds(const QString &data);
    IdList* parseFollowersId(const QString &data);
    bool parseUpdatePrivacy(const QString &data);
    Result parseGetPrivacy(const QString &data);
    User parseBlocksCreate(const QString &data);
    User parseBloclsDestroy(const QString &data);
    bool parseBlocksExists(const QString &data);
    QList<Ids> parseBlockingIds(const QString &data);
    QList<Tag> ParseTags(const QString &data);
    TagIds parseTagsCreate(const QString &data);
    QList<Tag> parseTagSuggestions(const QString &data);
    bool parseTagDestroy(const QString &data);
    TagIds parseTagDestroyBatch(const QString &data);
    User parseVerifyCredentials(const QString &data);
    Hash parseRateLimitStatus(const QString &data);
    User parseEndSession(const QString &data);
    User parseUpdateProfileImage(const QString &data);
    User parseUpdateProfile(const QString &data);
    QList<Status*> parseFavourites(const QString &data);
    Status* parseFavouritesCreate(const QString &data);
    Status* parseFavouritesDestroy(const QString &data);
    QList<Status*> parseFavouritesDestroyBatch(const QString &data);
    QList<Suggestion> parseAtUsers(const QString &data);

   private:
    Status *parseStatus(const QDomElement &node);
    User parseUser(const QDomElement &element);
    QString parseSource(const QDomElement &element);
    RetweetedStatus parseRetweetedStatus(const QDomElement &element);
    Comment *parseComment(const QDomNode &node);
    ReplyComment parseReplyComment(const QDomElement &element);
    Count parseCount(const QDomElement &element);
    Emtion parseEmtion(const QDomElement &element);

    DirectMessage *parseDirectmessage(const QDomNode &node);
    Sender parseSender(const QDomElement &element);
    Recipient parseRecipient(const QDomElement &element);
    Relationship parseRelationship(const QDomElement &element);
    Source ParseSource(const QDomElement &element);
    Target parseTarget(const QDomElement &element);
    Trend parseTrend(const QDomElement &element);
    Trends *parseTrends(const QDomNode &node);
    IdList *parseIdList(const QDomNode &node);
    Ids parseIds(const QDomElement &element);
    Result parseResult(const QDomElement &element);
    Tags *parseTags(const QDomNode &node);
    Tag parseTag(const QDomElement &element);
    TagIds parseTagIds(const QDomElement &element);
    Suggestion parseSuggestion(const QDomElement &element);
    Hash parseHash(const QDomElement &element);


};

#endif // PARSEXML_H
