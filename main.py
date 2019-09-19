import json
from pathlib import Path
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import urllib.request


TOKEN_FILE = 'token.txt'
TOKEN = Path(TOKEN_FILE).read_text().strip()

DATA_URL = 'http://resources.finance.ua/ru/public/currency-cash.json'

# import pdb; pdb.set_trace()


def start(update, context):
    """Command /start"""
    print('Command /start')
    update.message.reply_text('Hello, I am bot. How can I help ya?')
def sort(update, context):
    """command /sort"""
    print('Command /sort')
    data = update.message.text.replace('sort ', '').split(' ')
    update.message.reply_text(sortArray(data))

def sortDesc(update, context):
    """command /sortDesc"""
    print('Command /sortDesc')
    data = update.message.text.replace('sort desc ', '').split(' ')
    update.message.reply_text(desCsortArray(data))


def sortArray(array):
    array = str_list_to_int_list(array)
    mergeSort(array)
    return array

def desCsortArray(array):
    array = str_list_to_int_list(array)
    descBubbleSort(array)
    return array

def mergeSort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2  # Finding the mid of the array
        L = arr[:mid]  # Dividing the array elements
        R = arr[mid:]  # into 2 halves

        mergeSort(L)  # Sorting the first half
        mergeSort(R)  # Sorting the second half

        i = j = k = 0

        # Copy data to temp arrays L[] and R[]
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        # Checking if any element was left
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1


# Code to print the list
def printList(arr):
    for i in range(len(arr)):
        print(arr[i], end=" ")
    print()


# driver code to test the above code
if __name__ == '__main__':
    arr = [12, 11, 13, 5, 6, 7]
    print ("Given array is", end="\n")
    printList(arr)
    mergeSort(arr)
    print("Sorted array is: ", end="\n")
    printList(arr)

def descBubbleSort(arr):
    n = len(arr)
    # Traverse through all array elements
    for i in range(n):
        # Last i elements are already in place
        for j in range(0, n - i - 1):
            # traverse the array from 0 to n-i-1
            # Swap if the element found is greater
            # than the next element
            if arr[j] < arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

def kilometersMiles(update, context):
    """Command /start"""
    print('Command /kilometers miles')

    kilometers = int(update.message.text.replace('kilometers miles ', ''))
    conv = 0.621371
    miles = kilometers * conv
    update.message.reply_text('%0.3f kilometers is equal to %0.3f miles' % (kilometers, miles))


# # driver code
# kilometers = 5.5
#
# # conversion factor
# conv = 0.621371
#
# # calculate miles
# miles = kilometers * conv
# print('%0.3f kilometers is equal to %0.3f miles' % (kilometers, miles))
#
# kilometers = 6.5
#
# # calculate miles
# miles = kilometers * conv
# print('%0.3f kilometers is equal to %0.3f miles' % (kilometers, miles))


# def bubbleSort(arr):
#     n = len(arr)
#     # Traverse through all array elements
#     for i in range(n):
#         # Last i elements are already in place
#         for j in range(0, n - i - 1):
#             # traverse the array from 0 to n-i-1
#             # Swap if the element found is greater
#             # than the next element
#             if arr[j] > arr[j + 1]:
#                 arr[j], arr[j + 1] = arr[j + 1], arr[j]
def str_list_to_int_list(str_list):
    n = 0
    while n < len(str_list):
        str_list[n] = int(str_list[n])
        n += 1
    return(str_list)

def buy_usd(update, context):
    """Buying USD handler"""
    print('Buy USD')

    msg = update.message
    msg.bot.send_message(msg.chat_id, 'Вы хотите купить доллары')

    text = urllib.request.urlopen(DATA_URL).read()
    data = json.loads(text)

    sellers = [o for o in data ['organizations'] if 'USD' in o['currencies']]
    sellers.sort(key=lambda o: float(o['currencies']['USD']['ask']))
    best = sellers [0]
    response = f'Лучший курс:{best["currencies"]["USD"]["ask"]}\n' \
    f'{best["title"]} ({best["address"]}) тел.: {best["phone"]}\n' \
    f'{best["link"]}'
    msg.bot.send_message(msg.chat_id, response)



updater = Updater(token=TOKEN, use_context=True)
dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))
dp.add_handler(MessageHandler(Filters.regex('купить доллары'), buy_usd))
dp.add_handler(MessageHandler(Filters.regex('sort [\d]+'), sort))
dp.add_handler(MessageHandler(Filters.regex('sort desc [\d]+'), sortDesc))
dp.add_handler(MessageHandler(Filters.regex('kilometers miles [\d]+'), kilometersMiles))

updater.start_polling()
updater.idle()

