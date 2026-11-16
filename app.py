from flask import Flask, render_template, request
app = Flask(__name__)
CATALOGO = [
 {'id':'c1','titulo':'Horizonte','generos':{'rock'},'artista':'Aurora'},
 {'id':'c2','titulo':'Luz de ciudad','generos':{'pop'},'artista':'Nova'},
 {'id':'c3','titulo':'Ecos','generos':{'rock','indie'},'artista':'Nova'},
 {'id':'c4','titulo':'Ritmo azul','generos':{'rap'},'artista':'Delta'},
 {'id':'c5','titulo':'Camino','generos':{'pop','indie'},'artista':'Aurora'},
 {'id':'c6','titulo':'Noche','generos':{'jazz'},'artista':'Sol'},
]

def jaccard(a,b):
    a,b=set(a),set(b)
    return len(a & b)/len(a | b) if a | b else 0.0

def recomendar(generos=(), artistas=(), seleccionadas=()):
    generos,artistas,seleccionadas=set(generos),set(artistas),set(seleccionadas)
    candidatos=[]
    for c in CATALOGO:
        if c['id'] in seleccionadas: continue
        g=bool(c['generos'] & generos)
        a=c['artista'] in artistas
        if g or a:
            puntos=2*int(g)+2*int(a)+jaccard(c['generos'],generos)
            motivo=', '.join(x for x,ok in [('género',g),('artista',a)] if ok)
            candidatos.append({**c,'puntos':round(puntos,3),'motivo':motivo})
    return sorted(candidatos,key=lambda c:(-c['puntos'],c['titulo']))

@app.route('/',methods=['GET','POST'])
def inicio():
    generos=set(request.form.getlist('generos'))
    artistas=set(request.form.getlist('artistas'))
    seleccionadas=set(request.form.getlist('seleccionadas'))
    resultados=recomendar(generos,artistas,seleccionadas) if request.method=='POST' else []
    return render_template('index.html',catalogo=CATALOGO,generos=sorted(set().union(*(c['generos'] for c in CATALOGO))),artistas=sorted({c['artista'] for c in CATALOGO}),resultados=resultados,seleccion_generos=generos,seleccion_artistas=artistas,seleccionadas=seleccionadas,consultado=request.method=='POST')

if __name__=='__main__':
    app.run(debug=True)
