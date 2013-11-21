#ifndef CONSTDATA_H
#define CONSTDATA_H

//¸ÄµÄºÃÀÛ!
enum SinaKey{
    eVERIFY_CREDENTIALS = 2000,
    eFRIENDS_TIMELINE,
    eUSER_TIMELINE,
    eMENTIONS,
    eCOMMENTS_TIMELINE,
    eCOMMENTS_BY_ME,
    eCOMMENTS_TO_ME,
    eCOMMENTS,
    eCOUNTS,
    eREPOST_TIMELINE,
    eREPOST_BY_ME,
    eUNREAD,
    eRESET_COUNT,
    eEMOTIONS,
    eSHOW_ID,
    eUSER_STATUSES_ID,
    eUPDATE,
    eUPLOAD,
    eDESTROY,
    eREPOST,
    eCOMMENT,
    eCOMMENT_DESTROY,
    eCOMMENT_DESTROY_BATCH,
    eREPLY,
    eUSERS_SHOW,
    eFRIENDS,
    eFOLLOWERS,
    eUPDATE_REMARK,
    eSUGGESTIONS,
    eUSERS_HOT,
    eDIRECT_MESSAGES,
    eSENT,
    eNEW,
    eDESTROY_ID,
    eDIRECT_MESSAGES_DESTROY_BATCH,
    eFRIENDSHIPS_CREATE,
    eFRIENDSHIPS_DESTROY,
    eFRIENDSHIPS_EXISTS,
    eFRIENDSHIPS_SHOW,
    eFRIENDS_IDS,
    eFOLLOWERS_IDS,
    eTRENDS,
    eTRENDS_DAILY,
    eTRENDS_DESTROY,
    eTRENDS_FOLLOW,
    eTRENDS_HOURLY,
    eTRENDS_STATUSES,
    eTRENDS_WEEKLY,
    eUPDATE_PRIVACY,
    eGET_PRIVACY,
    eBLOCKS_CREATE,
    eBLOCKS_DESTROY,
    eBLOCKS_EXISTS,
    eBLOCKS_BLOCKING,
    eBLOCKS_BLOCKING_IDS,
    eTAGS,
    eTAGS_CREATE ,
    eTAGS_DESTROY,
    eTAGS_DESTROY_BATCH,
    eTAGS_SUGGESTIONS,
    eRATE_LIMIT_STATUS,
    eUPDATE_PROFILE,
    eFAVOURITES ,
    eFAVOURITES_CREATE,
    eFAVOURITES_DESTROY,
    eFAVOURITES_DESTROY_BATCH,
    eSUGGESTIONS_AT_USERS,
    eEND_SESSION,
    eUPDATE_PROFILE_IMAGE,
};


const QString DOMAIN_NAME = "http://api.t.sina.com.cn/";
const QString REQUEST_TOKEN = DOMAIN_NAME + "oauth/request_token";
const QString AUTHORIZE = DOMAIN_NAME + "oauth/authorize";
const QString ACCESS_TOKEN = DOMAIN_NAME + "oauth/access_token";

const QString USER_TIMELINE = DOMAIN_NAME + "statuses/user_timeline.xml";
const QString VERIFY_CREDENTIALS = DOMAIN_NAME + "account/verify_credentials.xml";
const QString FRIENDS_TIMELINE = DOMAIN_NAME+"statuses/friends_timeline.xml";
const QString MENTIONS = DOMAIN_NAME + "statuses/mentions.xml";
const QString COMMENTS_TIMELINE = DOMAIN_NAME + "statuses/comments_timeline.xml";
const QString COMMENTS_BY_ME = DOMAIN_NAME + "statuses/comments_by_me.xml";
const QString COMMENTS_TO_ME = DOMAIN_NAME + "statuses/comments_to_me.xml";
const QString COMMENTS = DOMAIN_NAME + "statuses/comments.xml";
const QString COUNTS = DOMAIN_NAME + "statuses/counts.xml";
const QString REPOST_TIMELINE = DOMAIN_NAME + "statuses/repost_timeline.xml";
const QString REPOST_BY_ME = DOMAIN_NAME + "statuses/repost_by_me.xml";
const QString UNREAD = DOMAIN_NAME + "statuses/unread.xml";
const QString RESET_COUNT = DOMAIN_NAME + "statuses/reset_count.xml";
const QString EMOTIONS = DOMAIN_NAME +"emotions.xml";
const QString SHOW_ID = DOMAIN_NAME + "statuses/show/: id.xml";
const QString USER_STATUSES_ID = DOMAIN_NAME + ":userid/statuses/:id.xml";
const QString UPDATE = DOMAIN_NAME + "statuses/update.xml";
const QString UPLOAD = DOMAIN_NAME + "statuses/upload.xml";
const QString DESTROY = DOMAIN_NAME + "statuses/destroy/:id.xml";
const QString REPOST = DOMAIN_NAME + "statuses/repost.xml";
const QString COMMENT = DOMAIN_NAME + "statuses/comment.xml";
const QString COMMENT_DESTROY = DOMAIN_NAME + "statuses/comment_destroy/:id.xml";
const QString COMMENT_DESTROY_BATCH = DOMAIN_NAME + "statuses/comment/destroy_batch.xml";
const QString REPLY = DOMAIN_NAME + "statuses/reply.xml";
const QString USERS_SHOW = DOMAIN_NAME + "users/show.xml";
const QString FRIENDS = DOMAIN_NAME + "statuses/friends.xml";
const QString FOLLOWERS = DOMAIN_NAME + "statuses/followers.xml";
const QString UPDATE_REMARK = DOMAIN_NAME + "user/friends/update_remark.xml";
const QString SUGGESTIONS = DOMAIN_NAME + "users/suggestions.xml";
const QString USERS_HOT = DOMAIN_NAME + "users/hot.xml";
const QString DIRECT_MESSAGES = DOMAIN_NAME + "direct_messages.xml";
const QString SENT = DOMAIN_NAME + "direct_messages/sent.xml";
const QString NEW = DOMAIN_NAME + "direct_messages/new.xml";
const QString DESTROY_ID = DOMAIN_NAME + "direct_messages/destroy/:id.xml";
const QString DIRECT_MESSAGES_DESTROY_BATCH = DOMAIN_NAME + "direct_messages/destroy_batch.xml";
const QString FRIENDSHIPS_CREATE = DOMAIN_NAME + "friendships/create.xml";
const QString FRIENDSHIPS_DESTROY = DOMAIN_NAME + "friendships/destroy.xml";
const QString FRIENDSHIPS_EXISTS = DOMAIN_NAME + "friendships/exists.xml";
const QString FRIENDSHIPS_SHOW = DOMAIN_NAME + "friendships/show.xml";
const QString FRIENDS_IDS = DOMAIN_NAME + "friends/ids.xml";
const QString FOLLOWERS_IDS = DOMAIN_NAME + "followers/ids.xml";
const QString TRENDS = DOMAIN_NAME + "trends.xml";
const QString TRENDS_STATUSES = DOMAIN_NAME + "trends/statuses.xml";
const QString TRENDS_FOLLOW = DOMAIN_NAME + "trends/follow.xml";
const QString TRENDS_DESTROY = DOMAIN_NAME + "trends/destroy.xml";
const QString TRENDS_HOURLY = DOMAIN_NAME + "trends/hourly.xml";
const QString TRENDS_DAILY = DOMAIN_NAME + "trends/daily.xml";
const QString TRENDS_WEEKLY = DOMAIN_NAME + "trends/weekly.xml";
const QString UPDATE_PRIVACY = DOMAIN_NAME + "account/update_privacy.xml";
const QString GET_PRIVACY = DOMAIN_NAME + "account/get_privacy.xml";
const QString BLOCKS_CREATE = DOMAIN_NAME + "blocks/create.xml";
const QString BLOCKS_DESTROY = DOMAIN_NAME + "blocks/destroy.xml";
const QString BLOCKS_EXISTS = DOMAIN_NAME + "blocks/exists.xml";
const QString BLOCKS_BLOCKING = DOMAIN_NAME + "blocks/blocking.xml";
const QString BLOCKS_BLOCKING_IDS = DOMAIN_NAME + "blocks/blocking.xml";
const QString TAGS = DOMAIN_NAME + "tags.xml";
const QString  TAGS_CREATE = DOMAIN_NAME + "tags/create.xml";
const QString TAGS_DESTROY = DOMAIN_NAME + "tags/destroy.xml";
const QString TAGS_SUGGESTIONS = DOMAIN_NAME + "tags/suggestions.xml";
const QString TAGS_DESTROY_BATCH = DOMAIN_NAME + "tags/destroy_batch.xml";
const QString RATE_LIMIT_STATUS = DOMAIN_NAME + "account/rate_limit_status.xml";
const QString END_SESSION = DOMAIN_NAME + "account/end_session.xml";
const QString UPDATE_PROFILE_IMAGE = DOMAIN_NAME + "account/update_profile_image.xml";
const QString UPDATE_PROFILE = DOMAIN_NAME + "account/update_profile.xml";
const QString FAVOURITES = DOMAIN_NAME + "favourites.xml";
const QString FAVOURITES_CREATE = DOMAIN_NAME + "favourites/create.xml";
const QString FAVOURITES_DESTROY = DOMAIN_NAME + "favourites/destroy/:id.xml";
const QString FAVOURITES_DESTROY_BATCH = DOMAIN_NAME + "favourites/destroy_batch.xml";
const QString SUGGESTIONS_AT_USERS = DOMAIN_NAME + "search/suggestions/at_users.xml";
#endif // CONSTDATA_H
