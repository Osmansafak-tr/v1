from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required

from .models import arastırmacı,yayın,yayın_tür
from .forms import yayinCreateForm

from neo4j import GraphDatabase
import itertools
# Create your views here.
def HomePageView(request):
    return render(request,'home.html')

def arastirmaciDetail(request,id):
    arastirmaci = arastırmacı.nodes.get(isim=id)
    print(arastirmaci.isim)

    return render(request,'arastirmaciDetail.html',{'arastirmaci':arastirmaci})

def arastirmaciDetailVis(request,id):
    isim = id
    print(isim)
    
    return render(request,'arastirmaciDetailVisualization.html',{"isim":isim})

def getAllYayin(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        arama_turu = request.POST.get('arama_turu')
        print(name)
        print(arama_turu)

        if arama_turu == "arastirmaci_adi":
            arastirmaci = arastırmacı.nodes.get(isim=name)
            yayinlar = []
            for i in arastirmaci.Yazdı:
                yayinlar += [i]

            return render(request,'getAllYayinlar.html',{'yayinlar':yayinlar})

        elif arama_turu == "yayin_adi":
            yayin = yayın.nodes.get(isim=name)
            yayinlar =[]
            yayinlar += [yayin]
            return render(request,'getAllYayinlar.html',{'yayinlar':yayinlar})

        elif arama_turu == "yayin_yili":
            yayinlar = yayın.nodes.filter(yıl=name)
            return render(request,'getAllYayinlar.html',{'yayinlar':yayinlar})

    else:
        yayinlar = yayın.nodes.all()
        return render(request,'getAllYayinlar.html',{'yayinlar':yayinlar})

@staff_member_required
def yayinCreateView(request):
    form = yayinCreateForm()

    return render(request,'yayinCreate.html',{'form':form})

@staff_member_required
def getYayinlarAdmin(request):
    if request.method == 'POST':
        from django.conf import settings

        username = settings.NEO4J_USERNAME
        password = settings.NEO4J_PASSWORD

        driver = GraphDatabase.driver(uri= "bolt://localhost:7687", auth=(username, password))

        s = request.POST.get('yazarlar')
        liste = s.split(',')

        print(liste)
        liste2 = []
        for i in liste:
            liste2 += [i.strip()]

        print(liste2)

        sene= request.POST.get('yayin_yili')
        konu= request.POST.get('yayin_ismi')
        isimler=liste2
        yayınyeri= request.POST.get('yayin_yeri')
        tür= request.POST.get('yayin_türü')
        
        
        session=driver.session()
        s1="MERGE (n:yayın{ isim: $konu, yıl:$sene }) RETURN n"
        session.run(s1,konu=konu,sene=sene)
        
        for isim in isimler:
            print(isimler)
        
            ad=isim
        
            session=driver.session()
            s2="MERGE (n:arastırmacı {isim: $ad}) RETURN n"
            session.run(s2,ad=ad)
        
        for isim in isimler:
            print(isim)
            
            ad=isim
        
            session=driver.session()
            s3="MATCH (a:arastırmacı), (b:yayın) WHERE a.isim = $ad AND b.isim = $konu CREATE (a)-[r:Yazdı]->(b) RETURN a,b"    
            session.run(s3,ad=ad,konu=konu)
        
        
        
        karma=list(itertools.permutations(isimler,2))
        for ikili in karma:
            print(ikili[0]+"-"+ikili[1])
            ad1=ikili[0]
            ad2=ikili[1]
            
            session=driver.session()
            sx="MATCH (a:arastırmacı {isim: $ad1}) MATCH (b:arastırmacı {isim: $ad2}) MERGE (a)-[r:ortak]->(b)  RETURN a, r, b"
            session.run(sx,ad1=ad1,ad2=ad2)
        
        
        

        session=driver.session()
        s4="MERGE (n:yayın_tür {tür:$tür ,yer:$yayınyeri}) RETURN n"
        session.run(s4,tür=tür,yayınyeri=yayınyeri)
            
        session=driver.session()
        s5="MATCH (a:yayın), (b:yayın_tür) WHERE a.isim = $konu AND b.tür=$tür AND b.yer = $yayınyeri CREATE (a)-[r:yayınlandı]->(b)  RETURN a,b" 
        session.run(s5,konu=konu,tür=tür,yayınyeri=yayınyeri)

    yayinlar = yayın.nodes.all()
    return render(request,'admin_getAllYayinlar.html',{'yayinlar':yayinlar})

def getArastirmacilarAdmin(request):

    arastirmacilar = arastırmacı.nodes.all()
    return render(request,'admin_getAllArastirmacilar.html',{'arastirmacilar':arastirmacilar})

def getTurlerAdmin(request):

    turler = yayın_tür.nodes.all()
    return render(request,'admin_getAllTurler.html',{'turler':turler})