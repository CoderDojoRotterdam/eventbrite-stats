import glob
import csv
from collections import Counter

def main():
  orders = get_orders()

  # print out a bunch of things
  print('total visitors: ' + str( total_visitors(orders) ) )
  print('total donations: ' + str( total_donators(orders) ) ) 
  print('total donated amount (in EUR): ' + str( total_donation_euros(orders)))
  print('total female ninjas: ' + str( total_female_ninjas(orders)))
  print('total male ninjas: ' + str( total_male_ninjas(orders)))
  print('percentage female ninjas ' + str( total_percentage_female_ninjas(orders)))
  print('percentage male ninjas ' + str( total_percentage_male_ninjas(orders)))
  print('total unique ninjas ' + str( total_unique_ninjas(orders)))
  print('total recurring ninjas ' + str( total_recurring_ninjas(orders)))
  print('percentage recurring ninjas ' + str( total_percentage_recurring_ninjas(orders)))

### methods to actually calculate some numbers
def total_visitors(orders=list()):
  return len(visitors(orders))

def total_donators(orders=list()):
  return len(donators(orders))

def total_donation_euros(orders=list()):
  return sum(map(lambda donation: float(donation.get('Totaal betaald')) - float(donation.get('Eventbrite-servicekosten')), donators(orders)))

def total_female_ninjas(orders=list()):
  return len(filter(lambda order: order.get('Geslacht deelnemer') == 'Meisje', visitors(orders)))

def total_male_ninjas(orders=list()):
  return len(filter(lambda order: order.get('Geslacht deelnemer') == 'Jongen', visitors(orders)))

def total_percentage_male_ninjas(orders=list()):
  return float(total_male_ninjas(orders)) / float(total_visitors(orders)) * 100.0

def total_percentage_female_ninjas(orders=list()):
  return float(total_female_ninjas(orders)) / float(total_visitors(orders)) * 100.0

def total_unique_ninjas(orders=list()):
  return len(unique_ninjas(orders))

def total_recurring_ninjas(orders=list()):
  recurring = filter(lambda ninja: ninja[1] > 1, unique_ninjas(orders))
  return len(recurring)

def total_percentage_recurring_ninjas(orders=list()):
  return float(total_recurring_ninjas(orders)) / float(total_visitors(orders)) * 100.0

def unique_ninjas(orders=list()):
  identifiers = map(generate_identifier, visitors(orders))
  return Counter(identifiers).most_common(total_visitors(orders))


### helper methods
def visitors(orders=list()):
  """Only return visitor records """
  return filter(lambda order: order.get('Tickettype') != 'Doneren', orders)

def donators(orders=list()):
  """Only return donator records"""
  return filter(lambda order: order.get('Tickettype') == 'Doneren', orders)

def generate_identifier(order):
  """Return a unique identifier by concatenating a lowercased stripped
  version of firstname and lastname of the ninja"""

  # get first and last names and convert to lowercase
  first_name = order.get('Voornaam').lower()
  last_name  = order.get('Achternaam').lower()

  #return as concatenated string with spaces stripped out
  return (first_name + last_name).translate(None, ' ')


# this method returns a list of all orders read from various CSV files
def get_orders():
  # read the directory ./data/*.csv
  reports = glob.glob('./data/*.csv')

  # list to store all orders
  orders = list()

  # loop over each report
  for report in reports:

    # open the file as readonly csv
    with open(report, 'r') as csvfile:

      # create a CSV DictReader from it
      reader = csv.DictReader(csvfile, delimiter=',')

      # and append all orders to the global orders list
      map(orders.append, reader)
  
  # finally; return the list of orders
  return orders
      
    
# kick things of
main()

# 0. Bestelnummer
# 1. Besteldatum
# 2. Voornaam
# 3. Achternaam
# 4. E-mail
# 5. Aantal
# 6. Tickettype
# 7. Type bestelling
# 8. Totaal betaald
# 9. Eventbrite-servicekosten
# 10. Eventbrite betalingskosten
# 11. Bezoekersstatus
# 12. Voornaam (ouder)
# 13. Achternaam (ouder)
# 14. Emailadres (Ouders)
# 15. Mobiel nummer (Ouders)
# 16. Ik heb een geldig telefoonnummer opgegeven zodat CoderDojo contact met mij op kan nemen in geval van nood. Wij behouden ons het recht voor om registraties zonder geldig telefoonnummer te annuleren.
# 17. Ik accepteer dat ik opgeroepen kan worden voor de ouderdienst en mijn registratie ongedaan gemaakt wordt bij weigering van ouderdienst zonder opgaaf van een geldige reden.
# 18. Zou je graag een workshop willen volgen? (Enkel bij genoeg aanmeldingen wordt de workshop gegeven)
# 19. Waar wil je graag mee aan de slag gaan?
# 20. Wat heb je tot nu toe al gedaan?
# 21. Ik neem mijn eigen laptop mee
# 22. Hoeveel ouders / verzorgers blijven er aanwezig?
# 23. Leeftijd deelnemer
# 24. Geslacht deelnemer
# 25. Woonplaats
# 26. Heb je een specifiek idee / suggestie waar wij je donatie aan kunnen spenderen?
# 27. Ik ga akkoord met het huisregelement van CoderDojo Rotterdam zoals beschreven op http://coderdojo-rotterdam.nl/huisregels
# 28. Met welke rede bezoek je CoderDojo Rotterdam?
# 29. Met wie van CoderDojo Rotterdam heb je gesproken