# Author: Max Grier
# Date: 5/27/2020
# Description: Portfolio Project - Hash Map.  Creating a hash map implementation
# that will be used to create a word count program.

# hash_map.py
# ===================================================
# Implement a hash map with chaining
# ===================================================


class SLNode:
    def __init__(self, key, value):
        self.next = None
        self.key = key
        self.value = value

    def __str__(self):
        return '(' + str(self.key) + ', ' + str(self.value) + ')'


class LinkedList:
    def __init__(self):
        self.head = None
        self.size = 0

    def add_front(self, key, value):
        """Create a new node and inserts it at the front of the linked list
        Args:
            key: the key for the new node
            value: the value for the new node"""
        new_node = SLNode(key, value)
        new_node.next = self.head
        self.head = new_node
        self.size = self.size + 1

    def remove(self, key):
        """Removes node from linked list
        Args:
            key: key of the node to remove """
        if self.head is None:
            return False
        if self.head.key == key:
            self.head = self.head.next
            self.size = self.size - 1
            return True
        cur = self.head.next
        prev = self.head
        while cur is not None:
            if cur.key == key:
                prev.next = cur.next
                self.size = self.size - 1
                return True
            prev = cur
            cur = cur.next
        return False

    def contains(self, key):
        """Searches linked list for a node with a given key
        Args:
        	key: key of node
        Return:
        	node with matching key, otherwise None"""
        if self.head is not None:
            cur = self.head
            while cur is not None:
                if cur.key == key:
                    return cur
                cur = cur.next
        return None

    def __str__(self):
        out = '['
        if self.head != None:
            cur = self.head
            out = out + str(self.head)
            cur = cur.next
            while cur != None:
                out = out + ' -> ' + str(cur)
                cur = cur.next
        out = out + ']'
        return out


def hash_function_1(key):
    hash = 0
    for i in key:
        hash = hash + ord(i)
    return hash


def hash_function_2(key):
    hash = 0
    index = 0
    for i in key:
        hash = hash + (index + 1) * ord(i)
        index = index + 1
    return hash


class HashMap:
    """
    Creates a new hash map with the specified number of buckets.
    Args:
        capacity: the total number of buckets to be created in the hash table
        function: the hash function to use for hashing values
    """

    def __init__(self, capacity, function):
        self._buckets = []
        for i in range(capacity):
            self._buckets.append(LinkedList())
        self.capacity = capacity
        self._hash_function = function
        self.size = 0

    def clear(self):
        """
        Empties out the hash table deleting all links in the hash table.
        """
        # Iterate through each bucket
        for bucket in self._buckets:
            # Resets the head to none, then makes it size 0 to effectively clear the bucket
            bucket.head = None
            bucket.size = 0
        self.size = 0
        return

    def get(self, key):
        """
        Returns the value with the given key.
        Args:
            key: the value of the key to look for
        Return:
            The value associated to the key. None if the link isn't found.
        """
        # Finds where the key is stored
        index = self._hash_function(key) % self.capacity
        # Variable for the position on the key
        position = self._buckets[index]
        # Finds the node where the key is
        node = position.contains(key)
        # Check the value in the node against the key we are looking for
        if node is not None:
            return node.value
        else:
            # Otherwise return none
            return None

    def resize_table(self, capacity):
        """
        Resizes the hash table to have a number of buckets equal to the given
        capacity. All links need to be rehashed in this function after resizing
        Args:
            capacity: the new number of buckets.
        """
        # Set the new hash map
        new_hash_map = []

        # Iterates through the capacity of the has map
        for i in range(capacity):
            new_hash_map.append(LinkedList())
        # Readjust the new capacity
        self.capacity = capacity

        # Iterate through the pre-resized buckets
        for bucket in self._buckets:
            # Proceed if there is data in the bucket
            if bucket.head is not None:
                # Set head node
                current = bucket.head
                # Cycle through current position
                while current is not None:
                    # Set the index of current
                    index = self._hash_function(current.key) % self.capacity
                    # Set the position in hash map
                    position = new_hash_map[index]
                    # Insert data from old node to new onw
                    position.add_front(current.key, current.value)
                    # Move to the next
                    current = current.next
        # Replaces old hash map with new rehashed data
        self._buckets = new_hash_map
        return

    def put(self, key, value):
        """
        Updates the given key-value pair in the hash table. If a link with the given
        key already exists, this will just update the value and skip traversing. Otherwise,
        it will create a new link with the given key and value and add it to the table
        bucket's linked list.

        Args:
            key: they key to use to has the entry
            value: the value associated with the entry
        """
        # Gets the index of the key value pair in the hash map
        index = self._hash_function(key) % self.capacity
        # Sets the position within the buckets
        position = self._buckets[index]

        # If the key is already in the hash map, replace value
        if position.contains(key) is not None:
            node = position.contains(key)
            node.value = value
        # Otherwise, add the key value pair to the hash map and increase size
        else:
            position.add_front(key, value)
            self.size += 1
        return

    def remove(self, key):
        """
        Removes and frees the link with the given key from the table. If no such link
        exists, this does nothing. Remember to search the entire linked list at the
        bucket.
        Args:
            key: they key to search for and remove along with its value
        """
        # Find index of the key
        index = self._hash_function(key) % self.capacity
        # Set the bucket where the key would be
        bucket = self._buckets[index]
        # If the key is in that bucket, call remove to remove it
        # then reduce the size by 1
        if bucket.contains(key):
            bucket.remove(key)
            self.size -= 1
            return
        # If the key cannot be found, return
        else:
            return

    def contains_key(self, key):
        """
        Searches to see if a key exists within the hash table

        Returns:
            True if the key is found False otherwise

        """
        # Gets the index of the key value pair in the hash map
        index = self._hash_function(key) % self.capacity
        # Sets the position within the buckets
        bucket = self._buckets[index]

        # Checks if the position contains that key
        # If so, return true
        if bucket.contains(key) is not None:
            return True
        # Otherwise, return false
        else:
            return False

    def empty_buckets(self):
        """
        Returns:
            The number of empty buckets in the table
        """
        # Counter variable
        bucket_count = 0

        # Iterate through all buckets
        for bucket in self._buckets:
            # If there isn't anything in the bucket, increase empty bucket count
            if bucket.size == 0:
                bucket_count += 1
        return bucket_count

    def table_load(self):
        """
        Returns:
            the ratio of (number of links) / (number of buckets) in the table as a float.

        """
        # Find the load ratio using size and capacity, turn to a float
        load_ratio = float(self.size / self.capacity)
        return load_ratio

    def __str__(self):
        """
        Prints all the links in each of the buckets in the table.
        """

        out = ""
        index = 0
        for bucket in self._buckets:
            out = out + str(index) + ': ' + str(bucket) + '\n'
            index = index + 1
        return out
