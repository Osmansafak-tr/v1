from neo4j import GraphDatabase
from bs4 import BeautifulSoup
from v1 import settings
import requests
import itertools


username = settings.NEO4J_USERNAME
password = settings.NEO4J_PASSWORD

driver = GraphDatabase.driver(uri= "bolt://localhost:7687", auth=(username,password))

r = requests.get('https://dblp.org/pid/28/2694.xml')
source = BeautifulSoup(r.content,"lxml")

texts = source.find_all('r')

index=0

text=texts[19]#ilki 7

index=index+1
print(index)
başlık = text.find('title')
print(başlık.get_text())
yıl = text.find('year')
print(yıl.get_text())

sene=yıl.get_text()
konu=başlık.get_text()

session=driver.session()
s1="CREATE (n:yayın{ isim: $konu, yıl:$sene }) RETURN n"
session.run(s1,konu=konu,sene=sene)



isimler = text.find_all('author')












for isim in isimler:
    print(isim.get_text())
    
    ad=isim.get_text()
    
    session=driver.session()
    s2="MERGE (n:arastırmacı {isim: $ad}) RETURN n"
    session.run(s2,ad=ad)
    
    session=driver.session()
    s3="MATCH (a:arastırmacı), (b:yayın) WHERE a.isim = $ad AND b.isim = $konu CREATE (a)-[r:Yazdı]->(b) RETURN a,b"    
    session.run(s3,ad=ad,konu=konu)
    
    
    
    

karma=list(itertools.permutations(isimler,2))
for ikili in karma:
    print(ikili[0].get_text()+"-"+ikili[1].get_text())
    ad1=ikili[0].get_text()
    ad2=ikili[1].get_text()
    
    session=driver.session()
    sx="MATCH (a:arastırmacı {isim: $ad1}) MATCH (b:arastırmacı {isim: $ad2}) MERGE (a)-[r:ortak]->(b)  RETURN a, r, b"
    session.run(sx,ad1=ad1,ad2=ad2)

    
    
    
    
    
    
    


if text.find('booktitle') != None:
    print("booktitle")
    yayın = text.find('booktitle')
    print(yayın.get_text())
    
    yayınyeri=yayın.get_text()
    
    session=driver.session()
    s4="MERGE (n:yayın_tür {tür:'inproceedings' ,yer:$yayınyeri}) RETURN n"
    session.run(s4,ad=ad,yayınyeri=yayınyeri)
    
    session=driver.session()
    s5="MATCH (a:yayın), (b:yayın_tür) WHERE a.isim = $konu AND b.tür='inproceedings' AND b.yer = $yayınyeri CREATE (a)-[r:yayınlandı]->(b)  RETURN a,b" 
    session.run(s5,konu=konu,yayınyeri=yayınyeri)




if text.find('journal') != None:
    print("journal")
    yayın = text.find('journal')
    print(yayın.get_text())
    
    yayınyeri=yayın.get_text()
    
    session=driver.session()
    s6="MERGE (n:yayın_tür {tür:'journal' ,yer:$yayınyeri}) RETURN n"
    session.run(s6,ad=ad,yayınyeri=yayınyeri)
    
    
    session=driver.session()
    s7="MATCH (a:yayın), (b:yayın_tür) WHERE a.isim = $konu AND b.tür='journal' AND b.yer = $yayınyeri CREATE (a)-[r:yayınlandı]->(b)  RETURN a,b" 
    session.run(s7,konu=konu,yayınyeri=yayınyeri)

    

    
print("\n\n")