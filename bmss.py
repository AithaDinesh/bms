from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import json
from prettytable import PrettyTable
import sys

bms3="https://in.bookmyshow.com/buytickets/sarkaru-vaari-paata-hyderabad/movie-hyd-ET00131962-MT/20220512"
bms1="https://in.bookmyshow.com/buytickets/sarkaru-vaari-paata-vizag-visakhapatnam/movie-viza-ET00131962-MT/20220512"
bms2="https://in.bookmyshow.com/buytickets/sarkaru-vaari-paata-chennai/movie-chen-ET00131962-MT/20220512"
#bms="https://in.bookmyshow.com/buytickets/sarkaru-vaari-paata-bengaluru/movie-bang-ET00131962-MT/20220512"
bms4="https://in.bookmyshow.com/buytickets/sarkaru-vaari-paata-warangal/movie-war-ET00131962-MT/20220512"
bms="https://in.bookmyshow.com/buytickets/sarkaru-vaari-paata-bengaluru/movie-bang-ET00131962-MT/20220512"
bms5="https://in.bookmyshow.com/buytickets/sarkaru-vaari-paata-tirupati/movie-tiru-ET00131962-MT/20220512"
bmss = [bms,bms1,bms2,bms4,bms5,bms3]
for i in bmss:
    req=Request(i,headers={'User-Agent': 'Mozilla/5.0'})
    webpage=urlopen(req).read()
    soup=BeautifulSoup(webpage,'html.parser')
    #print(soup)
    soup2=soup.find_all('script', type='text/javascript', src=None)

    #parse the aVN_details
    soup_text = ""
    for ele in soup2:
        soup_text = str(ele)
        if 'aVN_details' in soup_text:
            break
    start_index = soup_text.find("aVN_details")
    end_index = soup_text.find("nowDate")
    json_string = soup_text[start_index+18:end_index-7]
    json_string = '{"data":' + json_string + '}' 

    #print(json_string)

    #string to dict
    json_dict = json.loads(json_string)

    #print("\n\n" + ConsoleColor.BOLD  + ConsoleColor.BLUE + "<=========================BookMyShow===========================>\n" + ConsoleColor.END)
   
    FinalGross = 0
    FinalMaxGross = 0
    FinalShowCount = 0
    FinalTicketsPossible = 0
    FinalTicketsBooked = 0
    t3 = PrettyTable(['TheaterName','ShowCount', 'TotalTicketsBooked', 'TotalMaxTickets', 'TotalGross', 'TotalMaxGross'])


    for i in range(len(json_dict['data'])):
        data = json_dict['data'][i]
        #print(data['SubRegName'], data['VenueName'])
        TheaterGross = 0
        TheaterMaxGross = 0
        TotalMaxTicketsAvailable = 0
        TotalTicketsBooked = 0
        TheaterShowCount = 0
        t2 = PrettyTable(['ShowTime', 'TotalMaxseats', 'ToalSeatsBooked', 'TotalShowGross', 'TotalShowMaxGross'])
        for j in data['ShowTimes']:
            totalMaxSeats = 0
            totalBookedSeats = 0
            totalShowGross = 0
            totalShowMaxGross = 0
            TheaterShowCount = TheaterShowCount + 1
            t = PrettyTable(['ShowTime', 'Maxseats', 'SeatsBooked', 'CurPrice', 'SubGross', 'SubMaxGross'])
            for k in j['Categories']:
                MaxSeats = int(k['MaxSeats'])
                SeatsAvail = int(k['SeatsAvail'])
                CurPrice = float(k['CurPrice'])
                SeatsBooked = MaxSeats - SeatsAvail
                SubGross = SeatsBooked * CurPrice
                SubMaxGross = MaxSeats * CurPrice
                t.add_row([j['ShowTime'], MaxSeats, SeatsBooked, CurPrice, SubGross, SubMaxGross])
                totalShowGross = totalShowGross + SubGross
                totalShowMaxGross = totalShowMaxGross + SubMaxGross
                totalMaxSeats = totalMaxSeats + MaxSeats
                totalBookedSeats = totalBookedSeats + SeatsBooked
            
            t2.add_row([j['ShowTime'], totalMaxSeats, totalBookedSeats, totalShowGross, totalShowMaxGross])
            TheaterGross = TheaterGross + totalShowGross
            TotalTicketsBooked = TotalTicketsBooked + totalBookedSeats
            TotalMaxTicketsAvailable = TotalMaxTicketsAvailable+ totalMaxSeats
            TheaterMaxGross = TheaterMaxGross + totalShowMaxGross 
            '''
            if 'AM' in j['ShowTime']:
                t2.add_row([j['ShowTime'], totalMaxSeats, totalBookedSeats, totalShowGross, totalShowMaxGross])
                TheaterGross = TheaterGross + totalShowGross
                TotalTicketsBooked = TotalTicketsBooked + totalBookedSeats
                TotalMaxTicketsAvailable = TotalMaxTicketsAvailable+ totalMaxSeats
                TheaterMaxGross = TheaterMaxGross + totalShowMaxGross 
                print(t2)
            '''
        #print(t2) 
        t3.add_row([data['VenueName'], TheaterShowCount, TotalTicketsBooked, TotalMaxTicketsAvailable, TheaterGross, TheaterMaxGross])
        FinalGross = FinalGross + TheaterGross
        FinalMaxGross = FinalMaxGross + TheaterMaxGross
        FinalShowCount = FinalShowCount + TheaterShowCount
        FinalTicketsPossible = FinalTicketsPossible + TotalMaxTicketsAvailable
        FinalTicketsBooked = FinalTicketsBooked + TotalTicketsBooked


    #Theater gross list
    print(t3)

    #Final Gross
    t4 = PrettyTable(["Totatheaters", 'TotalShowCount', "TotalTicketsBooked", "TotalMaxTickets" ,"TotalGross", "TotalMaxGross"])
    t4.add_row([len(json_dict['data']), FinalShowCount, FinalTicketsBooked, FinalTicketsPossible, FinalGross, FinalMaxGross])
    print(t4)



