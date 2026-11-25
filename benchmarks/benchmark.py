import csv,datetime,json,os,platform,statistics,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from lcs import lcs_tabular
def run(cases,reps=5):
    raw=[]; blocked=False
    env=os.environ.copy(); env['PYTHONDONTWRITEBYTECODE']='1'
    for c in cases:
        optimum=len(lcs_tabular(c['a'],c['b']))
        for alg in ('A','B','C'):
            for mode in ('time','memory'):
                for rep in range(1,reps+1):
                    item={'case_id':c['id'],'m':c['m'],'n':c['n'],'seed':c['seed'],'algorithm':alg,'mode':mode,'replicate':rep,
                          'timestamp':datetime.datetime.now().astimezone().isoformat(),'python_version':platform.python_version(),'platform':platform.platform(),'timeout_s':5 if alg=='A' else 180,
                          'cpu_ms':None,'wall_ms':None,'peak_python_kib':None}
                    if alg=='A' and blocked:
                        item['status']='SKIPPED_BY_DESIGN'
                    else:
                        request={'a':c['a'],'b':c['b'],'algorithm':alg,'mode':mode,'optimal':optimum}
                        try:
                            p=subprocess.run([sys.executable,str(ROOT/'benchmarks/worker.py')],input=json.dumps(request),text=True,capture_output=True,timeout=item['timeout_s'],cwd=ROOT,env=env)
                            if p.returncode: item.update(status='ERROR',error=p.stderr[-1200:])
                            else: item.update(json.loads(p.stdout))
                        except subprocess.TimeoutExpired:
                            item['status']='TIMEOUT'
                            if alg=='A': blocked=True
                        except Exception as e: item.update(status='ERROR',error=repr(e))
                    raw.append(item)
                    if item['status'] in ('ERROR','INVALID','RECURSION_ERROR'): raise RuntimeError(str(item))
            print(c['id'],alg,flush=True)
    d=ROOT/'results/raw'; d.mkdir(parents=True,exist_ok=True)
    (d/'observaciones.json').write_text(json.dumps(raw,ensure_ascii=False,indent=2),encoding='utf-8')
    rows=[]
    for c in cases:
        for alg in ('A','B','C'):
            subset=[x for x in raw if x['case_id']==c['id'] and x['algorithm']==alg]
            times=[x['cpu_ms'] for x in subset if x['status']=='OK' and x['mode']=='time']
            mem=[x['peak_python_kib'] for x in subset if x['status']=='OK' and x['mode']=='memory']
            rows.append({'case_id':c['id'],'m':c['m'],'n':c['n'],'algorithm':alg,
                         'status':','.join(sorted(set(x['status'] for x in subset))),'time_n':len(times),'cpu_ms_median':statistics.median(times) if times else '',
                         'cpu_ms_min':min(times) if times else '','cpu_ms_max':max(times) if times else '',
                         'memory_n':len(mem),'peak_python_kib_median':statistics.median(mem) if mem else ''})
    with (ROOT/'results/summary.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
    return rows
