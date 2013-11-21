#ifndef WEIBODATA_H
#define WEIBODATA_H
#include <QString>
#include <QDateTime>



class Status;
class User
{
public:
    int m_iId;
    QString m_sScreenName;
    QString m_sName;
    int m_iProvince;
    int m_iCity;
    QString m_sLocation;
    QString m_sDescription;
    QString m_sUrl;
    QString m_sImageUrl;
    QString m_sDomain;
    QString m_sGender;

    int m_iFriendsCount;
    int m_iFollowersCount;
    int m_iStatusCount;
    int m_iFavouritesCount;
    int m_iNextCursor;
    int m_iPreviousCursor;

    QString m_sCreatedAt;
    bool m_bVerified;
    Status *m_status;

};

class RetweetedStatus
{
public:
    QString m_sCreatedAt;
    int m_iId;
    QString m_sText;
    QString m_sSource;

    bool m_bFavourited;
    bool m_bTruncated;

    int m_iReplyToStatusId;
    int m_iReplyToUserId;
    QString m_sReplyToScreenName;
    QString m_sThumbnailPic;
    QString m_sBmiddlePic;
    QString m_sOriginalPic;
    User m_user;


};

class Status
{
public:
    QString m_sCreatedAt;
    int m_iId;
    QString m_sText;
    QString m_sSource;
    bool m_bFavourited;
    bool m_bTruncated;
    int m_iReplyToStatusId;
    int m_iReplyToUserId;
    QString m_sReplyToScreenName;
    QString m_sThumbnailPic;
    QString m_sBmiddlePic;
    QString m_sOriginalPic;
    User m_user;
    RetweetedStatus m_retweetedStatus;

};
class ReplyComment
{
public:
    QString m_sCreatedAt;
    int m_iId;
    QString m_sText;
    User m_user;
};
class Comment
{
public:
    QString m_sCreatedAt;
    int m_iId;
    QString m_sText;
    User m_user;
    Status *m_status;
    ReplyComment m_replyComment;
    QString m_sSource;

};

class Count
{
public:
    int m_iId;
    int m_iComments;
    int m_iRt;
    int m_iNewStatus;
    int m_iFollowers;
    int m_iDm;
    int m_iMentions;
};

class Emtion
{
public:
    QString m_sPhrase;
    QString m_sType;
    QString m_sUrl;
    bool m_bIsHot;
    bool m_bCommon;
    int m_iOrderNumber;
    QString m_sCateGory;
};

class Sender
{
public:
    int m_iId;
    QString m_sScreenName;
    QString m_sName;
    int m_iProvince;
    int m_iCity;
    QString m_sLocation;
    QString m_sDescription;
    QString m_sUrl;
    QString m_sImageUrl;
    QString m_sDomain;
    QString m_sGender;

    int m_iFriendsCount;
    int m_iFollowersCount;
    int m_iStatusCount;
    int m_iFavouritesCount;

    QString m_sCreatedAt;
    bool m_bVerified;
    Status *m_status;
};

class Recipient
{
public:
    int m_iId;
    QString m_sScreenName;
    QString m_sName;
    int m_iProvince;
    int m_iCity;
    QString m_sLocation;
    QString m_sDescription;
    QString m_sUrl;
    QString m_sImageUrl;
    QString m_sDomain;
    QString m_sGender;

    int m_iFriendsCount;
    int m_iFollowersCount;
    int m_iStatusCount;
    int m_iFavouritesCount;

    QString m_sCreatedAt;
    bool m_bVerified;
    Status *m_status;
};


class DirectMessage
{
public:
    QString m_sCreatedAt;
    int m_iId;
    QString m_sText;
    int m_iSenderId;
    int m_iRecipientId;
    QString m_sSenderScreenName;
    QString m_sRecipientScreenName;
    Sender m_sender;
    Recipient m_Recipient;
};

class Source
{
public:
    int m_iId;
    QString m_sScreenName;
    bool m_bFollowing;
    bool m_bFollowedBy;
    bool m_bNotificationsEnabled;
};

class Target
{
public:
    int m_iId;
    QString m_sScreenName;
    bool m_bFollowing;
    bool m_bFollowedBy;
    bool m_bNotificationsEnabled;
};
class Relationship
{
public:
    Source m_source;
    Target m_target;
};



class Trend
{
public:
    int m_iTrendId;
    QString m_sHotWord;
    int m_iNum;
    QString m_sName;
    QString m_sQuery;
};

class Trends
{
public:
    QString m_sTime;
    Trend m_trend;
    int m_iAsOf;

};
class Ids
{
public:
    int m_iId;
};
class IdList
{
public:
    Ids m_ids;
    int m_iNextCursor;
    int m_iPreviousCursor;
};


class Tag
{
public:
    int m_iId;
    QString m_sValue;
};

class TagIds
{
public:
    int m_iTagId;
};

class Tags
{
public:
    Tag m_tag;
    int m_iTagId;
};

class Suggestion
{
public:
    int m_iUid;
    QString m_sNickName;
    QString m_sRemark;
};

class Hash
{
public:
    int m_iRemainingHits;
    int m_iHourlyLimit;
    int m_iResetTime;
    int m_iResetTimeInSeconds;
};

class Result
{
public:
    bool m_bComment;
    bool m_bDm;
    bool m_bRealName;
    bool m_bGeo;
    bool m_bBadge;
};

#endif // WEIBODATA_H
