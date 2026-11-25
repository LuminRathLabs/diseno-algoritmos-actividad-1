from . import validate
def lcs_recursive(a: str, b: str) -> str:
    """LCS recursiva directa sin memorización."""
    validate(a,b)
    def solve(i,j):
        if not i or not j: return ""
        if a[i-1]==b[j-1]: return solve(i-1,j-1)+a[i-1]
        x=solve(i-1,j); y=solve(i,j-1)
        return x if len(x)>=len(y) else y
    return solve(len(a),len(b))
