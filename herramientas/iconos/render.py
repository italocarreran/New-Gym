import json, math, numpy as np, sys
D=json.load(open('poses.json'))
# MediaPipe idx
NOSE,LEAR,REAR=0,7,8
J={'sh':(11,12),'el':(13,14),'wr':(15,16),'idx':(19,20),'hip':(23,24),'kn':(25,26),'an':(27,28),'toe':(31,32)}
EX={
 'press_banca':dict(src='Barbell_Bench_Press_-_Medium_Grip',lying=True,eq='bench_bar',static=['shin','thigh'],arms='bench',prim=['pecho'],sec=['hombros','tríceps'],nombre='Press de banca con barra'),
 'sentadilla':dict(src='Barbell_Squat',eq='squat_bar',arms='squat',prim=['cuádriceps'],sec=['glúteos','isquiotibiales','lumbar','pantorrillas'],nombre='Sentadilla con barra'),
 'peso_muerto':dict(src='Barbell_Deadlift',eq='bar_floor',prim=['lumbar','glúteos','isquiotibiales'],sec=['cuádriceps','trapecio','antebrazos','espalda media'],nombre='Peso muerto con barra'),
 'remo_barra':dict(src='Bent_Over_Barbell_Row',eq='bar',prim=['espalda media','dorsales'],sec=['bíceps','hombros','lumbar'],nombre='Remo con barra'),
 'curl_barra':dict(src='Barbell_Curl',eq='bar',static=['shin','thigh','trunk','uarm'],prim=['bíceps'],sec=['antebrazos'],nombre='Curl con barra recta'),
}
# bone lengths (units, height~1)
LEN=dict(shin=.245,thigh=.245,trunk=.29,uarm=.17,farm=.15,hand=.045,neck=.045)
HEADR=.062
W=dict(shin=(.062,.045),thigh=(.085,.065),uarm=(.052,.042),farm=(.042,.032),trunk=(.105,.125))

def ang(v,e1,e2): return math.atan2(v@e2,v@e1)
def mid(w,k): a,b=J[k]; return (w[a]+w[b])/2
def side(w,k,s): return w[J[k][s]]

def angles(w):
    w=np.array(w)[:,:3]
    L=(w[11]-w[12])+(w[23]-w[24]); L/=np.linalg.norm(L)
    g=np.array([0,1.,0]); g=g-(g@L)*L; g/=np.linalg.norm(g)
    e2=np.cross(L,g)
    A={}
    for s in (0,1):
        for name,(a,b) in dict(shin=('an','kn'),thigh=('kn','hip'),uarm=('sh','el'),farm=('el','wr')).items():
            A.setdefault(name,[]).append(ang(side(w,b,s)-side(w,a,s),g,e2))
    A={k:math.atan2(np.mean([math.sin(x) for x in v]),np.mean([math.cos(x) for x in v])) for k,v in A.items()}
    A['trunk']=ang(mid(w,'sh')-mid(w,'hip'),g,e2)
    head=(w[LEAR]+w[REAR])/2
    A['nose']=ang(w[NOSE]-head,g,e2)
    return A

def unit(a): return np.array([math.cos(a),math.sin(a)])  # in (down,forward) basis -> convert later

def build(A,lying=False):
    # 2D coords: x=forward, y=down. angle a in (g,e2) basis => vec=(sin a, cos a)
    v=lambda a:np.array([math.sin(a),math.cos(a)])
    if lying:
        # keep relative angles, rotate so trunk is horizontal
        rot=(-math.pi/2)-A['trunk'] if True else 0
        A={k:x+rot for k,x in A.items()}
    P={}
    P['an']=np.array([0.,0.])
    P['kn']=P['an']+LEN['shin']*v(A['shin'])
    P['hip']=P['kn']+LEN['thigh']*v(A['thigh'])
    P['sh']=P['hip']+LEN['trunk']*v(A['trunk'])
    P['el']=P['sh']+LEN['uarm']*v(A['uarm'])
    P['wr']=P['el']+LEN['farm']*v(A['farm'])
    P['hand']=P['wr']+LEN['hand']*v(A['farm'])
    P['head']=P['sh']+(LEN['neck']+HEADR)*v(A['trunk'])
    P['nosedir']=v(A['nose'])
    return P


def ik(P,tgt,elbow_pref):
    sh=P['sh']; d=tgt-sh; L=np.linalg.norm(d); a,b=LEN['uarm'],LEN['farm']+LEN['hand']*0.5
    L=min(L,a+b-1e-3); u=d/np.linalg.norm(d)
    x=(a*a-b*b+L*L)/(2*L); h=math.sqrt(max(a*a-x*x,0))
    n=np.array([-u[1],u[0]])
    if n@elbow_pref<0: n=-n
    el=sh+u*x+n*h; P['el']=el
    fd=(sh+u*L-el); fd/=np.linalg.norm(fd)
    P['wr']=el+fd*LEN['farm']; P['hand']=P['wr']+fd*LEN['hand']

def rotate(P,c,a):
    R=np.array([[math.cos(a),-math.sin(a)],[math.sin(a),math.cos(a)]])
    for k in P:
        if k=='nosedir': P[k]=R@P[k]
        else: P[k]=c+R@(P[k]-c)

def balance(P,E):
    for _ in range(30):
        m=lambda a,b:(P[a]+P[b])/2
        pts=[(m('an','kn'),.09),(m('kn','hip'),.2),(m('hip','sh'),.43),(P['head'],.08),(m('sh','el'),.06),(m('el','wr'),.04),
             (P.get('bar',P['hand']),.35)]
        cx=sum(p[0]*w for p,w in pts)/sum(w for p,w in pts)
        err=cx-(P['an'][0]+0.035)
        if abs(err)<1e-4: break
        h=max(P['head'][1]*-1+P['an'][1],.3)
        rotate(P,P['an'].copy(),-err/h*0.9)

def facing(P,lying):
    if lying: return 1
    t=P['sh']-P['hip']; t/=np.linalg.norm(t); n=P['nosedir']
    return 1 if (n[0]*(-t[1])+n[1]*t[0])*0+n[0]-t[0]*(n@t)>0 else -1

def capsule(p,q,r1,r2):
    p,q=np.array(p),np.array(q); d=q-p; n=np.array([-d[1],d[0]])/max(np.linalg.norm(d),1e-6)
    a,b,c,e=p+n*r1,q+n*r2,q-n*r2,p-n*r1
    f=lambda z:f'{z[0]:.1f},{z[1]:.1f}'
    circ=lambda c0,r:f'M{c0[0]-r:.1f},{c0[1]:.1f}a{r:.1f},{r:.1f} 0 1,0 {2*r:.1f},0a{r:.1f},{r:.1f} 0 1,0 {-2*r:.1f},0Z'
    return f'M{f(a)}L{f(b)}L{f(c)}L{f(e)}Z'+circ(p,r1)+circ(q,r2)

RED='#E5484D'
def render(P,ex,T,frame):
    E=EX[ex]; S=T['s']
    tr=lambda z:np.array([T['ox']+T['f']*z[0]*S,T['oy']+z[1]*S])
    Q={k:tr(v) for k,v in P.items() if k!='nosedir'}
    far_dx,far_dy=-0.022*S*T['f'],-0.006*S   # far side offset (behind)
    out=[]
    o=0.011*S  # outline
    GN,GF,OUT,EQ='#A3A9B0','#7F858D','#3A3F47','#3A3F47'
    prim,sec=set(E['prim']),set(E['sec'])
    def mus_fill(m): return (RED,1) if m in prim else ((RED,.45) if m in sec else None)
    seg={'shin':('an','kn'),'thigh':('kn','hip'),'uarm':('sh','el'),'farm':('el','wr'),'trunk':('hip','sh')}
    # muscles: (segment, t0,t1, side(+1 front/-1 back), width frac, offset frac)
    MUS={'cuádriceps':[('thigh',.1,.85,1,.6,.45)],'isquiotibiales':[('thigh',.15,.85,-1,.55,.5)],
         'glúteos':[('trunk',-.05,.18,-1,.6,.55)],'pantorrillas':[('shin',.3,.75,-1,.6,.45)],
         'pecho':[('trunk',.62,.88,1,.55,.55)],'espalda media':[('trunk',.55,.85,-1,.55,.55)],
         'dorsales':[('trunk',.35,.75,-1,.5,.6)],'lumbar':[('trunk',.15,.45,-1,.5,.6)],'trapecio':[('trunk',.85,1.05,-1,.5,.55)],
         'bíceps':[('uarm',.2,.85,1,.6,.45)],'tríceps':[('uarm',.2,.85,-1,.6,.45)],'antebrazos':[('farm',.05,.55,1,.7,.3)],
         'hombros':[('uarm',-.02,.25,0,.95,0)]}
    def part(name,dx=0,dy=0):
        a,b=seg[name]; p,q=Q[a]+[dx,dy],Q[b]+[dx,dy]
        r1,r2=W[name][0]*S/1.0,W[name][1]*S
        if name=='thigh': r1,r2=W['thigh'][1]*S,W['thigh'][0]*S
        if name=='shin': r1,r2=W['shin'][1]*S*.9,W['shin'][0]*S
        return p,q,r1/2*1.0,r2/2*1.0
    def muscles(name,limb,dx=0,dy=0,clip=None,dim=1.0):
        s=''
        p,q,r1,r2=part(name,dx,dy)
        d=q-p; L=np.linalg.norm(d); u=d/L; n=np.array([-u[1],u[0]])
        # front normal: for legs/arms (proximal->distal), front = rotate so that facing dir +x => use T['f']
        for m,specs in MUS.items():
            mf=mus_fill(m)
            if not mf: continue
            for (sg,t0,t1,fb,wf,of) in specs:
                if sg!=name: continue
                fr=n*(-1 if name in('uarm','farm') else 1)
                r=(r1+r2)/2
                a=p+d*t0+fr*fb*r*of; b=p+d*t1+fr*fb*r*of
                s+=f'<path d="{capsule(a,b,r*wf,r*wf)}" fill="{mf[0]}" fill-opacity="{mf[1]*dim:.2f}" clip-path="url(#{clip})"/>'
        return s
    defs=[]
    def limb(name,col,dx=0,dy=0,tag='',dim=1):
        p,q,r1,r2=part(name,dx,dy)
        cid=f'c_{name}{tag}_{frame}'
        dpath=capsule(p,q,r1,r2)
        defs.append(f'<clipPath id="{cid}"><path d="{dpath}"/></clipPath>')
        bg=f'<path d="{capsule(p,q,r1+o,r2+o)}" fill="{OUT}"/>'
        fg=f'<path d="{dpath}" fill="{col}"/>'+muscles(name,None,dx,dy,cid,dim)
        return bg,fg
    def foot(dx,dy,col):
        a=Q['an']+[dx,dy]; t=a+np.array([0.075*S*T['f'],0.03*S if not E.get('lying') else 0.03*S])
        return f'<path d="{capsule(a,t,.026*S+o,.018*S+o)}" fill="{OUT}"/>',f'<path d="{capsule(a,t,.026*S,.018*S)}" fill="{col}"/>'
    layers=[]
    # far side limbs
    for nm in ['farm','uarm']: layers.append(limb(nm,GF,far_dx,far_dy,'f',.75))
    for nm in ['shin','thigh']: layers.append(limb(nm,GF,far_dx,far_dy,'f',.75))
    layers.append(foot(far_dx,far_dy,GF))
    # head + neck
    hd=Q['head']; hr=HEADR*S
    layers.append((f'<circle cx="{hd[0]:.1f}" cy="{hd[1]:.1f}" r="{hr+o:.1f}" fill="{OUT}"/>',f'<circle cx="{hd[0]:.1f}" cy="{hd[1]:.1f}" r="{hr:.1f}" fill="{GN}"/>'))
    layers.append(limb('trunk',GN))
    for nm in ['thigh','shin']: layers.append(limb(nm,GN))
    layers.append(foot(0,0,GN))
    for nm in ['uarm','farm']: layers.append(limb(nm,GN))
    body=''.join(b+f for b,f in layers)
    # equipment
    eq=''; hand=Q['hand']; R=.128*S; sw=0.016*S
    if E['eq'] in('bar','bar_floor','squat_bar','bench_bar'):
        c=hand
        if E['eq']=='squat_bar': c=Q['bar']
        eq_bar=(f'<circle cx="{c[0]:.1f}" cy="{c[1]:.1f}" r="{R:.1f}" fill="none" stroke="{EQ}" stroke-width="{sw:.1f}"/>'
                f'<circle cx="{c[0]:.1f}" cy="{c[1]:.1f}" r="{R*.55:.1f}" fill="none" stroke="{EQ}" stroke-width="{sw*.6:.1f}"/>'
                f'<circle cx="{c[0]:.1f}" cy="{c[1]:.1f}" r="{sw*.9:.1f}" fill="{EQ}"/>')
    else: eq_bar=''
    gy=T['floor']
    floor=f'<line x1="{T["fx0"]:.1f}" y1="{gy:.1f}" x2="{T["fx1"]:.1f}" y2="{gy:.1f}" stroke="{EQ}" stroke-width="{sw:.1f}" stroke-linecap="round"/>'
    bench=''
    if E['eq']=='bench_bar':
        top=T['bench_top']; x0,x1=sorted([Q['hip'][0]+0.06*S*T['f'],Q['sh'][0]-0.08*S*T['f']])
        bench=(f'<rect x="{x0:.1f}" y="{top:.1f}" width="{x1-x0:.1f}" height="{0.05*S:.1f}" rx="{0.015*S:.1f}" fill="{EQ}"/>'
               f'<line x1="{x0+0.05*S:.1f}" y1="{top:.1f}" x2="{x0+0.05*S:.1f}" y2="{gy:.1f}" stroke="{EQ}" stroke-width="{sw:.1f}"/>'
               f'<line x1="{x1-0.05*S:.1f}" y1="{top:.1f}" x2="{x1-0.05*S:.1f}" y2="{gy:.1f}" stroke="{EQ}" stroke-width="{sw:.1f}"/>')
    # draw order: bench, body far parts..., plate drawn over body? plate is beside body (near side plate) -> on top
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512"><defs>{"".join(defs)}</defs>'
            f'{floor}{bench}{body}{eq_bar}</svg>')

def layout(Ps,E):
    pts=[]
    for P in Ps:
        for k,v in P.items():
            if k=='nosedir': continue
            pts.append(v)
        c=P.get('bar',P['hand']); pts.append(c+[.13,.13]); pts.append(c-[.13,.13]); pts.append(P['head']-[.07,.07])
    pts=np.array(pts); lo,hi=pts.min(0),pts.max(0)
    return lo,hi

import cairosvg
from PIL import Image
for ex,E in EX.items():
    As=[angles(D[f"{E['src']}_{fr}"]['world']) for fr in (0,1)]
    if E.get('lying'):
        for A in As:
            rel={k:A[k]-A['trunk'] for k in A}
            # choose trunk horizontal so knees end up below hips
            best=None
            for sg in (1,-1):
                B={k:sg*rel[k]-math.pi/2 for k in rel}
                B['nose']=math.pi
                P=build(B)
                if best is None or P['hip'][1]<best[1]['hip'][1]: best=(B,P)
            A.clear(); A.update(best[0])
    if E.get('lying'):
        for A in As: A['thigh']=math.radians(-103); A['shin']=math.radians(-172)
    for k in E.get('static',[]):
        m=math.atan2(sum(math.sin(A[k]) for A in As),sum(math.cos(A[k]) for A in As))
        for A in As: A[k]=m
    Ps=[build(A) for A in As]
    # facing: chirality trunk x nose
    t=Ps[0]['sh']-Ps[0]['hip']; n=Ps[0]['nosedir']
    f=1 if (t[0]*n[1]-t[1]*n[0])>0 else -1
    if E.get('lying'): f=1
    for P in Ps:
        for k in P: P[k]=np.array([P[k][0]*f,P[k][1]])
    for i,P in enumerate(Ps):
        if E.get('arms')=='bench':
            tdir=(P['hip']-P['sh'])/np.linalg.norm(P['hip']-P['sh'])
            up=np.array([0,-1.])
            tgt=P['sh']+up*(LEN['uarm']+LEN['farm'])*0.97 if i==0 else P['sh']+tdir*0.06+up*0.105
            ik(P,tgt,elbow_pref=-up+tdir*0.2)
        if E.get('arms')=='squat':
            bar=P['sh']+np.array([-0.035,0.005]); P['bar']=bar
            fw=np.array([1.,0]); ik(P,bar+fw*0.0,elbow_pref=np.array([0.2,1.]))
    if not E.get('lying'):
        for P in Ps: balance(P,E)
    lo,hi=layout(Ps,E)
    floor_u=max(P['an'][1] for P in Ps)+0.03
    if E['eq']=='bar_floor': floor_u=max(floor_u,max(P['hand'][1] for P in Ps)+.128)
    hi[1]=max(hi[1],floor_u)
    S=min(420/(hi[0]-lo[0]),420/(hi[1]-lo[1]))
    T=dict(s=S,f=1,ox=256-(lo[0]+hi[0])/2*S,oy=256-(lo[1]+hi[1])/2*S)
    T['floor']=T['oy']+floor_u*S; T['fx0']=T['ox']+lo[0]*S-10; T['fx1']=T['ox']+hi[0]*S+10
    if E.get('lying'): T['bench_top']=T['oy']+(Ps[0]['hip'][1]+W['trunk'][0]/2+0.012)*S
    for fr,P in enumerate(Ps):
        svg=render(P,ex,T,fr)
        open(f'out/{ex}_{fr}.svg','w').write(svg)
        cairosvg.svg2png(bytestring=svg.encode(),write_to=f'out/{ex}_{fr}.png',output_width=512,output_height=512)
    ims=[Image.open(f'out/{ex}_{i}.png').convert('RGBA') for i in (0,1)]
    fr=[]
    for im in ims:
        bg=Image.new('RGBA',im.size,'white'); bg.alpha_composite(im); fr.append(bg.convert('P',palette=Image.ADAPTIVE))
    fr[0].save(f'out/{ex}.gif',save_all=True,append_images=fr[1:],duration=900,loop=0)
    print(ex,'ok')
