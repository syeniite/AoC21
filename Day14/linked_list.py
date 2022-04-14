from dataclasses import dataclass


class LinkedList:

    def __init__(self, head=None):
        self.head = head
        self.tail = head
        self.length = 1 if head else 0

    def __len__(self):
        return self.length

    def __str__(self):
        if not self.tail:
            return "[]"
        else:
            current = self.head
            out = []

            while current:
                out.append(f'{current.key}')
                current = current.next

            return f"[{', '.join(out)}]"

    def add_last(self, element):
        self.length += 1

        if self.tail:
            element.prev = self.tail
            self.tail.next = element
            self.tail = element
        else:
            self.tail = element
            self.head = self.tail

    @staticmethod
    def add_right_to(element, to_be_inserted):
        to_be_inserted.prev = element
        to_be_inserted.next = element.next
        element.next.prev = to_be_inserted
        element.next = to_be_inserted

    def __iter__(self):
        return LinkedListIterator(self)


class Node:
    next = None
    prev = None

    def __init__(self, key):
        self.key = key


class LinkedListIterator:

    def __init__(self, linked_list):
        self.linked_list = linked_list
        self.current = self.linked_list.head

    def __next__(self):
        if self.current:
            result = self.current.key
            self.current = self.current.next

            return result
        raise StopIteration
