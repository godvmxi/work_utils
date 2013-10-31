#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <fcntl.h>
#include <errno.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <linux/netlink.h>
#include <unistd.h>
#include <asm/types.h>
#include <linux/rtnetlink.h>
#include <linux/netdevice.h>
#include <net/if_arp.h>
#include <netinet/if_ether.h>
#include <netinet/ether.h>
#include <linux/netdevice.h>
//#include <net/if.h>
//#include <sys/ioctl.h>

#define UEVENT_BUFFER_SIZE 2048*2
struct net_device_stats {
    unsigned long   rx_packets;
    unsigned long   tx_packets;
    unsigned long   rx_bytes;
    unsigned long   tx_bytes;
    unsigned long   rx_errors;
    unsigned long   tx_errors;
    unsigned long   rx_dropped;
    unsigned long   tx_dropped;
    unsigned long   multicast;
    unsigned long   collisions;
    unsigned long   rx_length_errors;
    unsigned long   rx_over_errors;
    unsigned long   rx_crc_errors;
    unsigned long   rx_frame_errors;
    unsigned long   rx_fifo_errors;
    unsigned long   rx_missed_errors;
    unsigned long   tx_aborted_errors;
    unsigned long   tx_carrier_errors;
    unsigned long   tx_fifo_errors;
    unsigned long   tx_heartbeat_errors;
    unsigned long   tx_window_errors;
    unsigned long   rx_compressed;
    unsigned long   tx_compressed;
};
struct {
	struct nlmsghdr nh;
	struct ifinfomsg ifi;
}struReq;

int main(void)
{
	struct sockaddr_nl client;

    struct timeval tv;
    int ntSocket, rcvlen, ret;
    fd_set fds;
    int buffersize = 1024;
//    struct net_device_stats *pstruInfo;
//    struct sockaddr_nl struAddr;

    struct ether_addr *pstruEther;

	struct nlmsghdr *pstruNL;
	struct ifinfomsg *pstruIF;
	struct rtattr *pstruAttr;

	struct sockaddr_nl struAddr;


	//struct net_device_stats *pstruInfo;


    //network device
    //ntSocket = socket(AF_NETLINK, SOCK_RAW, NETLINK_ROUTE);
    //normal device
    ntSocket = socket(AF_NETLINK, SOCK_RAW, NETLINK_KOBJECT_UEVENT);
    //ntSocket = socket(AF_NETLINK, SOCK_RAW, NETLINK_CONNECTOR);
    if (ntSocket < 0){
    	printf("error\n");
    	exit(1);
    }
    else {
    	printf("socket id --> %d\n",ntSocket);
    }
    memset(&client, 0, sizeof(client));
    client.nl_family = AF_NETLINK;
    client.nl_pid = getpid();
    client.nl_groups = 0;
    //client.nl_groups = RTMGRP_IPV4_IFADDR | RTMGRP_LINK ; /* receive broadcast message*/
    setsockopt(ntSocket, SOL_SOCKET, SO_RCVBUF, &buffersize, sizeof(buffersize));
    bind(ntSocket, (struct sockaddr*)&client, sizeof(client));
    printf("begin monitor usb\n");

    /*
    * 发送一个请求
    */
//	memset(&struReq, 0, sizeof(struReq));
//	struReq.nh.nlmsg_len = NLMSG_LENGTH(sizeof(struReq));
//	struReq.nh.nlmsg_type = RTM_GETLINK;
//	struReq.nh.nlmsg_flags = NLM_F_REQUEST | NLM_F_DUMP;
//	struReq.ifi.ifi_family = AF_UNSPEC;
//	memset(&struAddr, 0, sizeof(struAddr));
//	struAddr.nl_family = AF_NETLINK;
//	struAddr.nl_pid = 0;
//	struAddr.nl_groups = 0;
//	if(sendto(ntSocket, &struReq, struReq.nh.nlmsg_len, 0,
//		(struct sockaddr *)&struAddr, sizeof(struAddr)) < 0)
//	{
//		fprintf(stderr, "发送数据错误:%s\n", strerror(errno));
//		return -1;
//	}


    while (1) 
	{
        char buf[UEVENT_BUFFER_SIZE] = { 0 };
        FD_ZERO(&fds);
        FD_SET(ntSocket, &fds);
        tv.tv_sec = 0;
        tv.tv_usec = 100 * 1000;
        ret = select(ntSocket + 1, &fds, NULL, NULL, &tv);
        if(!(ret > 0 && FD_ISSET(ntSocket, &fds)))
            continue;
        /* receive data */
        rcvlen = recv(ntSocket, &buf, sizeof(buf), 0);
//        if (rcvlen > 0) {
//        		printf("\n%d -> %s\n", rcvlen ,buf);
//        }
        printf("获取数据--> %d  --> %d\n",rcvlen,IFF_UP);
//       for(i = 0; i< rcvlen;i++)
//       {
//          	printf("%3X",buf[i]);
//       }
       // You can do something here to make the program more perfect!!!


//       pstruNL = (struct nlmsghdr *)buf;
//       fprintf(stderr, "nlmsghdr ->\n");
//       fprintf(stderr, "len\t\ttype\t\tindex\t\tflags\t\tchang\n");
//       fprintf(stderr, "%d\t\t%d\t\t%d\t\t%d\t\t%d\n",
//    		   pstruNL -> nlmsg_len, pstruNL -> nlmsg_type, pstruNL -> nlmsg_seq, pstruNL -> nlmsg_flags, pstruNL -> nlmsg_pid);
//
//
//	   /*
//		 判断是否继续有数据
//		*/
//		while(NLMSG_OK(pstruNL, rcvlen))
//		{
//			/*
//			* 数据已经获取完成
//			*/
//			if(pstruNL -> nlmsg_type == NLMSG_DONE)
//			{
//				printf("NLMSG_DONE\n");
//				break;
//			}
//			if(pstruNL -> nlmsg_type == NLMSG_ERROR)
//			{
//				/*
//				 * 发生一个错误
//				*/
//				struct nlmsgerr *pstruError;
//				pstruError = (struct nlmsgerr *)NLMSG_DATA(pstruNL);
//				fprintf(stderr, "发生错误[%s]\n",strerror(-pstruError -> error));
//				break;
//			}
//			/*
//			 * 下面通过宏获取数据
//			 */
//			struct ifinfomsg *pstruIF;
//			pstruIF = NLMSG_DATA(pstruNL);
//
//			fprintf(stderr, "ifinfomsg ->\n");
//			fprintf(stderr,"family\t\tpad\t\tindex\t\tflags\t\ttypes");
////			fprintf(stderr, "%s   %s  %d  %d  %d\n",pstruIF->ifi_family,pstruIF->__ifi_pad,pstruIF->ifi_index,pstruIF->ifi_flags,pstruIF->ifi_type);
//
//			fprintf(stderr, " %d  %d\n",pstruIF->ifi_flags,pstruIF->ifi_type);
//
//
//			//do some things
//			/*
//			 下面通过宏获取属性
//			 */
//			//struct rtattr *pstruAttr;
//			pstruAttr = IFLA_RTA(pstruIF);
//			int nAttrLen;
//			nAttrLen = NLMSG_PAYLOAD(pstruNL, sizeof(struct ifinfomsg));
//			//int msgid = 0;
//			printf("\n");
//			while(0)
//			//while(RTA_OK(pstruAttr, nAttrLen))
//			{
//				//printf("rta ok  ->  %d  type -> %d\n",msgid++,pstruAttr->rta_type);
//
//				switch(pstruAttr->rta_type)
//				{
//					case IFLA_UNSPEC://0
//						fprintf(stderr, "\tIFLA_UNSPEC:%s\n",
//							(char *)RTA_DATA(pstruAttr));
//						break;
//					case IFLA_LINK://0
//						fprintf(stderr, "\tIFLA_UNSPEC:%d\n",
//							(int )RTA_DATA(pstruAttr));
//						break;
//					case IFLA_IFNAME://0
//						fprintf(stderr, "\t设备名称:%s\n",
//							(char *)RTA_DATA(pstruAttr));
//						break;
//					case IFLA_MTU:
//						fprintf(stderr, "\t设备MTU:%d\n",
//							*(unsigned int *)RTA_DATA(pstruAttr));
//						break;
//					case IFLA_QDISC:
//						fprintf(stderr, "\t设备队列:%s\n",
//							(char *)RTA_DATA(pstruAttr));
//						break;
//					case IFLA_ADDRESS:
//						if(pstruIF -> ifi_type == ARPHRD_ETHER)
//						{
//							pstruEther = (struct ether_addr *)RTA_DATA(pstruAttr);
//							fprintf(stderr, "\tMAC地址:%s\n",ether_ntoa(pstruEther));
//
//						}
//						break;
//					case IFLA_BROADCAST:
//					if(pstruIF -> ifi_type == ARPHRD_ETHER)
//					{
//						pstruEther = (struct ether_addr *)
//							RTA_DATA(pstruAttr);
//						fprintf(stderr, "\t广播MAC地址:%s\n",
//							ether_ntoa(pstruEther));
//					}
//					break;
//					case IFLA_STATS://0
//						printf("IFLA_STATS\n");
//						struct net_device_stats *state = (struct net_device_stats *)RTA_DATA(pstruAttr);
//						fprintf(stderr, "\tIFLA_STATS:%s\n",(char *)RTA_DATA(pstruAttr));
//						fprintf(stderr, "\t rx_bytes:%ld\n",state->rx_bytes);
//						fprintf(stderr, "\t tx_bytes:%ld\n",state->tx_bytes);
//						break;
//
//
//					default :
//						break;
//				}
//
//
//				pstruAttr = RTA_NEXT(pstruAttr, nAttrLen);
//
//			}
//			break;
//
//		}

    }
    close(ntSocket);
    return 0;
}
