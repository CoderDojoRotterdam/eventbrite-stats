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

  print('popular subjects:', popular_subjects(orders))
  print('ninja cities', ninja_cities(orders))

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

def ninja_cities(orders=list()):
  cities = map(lambda order: order.get('Woonplaats').lower(), visitors(orders))
  return Counter(cities).most_common(total_visitors(orders))

def popular_subjects(orders=list()):
  # define the headers on which we can pull subjects from the record
  # since we've changed the exact question a couple of times throughout the year
  subject_headers = [
    'Waar ga je mee aan de slag?',
    'Waar wil je graag mee aan de slag gaan?'
  ]

  # pull the values from the records
  popular = map(lambda order: order.get(subject_headers[0]) or order.get(subject_headers[1]), orders)

  # filter the None values and empty strings and return the rest
  return  filter(lambda subject: subject != None and subject != '', popular)



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