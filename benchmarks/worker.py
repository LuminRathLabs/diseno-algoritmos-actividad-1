import json,sys,time,tracemalloc
from pathlib import Path
root=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root/'src'))
from lcs import lcs_recursive,lcs_hirschberg,lcs_tabular
def subseq(s,t):
    it=iter(t)
    return all(any(c==x for x in it) for c in s)
req=json.loads(sys.stdin.read())
f={'A':lcs_recursive,'B':lcs_hirschberg,'C':lcs_tabular}[req['algorithm']]
try:
    if req['mode']=='memory':
        tracemalloc.start()
        s=f(req['a'],req['b'])
        peak=tracemalloc.get_traced_memory()[1]/1024
        tracemalloc.stop()
        result={'cpu_ms':None,'wall_ms':None,'peak_python_kib':peak,'calls':1}
    else:
        start=time.process_time_ns(); wall=time.perf_counter_ns(); calls=0
        while True:
            s=f(req['a'],req['b']); calls+=1
            elapsed=time.process_time_ns()-start
            if elapsed>=125_000_000: break
        duration=time.perf_counter_ns()-wall
        result={'cpu_ms':elapsed/calls/1e6,'wall_ms':duration/calls/1e6,'peak_python_kib':None,'calls':calls}
    valid=len(s)==req['optimal'] and subseq(s,req['a']) and subseq(s,req['b'])
    result.update(status='OK' if valid else 'INVALID',lcs_length=len(s))
    print(json.dumps(result))
except RecursionError:
    print(json.dumps({'status':'RECURSION_ERROR'}))
except Exception as e:
    print(json.dumps({'status':'ERROR','error':repr(e)}))
