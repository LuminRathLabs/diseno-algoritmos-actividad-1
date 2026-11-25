import json, random
def generate(root):
    cases=[]
    for n in (8,12,16,20,32,64,128,256,512,1000):
        seed=20261114+n; r=random.Random(seed)
        cases.append(dict(id=f'n{n}',m=n,n=n,seed=seed,alphabet='ACGT',a=''.join(r.choices('ACGT',k=n)),b=''.join(r.choices('ACGT',k=n))))
    (root/'datasets').mkdir(exist_ok=True)
    (root/'datasets/cases.json').write_text(json.dumps(cases,indent=2,ensure_ascii=False),encoding='utf-8')
    return cases
