#include <stdio.h>
#include <string.h>
#include <errno.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <unistd.h>
#include <asm/types.h>
#include <linux/netlink.h>
#include <linux/rtnetlink.h>
#include <linux/netdevice.h>
#include <net/if_arp.h>
#include <netinet/if_ether.h>
#include <netinet/ether.h>

int main()
{
    int nSocket, nLen, nAttrLen;
    char szBuffer[4096];
    struct {
        struct nlmsghdr nh;
        struct ifinfomsg ifi;
    }struReq;
    struct sockaddr_nl struAddr;
    struct nlmsghdr *pstruNL;
    struct ifinfomsg *pstruIF;
    struct rtattr *pstruAttr;
    struct net_device_stats *pstruInfo;
    struct ether_addr *pstruEther;

    /*
     * 创建一个PF_NETLINK的SOCKET,使用NETLINK_ROUTE协议
     */
    nSocket = socket(PF_NETLINK, SOCK_DGRAM, NETLINK_ROUTE);
    if(nSocket < 0)
    {
        fprintf(stderr, "创建SOCKET错误:%s\n", strerror(errno));
        return -1;
    }

    /*
     * 绑定地址
     */
    memset(&struAddr, 0, sizeof(struAddr));
    struAddr.nl_family = AF_NETLINK;
    struAddr.nl_pid = getpid();
    struAddr.nl_groups = 0;
    if(bind(nSocket, (struct sockaddr *)&struAddr, sizeof(struAddr)) < 0)
    {
        fprintf(stderr, "绑定SOCKET错误:%s\n", strerror(errno));
        return -1;
    }

    /*
     * 发送一个请求
     */
    memset(&struReq, 0, sizeof(struReq));
    struReq.nh.nlmsg_len = NLMSG_LENGTH(sizeof(struReq));
    struReq.nh.nlmsg_type = RTM_GETLINK;
    struReq.nh.nlmsg_flags = NLM_F_REQUEST | NLM_F_DUMP;
    struReq.ifi.ifi_family = AF_UNSPEC;
    memset(&struAddr, 0, sizeof(struAddr));
    struAddr.nl_family = AF_NETLINK;
    struAddr.nl_pid = 0;
    struAddr.nl_groups = 0;
    if(sendto(nSocket, &struReq, struReq.nh.nlmsg_len, 0,
        (struct sockaddr *)&struAddr, sizeof(struAddr)) < 0)
    {
        fprintf(stderr, "发送数据错误:%s\n", strerror(errno));
        return -1;
    }

    /*
     * 循环接收数据，直到超时
     */
    alarm(30);
    memset(szBuffer, 0, sizeof(szBuffer));
    while((nLen = recv(nSocket, szBuffer, sizeof(szBuffer), 0)))
    {
        alarm(0);
        pstruNL = (struct nlmsghdr *)szBuffer;
        /*
         * 判断是否继续有数据
         */
        while(NLMSG_OK(pstruNL, nLen))
        {
            /*
             * 数据已经获取完成
             */
            if(pstruNL -> nlmsg_type == NLMSG_DONE)
                break;
            if(pstruNL -> nlmsg_type == NLMSG_ERROR)
            {
                /*
                 * 发生一个错误
                 */
                struct nlmsgerr *pstruError;

                pstruError = (struct nlmsgerr *)NLMSG_DATA(pstruNL);
                fprintf(stderr, "发生错误[%s]\n",
                    strerror(-pstruError -> error));
                break;
            }

            /*
             * 下面通过宏获取数据
             */
            pstruIF = NLMSG_DATA(pstruNL);
            fprintf(stderr, "获取到设备[%d]信息\n", pstruIF -> ifi_index);
            fprintf(stderr, "\t设备类型:");
            switch(pstruIF -> ifi_type)
            {
                case ARPHRD_ETHER:
                    fprintf(stderr, "以太网\n");
                    break;
                case ARPHRD_PPP:
                    fprintf(stderr, "PPP拨号\n");
                    break;
                case ARPHRD_LOOPBACK:
                    fprintf(stderr, "环路设备\n");
                    break;
                default:
                    fprintf(stderr, "未知\n");
                    break;
            }
            fprintf(stderr, "\t设备状态:");
            if((pstruIF -> ifi_flags & IFF_UP )== IFF_UP)
                fprintf(stderr, " UP");
            if((pstruIF -> ifi_flags & IFF_BROADCAST) == IFF_BROADCAST)
                fprintf(stderr, " BROADCAST");
            if((pstruIF -> ifi_flags & IFF_DEBUG) == IFF_DEBUG)
                fprintf(stderr, " DEBUG");
            if((pstruIF -> ifi_flags & IFF_LOOPBACK) == IFF_LOOPBACK)
                fprintf(stderr, " LOOPBACK");
            if((pstruIF -> ifi_flags & IFF_POINTOPOINT) == IFF_POINTOPOINT)
                fprintf(stderr, " POINTOPOINT");
            if((pstruIF -> ifi_flags & IFF_RUNNING) == IFF_RUNNING)
                fprintf(stderr, " RUNNING");
            if((pstruIF -> ifi_flags & IFF_NOARP) == IFF_NOARP)
                fprintf(stderr, " NOARP");
            if((pstruIF -> ifi_flags & IFF_PROMISC) == IFF_PROMISC)
                fprintf(stderr, " PROMISC");
            if((pstruIF -> ifi_flags & IFF_NOTRAILERS) == IFF_NOTRAILERS)
                fprintf(stderr, " NOTRAILERS");
            if((pstruIF -> ifi_flags & IFF_ALLMULTI) == IFF_ALLMULTI)
                fprintf(stderr, " ALLMULTI");
            if((pstruIF -> ifi_flags & IFF_MASTER) == IFF_MASTER)
                fprintf(stderr, " MASTER");
            if((pstruIF -> ifi_flags & IFF_SLAVE) == IFF_SLAVE)
                fprintf(stderr, " SLAVE");
            if((pstruIF -> ifi_flags & IFF_MULTICAST) == IFF_MULTICAST)
                fprintf(stderr, " MULTICAST");
            if((pstruIF -> ifi_flags & IFF_PORTSEL) == IFF_PORTSEL)
                fprintf(stderr, " SLAVE");
            if((pstruIF -> ifi_flags & IFF_AUTOMEDIA) == IFF_AUTOMEDIA)
                fprintf(stderr, " AUTOMEDIA");
            if((pstruIF -> ifi_flags & IFF_DYNAMIC) == IFF_DYNAMIC)
                fprintf(stderr, " DYNAMIC");
            fprintf(stderr, "\n");

            /*
             * 下面通过宏获取属性
             */
            pstruAttr = IFLA_RTA(pstruIF);
            nAttrLen = NLMSG_PAYLOAD(pstruNL, sizeof(struct ifinfomsg));
            while(RTA_OK(pstruAttr, nAttrLen))
            {
                switch(pstruAttr->rta_type)
                {
                    case IFLA_IFNAME:
                        fprintf(stderr, "\t设备名称:%s\n",
                            (char *)RTA_DATA(pstruAttr));
                        break;
                    case IFLA_MTU:
                        fprintf(stderr, "\t设备MTU:%d\n",
                            *(unsigned int *)RTA_DATA(pstruAttr));
                        break;
                    case IFLA_QDISC:
                        fprintf(stderr, "\t设备队列:%s\n",
                            (char *)RTA_DATA(pstruAttr));
                        break;
                    case IFLA_ADDRESS:
                        if(pstruIF -> ifi_type == ARPHRD_ETHER)
                        {
                            pstruEther = (struct ether_addr *)
                                RTA_DATA(pstruAttr);
                            fprintf(stderr, "\tMAC地址:%s\n",
                                ether_ntoa(pstruEther));
                        }
                        break;
                    case IFLA_BROADCAST:
                        if(pstruIF -> ifi_type == ARPHRD_ETHER)
                        {
                            pstruEther = (struct ether_addr *)
                                RTA_DATA(pstruAttr);
                            fprintf(stderr, "\t广播MAC地址:%s\n",
                                ether_ntoa(pstruEther));
                        }
                        break;
                    case IFLA_STATS:
                        pstruInfo = (struct net_device_stats *) RTA_DATA(pstruAttr);
                        fprintf(stderr, "\t接收信息:\n");
/*
                        fprintf(stderr, "\t\t接收报文:%lu 字节:%lu\n",pstruInfo->rx_packets,pstruInfo->rx_bytes);
                        fprintf(stderr, "\t\terrors:%lu dropped:%lu "
                                "multicast:%lu collisions:%lu\n",
                            pstruInfo -> rx_errors, pstruInfo -> rx_droppesd,
                            pstruInfo -> multicast, pstruInfo -> collisions);
                        fprintf(stderr, "\t\tlength:%lu over:%lu crc:%lu "
                                "frame:%lu fifo:%lu missed:%lu\n",
                            pstruInfo -> rx_length_errors,
                            pstruInfo -> rx_over_errors,
                            pstruInfo -> rx_crc_errors,
                            pstruInfo -> rx_frame_errors,
                            pstruInfo -> rx_fifo_errors,
                            pstruInfo -> rx_missed_errors);
                        fprintf(stderr, "\t发送信息:\n");
                        fprintf(stderr, "\t\t发送报文:%lu 字节:%lu\n",
                            pstruInfo -> tx_packets, pstruInfo -> tx_bytes);
                        fprintf(stderr, "\t\terrors:%lu dropped:%lu\n",
                            pstruInfo -> tx_errors, pstruInfo -> tx_dropped);
                        fprintf(stderr, "\t\taborted:%lu carrier:%lu fifo:%lu"
                                " heartbeat:%lu window:%lu\n",
                            pstruInfo -> tx_aborted_errors,
                            pstruInfo -> tx_carrier_errors,
                            pstruInfo -> tx_fifo_errors,
                            pstruInfo -> tx_heartbeat_errors,
                            pstruInfo -> tx_window_errors);
*/
                        break;
                    default:
                        break;

                }
                /*
                 * 继续下一个属性
                 */
                pstruAttr = RTA_NEXT(pstruAttr, nAttrLen);
            }
            /*
             * 继续下一个数据
             */
            pstruNL = NLMSG_NEXT(pstruNL, nLen);
        }
        memset(szBuffer, 0, sizeof(szBuffer));
        alarm(30);
    }
    return 0;
}
