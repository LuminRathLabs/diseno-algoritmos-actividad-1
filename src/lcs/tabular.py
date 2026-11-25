from . import validate
def lcs_tabular(a: str, b: str) -> str:
    """LCS mediante tabla de longitudes y reconstrucción."""
    validate(a,b)
    m,n=len(a),len(b)
    table=[[0]*(n+1) for _ in range(m+1)]
    for i in range(1,m+1):
        row,prev=table[i],table[i-1]
        for j in range(1,n+1):
            row[j]=prev[j-1]+1 if a[i-1]==b[j-1] else max(prev[j],row[j-1])
    result=[]
    while m and n:
        if a[m-1]==b[n-1]: result.append(a[m-1]); m-=1; n-=1
        elif table[m-1][n]>=table[m][n-1]: m-=1
        else: n-=1
    return ''.join(reversed(result))
