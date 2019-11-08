from multiprocessing import Process, Manager
import pandas as pd

def parallel_process(cfg, function, data):

    n = len(data)

    p = cfg.num_processes()

    r = int(n / p)

    processes = []
    manager = Manager()
    return_dict = manager.dict()

    # creating processes
    for w in range(p):
        i1 = w * r
        i2 = (w+1) * r
       
        if isinstance(data,type(pd.DataFrame())) == True:
           pcommits = data.iloc[i1:i2] 
        else:
           pcommits = data[i1:i2]
   
        p = Process(target=function, args=(w, cfg, pcommits, return_dict))
        processes.append(p)
        p.start()

    # completing process
    for p in processes:
        p.join()

    dF = pd.DataFrame()

    dfs = return_dict.values()
    for df in dfs:
        dF = pd.concat([dF, df], ignore_index=True)
        cfg.logger.info(str(df.shape))

    cfg.logger.info(str(dF.shape))

    return dF


