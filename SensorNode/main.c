#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#include "shell.h"
#include "msg.h"
#include "net/emcute.h"
#include "net/ipv6/addr.h"

#include "saul.h"
#include "saul_reg.h"
#include "xtimer.h"

#ifndef EMCUTE_ID
#define EMCUTE_ID           ("gertrud")
#endif
#define EMCUTE_PRIO         (THREAD_PRIORITY_MAIN - 1)

#define NUMOFSUBS           (16U)
#define TOPIC_MAXLEN        (64U)
mutex_t mutex;
static char stack[THREAD_STACKSIZE_DEFAULT];
static msg_t queue[8];
static emcute_sub_t subscriptions[NUMOFSUBS];
static char topics[NUMOFSUBS][TOPIC_MAXLEN];
static void *emcute_thread(void *arg);

char * dest_addr = "2600:1f18:61c5:5b01:9598:2ed:a6a8:fc4f";
int dest_port = 1885;

char * topic_pub_temp = "mytopic/temp1";	// Send temperature on this topic
char * topic_request = "mytopic/request1";	// Receive requests on this topic
emcute_topic_t topic_pub;

int connected = 0;

// Function prototypes
static int subscribe_for_requests(void);
char *read_temp(void);
static int publish_temp(emcute_topic_t *topic);
static int subscribe_for_requests(void);


static void *emcute_thread(void *arg)
{
    (void)arg;
    emcute_run(CONFIG_EMCUTE_DEFAULT_PORT, EMCUTE_ID);
    return NULL;    /* should never be reached */
}

// Read the temperature using SAUL
char *read_temp(void)
{
	saul_reg_t *dev = saul_reg_find_nth(8); // find the temperature sensor
	phydat_t result;
	saul_reg_read(dev, &result);
	
	char *str = malloc(sizeof(char) * 20);
	sprintf(str, "%d,%d", result.val[0], result.scale);	// Store the value and scale as string
	
	return str;
}

// Connect to a MQTTSN Broker
static int connect_to_broker(void)
{
	sock_udp_ep_t gw = { .family = AF_INET6, .port = CONFIG_EMCUTE_DEFAULT_PORT };

    // Set ipv6 and port
    ipv6_addr_from_str((ipv6_addr_t *)&gw.addr.ipv6, dest_addr);
    gw.port = dest_port;
    
    // Connect to broker
    int conn = emcute_con(&gw, true, NULL, NULL, 0, 0);
    if ( conn == EMCUTE_OK || conn == EMCUTE_NOGW) {
    	connected = 1;
    	printf("Successfully connected to gateway\n");
    	return 0;
    }
    else{
    	printf("Error: Could not connect. Make sure that the broker is running and restart the program \n");
        connected = 0;
        return 1;
    }
}

// Publish the temperature
static int publish_temp(emcute_topic_t *topic){

	mutex_lock(&mutex);	// Synchronize the function
    unsigned flags = EMCUTE_QOS_0;
    char * temp = read_temp();
    
    int status = emcute_pub(topic, temp, strlen(temp), flags);
    if(status == EMCUTE_OK){
    	printf("Temperature pubished\n");
		mutex_unlock(&mutex);
		return 0;
    }
    else{
    	printf("Error while publishing ocured\n");
    	mutex_unlock(&mutex);
    	return 1;
    }
}

// Process requests
static void on_pub(const emcute_topic_t *topic, void *data, size_t len){

	(void) len;
	(void) topic;
	
	char *in = (char *)data;
	char *req = "get_temp_now";
	
	// Process request: Publish temp. imediatly
	if( strcmp(topic->name, topic_request) == 0 ){
		if( strcmp(in, req) == 0){
			printf("Sending requested data\n");
			publish_temp(&topic_pub);
		}
	}
}


// Subscribe for requests topic
static int subscribe_for_requests(void){
	
	unsigned flags = EMCUTE_QOS_0;
	
	/* find empty subscription slot */
   	unsigned i = 0;
    	for (; (i < NUMOFSUBS) && (subscriptions[i].topic.id != 0); i++) {}
    	if (i == NUMOFSUBS) {
        	puts("error: no memory to store new subscriptions");
        	return 1;
    	}

    subscriptions[i].cb = on_pub;
    strcpy(topics[i], topic_request);
    subscriptions[i].topic.name = topics[i];

	if (emcute_sub(&subscriptions[i], flags) != EMCUTE_OK) {
        printf("error: unable to subscribe\n");
        return 1;
    }

    printf("Now subscribed\n");
    return 0;
}


int main(void)
{

    /* the main thread needs a msg queue to be able to run `ping6`*/
    msg_init_queue(queue, ARRAY_SIZE(queue));

    /* initialize our subscription buffers */
    memset(subscriptions, 0, (NUMOFSUBS * sizeof(emcute_sub_t)));
	mutex_init(&mutex);
    /* start the emcute thread */
    thread_create(stack, sizeof(stack), EMCUTE_PRIO, 0, emcute_thread, NULL, "emcute");
    
    printf("Sensor node is running\n");
    printf("Connecting to broker...\n");
    connect_to_broker();	// Connect to the broker
    subscribe_for_requests(); 	// Subscribe to get requests
    topic_pub.name = topic_pub_temp;	// Obtain topic id for publishing
    if (emcute_reg(&topic_pub) != EMCUTE_OK) {
    	printf("Error: Unable to obtain topic ID for publishing\n");
        return 1;
    }
    // Endless publishing loop
    while(1){
    	publish_temp(&topic_pub);
    	xtimer_sleep(60);
    }
                  
    return 0;
}

