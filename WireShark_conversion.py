myConvertion={'00':'00','CC':'01','AC':'02','60':'03','79':'04','B5':'05','D5':'06','19':'07','F0':'08','3C':'09','5C':'0A','90':'0B','89':'0C','45':'0D','25':'0E','E9':'0F','FD':'10','31':'11','51':'12','9D':'13','84':'14','48':'15','28':'16','E4':'17','0D':'18','C1':'19','A1':'1A','6D':'1B','74':'1C','B8':'1D','D8':'1E','14':'1F','2E':'20','E2':'21','82':'22','4E':'23','57':'24','9B':'25','FB':'26','37':'27','DE':'28','12':'29','72':'2A','BE':'2B','A7':'2C','6B':'2D','0B':'2E','C7':'2F','D3':'30','1F':'31','7F':'32','B3':'33','AA':'34','66':'35','06':'36','CA':'37','23':'38','EF':'39','8F':'3A','43':'3B','5A':'3C','96':'3D','F6':'3E','3A':'3F','42':'40','8E':'41','EE':'42','22':'43','3B':'44','F7':'45','97':'46','5B':'47','B2':'48','7E':'49','1E':'4A','D2':'4B','CB':'4C','07':'4D','67':'4E','AB':'4F','BF':'50','73':'51','13':'52','DF':'53','C6':'54','0A':'55','6A':'56','A6':'57','4F':'58','83':'59','E3':'5A','2F':'5B','36':'5C','FA':'5D','9A':'5E','56':'5F','6C':'60','A0':'61','C0':'62','0C':'63','15':'64','D9':'65','B9':'66','75':'67','9C':'68','50':'69','30':'6A','FC':'6B','E5':'6C','29':'6D','49':'6E','85':'6F','91':'70','5D':'71','3D':'72','F1':'73','E8':'74','24':'75','44':'76','88':'77','61':'78','AD':'79','CD':'7A','01':'7B','18':'7C','D4':'7D','B4':'7E','78':'7F','C5':'80','09':'81','69':'82','A5':'83','BC':'84','70':'85','10':'86','DC':'87','35':'88','F9':'89','99':'8A','55':'8B','4C':'8C','80':'8D','E0':'8E','2C':'8F','38':'90','F4':'91','94':'92','58':'93','41':'94','8D':'95','ED':'96','21':'97','C8':'98','04':'99','64':'9A','A8':'9B','B1':'9C','7D':'9D','1D':'9E','D1':'9F','EB':'A0','27':'A1','47':'A2','8B':'A3','92':'A4','5E':'A5','3E':'A6','F2':'A7','1B':'A8','D7':'A9','B7':'AA','7B':'AB','62':'AC','AE':'AD','CE':'AE','02':'AF','16':'B0','DA':'B1','BA':'B2','76':'B3','6F':'B4','A3':'B5','C3':'B6','0F':'B7','E6':'B8','2A':'B9','4A':'BA','86':'BB','9F':'BC','53':'BD','33':'BE','FF':'BF','87':'C0','4B':'C1','2B':'C2','E7':'C3','FE':'C4','32':'C5','52':'C6','9E':'C7','77':'C8','BB':'C9','DB':'CA','17':'CB','0E':'CC','C2':'CD','A2':'CE','6E':'CF','7A':'D0','B6':'D1','D6':'D2','1A':'D3','03':'D4','CF':'D5','AF':'D6','63':'D7','8A':'D8','46':'D9','26':'DA','EA':'DB','F3':'DC','3F':'DD','5F':'DE','93':'DF','A9':'E0','65':'E1','05':'E2','C9':'E3','D0':'E4','1C':'E5','7C':'E6','B0':'E7','59':'E8','95':'E9','F5':'EA','39':'EB','20':'EC','EC':'ED','8C':'EE','40':'EF','54':'F0','98':'F1','F8':'F2','34':'F3','2D':'F4','E1':'F5','81':'F6','4D':'F7','A4':'F8','68':'F9','08':'FA','C4':'FB','DD':'FC','11':'FD','71':'FE','BD':'FF',}
#file1 = open("myfile.txt","r+")
file1 = open("C:/Users/mman.ISISPACE/Desktop/Python_test/WireSharkData1.txt","r+")
file1.seek(0)

#skip no-frame bytes
s = file1.read(72)
print('Header')
#Header
for x in range(6):
    s = file1.read(2)
    print(myConvertion[s.upper()])

print('Datafield')    
#Datafield
for x in range(217):
    s = file1.read(2)
    print(myConvertion[s.upper()]) 

file1.close()