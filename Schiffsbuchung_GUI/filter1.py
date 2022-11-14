# Datei zur Programmierung der Filter Funktion
# To-do-List
# 1. Verkettete Liste erstellen
# 2. Liste nach Elementen Filtern können
# 3. Liste mit Test Werten ausgeben (Terminal)
# 4. Excel Datei einlesen
# 5. Liste mit den Werten aus der Excel Datei Füllen
# 6. Filter austesten

# 1 Klassen für Verkettete Liste

class Node:

    def __init__(self, data):
        ## data of the node
        self.data = data

        ## next pointer
        self.next = None


class LinkedList:

    def __init__(self):
        ## initializing the head with None
        self.head = None

    def insert(self, new_node):
        ## check whether the head is empty or not
        if self.head:
            ## getting the last node
            last_node = self.head
            while last_node.next != None:
                last_node = last_node.next

            ## assigning the new node to the next pointer of last node
            last_node.next = new_node

        else:
            ## head is empty
            ## assigning the node to head
            self.head = new_node

    def display(self):
        ## variable for iteration
        temp_node = self.head

        ## iterating until we reach the end of the linked list
        while temp_node != None:
            ## printing the node data
            print(temp_node.data, end='->')

            ## moving to the next node
            temp_node = temp_node.next

        print('Null')


if __name__ == '__main__':
    ## instantiating the linked list
    linked_list = LinkedList()

    ## inserting the data into the linked list
    linked_list.insert(Node(1))
    linked_list.insert(Node(2))
    linked_list.insert(Node(3))
    linked_list.insert(Node(4))
    linked_list.insert(Node(5))
    linked_list.insert(Node(6))
    linked_list.insert(Node(7))

    ## printing the linked list
    linked_list.display()


# 2 Test Liste Flitern
def Testfilter():
    print("Hier kommt ein Testfilter")
    return 0
Testfilter()

# 3 Ausgabe


# 4 Excel Datei einlesen
read_excel(../Aufgabe 2 Reiseportal/Schiffreisen.xlsx) #excel datei lesen


# 5 Liste mit Excel füllen


# 6 Filtern
def Filter():
    print("Hier kommt der richtige Filter")
    return 0

Filter()

