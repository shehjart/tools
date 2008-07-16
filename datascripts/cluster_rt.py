#!/usr/bin/python



from Numeric import *
from Pycluster import kcluster
from Pycluster import clustercentroids
import sys


class rt_telemetry_clusterer:

	#static init data
	timeblocks = None
	npasses = None
	nclusters = None
	#where to send the output
	output = None
	#merge at most these many data points
	merge_threshold = None
	
	
	#use arithmetic mean as clustering method
	method = "a"
	#user euclidean distance function
	dist = "e"
	#clustering transpose
	cluster_transpose = 1
	centroids_transpose = 1
	weights = None
	masks = None


	#dynamic state
	blockcount = 0
	timestamps = []
	restimes = []
	cluster_index = None
	centroids = None
	prev_cluster = None
	same_cluster_count = None
	merge_start_idx = None

	datapoints_count = 0
	mergecount = 0
	merged_datapoints = 0
	clustered_datapoints_count = 0

	def __init__(self, timeblocks, nclusters, npasses, mergethresh = 3,
			output = sys.stdout):
		self.timeblocks = timeblocks
		self.npasses = npasses
		self.nclusters = nclusters
		if mergethresh is None:
			self.merge_threshold = 3
		else:
			self.merge_threshold = mergethresh

		if output is None:
			self.output = sys.stdout
		else:
			self.output = output

		return

	def find_clusters(self):
		#print "Finding clusters.."
		#print "Response times: " + str(self.restimes)
		data_array = array([self.restimes])
		cluster_index, error, nfound = kcluster(data_array, 
				nclusters = self.nclusters, mask = self.masks,
				weight = self.weights, 
				transpose = self.cluster_transpose,
				npass =  self.npasses, method = self.method, 
				dist = self.dist)

		return cluster_index


	def find_cluster_centroids(self, cluster_index):
		#print "Finding cluster centroids.."
		data_arr = array([self.restimes])
		centroids, cmask = clustercentroids(data_arr, mask = self.masks,
				transpose = self.centroids_transpose, 
				clusterid = cluster_index, method = self.method)

		return centroids

	def merge_data_points(self):
		timestamp_total = float(0)
		self.mergecount = self.mergecount + 1
		for i in range(self.merge_start_idx, 
				self.merge_start_idx + self.same_cluster_count+1):
			#print "Merging " + str(i) + " " + str(self.restimes[i])
			timestamp_total = timestamp_total + self.timestamps[i]
			self.merged_datapoints = self.merged_datapoints + 1
	
		avg_timestamp = timestamp_total / float(self.same_cluster_count + 1)
		cluster_id = self.cluster_index[self.merge_start_idx]
		centroid = self.centroids[cluster_id]
		self.clustered_datapoints_count = self.clustered_datapoints_count + 1
		self.output.write(str(avg_timestamp) + "  " + str(centroid) + "\n")


	def init_new_merge(self, idx):
		self.prev_cluster = self.cluster_index[idx]
		self.merge_start_idx = idx
		self.same_cluster_count = 0
		#print "init_new_merge: prev_cluster: " + str(self.prev_cluster)
		#print "init_new_merge: merge_start_idx: " + str(self.merge_start_idx)
		#print "init_new_merge: same_cluster_count: " + str(self.same_cluster_count)
		return


	def test_and_merge(self, idx):

		if self.prev_cluster is None:
			#print "Initing new merge"
			self.init_new_merge(idx)
			return

		if self.prev_cluster == self.cluster_index[idx]:
			#print "Cluster same as previous one"
			self.same_cluster_count = self.same_cluster_count + 1
		else:
			#print "Cluster not same as previous one"
			if self.same_cluster_count < self.merge_threshold and self.same_cluster_count > 0:
				#print "Merging when threshold not reached"
				self.merge_data_points()
			else:
				#create data point here for previous one
				timestamp = self.timestamps[idx]
				restime = self.restimes[idx]
				self.clustered_datapoints_count = self.clustered_datapoints_count + 1
				self.output.write(str(timestamp) + " " + str(restime) + "\n")

			self.init_new_merge(idx)
			return

		if self.same_cluster_count == (self.merge_threshold - 1):
			#print "Merge threshold reached"
			self.merge_data_points()
			self.prev_cluster = None


	def merge_clustered_telemetry(self):
		#print "Merging clustered telemetry"
		for idx in range(0, len(self.cluster_index)):
			#print "Testing merge: idx " + str(idx) + " cluster: " + str(self.cluster_index[idx])
			self.test_and_merge(idx)

		return None


	def render_clustered_telemetry(self, tm):
		pass

	def build_clustered_telemetry(self):
		#print "Building clustered telemetry: block_count: " +str(self.blockcount)
		self.cluster_index = self.find_clusters()
		#print "cluster_index: " + str(self.cluster_index.tolist())
		self.centroids = self.find_cluster_centroids(self.cluster_index)[0]
		#print "centroids: " + str(self.centroids.tolist())
		clustered_tm = self.merge_clustered_telemetry()
		self.restimes = []
		self.timestamps = []
		self.blockcount = 0
		self.cluster_index = None
		self.centroids = None
		self.prev_cluster = None
		self.same_cluster_count = None
		self.merge_start_idx = None

		#print "Done merging."
		return clustered_tm

	def cluster_telemetry(self, timestamp, restime):
		#print "Clustering telemetry"
		#print "Appending to data points: block_count: " + str(self.blockcount)
		self.timestamps.append(timestamp)
		self.restimes.append(restime)
		self.blockcount = self.blockcount + 1
		self.datapoints_count = self.datapoints_count + 1	
		if self.blockcount == (self.timeblocks):
			#print "Have enough data points: block_count: " + str(self.blockcount)
			clustered_tm = self.build_clustered_telemetry()
			self.render_clustered_telemetry(clustered_tm)
			

	def flush_clusters(self):
		#print "Flushing clusters"
		if len(self.restimes) > 0:
			clustered_tm = self.build_clustered_telemetry()
			self.render_clustered_telemetry(clustered_tm)

	def __del__(self):
		#print "Deleting.."
		self.flush_clusters()
	
		sys.stderr.write("npasses " + str(self.npasses) + "\n")
		sys.stderr.write("nclusters " + str(self.nclusters) + "\n")
		sys.stderr.write("merge_threshold " + str(self.merge_threshold) + "\n")
		sys.stderr.write("datapoints_count " + str(self.datapoints_count) +"\n")
		sys.stderr.write("mergecount " + str(self.mergecount) + "\n")
		sys.stderr.write("merged_datapoints " + str(self.merged_datapoints) + "\n")
		sys.stderr.write("clustered_datapoints_count " + str(self.clustered_datapoints_count) + "\n")


		return


def main(timeblocks, nclusters, npasses, mergethresh, ofile):

	if ofile is None:
		output = sys.stdout
	else:
		output = open(ofile, "w")

	clusterer = rt_telemetry_clusterer(timeblocks, nclusters, npasses, 
			mergethresh, output)

	for line in sys.stdin:
		linetokens = line.strip().split(" ")
		timestamp_msecs = float(linetokens[0]) * 60000
		restime = float(linetokens[1])
		clusterer.cluster_telemetry(timestamp_msecs, restime)
		#print line.strip()

	clusterer.flush_clusters()




def usage():
	print "cluster_rt: Used for creating clustered response time"
	print "data points from the response time telemetry output"
	print "generated by visual_stats.py script in nfsreplay."
	print "USAGE: cluster_rt <OPTIONS>\n"
	print "Data is read from stdin.\n"

	print "\t\t--timeblocks <msecs>"
	print "\t\t\tCreate clusters among the response time figures"
	print "\t\t\tfor all the requests figuring in <msecs> milisecond"
	print "\t\t\tblocks.\n"

	print "\t\t--nclusters <num>"
	print "\t\t\tWithin the requests appearing in <msecs>"
	print "\t\t\tmilisecond periods, create <num> clusters.\n"

	print "\t\t--npasses <npasses>"
	print "\t\t\tRun <npasses> number of passes through the"
	print "\t\t\tk-means clustering algorithm.\n"

	print "\t\t--mergethresh <mcount>"
	print "\t\t\tMerge at most <mcount> data points of the same"
	print "\t\tcluster.\n"

	print "\t\t--output <output_file>"
	print "\t\t\tWrite clustered telemetry output here."



if __name__ == "__main__":
	if len(sys.argv) < 7:
		usage()
		sys.exit(-1)

	if "--nclusters" in sys.argv:
		ncluster = int(sys.argv[sys.argv.index("--nclusters") + 1])
	else:
		print "Number of clusters missing."
		usage()
		sys.exit(-1)

	if "--timeblocks" in sys.argv:
		timeblocks = int(sys.argv[sys.argv.index("--timeblocks") + 1])
	else:
		print "Time blocks missing."
		usage()
		sys.exit(-1)

	if "--npasses" in sys.argv:
		npasses = int(sys.argv[sys.argv.index("--npasses") + 1])
	else:
		print "Number of passes missing."
		usage()
		sys.exit(-1)

	if "--mergethresh" in sys.argv:
		mergethresh = int(sys.argv[sys.argv.index("--mergethresh") + 1])
	else:
		mergethresh = None
	
	if "--output" in sys.argv:
		ofile = sys.argv[sys.argv.index("--output") + 1]
	else:
		ofile = None

	main(timeblocks, ncluster, npasses, mergethresh, ofile)

