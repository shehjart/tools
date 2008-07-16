#!/usr/bin/python


def main():
	traces = ['OSC-C', 'CSE']
	schedulers = ['deadline', 'cfq', 'anticipatory']
	as_params = ['antic_expire','read_batch_expire','read_expire','write_batch_expire','write_expire']
	cfq_params = ['fifo_expire_async','fifo_expire_sync','quantum','slice_async','slice_async_rq','slice_idle','slice_sync']
	dl_params = ['fifo_batch','front_merges','read_expire','write_expire','writes_starved']

	sched_params = {'deadline':dl_params, 'cfq':cfq_params, 'anticipatory':as_params}

	maxprocesscount =8 
	minprocesscount = 1
	process_step = 2
	processes = range(minprocesscount, maxprocesscount + 1, process_step)

	param_values = {}

	#anticipatory params
	#param_values['read_expire'] = [1,2,3,4,5]
	#param_values['write_expire'] = [1,2,3,4,5]
	param_values['read_batch_expire'] = [250,500]
	param_values['write_batch_expire'] = [125,250,500]
	param_values['antic_expire'] = [3,6.7,9]

	param_values['back_seek_max'] = [4096,8192,16384] 
	param_values['back_seek_penalty'] = []
	param_values['fifo_expire_async']=[250,500,1000]
	param_values['fifo_expire_sync']=[125,250]
	param_values['quantum']=[]
	param_values['slice_async'] = [40,80,160]
	param_values['slice_async_rq']=[]
	param_values['slice_idle']=[4,8,16]
	param_values['slice_sync'] = [100,150,200]

	#deadline params
	#msecs
	param_values['read_expire']=[100,300,500]
	#secs
	param_values['write_expire']=[2,5]
	param_values['writes_starved']=[2,6]
	param_values['front_merges']=[]
	param_values['fifo_batch']=[]


	for trace in traces:
		for sched in schedulers:
			params = sched_params[sched]
			for param in params:
				pvalues = param_values[param]
				for pvalue in pvalues:
					for proc in processes:
						print trace + ": "+ sched +": "+ param + ": " + str(pvalue) + ": " + str(proc)



if __name__ == "__main__":
	main()
