import sys
import tkinter
from tkinter import messagebox
from mongoengine import *
from tkinter import ttk
from xlwt import *
import subprocess
import os
from os.path import exists


class location(EmbeddedDocument):
    type = StringField()
    coordinates = ListField(DecimalField())
    is_location_exact = BooleanField()


class address(EmbeddedDocument):
    street = StringField()
    suburb = StringField()
    government_area = StringField()
    market = StringField()
    country = StringField()
    country_code = StringField()
    location = EmbeddedDocumentField(location)


class availability(EmbeddedDocument):
    availability_30 = IntField()
    availability_60 = IntField()
    availability_90 = IntField()
    availability_365 = IntField()


class review_scores(EmbeddedDocument):
    review_scores_accuracy = IntField()
    review_scores_cleanliness = IntField()
    review_scores_checkin = IntField()
    review_scores_communication = IntField()
    review_scores_location = IntField()
    review_scores_value = IntField()
    review_scores_rating = IntField()


class reviews(EmbeddedDocument):
    _id = StringField(max_length=9)
    date = LongField()
    listing_id = StringField()
    reviewer_id = StringField()
    reviewer_name = StringField()
    comments = StringField()

class host(EmbeddedDocument):
    host_id = StringField(max_length=8)
    host_url = StringField()
    host_name = StringField()
    host_location = StringField()
    host_about = StringField()
    host_response_time = StringField()
    host_thumbnail_url = StringField()
    host_picture_url = StringField()
    host_neighbourhood = StringField()
    host_response_rate = IntField()
    host_is_superhost = BooleanField()
    host_has_profile_pic = BooleanField()
    host_identity_verified = BooleanField()
    host_listings_count = IntField()
    host_total_listings_count = IntField()
    host_verifications = ListField(StringField())
    review_scores = EmbeddedDocumentField(review_scores)
    reviews = EmbeddedDocumentField(reviews)

class smjestaj(Document):
    _id = StringField(max_length=8)
    listing_url = StringField()
    name = StringField()
    summary = StringField()
    interaction = StringField()
    house_rules = StringField()
    property_type = StringField()
    room_type = StringField()
    bed_type = StringField()
    minimum_nights = StringField()
    maximum_nights = StringField()
    cancellation_policy = StringField()
    last_scraped = DateTimeField()
    calendar_last_scraped = DateTimeField()
    first_review = DateTimeField()
    last_review = DateTimeField()
    accommodates = IntField()
    bedrooms = IntField()
    number_of_reviews = IntField()
    bathrooms = DecimalField()
    amenities = ListField(StringField())
    price = DecimalField()
    security_deposit = DecimalField()
    cleaning_fee = DecimalField()
    extra_people = DecimalField()
    guests_included = DecimalField()
    host = EmbeddedDocumentField(host)
    availability = EmbeddedDocumentField(availability)
    description = StringField()
    images = StringField()
    notes = StringField()
    beds = IntField()
    space = StringField()
    neighborhood_overview= StringField()
    reviews = ListField(EmbeddedDocumentField(reviews))
    access = StringField()
    review_scores = EmbeddedDocumentField(review_scores)
    address = EmbeddedDocumentField(address)
    transit = StringField()
    weekly_price = DecimalField()
    monthly_price = DecimalField()
    reviews_per_month = IntField()
    meta = {'collection': 'listingsAndReviews'} #EKSTREMNO KRUCIJALNA STVAR! Took me YEARS to get it





def provjeraParametara(minNocenjaVar,maxNocenjaVar,brojSobaVar):
    if (minNocenjaVar == "" or maxNocenjaVar == "" or brojSobaVar == ""):
        tkinter.messagebox.showinfo(title="Upozorenje!",
                                    message="Unesite sva 3 parametra!!!")
        return False
    elif (int(maxNocenjaVar) < int(minNocenjaVar)):
        tkinter.messagebox.showinfo(title="Upozorenje!",
                                    message="Minimalan broj noćenja ne može biti manji od maksimalnog broja noćenja!!!")
        return False
    return True

def izracunPCC(minNocenjaVar,maxNocenjaVar,brojSobaVar):

    if(provjeraParametara(minNocenjaVar,maxNocenjaVar,brojSobaVar)):
        PCC= smjestaj.objects((Q(minimum_nights__gte =minNocenjaVar) & Q(maximum_nights__lte =maxNocenjaVar)) & Q(bedrooms=brojSobaVar)).average("cleaning_fee")
        PCC2=(PCC.to_decimal())
        tkinter.messagebox.showinfo(title="Prosječna cijena čišćenja za odabrane paremetre",
                                    message="Prosječna cijena čišćenja je: {:.2f}  $".format(PCC2))

def izracunPC(minNocenjaVar,maxNocenjaVar,brojSobaVar):

    if (provjeraParametara(minNocenjaVar, maxNocenjaVar, brojSobaVar)):
        PC = smjestaj.objects((Q(minimum_nights__gte=minNocenjaVar) & Q(maximum_nights__lte=maxNocenjaVar)) & Q(
            bedrooms=brojSobaVar)).average("price")
        PC2 = (PC.to_decimal())
        tkinter.messagebox.showinfo(title="Prosječna cijena smještaja za odabrane paremetre",
                                    message="Prosječna cijena smještaja je: {:.2f}  $".format(PC2))

def izracunDep(minNocenjaVar,maxNocenjaVar,brojSobaVar):

    if(provjeraParametara(minNocenjaVar,maxNocenjaVar,brojSobaVar)):
        Rec = smjestaj.objects((Q(minimum_nights__gte=minNocenjaVar) & Q(maximum_nights__lte=maxNocenjaVar)) & Q(
            bedrooms=brojSobaVar)).sum("accommodates")
        tkinter.messagebox.showinfo(title="Smještajni kapacitet",
                                    message="Ukupni smještajni kapacitet iznosi: {} osoba  ".format(Rec))

def izrKrevetZemlja (zemljaVar):
    if(zemljaVar !=""):
        KZ = smjestaj.objects(address__country= zemljaVar).sum("beds")
        tkinter.messagebox.showinfo(title= "Smještajni kapacitet", message = f"Broj kreveta za {zemljaVar} je: {KZ}")

def izrSmjestajZemlja (zemljaVar):
    SZ = smjestaj.objects(address__country = zemljaVar).count()
    tkinter.messagebox.showinfo(title="Broj smještajnih jedinica", message=f"Broj smještajnih jedinica za {zemljaVar} je: {SZ}")

def izrKapacitetZemlja (zemljaVar):
    KapZ = smjestaj.objects(address__country = zemljaVar).sum('accommodates')
    tkinter.messagebox.showinfo(title="Smještajni kapacitet",
                                message=f"Broj ljudi koji mogu biti smješteni za {zemljaVar} je: {KapZ}")

def kreirajSS ():

    wb = Workbook()
    ws =wb.add_sheet("Podaci")
    stupci = ["ID","name", "property_type","minimum_nights","maximum_nights", "summary","price", "security_deposit","cleaning_fee", "bathrooms", "bedrooms", "accommodates", "beds", "country","street" , "host_name", "host_identity_verified", "review_score","property_type"]

    j=0
    for stup in stupci:
        ws.write(0, j, stup)
        j+=1

    i=1
    for s in smjestaj.objects():
        j=0
        ws.write (i,j, s._id )
        ws.write(i, j+1, s.name)
        ws.write(i, j+2, s.property_type)
        ws.write(i, j+3, s.minimum_nights)
        ws.write(i, j+4, s.maximum_nights)
        ws.write(i, j+5, s.summary)
        ws.write(i, j+6, s.price)
        ws.write(i, j+7, s.security_deposit)
        ws.write(i, j+8, s.cleaning_fee)
        ws.write(i, j+9, s.bathrooms)
        ws.write(i, j + 10, s.bedrooms)
        ws.write(i, j + 11, s.accommodates)
        ws.write(i, j + 12, s.beds)
        ws.write(i, j + 13, s.address.country)
        ws.write(i, j + 14, s.address.street)
        ws.write(i, j + 15, s.host.host_name)
        ws.write(i, j + 16, s.host.host_identity_verified)
        ws.write(i, j + 17, s.review_scores.review_scores_value)
        ws.write(i, j + 18, s.property_type)
        i+=1
    wb.save('Podaci.xls')


def otvoriSS():
    if not exists('Podaci.xls'):
        kreirajSS()

    os.chdir(sys.path[0])
    os.system('start excel.exe Podaci.xls')

def prosjecniTrosakZemlja(zemljaVar):
    PTS  = smjestaj.objects(address__country = zemljaVar).average('price')
    PTC = smjestaj.objects(address__country=zemljaVar).average('cleaning_fee')
    PTZ = PTC.to_decimal() + PTS.to_decimal()
    tkinter.messagebox.showinfo(title="Prosječni trošak smještaja zemlje",
                                message="Prosječni trošak smještaja, uključujući i troškove čišćenja, je: {:.2f}".format(PTZ))


# Povezivanje s ATLAS MongoDB bazom sa setom podataka airbnb
DB_URI = "mongodb+srv://erik:Heets7896@cluster0.47e6x.mongodb.net/sample_airbnb?retryWrites=true&w=majority"
connect(host=DB_URI)



window=tkinter.Tk()
# add widgets here

brojSobaVar = tkinter.StringVar()
minNocenjaVar = tkinter.StringVar()
maxNocenjaVar = tkinter.StringVar()
zemljaVar = tkinter.StringVar()

prosjecnaCijenaCiscenja=tkinter.Button(window, text="Prosječna cijena čišćenja",command = lambda:izracunPCC(minNocenjaVar.get(),maxNocenjaVar.get(),brojSobaVar.get()) )
prosjecnaCijenaCiscenja.grid(column = 3, row = 0, padx= 25, pady = 30 )
prosjecnaCijenaGumb=tkinter.Button(window, text="Prosječna cijena smještaja",command = lambda:izracunPC(minNocenjaVar.get(),maxNocenjaVar.get(),brojSobaVar.get()))
prosjecnaCijenaGumb.grid (column =3, row = 1, padx= 25, pady = 30 )
brojRecenzijaGumb= tkinter.Button(window, text="Ukupni smještajni kapacitet",command = lambda:izracunDep(minNocenjaVar.get(),maxNocenjaVar.get(),brojSobaVar.get()))
brojRecenzijaGumb.grid(column = 3,row = 2, padx= 25, pady = 30 )
brojSmjestajnihJedinica= tkinter.Button(window, text="Ukupni broj smještajnih jedinica \n za odabranu zemlju", command=lambda:izrSmjestajZemlja(zemljeCombo.get()))
brojSmjestajnihJedinica.grid(column = 1,row = 5, padx= 25, pady = 30 )

brojKrevetaZemlja= tkinter.Button(window, text="Ukupni broj kreveta \n za odabranu zemlju", command = lambda:izrKrevetZemlja(zemljeCombo.get()))
brojKrevetaZemlja.grid(column = 2,row = 5, padx= 25 )
smjestajniKapacitetZemlje= tkinter.Button(window, text="Smještajni kapacitet \n za odabranu zemlju",command=lambda:izrKapacitetZemlja(zemljeCombo.get()))
smjestajniKapacitetZemlje.grid(column = 3,row = 5, padx= 25 )
otvoriDokument= tkinter.Button(window, text="Otvaranje tabličnog kalkulatora",command=otvoriSS)
otvoriDokument.grid(column = 2,row = 6, pady=25 )
prosjecniTrosakZemlje = tkinter.Button(window, text = "Prosječni trošak smještaja \n zemlje", command = lambda: prosjecniTrosakZemlja(zemljeCombo.get()))
prosjecniTrosakZemlje.grid(column=3, row = 6, pady=25)

L1 = tkinter.Label(window, text="Broj soba:" )
L1.grid(row=0, column=1, pady= 20)

L2= tkinter.Label(window, text="Minimalno noćenja:" )
L2.grid(row=1, column=1, pady= 20)

L3 = tkinter.Label(window, text="Maksimalno noćenja:" )
L3.grid(row=2, column=1, pady= 20)

L4 = tkinter.Label(window, text="Zemlja smještaja:" )
L4.grid(row=4, column=1, pady= 20)

L5 = tkinter.Label(window, text="-----Analiza pojedine zemlje-----" )
L5.grid(row=3, column=1, pady= 20, padx=10)





zemljeCombo = tkinter.ttk.Combobox(window)
zemljeCombo['values']= ('Brazil', 'Portugal', 'United States', 'Canada', 'Hong Kong', 'Australia', 'Turkey', 'Spain', 'China')
zemljeCombo.current(0)
zemljeCombo.grid(row = 4, column =2, pady = 25, padx =20)




brojSobaEntry = tkinter.Entry(window, textvariable=brojSobaVar)
brojSobaEntry.grid(row=0, column=2, pady= 25)


minNocenjaEntry = tkinter.Entry (window, textvariable= minNocenjaVar)
minNocenjaEntry.grid(row = 1, column =2, pady = 25)


maxNocenjaEntry = tkinter.Entry(window, textvariable= maxNocenjaVar)
maxNocenjaEntry.grid(row = 2, column =2, pady = 25, padx =20)

window.title('Analiza smještajnih jedinica')
window.geometry("620x600+10+20")
window.mainloop()

