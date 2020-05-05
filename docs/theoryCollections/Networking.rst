NETWORKING FUNDAMENTAL - DEFINITIONS AND THEORIES
=================================================

I. BANDWIDTH
------------

1. Definition:

Network bandwidth is the capacity of a wired or wireless network communications link to transmit the maximum amount of
data from one point to another over a computer network or internet connection in a given amount of time -- usually,
one second. Synonymous with capacity, bandwidth describes the data transfer rate. Bandwidth is not a measure of network
speed -- a common misconception.

2. How bandwidth works?

The more bandwidth a data connection has, the more data it can send and receive at one time. Bandwidth can be compared
to the amount of water that can flow through a water pipe. The bigger the pipe, the more water can flow through it at
one time.

Bandwidth works on the same principle. So, the higher the capacity of the communication link, or pipe, the more data can
flow through it per second.

End users pay for the capacity of their network connections. Therefore, the greater the capacity of the link, the more
expensive it is.

3. Bandwidth vs. speed:

The terms bandwidth and speed are often used interchangeably – but not correctly. The cause of the confusion may be due,
in part, to their use in advertisements by internet service providers (ISPs) that refer to greater speeds when they
actually mean bandwidth. Essentially, speed refers to the rate at which data can be sent, while the definition of
bandwidth is the capacity for that speed. To use the common water metaphor, speed refers to how quickly water is flowing
through a pipe; bandwidth refers to the diameter of the pipe. In order to avoid confusion, it makes more sense to use
the terms bandwidth (or bandwidth capacity) and network speed, rather than bandwidth speed.

4. Why bandwidth is important:

In any given deployment location, such as a house or business, there are bandwidth limits. That is, there is only so
much space in the pipe for the data to flow. Because of this reason, multiple devices in a single location must share
the bandwidth. Some devices, such as a television, are bandwidth hogs, while tablets typically use far less in comparison.
Although speed and bandwidth are not interchangeable, greater bandwidth is essential if tolerable speed is to be
maintained on multiple devices.

5. How to measure bandwidth:

While bandwidth is traditionally expressed in bits per second (bps), modern network links have greater capacity, which
is typically measured in millions of bits per second (megabits per second, or Mbps) or billions of bits per second
(gigabits per second, or Gbps).

Bandwidth connections can be symmetrical, which means the data capacity is the same in both directions to upload or
download data, or asymmetrical, which means download and upload capacity are not equal. In asymmetrical connections,
upload capacity is typically smaller than download capacity.

6. Considerations for calculating bandwidth:

Technology advances have made some bandwidth calculations more complex, and they can depend on the type of network link
being used. For example, optical fiber using different types of light waves and time-division multiplexing can transmit
more data through a connection at one time, which effectively increases its bandwidth. In wireless networks, bandwidth
is defined as the spectrum of frequencies that operators license from the Federal Communications Commission (FCC) and
the National Telecommunications and Information Administration (NTIA) for use in mobile services in the U.S.

Effective bandwidth, which is the highest reliable transmission rate a link can provide, can be measured using a
bandwidth test in which the link's capacity is determined by repeatedly measuring the time required for a specific
file to leave its point of origin and successfully download at its destination.

In addition to testing, organizations need to calculate how much bandwidth they need to run all the applications on
their networks. To find out how much capacity they need, organizations must calculate the maximum number of users who
might be using the network connection at one time and then multiply that number times the bandwidth capacity required
by each application.

To calculate needed bandwidth for the cloud, it's important to know the capacity needed to send and receive traffic
from public clouds. Capacity can be affected by any congestion on the connections used to reach public cloud providers,
particularly if that data is traveling over the internet.

When looking into how much bandwidth a specific application will need, there are two basic steps to calculating
bandwidth requirements:

    1. Determine the amount of available network bandwidth, expressed in bytes per second (Bps).
    2. Determine the average utilization required by the specific application, expressed in bytes per second.

After determining the network's bandwidth, it is necessary to see how much bandwidth each application is using.
Bandwidth testing can be used to detect the number of bytes per second the application sends across the network.

7. Factors affecting performance:
The maximum capacity of a network connection is only one factor that affects network performance. Packet loss, latency
and jitter can all degrade network throughput and make a high-capacity link perform like one with less available
bandwidth. An end-to-end network path usually consists of multiple network links, each with different bandwidth capacity.
As a result, the link with the lowest bandwidth is often described as the bottleneck because the lowest bandwidth
connection can limit the overall data capacity of all the connections in the path.

8. Bandwidth on demand:
The maximum available bandwidth for dedicated communication links is typically sold at a set price by the month. However,
bandwidth on demand -- also called dynamic bandwidth allocation, or burstable bandwidth -- is an option that enables
subscribers to increase the amount of available bandwidth at specific times or for specific purposes. Bandwidth on
demand is a technique that can provide additional capacity on a communications link to accommodate bursts in data
traffic that temporarily require more bandwidth.

Rather than overprovisioning the network with expensive dedicated links, bandwidth on demand provided by service
providers is frequently used in wide area networks (WANs) to increase capacity as needed for a particular event or at a
particular time of day. Using this technique, bandwidth on a shared telecommunications network can be increased, and
users pay for only the additional bandwidth they consume.

Bandwidth on demand is available through many service providers because the network links they provide to customers have
additional bandwidth available through them, but customers pay only for the capacity they need. For example, a 100 Mbps
link might be able to burst up to a gigabit because the service provider's connection has available capacity. If a user
needed more than the absolute maximum bandwidth available on that link, another physical connection would be required.

Occasionally, a service provider will enable customers to burst above their subscribed bandwidth cap without charging
additional bandwidth usage fees.

9. SD-WAN eases bandwidth needs:

Software-defined WAN (SD-WAN) technology provides customers with extra capacity because it makes bandwidth from multiple
connections, rather than one, available to users. These often include a Multiprotocol Label Switching (MPLS) connection
or other types of dedicated bandwidth link, plus a broadband internet link or cellular connection.

10. Bandwidth throttling:

ISPs or network administrators sometimes intentionally adjust the speed -- up or down -- of data traveling over the
network, a measure known as bandwidth throttling. There are different reasons for bandwidth throttling, including
limiting network congestion, particularly on public access networks. ISPs may use bandwidth throttling to reduce usage
of a particular user or class of users. For example, with tiered pricing, a service provider can offer a menu of upload
and download bandwidth. ISPs can also throttle bandwidth to even out usage across all users on the network.

The use of bandwidth throttling has been criticized by net neutrality advocates, who say that political or economic
motivations are behind the practice of bandwidth throttling and that they unfairly target segments of the population.

To see if an ISP is throttling bandwidth, a speed test can be run. Speed tests measure the speed between a device and a
test server, using a device's internet connection. ISPs offer speed tests from their internet sites, and independent
tests are also available from services such as Speedtest. Because many factors can affect the results of a speed test,
it is generally recommended to perform multiple tests at different times of the day and engage different servers
available through the speed test site.

Some people also suggest installing a virtual private network (VPN) if you're looking for more accurate results of your
speed test.

There are also network bandwidth monitoring tools available to help identify performance issues, such as a faulty router
or a virus-infected computer on the network. As noted above, bandwidth monitoring can also help network administrators
better plan for future network growth, seeing where in the network the bandwidth capacity is most needed. Monitoring
tools can also help administrators see if their ISP is living up to the service-level agreement (SLA) in their contract.

# Data transfer throttling
Data transfer throttling – the intentional restriction of the amount of digital data, particularly for the purposes of
preventing spam or bulk email transmission through a network server – can be considered another form of bandwidth
throttling. If it is implemented on a large enough scale, data transfer throttling can control the spread of computer
viruses, worms or other malware through the internet.

Reference
=========
What is bandwidth and how is it measured? (2019, December 5).
Retrieved from https://searchnetworking.techtarget.com/definition/bandwidth