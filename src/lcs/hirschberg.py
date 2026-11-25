from . import validate
def lcs_hirschberg(a: str, b: str) -> str:
    """Hirschberg por rangos y filas lineales, sin matriz completa."""
    validate(a,b)
    if len(b)>len(a): a,b=b,a
    out=[]
    def lengths(x0,x1,y0,y1,reverse):
        width=y1-y0; prev=[0]*(width+1)
        xr=range(x1-1,x0-1,-1) if reverse else range(x0,x1)
        for i in xr:
            curr=[0]*(width+1)
            for k in range(1,width+1):
                j=y1-k if reverse else y0+k-1
                curr[k]=prev[k-1]+1 if a[i]==b[j] else max(prev[k],curr[k-1])
            prev=curr
        return prev
    def solve(x0,x1,y0,y1):
        if x0==x1 or y0==y1: return
        if x1-x0==1:
            if any(a[x0]==b[j] for j in range(y0,y1)): out.append(a[x0])
            return
        mid=(x0+x1)//2; w=y1-y0
        left=lengths(x0,mid,y0,y1,False); right=lengths(mid,x1,y0,y1,True)
        split=max(range(w+1),key=lambda k:left[k]+right[w-k])
        del left,right
        solve(x0,mid,y0,y0+split); solve(mid,x1,y0+split,y1)
    solve(0,len(a),0,len(b))
    return ''.join(out)
