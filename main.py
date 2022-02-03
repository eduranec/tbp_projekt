import tkinter

from mongoengine import *


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
    host = ReferenceField('host')
    availability = ReferenceField('availability')
    description = StringField()
    images = StringField()
    notes = StringField()
    beds = IntField()
    space = StringField()
    neighborhood_overview= StringField()
    reviews = ReferenceField('reviews')
    access = StringField()
    review_scores = ReferenceField('review_scores')
    address = ReferenceField('address')
    transit = StringField()
    meta = {'collection': 'listingsAndReviews'} #EKSTREMNO KRUCIJALNA STVAR! Took me YEARS to get it




class location(Document):
    type = StringField()
    coordinates = ListField(DecimalField())
    is_location_exact = BooleanField()


class address(Document):
    street = StringField()
    suburb = StringField()
    government_area = StringField()
    market = StringField()
    country = StringField()
    country_code = StringField()
    location = ReferenceField('location')


class availability(Document):
    availability_30 = IntField()
    availability_60 = IntField()
    availability_90 = IntField()
    availability_365 = IntField()


class review_scores(Document):
    review_scores_accuracy = IntField()
    review_scores_cleanliness = IntField()
    review_scores_checkin = IntField()
    review_scores_communication = IntField()
    review_scores_location = IntField()
    review_scores_value = IntField()
    review_scores_rating = IntField()


class reviews(Document):
    _id = StringField(max_length=9)
    date = LongField()
    listing_id = StringField()
    reviewer_id = StringField()
    reviewer_name = StringField()
    comments = StringField()

class host(Document):
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
    review_scores = ReferenceField('review_scores')
    reviews = ReferenceField('reviews')

def izracunPCC():
    return

# Povezivanje s ATLAS MongoDB bazom sa setom podataka airbnb
DB_URI = "mongodb+srv://erik:Heets7896@cluster0.47e6x.mongodb.net/sample_airbnb?retryWrites=true&w=majority"
connect(host=DB_URI)



window=tkinter.Tk()
# add widgets here

prosjecnaCijenaCiscenja=tkinter.Button(window, text="Prosječna cijena čišćenja",command = izracunPCC() )
prosjecnaCijenaCiscenja.grid(column = 3, row = 0, padx= 25, pady = 30 )

prosjecnaCijenaGumb=tkinter.Button(window, text="Prosječna cijena")
prosjecnaCijenaGumb.grid (column =3, row = 1, padx= 25, pady = 30 )
brojRecenzijaGumb= tkinter.Button(window, text="Broj recenzija")
brojRecenzijaGumb.grid(column = 3,row = 2, padx= 25, pady = 30 )
brojSmjestajnihJedinica= tkinter.Button(window, text="Ukupni broj smještajnih jedinica \n za odabranu zemlju")
brojSmjestajnihJedinica.grid(column = 1,row = 5, padx= 25, pady = 30 )
brojKrevetaZemlja= tkinter.Button(window, text="Ukupni broj kreveta \n za odabranu zemlju")
brojKrevetaZemlja.grid(column = 2,row = 5, padx= 25 )
smjestajniKapacitetZemlje= tkinter.Button(window, text="Smještajni kapacitet \n za odabranu zemlju")
smjestajniKapacitetZemlje.grid(column = 3,row = 5, padx= 25 )

otvoriDokument= tkinter.Button(window, text="Otvaranje dokumenta \n sa smještajnim jednicima")
otvoriDokument.grid(column = 2,row = 6, pady=25 )

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


zemljaVar = ""
zemljaEntry = tkinter.Entry(window,textvariable=zemljaVar)
zemljaEntry.grid(row = 4, column =2, pady = 25, padx =20)

brojSobaVar = ""
brojSobaEntry = tkinter.Entry(window, textvariable=brojSobaVar)
brojSobaEntry.grid(row=0, column=2, pady= 25)

minNocenjaVar = ""
minNocenjaEntry = tkinter.Entry (window, textvariable= minNocenjaVar)
minNocenjaEntry.grid(row = 1, column =2, pady = 25)

maxNocenjaVar = ""
maxNocenjaEntry = tkinter.Entry(window, textvariable= maxNocenjaVar)
maxNocenjaEntry.grid(row = 2, column =2, pady = 25, padx =20)

window.title('Analiza smještajnih jedinica')
window.geometry("600x600+10+20")
window.mainloop()

