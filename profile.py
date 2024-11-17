import geni.portal as portal
import geni.rspec.pg as pg
import geni.rspec.igext as igext
pc = portal.Context()
rspec = pg.Request()
#node0 = pg.RawPC("node-0")

pc.defineParameter("node_type", "Hardware spec of nodes to use. <br> Refer <a href=\"http://docs.aptlab.net/hardware.html#%28part._apt-cluster%29\">manual</a> for more details.",
 portal.ParameterType.NODETYPE, "r320", legalValues=["r320", "c6220", "c6320", "xl170"], advanced=False, groupId=None)
pc.defineParameter("num_nodes", "Number of nodes to use.<br> Check cluster availability <a href=\"https://www.cloudlab.us/cluster-graphs.php\">here</a>.",
 portal.ParameterType.INTEGER, 5, legalValues=[], advanced=False, groupId=None)

nodes = []
interfaces = []
params = pc.bindParameters()
if params.num_nodes < 1:
    pc.reportError(portal.ParameterError("You must choose a minimum of 1 node "))
pc.verifyParameters()
link = pg.LAN("link-0")
#nodes.append(pg.RawPC("master"))
#nodes[0].hardware_type = params.node_type
#nodes[0].disk_image="urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU18-64-STD"
#nodes[0].Site("27")
#bs = nodes[0].Blockstore("bs", "/opt")
#bs.size = "50GB"

for i in range(params.num_nodes):
    nodes.append(pg.RawPC("node-%s" % (i+1)))
    nodes[i].hardware_type = params.node_type
    # nodes[i].disk_image="urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU18-64-STD"
    nodes[i].disk_image="urn:publicid:IDN+apt.emulab.net+image+rperf-PG0:rdma-cluster.node-1"
    nodes[i].Site("27")
    nodes[i].addService(pg.Execute(shell="sh", command="/local/repository/dramhit-top.sh"))
    
    interfaces.append(nodes[i].addInterface("interface-%s" % i))
    ip = "10.0.2." + str(i+1)
    interfaces[i].addAddress(pg.IPv4Address(ip, "255.255.255.0"))
    link.addInterface(interfaces[i])
    rspec.addResource(nodes[i])

rspec.addResource(link)

instructions = "\n* login to node-1. \n* switch user to root. `sudo  -i`. \n* Infiniband is configured in the private interface(10.*) "
desc = "An infiniband configured cluster of nodes."
tour = igext.Tour()
tour.Description(type=igext.Tour.TEXT, desc=desc)
tour.Instructions(type=igext.Tour.MARKDOWN, inst=instructions)
rspec.addTour(tour)
pc.printRequestRSpec(rspec)
