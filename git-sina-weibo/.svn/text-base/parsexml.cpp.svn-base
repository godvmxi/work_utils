#include "parsexml.h"
#include <QDebug>
#include <QDomDocument>
#include <QNetworkAccessManager>
#include <QNetworkReply>
#include <QNetworkRequest>
#include <QTextCodec>
#include <QDomNode>

QList<Status*> ParseXml::parseFriendsTimeline(const QString &data)
{
    QList<Status*> statusList;
    QDomDocument doc;
    doc.setContent(data);
    if(!doc.isNull())
    {
        QDomNodeList nodeList = doc.elementsByTagName("status");
        for(int i = 0;i != nodeList.count();i++)
        {
            Status *status = parseStatus(nodeList.at(i).toElement());
            statusList.append(status);
        }
    }
    return statusList;
}
Status* ParseXml::parseStatus(const QDomElement &node)
{
    Status *status = new Status;
    QDomNode child = node.firstChild();
    while(!child.isNull())
    {
        QDomElement element = child.toElement();
        qDebug()<<"element.tagName() is"<<element.tagName();
        if("created_at" == element.tagName())
        {
            status->m_sCreatedAt = element.text();
            qDebug()<<status->m_sCreatedAt;
        } else if("id" == element.tagName())
        {
            status->m_iId = element.text().toInt();
        } else if("text" == element.tagName())
        {
            status->m_sText = element.text();
            qDebug()<<status->m_sText;
        } else if("source" == element.tagName())
        {
            status->m_sSource = parseSource(element);
            qDebug()<<status->m_sSource;
        } else if("favourited" == element.tagName())
        {
            if("true" == element.text())
            {
                status->m_bFavourited = true;
            } else if("false" == element.tagName())
            {
                status->m_bFavourited = false;
            }
        } else if("truncated" == element.tagName())
        {
            if("true" == element.text())
            {
                status->m_bTruncated = true;
            } else if("false" == element.text())
            {
                status->m_bTruncated = false;
            }
        } else if("in_reply_to_status_id" == element.tagName())
        {
            status->m_iReplyToStatusId = element.text().toInt();
        } else if("in_reply_to_user_id" == element.tagName())
        {
            status->m_iReplyToUserId = element.text().toInt();
        } else if("in_reply_to_screen_name" == element.tagName())
        {
            status->m_sReplyToScreenName = element.text();
            qDebug()<<status->m_sReplyToScreenName;
        } else if("thumbnail_pic" == element.tagName())
        {
            status->m_sThumbnailPic = element.text();
            QNetworkRequest m_request;
            m_request.setUrl(QUrl(status->m_sThumbnailPic));
            QNetworkAccessManager *m_manager = new QNetworkAccessManager;
            QNetworkReply *m_reply = m_manager->get(m_request);
            qDebug()<<m_reply;
        } else if("bmiddle_pic" == element.tagName())
        {
            status->m_sBmiddlePic = element.text();
            QNetworkRequest m_request;
            m_request.setUrl(QUrl(status->m_sThumbnailPic));
            QNetworkAccessManager *m_manager = new QNetworkAccessManager;
            QNetworkReply *m_reply = m_manager->get(m_request);
            qDebug()<<m_reply;
        } else if("original_pic" == element.tagName())
        {
            status->m_sOriginalPic = element.text();
            QNetworkRequest m_request;
            m_request.setUrl(QUrl(status->m_sThumbnailPic));
            QNetworkAccessManager *m_manager = new QNetworkAccessManager;
            QNetworkReply *m_reply = m_manager->get(m_request);
            qDebug()<<m_reply;
        } else if("user" == element.tagName())
        {
            status->m_user = parseUser(element);
            //qDebug()<<User.m_sScreenName;
        } else if("retweeted_status" == element.tagName())
        {
            status->m_retweetedStatus = parseRetweetedStatus(element);
            //qDebug()<<status->m_retweetedStatus;
        }
        child = child.nextSibling();
    }
    return status;
}
User ParseXml::parseUser(const QDomElement &element)
{
    QTextCodec::setCodecForTr(QTextCodec::codecForName("GB18030"));
    User user;
    QDomNode body = element.firstChild();

    while(!body.isNull())
    {
        QDomElement userElement = body.toElement();
        qDebug()<<"userElement.tagName() is"<<userElement.tagName();
        if(userElement.tagName() == "id")
        {
            user.m_iId = userElement.text().toInt();
        } else if(userElement.tagName() == "screen_name")
        {
            user.m_sScreenName = userElement.text();
            qDebug()<<user.m_sScreenName;
        } else if(userElement.tagName() == "name")
        {
            user.m_sName = userElement.text();
        } else if(userElement.tagName() == "province")
        {
            user.m_iProvince = userElement.text().toInt();
        } else if(userElement.tagName() == "city")
        {
            user.m_iCity = userElement.text().toInt();
        } else if(userElement.tagName() == "location")
        {
            user.m_sLocation = userElement.text();
            qDebug()<<user.m_sLocation;
        } else if(userElement.tagName() == "description")
        {
            user.m_sDescription = userElement.text();
            qDebug()<<user.m_sDescription;
        } else if(userElement.tagName() == "url")
        {
            user.m_sUrl = userElement.text();
            qDebug()<<user.m_sUrl;
        } else if(userElement.tagName() == "profile_image_url")
        {
            user.m_sImageUrl = userElement.text();
        } else if(userElement.tagName() == "domain")
        {
            user.m_sDomain = userElement.text();
        } else if(userElement.tagName() == "gender")
        {
            if(userElement.text() == "f")
            {
                user.m_sGender = QObject::tr("Å®");
            } else if(userElement.text() == "m")
            {
                user.m_sGender = QObject::tr("ÄÐ");
            }

            qDebug()<<user.m_sGender;
        } else if(userElement.tagName() == "followers_count")
        {
            user.m_iFollowersCount = userElement.text().toInt();
            qDebug()<<user.m_iFollowersCount;
        } else if(userElement.tagName() == "friends_count")
        {
            user.m_iFriendsCount = userElement.text().toInt();
            qDebug()<<user.m_iFriendsCount;
        } else if(userElement.tagName() == "statuses_count")
        {
            user.m_iStatusCount = userElement.text().toInt();
            qDebug()<<user.m_iStatusCount;
        } else if(userElement.tagName() == "favourites_count")
        {
            user.m_iFavouritesCount = userElement.text().toInt();
            qDebug()<<user.m_iFavouritesCount;
        } else if(userElement.tagName() == "created_at")
        {
            user.m_sCreatedAt = userElement.text();
            qDebug()<<user.m_sCreatedAt;
        } else if(userElement.tagName() == "verified")
        {
            if(userElement.text() == "true")
            {
                user.m_bVerified = true;
            } else if(userElement.text() == "false")
            {
                user.m_bVerified = false;
            }
            qDebug()<<user.m_bVerified;
        } else if(userElement.tagName() == "status")
        {
            user.m_status = parseStatus(userElement);
        }
        body = body.nextSibling();
    }
    return user;
}
QString ParseXml::parseSource(const QDomElement &element)
{
    QString str;
    QDomNode node = element.firstChild();
    while(!node.isNull())
    {
        QDomElement sourceElement = node.toElement();
        qDebug()<<"sourceElement.tagName() is"<<sourceElement.tagName();
        if(sourceElement.tagName() == "a"&&sourceElement.attribute("herf") == "")
        {
            str = sourceElement.text();
            qDebug()<<str;
        }
        node = node.nextSibling();
    }
    return str;
}
RetweetedStatus ParseXml::parseRetweetedStatus(const QDomElement &element)
{
    RetweetedStatus retweetedStatus;
    QDomNode child = element.firstChild();
    while(!child.isNull())
    {
        QDomElement retweetedElement = child.toElement();
        qDebug()<<"retweetedElement.tagName() is"<<retweetedElement.tagName();
        if(retweetedElement.tagName() == "created_at")
        {
            retweetedStatus.m_sCreatedAt = retweetedElement.text();
            qDebug()<<retweetedStatus.m_sCreatedAt;
        } else if(retweetedElement.tagName() == "id")
        {
            retweetedStatus.m_iId = retweetedElement.text().toInt();
        } else if(retweetedElement.tagName() == "text")
        {
            retweetedStatus.m_sText = retweetedElement.text();
            qDebug()<<retweetedStatus.m_sText;
        } else if(retweetedElement.tagName() == "source")
        {
            retweetedStatus.m_sSource = parseSource(retweetedElement);
            //qDebug()<<retweetedStatus.m_sSource;
        } else if(retweetedElement.tagName() == "favourited")
        {
            if(retweetedElement.text() == "true")
            {
                retweetedStatus.m_bFavourited = true;
            } else if(retweetedElement.text() == "false")
            {
                retweetedStatus.m_bFavourited = false;
            }
        } else if(retweetedElement.tagName() == "truncated")
        {
            if(retweetedElement.text() == "true")
            {
                retweetedStatus.m_bTruncated = true;
            } else if(retweetedElement.text() == "false")
            {
                retweetedStatus.m_bTruncated = false;
            }
        } else if(retweetedElement.tagName() == "in_reply_to_status_id")
        {
            retweetedStatus.m_iReplyToStatusId = retweetedElement.text().toInt();
        } else if(retweetedElement.tagName() == "in_reply_to_user_id")
        {
            retweetedStatus.m_iReplyToUserId = retweetedElement.text().toInt();
        } else if(retweetedElement.tagName() == "in_reply_to_screen_name")
        {
            retweetedStatus.m_sReplyToScreenName = retweetedElement.text();
            qDebug()<<retweetedStatus.m_sReplyToScreenName;
        } else if(retweetedElement.tagName() == "thumbnail_pic")
        {
            retweetedStatus.m_sThumbnailPic = retweetedElement.text();
            QNetworkRequest m_request;
            m_request.setUrl(QUrl(retweetedStatus.m_sThumbnailPic));
            QNetworkAccessManager *m_manager = new QNetworkAccessManager;
            QNetworkReply *m_reply = m_manager->get(m_request);
            qDebug()<<m_reply;
        } else if(retweetedElement.tagName() == "bmiddle_pic")
        {
            retweetedStatus.m_sBmiddlePic = retweetedElement.text();
            QNetworkRequest m_request;
            m_request.setUrl(QUrl(retweetedStatus.m_sThumbnailPic));
            QNetworkAccessManager *m_manager = new QNetworkAccessManager;
            QNetworkReply *m_reply = m_manager->get(m_request);
            qDebug()<<m_reply;
        } else if(retweetedElement.tagName() == "original_pic")
        {
            retweetedStatus.m_sOriginalPic = retweetedElement.text();
            QNetworkRequest m_request;
            m_request.setUrl(QUrl(retweetedStatus.m_sThumbnailPic));
            QNetworkAccessManager *m_manager = new QNetworkAccessManager;
            QNetworkReply *m_reply = m_manager->get(m_request);
            qDebug()<<m_reply;
        } else if(retweetedElement.tagName() == "user")
        {
            retweetedStatus.m_user = parseUser(retweetedElement);
            //qDebug()<<retweetedStatus->m_user;
        }
        child = child.nextSibling();
    }
    return retweetedStatus;
}

QList<Status*> ParseXml::parseUserTimeline(const QString &data)
{
    QList<Status*> statusList;
    QDomDocument doc;
    doc.setContent(data);
    if(!doc.isNull())
    {
        QDomNodeList nodeList = doc.elementsByTagName("status");
        for(int i = 0;i != nodeList.count();i++)
        {
            Status *status = parseStatus(nodeList.at(i).toElement());
            statusList.append(status);
        }
    }
    return statusList;
}

Comment* ParseXml::parseComment(const QDomNode &node)
{
    Comment *comments = new Comment;
    QDomNode child = node.firstChild();
    while(!child.isNull())
    {
        QDomElement element = child.toElement();
        qDebug()<<"element.tagName() is"<<element.tagName();
        if("created_at" == element.tagName())
        {
            comments->m_sCreatedAt = element.text();
            qDebug()<<comments->m_sCreatedAt;
        } else if("id" == element.tagName())
        {
            comments->m_iId = element.text().toInt();
        } else if("text" == element.tagName())
        {
            comments->m_sText = element.text();
            qDebug()<<comments->m_sText;
        } else if("source" == element.tagName())
        {
            comments->m_sSource = parseSource(element);
            qDebug()<<comments->m_sSource;
        } else if(element.tagName() == "user")
        {
            comments->m_user = parseUser(element);
        } else if(element.tagName() == "status")
        {
            comments->m_status = parseStatus(element);
        } else if(element.tagName() == "reply_comment")
        {
            comments->m_replyComment = parseReplyComment(element);
        }
        child = child.nextSibling();
    }
    return comments;
}
Count ParseXml::parseCount(const QDomElement &element)
{
    Count counts;
    QDomNode body = element.firstChild();

    while(!body.isNull())
    {
        QDomElement countElement = body.toElement();
        qDebug()<<"countElement.tagName() is"<<countElement.tagName();
        if(countElement.tagName() == "id")
        {
            counts.m_iId = countElement.text().toInt();
            qDebug()<<counts.m_iId;
        } else if(countElement.tagName() == "comments")
        {
            counts.m_iComments = countElement.text().toInt();
            qDebug()<<counts.m_iComments;
        } else if(countElement.tagName() == "rt")
        {
            counts.m_iRt = countElement.text().toInt();
            qDebug()<<counts.m_iRt;
        } else if(countElement.tagName() == "new_status")
        {
            counts.m_iNewStatus = countElement.text().toInt();
        } else if(countElement.tagName() == "followers")
        {
            counts.m_iFollowers = countElement.text().toInt();
            qDebug()<<counts.m_iFollowers;
        } else if(countElement.tagName() == "dm")
        {
            counts.m_iDm = countElement.text().toInt();
            qDebug()<<counts.m_iDm;
        } else if(countElement.tagName() == "mentions")
        {
            counts.m_iMentions = countElement.text().toInt();
            qDebug()<<counts.m_iMentions;
        }
        body = body.nextSibling();
    }
    return counts;
}
Emtion ParseXml::parseEmtion(const QDomElement &element)
{
    Emtion emtions;
    QDomNode node = element.firstChild();

    while(!node.isNull())
    {
        QDomElement emtionElement = node.toElement();
        qDebug()<<"emtionElement.tagName() is"<<emtionElement.tagName();
        if(emtionElement.tagName() == "phrase")
        {
            emtions.m_sPhrase = emtionElement.text();
            qDebug()<<emtions.m_sPhrase;
        } else if(emtionElement.tagName() == "type")
        {
            emtions.m_sType = emtionElement.text();
            qDebug()<<emtions.m_sType;
        } else if(emtionElement.tagName() == "url")
        {
            emtions.m_sUrl = emtionElement.text();
            qDebug()<<emtions.m_sUrl;
        } else if(emtionElement.tagName() == "is_hot")
        {
            //emtions.m_bIsHot = emtionElement.text();
            if(emtionElement.text() == "true")
            {
                emtions.m_bIsHot = true;
            } else if(emtionElement.text() == "false")
            {
                emtions.m_bIsHot = false;
            }
        } else if(emtionElement.tagName() == "is_common")
        {
            //emtions.m_bCommon = emtionElement.text();
            if(emtionElement.text() == "true")
            {
                emtions.m_bCommon = true;
            } else if(emtionElement.text() == "false")
            {
                emtions.m_bCommon = false;
            }
        } else if(emtionElement.tagName() == "order_number")
        {
            emtions.m_iOrderNumber = emtionElement.text().toInt();
            qDebug()<<emtions.m_iOrderNumber;
        } else if(emtionElement.tagName() == "category")
        {
            emtions.m_sCateGory = emtionElement.text();
            qDebug()<<emtions.m_sCateGory;
        }
        node = node.nextSibling();
    }
    return emtions;
}

ReplyComment ParseXml::parseReplyComment(const QDomElement &element)
{
    ReplyComment replyComments;
    QDomNode node = element.firstChild();

    while(!node.isNull())
    {
        QDomElement element = node.toElement();
        qDebug()<<"element.tagName() is"<<element.tagName();
        if("created_at" == element.tagName())
        {
            replyComments.m_sCreatedAt = element.text();
            qDebug()<<replyComments.m_sCreatedAt;
        } else if("id" == element.tagName())
        {
            replyComments.m_iId = element.text().toInt();
        } else if("text" == element.tagName())
        {
            replyComments.m_sText = element.text();
            qDebug()<<replyComments.m_sText;
        } else if(element.tagName() == "user")
        {
            replyComments.m_user = parseUser(element);
        }
        node = node.nextSibling();
    }
    return replyComments;
}
DirectMessage* ParseXml::parseDirectmessage(const QDomNode &node)
{
    DirectMessage *directMessages = new DirectMessage;
    QDomNode child = node.firstChild();

    while(!child.isNull())
    {
        QDomElement element = child.toElement();
        qDebug()<<"element.tagName() is"<<element.tagName();
        if("created_at" == element.tagName())
        {
            directMessages->m_sCreatedAt = element.text();
            qDebug()<<directMessages->m_sCreatedAt;
        } else if("id" == element.tagName())
        {
            directMessages->m_iId = element.text().toInt();
        } else if("text" == element.tagName())
        {
            directMessages->m_sText = element.text();
            qDebug()<<directMessages->m_sText;
        } else if(element.tagName() == "sender_id")
        {
            directMessages->m_iSenderId = element.text().toInt();
            qDebug()<<directMessages->m_iSenderId;
        } else if(element.tagName() == "recipient_id")
        {
            directMessages->m_iRecipientId = element.text().toInt();
            qDebug()<<directMessages->m_iRecipientId;
        } else if(element.tagName() == "sender_screen_name")
        {
            directMessages->m_sSenderScreenName = element.text();
            qDebug()<<directMessages->m_sSenderScreenName;
        } else if(element.tagName() == "recipient_screen_name")
        {
            directMessages->m_sRecipientScreenName = element.text();
            qDebug()<<directMessages->m_sRecipientScreenName;
        } else if(element.tagName() == "sender")
        {
            directMessages->m_sender = parseSender(element);
        } else if(element.tagName() == "recipient")
        {
            directMessages->m_Recipient = parseRecipient(element);
        }
        child = child.nextSibling();
    }
    return directMessages;
}
Sender ParseXml::parseSender(const QDomElement &element)
{
    Sender sender;
    QDomNode node = element.firstChild();

    while(!node.isNull())
    {
        QDomElement senderElement = node.toElement();
        qDebug()<<senderElement.tagName();
        if(senderElement.tagName() == "id")
        {
            sender.m_iId = senderElement.text().toInt();
        } else if(senderElement.tagName() == "screen_name")
        {
            sender.m_sScreenName = senderElement.text();
            qDebug()<<sender.m_sScreenName;
        } else if(senderElement.tagName() == "name")
        {
            sender.m_sName = senderElement.text();
        } else if(senderElement.tagName() == "province")
        {
            sender.m_iProvince = senderElement.text().toInt();
        } else if(senderElement.tagName() == "city")
        {
            sender.m_iCity = senderElement.text().toInt();
        } else if(senderElement.tagName() == "location")
        {
            sender.m_sLocation = senderElement.text();
            qDebug()<<sender.m_sLocation;
        } else if(senderElement.tagName() == "description")
        {
            sender.m_sDescription = senderElement.text();
            qDebug()<<sender.m_sDescription;
        } else if(senderElement.tagName() == "url")
        {
            sender.m_sUrl = senderElement.text();
            qDebug()<<sender.m_sUrl;
        } else if(senderElement.tagName() == "profile_image_url")
        {
           sender.m_sImageUrl = senderElement.text();
        } else if(senderElement.tagName() == "domain")
        {
            sender.m_sDomain = senderElement.text();
        } else if(senderElement.tagName() == "gender")
        {
            sender.m_sGender = senderElement.text();
            qDebug()<<sender.m_sGender;
        } else if(senderElement.tagName() == "followers_count")
        {
            sender.m_iFollowersCount = senderElement.text().toInt();
            qDebug()<<sender.m_iFollowersCount;
        } else if(senderElement.tagName() == "friends_count")
        {
            sender.m_iFriendsCount = senderElement.text().toInt();
            qDebug()<<sender.m_iFriendsCount;
        } else if(senderElement.tagName() == "statuses_count")
        {
            sender.m_iStatusCount = senderElement.text().toInt();
            qDebug()<<sender.m_iStatusCount;
        } else if(senderElement.tagName() == "favourites_count")
        {
            sender.m_iFavouritesCount = senderElement.text().toInt();
            qDebug()<<sender.m_iFavouritesCount;
        } else if(senderElement.tagName() == "created_at")
        {
            sender.m_sCreatedAt = senderElement.text();
            qDebug()<<sender.m_sCreatedAt;
        } else if(senderElement.tagName() == "verified")
        {
            if(senderElement.text() == "true")
            {
                sender.m_bVerified = true;
            } else if(senderElement.text() == "false")
            {
                sender.m_bVerified = false;
            }
            qDebug()<<sender.m_bVerified;
        }
        node = node.nextSibling();
    }
    return sender;
}
Recipient ParseXml::parseRecipient(const QDomElement &element)
{
    Recipient recipient;
    QDomNode node = element.firstChild();

    while(!node.isNull())
    {
        QDomElement recipientElement = node.toElement();
        qDebug()<<recipientElement.tagName();
        if(recipientElement.tagName() == "id")
        {
            recipient.m_iId = recipientElement.text().toInt();
        } else if(recipientElement.tagName() == "screen_name")
        {
            recipient.m_sScreenName = recipientElement.text();
            qDebug()<<recipient.m_sScreenName;
        } else if(recipientElement.tagName() == "name")
        {
            recipient.m_sName = recipientElement.text();
        } else if(recipientElement.tagName() == "province")
        {
            recipient.m_iProvince = recipientElement.text().toInt();
        } else if(recipientElement.tagName() == "city")
        {
            recipient.m_iCity = recipientElement.text().toInt();
        } else if(recipientElement.tagName() == "location")
        {
            recipient.m_sLocation = recipientElement.text();
            qDebug()<<recipient.m_sLocation;
        } else if(recipientElement.tagName() == "description")
        {
            recipient.m_sDescription = recipientElement.text();
            qDebug()<<recipient.m_sDescription;
        } else if(recipientElement.tagName() == "url")
        {
            recipient.m_sUrl = recipientElement.text();
            qDebug()<<recipient.m_sUrl;
        } else if(recipientElement.tagName() == "profile_image_url")
        {
           recipient.m_sImageUrl = recipientElement.text();
        } else if(recipientElement.tagName() == "domain")
        {
            recipient.m_sDomain = recipientElement.text();
        } else if(recipientElement.tagName() == "gender")
        {
            recipient.m_sGender = recipientElement.text();
            qDebug()<<recipient.m_sGender;
        } else if(recipientElement.tagName() == "followers_count")
        {
            recipient.m_iFollowersCount = recipientElement.text().toInt();
            qDebug()<<recipient.m_iFollowersCount;
        } else if(recipientElement.tagName() == "friends_count")
        {
            recipient.m_iFriendsCount = recipientElement.text().toInt();
            qDebug()<<recipient.m_iFriendsCount;
        } else if(recipientElement.tagName() == "statuses_count")
        {
            recipient.m_iStatusCount = recipientElement.text().toInt();
            qDebug()<<recipient.m_iStatusCount;
        } else if(recipientElement.tagName() == "favourites_count")
        {
            recipient.m_iFavouritesCount = recipientElement.text().toInt();
            qDebug()<<recipient.m_iFavouritesCount;
        } else if(recipientElement.tagName() == "created_at")
        {
            recipient.m_sCreatedAt = recipientElement.text();
            qDebug()<<recipient.m_sCreatedAt;
        } else if(recipientElement.tagName() == "verified")
        {
            if(recipientElement.text() == "true")
            {
                recipient.m_bVerified = true;
            } else if(recipientElement.text() == "false")
            {
                recipient.m_bVerified = false;
            }
            qDebug()<<recipient.m_bVerified;
        }
        node = node.nextSibling();
    }
    return recipient;
}
Relationship ParseXml::parseRelationship(const QDomElement &element)
{
    Relationship relationship;
    QDomNode node = element.firstChild();

    while(!node.isNull())
    {
        QDomElement relationElement = node.toElement();
        qDebug()<<relationElement.tagName();
        if(relationElement.tagName() == "source")
        {
            relationship.m_source = ParseSource(relationElement);
        } else if(relationElement.tagName() == "target")
        {
            relationship.m_target = parseTarget(relationElement);
        }
        node = node.nextSibling();
    }
    return relationship;
}
Source ParseXml::ParseSource(const QDomElement &element)
{
    Source source;
    QDomNode node = element.firstChild();

    while(!node.isNull())
    {
        QDomElement sourceElement = node.toElement();
        qDebug()<<sourceElement.tagName();
        if(sourceElement.tagName() == "id")
        {
            source.m_iId = sourceElement.text().toInt();
            qDebug()<<source.m_iId;
        } else if(sourceElement.tagName() == "screen_name")
        {
            source.m_sScreenName = sourceElement.text();
            qDebug()<<source.m_sScreenName;
        } else if(sourceElement.tagName() == "following")
        {
            //source.m_bFollowing = sourceElement.text();
            if(sourceElement.text() == "true")
            {
                source.m_bFollowing = true;
            } else if(sourceElement.text() == "false")
            {
                source.m_bFollowing = false;
            }
        } else if(sourceElement.tagName() == "followed_by")
        {
            //source.m_bFollowedBy = sourceElement.text();
            if(sourceElement.text() == "true")
            {
                source.m_bFollowedBy = true;
            } else if(sourceElement.text() == "false")
            {
                source.m_bFollowedBy = false;
            }
        } else if(sourceElement.tagName() == "notifications_enabled")
        {
            //source.m_bNotificationsEnabled = sourceElement.text();
            if(sourceElement.text() == "true")
            {
                source.m_bNotificationsEnabled = true;
            } else if(sourceElement.text() == "false")
            {
                source.m_bNotificationsEnabled = false;
            }
        }
        node = node.nextSibling();
    }
    return source;
}
Target ParseXml::parseTarget(const QDomElement &element)
{
    Target target;
    QDomNode node = element.firstChild();

    while(!node.isNull())
    {
        QDomElement targetElement = node.toElement();
        qDebug()<<targetElement.tagName();
        if(targetElement.tagName() == "id")
        {
            target.m_iId = targetElement.text().toInt();
            qDebug()<<target.m_iId;
        } else if(targetElement.tagName() == "screen_name")
        {
            target.m_sScreenName = targetElement.text();
            qDebug()<<target.m_sScreenName;
        } else if(targetElement.tagName() == "following")
        {
            //target.m_bFollowing = targetElement.text();
            if(targetElement.text() == "true")
            {
                target.m_bFollowing = true;
            } else if(targetElement.text() == "false")
            {
                target.m_bFollowing = false;
            }
        } else if(targetElement.tagName() == "followed_by")
        {
            //target.m_bFollowedBy = targetElement.text();
            if(targetElement.text() == "true")
            {
                target.m_bFollowedBy = true;
            } else if(targetElement.text() == "false")
            {
                target.m_bFollowedBy = false;
            }
        } else if(targetElement.tagName() == "notifications_enabled")
        {
            //target.m_bNotificationsEnabled = targetElement.text();
            if(targetElement.text() == "true")
            {
                target.m_bNotificationsEnabled = true;
            } else if(targetElement.text() == "false")
            {
                target.m_bNotificationsEnabled = false;
            }
        }
        node = node.nextSibling();
    }
    return target;
}
Trend ParseXml::parseTrend(const QDomElement &element)
{
    Trend trend;
    QDomNode node = element.firstChild();

    while(!node.isNull())
    {
        QDomElement trendElement = node.toElement();
        qDebug()<<trendElement.tagName();
        if(trendElement.tagName() == "trend_id")
        {
            trend.m_iTrendId = trendElement.text().toInt();
            qDebug()<<trend.m_iTrendId;
        } else if(trendElement.tagName() == "hotword")
        {
            trend.m_sHotWord = trendElement.text();
            qDebug()<<trend.m_sHotWord;
        } else if(trendElement.tagName() == "num")
        {
            trend.m_iNum = trendElement.text().toInt();
            qDebug()<<trend.m_iNum;
        } else if(trendElement.tagName() == "name")
        {
            trend.m_sName = trendElement.text();
            qDebug()<<trend.m_sName;
        } else if(trendElement.tagName() == "query")
        {
            trend.m_sQuery = trendElement.text();
            qDebug()<<trend.m_sQuery;
        }
        node = node.nextSibling();
    }
    return trend;
}
Trends* ParseXml::parseTrends(const QDomNode &node)
{
    Trends *trends = new Trends;
    QDomNode child = node.firstChild();

    while(!child.isNull())
    {
        QDomElement element = child.toElement();
        qDebug()<<element.tagName();
        if(element.tagName() == "time")
        {
            trends->m_sTime = element.text();
            qDebug()<<trends->m_sTime;
        } else if(element.tagName() == "trend")
        {
            trends->m_trend = parseTrend(element);
        } else if(element.tagName() == "as_of")
        {
            trends->m_iAsOf = element.text().toInt();
            qDebug()<<trends->m_iAsOf;
        }
        child = child.nextSibling();
    }
    return trends;
}
IdList* ParseXml::parseIdList(const QDomNode &node)
{
    IdList *idList = new IdList;
    QDomNode body = node.firstChild();

    while(!body.isNull())
    {
        QDomElement element = body.toElement();
        qDebug()<<element.tagName();
        if(element.tagName() == "ids")
        {
          idList->m_ids = parseIds(element);
        } else if(element.tagName() == "next_cursor")
        {
            idList->m_iNextCursor = element.text().toInt();
            qDebug()<<idList->m_iNextCursor;
        } else if(element.tagName() == "previous_cursor")
        {
            idList->m_iPreviousCursor = element.text().toInt();
            qDebug()<<idList->m_iPreviousCursor;
        }
        body = body.nextSibling();
    }
    return idList;
}
Ids ParseXml::parseIds(const QDomElement &element)
{
    Ids id;
    QDomNode node = element.firstChild();

    while(!node.isNull())
    {
        QDomElement idElement = node.toElement();
        qDebug()<<idElement.tagName();
        if(idElement.tagName() == "id")
        {
            id.m_iId = idElement.text().toInt();
            qDebug()<<id.m_iId;
        }
        node = node.nextSibling();
    }
    return id;
}
Tag ParseXml::parseTag(const QDomElement &element)
{
    Tag tag;
    QDomNode node = element.firstChild();

    while(!node.isNull())
    {
        QDomElement tagElement = node.toElement();
        qDebug()<<tagElement.tagName();
        if(tagElement.tagName() == "id")
        {
            tag.m_iId = tagElement.text().toInt();
            qDebug()<<tag.m_iId;
        } else if(tagElement.tagName() == "value")
        {
            tag.m_sValue = tagElement.text();
            qDebug()<<tag.m_sValue;
        }
        node = node.nextSibling();
    }
    return tag;
}
TagIds ParseXml::parseTagIds(const QDomElement &element)
{
    TagIds tagIds;
    QDomNode node = element.firstChild();

    while(!node.isNull())
    {
        QDomElement tagIdElement = node.toElement();
        qDebug()<<tagIdElement.tagName();
        if(tagIdElement.tagName() == "tagid")
        {
            tagIds.m_iTagId = tagIdElement.text().toInt();
            qDebug()<<tagIds.m_iTagId;
        }
        node = node.nextSibling();
    }
    return tagIds;
}
Tags* ParseXml::parseTags(const QDomNode &node)
{
    Tags *tags = new Tags;
    QDomNode child = node.firstChild();

    while(!child.isNull())
    {
        QDomElement element = child.toElement();
        qDebug()<<element.tagName();
        if(element.tagName() == "tag")
        {
            tags->m_tag = parseTag(element);
        } else if(element.tagName() == "tagid")
        {
            tags->m_iTagId = element.text().toInt();
            qDebug()<<tags->m_iTagId;
        }
        child = child.nextSibling();
    }
    return tags;
}
Suggestion ParseXml::parseSuggestion(const QDomElement &element)
{
    Suggestion suggestion;
    QDomNode node = element.firstChild();

    while(!node.isNull())
    {
        QDomElement suggestionElement = node.toElement();
        qDebug()<<suggestionElement.tagName();
       if(suggestionElement.tagName() == "uid")
       {
           suggestion.m_iUid = suggestionElement.text().toInt();
           qDebug()<<suggestion.m_iUid;
       } else if(suggestionElement.tagName() == "nickname")
       {
           suggestion.m_sNickName = suggestionElement.text();
           qDebug()<<suggestion.m_sNickName;
       } else if(suggestionElement.tagName() == "remark")
       {
           suggestion.m_sRemark = suggestionElement.text();
           qDebug()<<suggestion.m_sRemark;
       }
       node = node.nextSibling();
    }
    return suggestion;
}
Hash ParseXml::parseHash(const QDomElement &element)
{
    Hash hash;
    QDomNode node = element.firstChild();

    while(!node.isNull())
    {
        QDomElement hashElement = node.toElement();
        qDebug()<<hashElement.tagName();
        if(hashElement.tagName() == "remaining_hits")
        {
            hash.m_iRemainingHits = hashElement.text().toInt();
            qDebug()<<hash.m_iRemainingHits;
        } else if(hashElement.tagName() == "hourly_limit")
        {
            hash.m_iHourlyLimit = hashElement.text().toInt();
            qDebug()<<hash.m_iHourlyLimit;
        } else if(hashElement.tagName() == "reset_time_in_seconds")
        {
            hash.m_iResetTimeInSeconds = hashElement.text().toInt();
            qDebug()<<hash.m_iResetTimeInSeconds;
        } else if(hashElement.tagName() == "reset_time")
        {
            hash.m_iResetTime = hashElement.text().toInt();
            qDebug()<<hash.m_iResetTime;
        }
        node = node.nextSibling();
    }
    return hash;
}

Result ParseXml::parseResult(const QDomElement &element)
{
    Result result;
    QDomNode node = element.firstChild();

    while(!node.isNull())
    {
        QDomElement resultElement = node.toElement();
        qDebug()<<resultElement.tagName();
        if(resultElement.tagName() == "comment")
        {
            if(resultElement.text() == "1")
            {
                result.m_bComment = true;
            } else if(resultElement.text() == "0")
            {
                result.m_bComment = false;
            }
        } else if(resultElement.tagName() == "dm")
        {
            if(resultElement.text() == "1")
            {
                result.m_bDm = true;
            } else if(resultElement.text() == "0")
            {
                result.m_bDm = false;
            }
        } else if(resultElement.tagName() == "real_name")
        {
            if(resultElement.text() == "1")
            {
                result.m_bRealName = true;
            } else if(resultElement.text() == "0")
            {
                result.m_bRealName = false;
            }
        } else if(resultElement.tagName() == "geo")
        {
            if(resultElement.text() == "1")
            {
                result.m_bGeo = true;
            } else if(resultElement.text() == "0")
            {
                result.m_bGeo = false;
            }
        } else if(resultElement.tagName() == "badge")
        {
            if(resultElement.text() == "1")
            {
                result.m_bBadge = true;
            } else if(resultElement.text() == "0")
            {
                result.m_bBadge = false;
            }
        }
        node = node.nextSibling();
    }
    return result;
}

QList<Status*> ParseXml::parseMentions(const QString &data)
{
    QList<Status*> mentionList;
    QDomDocument doc;
    doc.setContent(data);
    if(!doc.isNull())
    {
        QDomNodeList nodeList = doc.elementsByTagName("status");
        for(int i = 0;i != nodeList.count();i++)
        {
            Status *status = parseStatus(nodeList.at(i).toElement());
            mentionList.append(status);
        }
    }
    return mentionList;
}
QList<Comment*> ParseXml::parseCommentsTimeline(const QString &data)
{
    QList<Comment*> commentsList;
    QDomDocument doc;
    doc.setContent(data);
    if(!doc.isNull())
    {
        QDomNodeList nodeList = doc.elementsByTagName("comment");
        for(int i = 0;i != nodeList.count();i++)
        {
            Comment *comments = parseComment(nodeList.at(i));
            commentsList.append(comments);
        }
    }
    return commentsList;
}
QList<Comment*> ParseXml::parseCommentsByMe(const QString &data)
{
    QList<Comment*> commentList;
    QDomDocument doc;
    doc.setContent(data);
    if(!doc.isNull())
    {
        QDomNodeList nodeList = doc.elementsByTagName("comment");
        for(int i = 0;i != nodeList.count();i++)
        {
            Comment *comments = parseComment(nodeList.at(i));
            commentList.append(comments);
        }
    }
    return commentList;
}
QList<Comment*> ParseXml::parseCommentsToMe(const QString &data)
{
    Status status;
    int64_t id = status.m_iId;

    QList<Comment*> commentList;
    QDomDocument doc;
    doc.setContent(data);
    if(!doc.isNull())
    {
        QDomNodeList nodeList = doc.elementsByTagName("comment");
        for(int i = 0;i != nodeList.count();i++)
        {
            Comment *comments = parseComment(nodeList.at(i));
            commentList.append(comments);
        }
    }
    return commentList;
}
QList<Comment*> ParseXml::parseComments(const QString &data)
{
    QList<Comment*> stringList;
    QDomDocument doc;
    doc.setContent(data);
    if(!doc.isNull())
    {
        QDomNodeList nodeList = doc.elementsByTagName("comment");
        for(int i = 0;i != nodeList.count();i++)
        {
            Comment *comments = parseComment(nodeList.at(i));
            stringList.append(comments);
        }
    }
    return stringList;
}
QList<Count*> ParseXml::parseCounts(const QString &data)
{
    QList<Count*> countList;
    QDomDocument doc;
    doc.setContent(data);
    if(!doc.isNull())
    {
        QDomNodeList nodeList = doc.elementsByTagName("count");
        for(int i = 0;i != nodeList.count();i++)
        {
            Count counts = parseCount(nodeList.at(i).toElement());
            countList.append(&counts);
        }
    }
    return countList;
}
QList<Status*> ParseXml::parseRepostTimeline(const QString &data)
{
    QList<Status*> statusList;
    QDomDocument doc;
    doc.setContent(data);
    if(!doc.isNull())
    {
        QDomNodeList nodeList = doc.elementsByTagName("status");
        for(int i = 0;i != nodeList.count();i++)
        {
            Status *status = parseStatus(nodeList.at(i).toElement());
            statusList.append(status);
        }
    }
    return statusList;
}
QList<Status*> ParseXml::parseRepostByMe(const QString &data)
{
    QList<Status*> statusList;
    QDomDocument doc;
    doc.setContent(data);
    if(!doc.isNull())
    {
        QDomNodeList nodeList = doc.elementsByTagName("status");
        for(int i = 0;i != nodeList.count();i++)
        {
            Status *status = parseStatus(nodeList.at(i).toElement());
            statusList.append(status);
        }
    }
    return statusList;
}
Count ParseXml::parseUnRead(const QString &data)
{

    QDomDocument doc;
    doc.setContent(data);
    if(!doc.isNull())
    {
        QDomNodeList nodeList = doc.elementsByTagName("count");
        for(int i =0;i != nodeList.count();i++)
       {
            Count count = parseCount(nodeList.at(i).toElement());
            return count;
       }

    }

}
bool ParseXml::parseResetCount(const QString &data)
{
    QDomDocument doc;
    doc.setContent(data);
    if(!doc.isNull())
    {
        QDomNodeList nodeList = doc.elementsByTagName("result");
        for(int i =0;i != nodeList.count();i++)
        {
            if(nodeList.at(i).toElement().text() == "true")
          {
            return true;
          } else if(nodeList.at(i).toElement().text() == "false")
          {
            return false;
          }
        }
    }
}
QList<Emtion*> ParseXml::parseEmotions(const QString &data)
{
    QList<Emtion*> emtionList;
    QDomDocument doc;
    doc.setContent(data);
    if(!doc.isNull())
    {
        QDomNodeList nodeList = doc.elementsByTagName("emtion");
        for(int i = 0;i != nodeList.count();i++)
        {
            Emtion emtions = parseEmtion(nodeList.at(i).toElement());
            emtionList.append(&emtions);
        }
    }
    return emtionList;
}
QList<Status*> ParseXml::parseShow(const QString &data)
{

    QList<Status*> statusList;
    QDomDocument doc;
    doc.setContent(data);
    if(!doc.isNull())
    {
        QDomNodeList nodeList = doc.elementsByTagName("status");
        for(int i = 0;i != nodeList.count();i++)
       {
           Status *status = parseStatus(nodeList.at(i).toElement());
            statusList.append(status);
       }
    }
     return statusList;
}
Status* ParseXml::parseUpDate(const QString &data)
{
    Status *status = new Status;
    QDomDocument doc;
    doc.setContent(data);
    if(!doc.isNull())
    {
        QDomNodeList nodeList = doc.elementsByTagName("status");
        for(int i = 0;i != nodeList.count();i++)
       {
           status = parseStatus(nodeList.at(i).toElement());

       }

    }
    return status;
}
Status* ParseXml::parseUpLoad(const QString &data)
{
    Status *status = new Status;
    QDomDocument doc;
    doc.setContent(data);
    if(!doc.isNull())
    {
        QDomNodeList nodeList = doc.elementsByTagName("status");
        for(int i = 0;i != nodeList.count();i++)
       {
           status = parseStatus(nodeList.at(i).toElement());

       }
    }
    return status;
}
Status* ParseXml::parseDestroy(const QString &data)
{
    Status *status = new Status;
    QDomDocument doc;
    doc.setContent(data);
    if(!doc.isNull())
    {
        QDomNodeList nodeList = doc.elementsByTagName("status");
        for(int i = 0;i != nodeList.count();i++)
       {
           status = parseStatus(nodeList.at(i).toElement());

       }
    }
    return status;
}
Status* ParseXml::parseRepost(const QString &data)
{
    Status *status = new Status;
    QDomDocument doc;
    doc.setContent(data);
    if(!doc.isNull())
    {
        QDomNodeList nodeList = doc.elementsByTagName("status");
        for(int i = 0;i != nodeList.count();i++)
       {
           status = parseStatus(nodeList.at(i).toElement());

       }
    }
    return status;
}
Comment* ParseXml::ParseComment(const QString &data)
{
    Comment *comment = new Comment;
    QDomDocument doc;
    doc.setContent(data);
    if(!doc.isNull())
    {
        QDomNodeList nodeList = doc.elementsByTagName("comment");
        for(int i = 0;i != nodeList.count();i++)
        {
            comment = parseComment(nodeList.at(i));

        }
    }
    return comment;
}
Comment* ParseXml::parseCommentDestroy(const QString &data)
{
    Comment *comment = new Comment;
    QDomDocument doc;
    doc.setContent(data);
    if(!doc.isNull())
    {
        QDomNodeList nodeList = doc.elementsByTagName("comment");
        for(int i = 0;i != nodeList.count();i++)
        {
            comment = parseComment(nodeList.at(i));

        }
    }
    return comment;
}
QList<Comment*> ParseXml::parseCommentDestroyBatch(const QString &data)
{
    QList<Comment*> commentList;
    QDomDocument doc;
    doc.setContent(data);
    if(!doc.isNull())
    {
        QDomNodeList nodeList = doc.elementsByTagName("comment");
        for(int i = 0;i != nodeList.count();i++)
        {
            Comment *comments = parseComment(nodeList.at(i));
            commentList.append(comments);
        }
    }
    return commentList;
}
Comment* ParseXml::parseReply(const QString &data)
{
    Comment *comment = new Comment;
    QDomDocument doc;
    doc.setContent(data);
    if(!doc.isNull())
    {
        QDomNodeList nodeList = doc.elementsByTagName("comment");
        for(int i = 0;i != nodeList.count();i++)
        {
            comment = parseComment(nodeList.at(i));

        }
    }
    return comment;
}
User ParseXml::parseUserShow(const QString &data)
{
    QDomDocument doc;
    doc.setContent(data);
    if(!doc.isNull())
    {
        QDomNodeList nodeList = doc.elementsByTagName("user");
        for(int i = 0;i != nodeList.count();i++)
        {
            User user = parseUser(nodeList.at(i).toElement());
            return user;
        }

    }
}
QList<User> ParseXml::parseStatusFriends(const QString &data)
{
    QList<User> userList;
    QDomDocument doc;
    doc.setContent(data);
    if(!doc.isNull())
    {
        QDomNodeList nodeList = doc.elementsByTagName("user");
        for(int i = 0;i != nodeList.count();i++)
        {
            User users = parseUser(nodeList.at(i).toElement());
            userList.append(users);
        }
    }
    return userList;
}
QList<User> ParseXml::parseFollowers(const QString &data)
{
    QList<User> userList;
    QDomDocument doc;
    doc.setContent(data);
    if(!doc.isNull())
    {
        QDomNodeList nodeList = doc.elementsByTagName("user");
        for(int i = 0;i != nodeList.count();i++)
        {
            User users = parseUser(nodeList.at(i).toElement());
            userList.append(users);

        }
    }
    return userList;
}
QList<User> ParseXml::parseUsersHot(const QString &data)
{
    QList<User> userList;
    QDomDocument doc;
    doc.setContent(data);
    if(!doc.isNull())
    {
        QDomNodeList nodeList = doc.elementsByTagName("user");
        for(int i = 0;i != nodeList.count();i++)
        {
            User users = parseUser(nodeList.at(i).toElement());
            userList.append(users);

        }
    }
    return userList;
}
User ParseXml::parseUpDateRemark(const QString &data)
{
    QDomDocument doc;
    doc.setContent(data);
    if(!doc.isNull())
    {
        QDomNodeList nodeList = doc.elementsByTagName("user");
        for(int i = 0;i != nodeList.count();i++)
        {
            User users = parseUser(nodeList.at(i).toElement());
            return users;
        }
    }
}
QList<User> ParseXml::parseSuggestions(const QString &data)
{
    QList<User> userList;
    QDomDocument doc;
    doc.setContent(data);
    if(!doc.isNull())
    {
        QDomNodeList nodeList = doc.elementsByTagName("user");
        for(int i = 0;i != nodeList.count();i++)
        {
            User users = parseUser(nodeList.at(i).toElement());
            userList.append(users);

        }
    }
    return userList;
}
QList<DirectMessage*> ParseXml::parseDirectmessages(const QString &data)
{
    QList<DirectMessage*> messagesList;
    QDomDocument doc;
    doc.setContent(data);
    if(!doc.isNull())
    {
        QDomNodeList nodeList = doc.elementsByTagName("direct_message");
        for(int i = 0;i !=nodeList.count();i++)
        {
            DirectMessage *messages = parseDirectmessage(nodeList.at(i));
            messagesList.append(messages);
        }
    }
    return messagesList;

}
QList<DirectMessage*> ParseXml::parseMessageSent(const QString &data)
{
    QList<DirectMessage*> messagesList;
    QDomDocument doc;
    doc.setContent(data);
    if(!doc.isNull())
    {
        QDomNodeList nodeList = doc.elementsByTagName("direct_message");
        for(int i = 0;i !=nodeList.count();i++)
        {
            DirectMessage *messages = parseDirectmessage(nodeList.at(i));
            messagesList.append(messages);
        }
    }
    return messagesList;
}
DirectMessage* ParseXml::parseMessage(const QString &data)
{
    DirectMessage *messages = new DirectMessage;
    QDomDocument doc;
    doc.setContent(data);
    if(!doc.isNull())
    {
        QDomNodeList nodeList = doc.elementsByTagName("direct_message");
        for(int i = 0;i !=nodeList.count();i++)
        {
            messages = parseDirectmessage(nodeList.at(i));

        }
    }
    return messages;
}
DirectMessage* ParseXml::parseMessageDestroy(const QString &data)
{
    DirectMessage *messages = new DirectMessage;
    QDomDocument doc;
    doc.setContent(data);
    if(!doc.isNull())
    {
        QDomNodeList nodeList = doc.elementsByTagName("direct_message");
        for(int i = 0;i !=nodeList.count();i++)
        {
            messages = parseDirectmessage(nodeList.at(i));

        }
    }
    return messages;
}
QList<DirectMessage*> ParseXml::parseMessageDestroyBatch(const QString &data)
{
    QList<DirectMessage*> messagesList;
    QDomDocument doc;
    doc.setContent(data);
    if(!doc.isNull())
    {
        QDomNodeList nodeList = doc.elementsByTagName("direct_message");
        for(int i = 0;i !=nodeList.count();i++)
        {
            DirectMessage *messages = parseDirectmessage(nodeList.at(i));
            messagesList.append(messages);
        }
    }
    return messagesList;
}
User ParseXml::parseFriendshipCreate(const QString &data)
{
    QDomDocument doc;
    doc.setContent(data);
    if(!doc.isNull())
    {
        QDomNodeList nodeList = doc.elementsByTagName("user");
        for(int i = 0;i != nodeList.count();i++)
        {
            User users = parseUser(nodeList.at(i).toElement());
            return users;
        }

    }
}
User ParseXml::parseFriendshipDestroy(const QString &data)
{
    QDomDocument doc;
    doc.setContent(data);
    if(!doc.isNull())
    {
        QDomNodeList nodeList = doc.elementsByTagName("user");
        for(int i = 0;i != nodeList.count();i++)
        {
            User users = parseUser(nodeList.at(i).toElement());
            return users;
        }
    }
}
bool ParseXml::parseFriendshipexists(const QString &data)
{
    QDomDocument doc;
    doc.setContent(data);
    if(!doc.isNull())
    {
        QDomNodeList nodeList = doc.elementsByTagName("friends");
        for(int i = 0;i != nodeList.count();i++)
        {
            if(nodeList.at(i).toElement().text() == "true")
           {
              return true;
           } else if(nodeList.at(i).toElement().text() == "false")
           {
              return false;
           }
        }
    }
}
Relationship ParseXml::parseFriendshipShow(const QString &data)
{
    QDomDocument doc;
    doc.setContent(data);
    if(!doc.isNull())
    {
        QDomNodeList nodeList = doc.elementsByTagName("relationship");
        for(int i = 0;i != nodeList.count();i++)
        {
            Relationship relationship = parseRelationship(nodeList.at(i).toElement());
            return relationship;
        }
    }
}
QList<Trend> ParseXml::ParseTrends(const QString &data)
{
    QList<Trend> trendList;
    QDomDocument doc;
    doc.setContent(data);
    if(!doc.isNull())
    {
        QDomNodeList nodeList = doc.elementsByTagName("trend");
        for(int i = 0;i != nodeList.count();i++)
        {
            Trend trends = parseTrend(nodeList.at(i).toElement());
            trendList.append(trends);
        }
    }
    return trendList;
}
QList<Status*> ParseXml::parseTrendStatus(const QString &data)
{
    QList<Status*> statusList;
    QDomDocument doc;
    doc.setContent(data);
    if(!doc.isNull())
    {
        QDomNodeList nodeList = doc.elementsByTagName("status");
        for(int i =0 ;i != nodeList.count();i++)
        {
            Status *status = parseStatus(nodeList.at(i).toElement());
            statusList.append(status);
        }
    }
    return statusList;
}
QList<int> ParseXml::parseTrendsFollow(const QString &data)
{
    QList<int> var;
    QDomDocument doc;
    doc.setContent(data);
    if(!doc.isNull())
    {
        QDomNodeList nodeList = doc.elementsByTagName("topicid");
        for(int i =0 ;i != nodeList.count();i++)
        {
            var.append(nodeList.at(i).toElement().text().toInt());
            //var.append("<br />");
        }
    }
    return var;
}
bool ParseXml::parseTrendDestroy(const QString &data)
{
    QDomDocument doc;
    doc.setContent(data);
    if(!doc.isNull())
    {
        QDomNodeList nodeList = doc.elementsByTagName("result");
        for(int i =0 ;i != nodeList.count();i++)
        {
            if(nodeList.at(i).toElement().text() == "true")
            {
                return true;
            } else if(nodeList.at(i).toElement().text() == "false")
            {
                return false;
            }
        }
    }
}
QList<Trends*> ParseXml::parseTrendsHourly(const QString &data)
{
    QList<Trends*> trendList;
    QDomDocument doc;
    doc.setContent(data);
    if(!doc.isNull())
    {
        QDomNodeList nodeList = doc.elementsByTagName("trend");
        for(int i = 0;i != nodeList.count();i++)
        {
            Trends *trends = parseTrends(nodeList.at(i));
            trendList.append(trends);
        }
    }
    return trendList;
}
QList<Trends*> ParseXml::parseTrendsDaily(const QString &data)
{
    QList<Trends*> trendList;
    QDomDocument doc;
    doc.setContent(data);
    if(!doc.isNull())
    {
        QDomNodeList nodeList = doc.elementsByTagName("trend");
        for(int i = 0;i != nodeList.count();i++)
        {
            Trends *trends = parseTrends(nodeList.at(i));
            trendList.append(trends);
        }
    }
    return trendList;
}
QList<Trends*> ParseXml::parseTrendsWeekly(const QString &data)
{
    QList<Trends*> trendList;
    QDomDocument doc;
    doc.setContent(data);
    if(!doc.isNull())
    {
        QDomNodeList nodeList = doc.elementsByTagName("trend");
        for(int i = 0;i != nodeList.count();i++)
        {
            Trends *trends = parseTrends(nodeList.at(i));
            trendList.append(trends);
        }
    }
    return trendList;
}
IdList* ParseXml::parseFriendIds(const QString &data)
{
    IdList *idList = new IdList;
    QDomDocument doc;
    doc.setContent(data);
    if(!doc.isNull())
    {
        QDomNodeList nodeList = doc.elementsByTagName("id_list");
        for(int i =0 ;i != nodeList.count();i++)
        {
            idList = parseIdList(nodeList.at(i));

        }
    }
    return idList;
}
IdList* ParseXml::parseFollowersId(const QString &data)
{
    IdList *idList = new IdList;
    QDomDocument doc;
    doc.setContent(data);
    if(!doc.isNull())
    {
        QDomNodeList nodeList = doc.elementsByTagName("id_list");
        for(int i =0 ;i != nodeList.count();i++)
        {
            idList = parseIdList(nodeList.at(i));

        }
    }
    return idList;
}
bool ParseXml::parseUpdatePrivacy(const QString &data)
{
    QDomDocument doc;
    doc.setContent(data);
    if(!doc.isNull())
    {
        QDomNodeList nodeList = doc.elementsByTagName("result");
        for(int i =0 ;i != nodeList.count();i++)
        {
            if(nodeList.at(i).toElement().text() == "true")
            {
                return true;
            } else if(nodeList.at(i).toElement().text() == "false")
            {
                return false;
            }
        }
    }
}

Result ParseXml::parseGetPrivacy(const QString &data)
{
    QDomDocument doc;
    doc.setContent(data);
    if(!doc.isNull())
    {
        QDomNodeList nodeList = doc.elementsByTagName("result");
        for(int i =0 ;i != nodeList.count();i++)
        {
            Result result = parseResult(nodeList.at(i).toElement());
            return result;
        }
    }
}
User ParseXml::parseBlocksCreate(const QString &data)
{
    QDomDocument doc;
    doc.setContent(data);
    if(!doc.isNull())
    {
        QDomNodeList nodeList = doc.elementsByTagName("user");
        for(int i =0 ;i != nodeList.count();i++)
        {
            User user = parseUser(nodeList.at(i).toElement());
            return user;
        }
    }
}
User ParseXml::parseBloclsDestroy(const QString &data)
{
    QDomDocument doc;
    doc.setContent(data);
    if(!doc.isNull())
    {
        QDomNodeList nodeList = doc.elementsByTagName("user");
        for(int i =0 ;i != nodeList.count();i++)
        {
            User user = parseUser(nodeList.at(i).toElement());
            return user;
        }
    }
}
bool ParseXml::parseBlocksExists(const QString &data)
{
    QDomDocument doc;
    doc.setContent(data);
    if(!doc.isNull())
    {
        QDomNodeList nodeList = doc.elementsByTagName("result");
        for(int i =0 ;i != nodeList.count();i++)
       {
           if(nodeList.at(i).toElement().text() == "true")
            {
                return true;
            } else if(nodeList.at(i).toElement().text() == "false")
            {
                return false;
            }
       }
    }
}
QList<Ids> ParseXml::parseBlockingIds(const QString &data)
{
    QList<Ids> idList;
    QDomDocument doc;
    doc.setContent(data);
    if(!doc.isNull())
    {
        QDomNodeList nodeList = doc.elementsByTagName("id");
        for(int i = 0;i != nodeList.count();i++)
        {
            Ids id = parseIds(nodeList.at(i).toElement());
            idList.append(id);
        }
    }
    return idList;
}
QList<Tag> ParseXml::ParseTags(const QString &data)
{
    QList<Tag> tagList;
    QDomDocument doc;
    doc.setContent(data);
    if(!doc.isNull())
    {
        QDomNodeList nodeList = doc.elementsByTagName("tag");
        for(int i = 0;i != nodeList.count();i++)
        {
            Tag tag = parseTag(nodeList.at(i).toElement());
            tagList.append(tag);
        }
    }
    return tagList;
}
TagIds ParseXml::parseTagsCreate(const QString &data)
{
    QDomDocument doc;
    doc.setContent(data);
    if(!doc.isNull())
    {
        QDomNodeList nodeList = doc.elementsByTagName("tagid");
        for(int i = 0;i != nodeList.count();i++)
        {
            TagIds tagIds = parseTagIds(nodeList.at(i).toElement());
            return tagIds;
        }
    }
}
QList<Tag> ParseXml::parseTagSuggestions(const QString &data)
{
    QList<Tag> tagList;
    QDomDocument doc;
    doc.setContent(data);
    if(!doc.isNull())
    {
        QDomNodeList nodeList = doc.elementsByTagName("tag");
        for(int i = 0;i != nodeList.count();i++)
        {
            Tag tag = parseTag(nodeList.at(i).toElement());
            tagList.append(tag);
        }
    }
    return tagList;
}
bool ParseXml::parseTagDestroy(const QString &data)
{
    QDomDocument doc;
    doc.setContent(data);
    if(!doc.isNull())
    {
        QDomNodeList nodeList = doc.elementsByTagName("result");
        for(int i = 0;i != nodeList.count();i++)
       {

           if(nodeList.at(i).toElement().text() == "1")
            {
                return true;
            } else if(nodeList.at(i).toElement().text() == "0")
            {
                return false;
            }
       }

    }
}
TagIds ParseXml::parseTagDestroyBatch(const QString &data)
{
    QDomDocument doc;
    doc.setContent(data);
    if(!doc.isNull())
    {
        QDomNodeList nodeList = doc.elementsByTagName("tagids");
        for(int i = 0;i != nodeList.count();i++)
        {
            TagIds tag = parseTagIds(nodeList.at(i).toElement());
            return tag;
        }
    }
}
User ParseXml::parseVerifyCredentials(const QString &data)
{
    QDomDocument doc;
    doc.setContent(data);
    if(!doc.isNull())
    {
        QDomNodeList nodeList = doc.elementsByTagName("user");
        for(int i = 0;i != nodeList.count();i++)
        {
            User user = parseUser(nodeList.at(i).toElement());
            return user;
        }
    }
}
Hash ParseXml::parseRateLimitStatus(const QString &data)
{
    QDomDocument doc;
    doc.setContent(data);
    if(!doc.isNull())
    {
        QDomNodeList nodeList = doc.elementsByTagName("hash");
        for(int i = 0;i != nodeList.count();i++)
        {
            Hash hash = parseHash(nodeList.at(i).toElement());
            return hash;
        }
    }
}
User ParseXml::parseEndSession(const QString &data)
{
    QDomDocument doc;
    doc.setContent(data);
    if(!doc.isNull())
    {
        QDomNodeList nodeList = doc.elementsByTagName("user");
        for(int i = 0;i != nodeList.count();i++)
        {
            User user = parseUser(nodeList.at(i).toElement());
            return user;
        }
    }
}
User ParseXml::parseUpdateProfileImage(const QString &data)
{
    QDomDocument doc;
    doc.setContent(data);
    if(!doc.isNull())
    {
        QDomNodeList nodeList = doc.elementsByTagName("user");
        for(int i = 0;i != nodeList.count();i++)
        {
            User user = parseUser(nodeList.at(i).toElement());
            return user;
        }
    }
}
User ParseXml::parseUpdateProfile(const QString &data)
{
    QDomDocument doc;
    doc.setContent(data);
    if(!doc.isNull())
    {
        QDomNodeList nodeList = doc.elementsByTagName("user");
        for(int i = 0;i != nodeList.count();i++)
        {
            User user = parseUser(nodeList.at(i).toElement());
            return user;
        }
    }
}
QList<Status*> ParseXml::parseFavourites(const QString &data)
{
    QList<Status*> statusList;
    QDomDocument doc;
    doc.setContent(data);
    if(!doc.isNull())
    {
        QDomNodeList nodeList = doc.elementsByTagName("status");
        for(int i = 0;i != nodeList.count();i++)
        {
            Status *status = parseStatus(nodeList.at(i).toElement());
            statusList.append(status);
        }
    }
    return statusList;
}
Status* ParseXml::parseFavouritesCreate(const QString &data)
{
    Status *status = new Status;
    QDomDocument doc;
    doc.setContent(data);
    if(!doc.isNull())
    {
        QDomNodeList nodeList = doc.elementsByTagName("status");
        for(int i = 0;i != nodeList.count();i++)
        {
            status = parseStatus(nodeList.at(i).toElement());

        }
    }
    return status;
}
Status* ParseXml::parseFavouritesDestroy(const QString &data)
{
    Status *status = new Status;
    QDomDocument doc;
    doc.setContent(data);
    if(!doc.isNull())
    {
        QDomNodeList nodeList = doc.elementsByTagName("status");
        for(int i = 0;i != nodeList.count();i++)
        {
            status = parseStatus(nodeList.at(i).toElement());

        }
    }
    return status;
}
QList<Status*> ParseXml::parseFavouritesDestroyBatch(const QString &data)
{
    QList<Status*> statusList;
    QDomDocument doc;
    doc.setContent(data);
    if(!doc.isNull())
    {
        QDomNodeList nodeList = doc.elementsByTagName("status");
        for(int i = 0;i != nodeList.count();i++)
        {
            Status *status = parseStatus(nodeList.at(i).toElement());
            statusList.append(status);
        }
    }
    return statusList;
}
QList<Suggestion> ParseXml::parseAtUsers(const QString &data)
{
    QList<Suggestion> suggestionList;
    QDomDocument doc;
    doc.setContent(data);
    if(!doc.isNull())
    {
        QDomNodeList nodeList = doc.elementsByTagName("suggestion");
        for(int i = 0;i != nodeList.count();i++)
        {
            Suggestion suggestion = parseSuggestion(nodeList.at(i).toElement());
            suggestionList.append(suggestion);
        }
    }
    return suggestionList;
}


