import csv,ctypes,json,os,platform,statistics
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def ram_gib():
    try:
        class M(ctypes.Structure):
            _fields_=[('length',ctypes.c_ulong),('load',ctypes.c_ulong)]+[(x,ctypes.c_ulonglong) for x in ('total','avail','totalpage','availpage','totalvirtual','availvirtual','availextended')]
        m=M(); m.length=ctypes.sizeof(m)
        if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m)): return round(m.total/1024**3,2)
    except Exception: pass
    return None

def capture_environment(root):
    import datetime
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,r'HARDWARE\DESCRIPTION\System\CentralProcessor\0') as key:
            cpu=winreg.QueryValueEx(key,'ProcessorNameString')[0].strip()
    except (ImportError, OSError):
        cpu=os.environ.get('PROCESSOR_IDENTIFIER') or platform.processor() or 'No disponible'
    ram=ram_gib()
    machine=f"{platform.platform()}; Python {platform.python_version()}; CPU: {cpu}; RAM: {str(ram)+' GiB' if ram is not None else 'no disponible'}"
    target=root/'results/raw/environment.json'
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(json.dumps({'machine':machine,'captured_at':datetime.datetime.now().astimezone().isoformat()},ensure_ascii=False,indent=2),encoding='utf-8')
    return machine

def write_outputs(root):
    with (root/'results/summary.csv').open(encoding='utf-8',newline='') as f: rows=list(csv.DictReader(f))
    raw=json.loads((root/'results/raw/observaciones.json').read_text(encoding='utf-8'))
    for r in rows:
        subset=[x for x in raw if x['case_id']==r['case_id'] and x['algorithm']==r['algorithm']]
        for mode,col,key in [('time','cpu_ms_median','cpu_ms'),('memory','peak_python_kib_median','peak_python_kib')]:
            vals=[x[key] for x in subset if x['status']=='OK' and x['mode']==mode]
            assert (not vals and not r[col]) or abs(float(r[col])-statistics.median(vals))<1e-9
    by={(int(r['m']),r['algorithm']):r for r in rows}
    sizes=sorted(set(int(r['m']) for r in rows))
    figdir=root/'results/figures'; figdir.mkdir(parents=True,exist_ok=True)
    plt.rcParams.update({'font.size':13,'axes.labelsize':13,'legend.fontsize':13,'xtick.labelsize':12.5,'ytick.labelsize':12.5})
    for col,label,name in [('cpu_ms_median','CPU por ejecución (ms)','cpu.png'),('peak_python_kib_median','Pico Python (KiB)','memoria.png')]:
        fig,ax=plt.subplots(figsize=(7.4,3.3),layout='constrained')
        for alg,color in [('A','#a64037'),('B','#176c77'),('C','#3059a0')]:
            pts=[(n,float(by[n,alg][col])) for n in sizes if by[n,alg][col] and float(by[n,alg][col])>0]
            if pts: ax.plot([p[0] for p in pts],[p[1] for p in pts],marker='o',label=alg,color=color)
        ax.set_xscale('log'); ax.set_yscale('log'); ax.set_xlabel('Longitud de cada cadena (símbolos)'); ax.set_ylabel(label)
        ax.grid(True,which='both',alpha=.22); ax.legend(title='Versión'); fig.savefig(figdir/name,dpi=180); plt.close(fig)
    print('Mediciones verificadas y gráficas actualizadas.')
