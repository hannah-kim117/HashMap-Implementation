# Name:Hannah Kim
# OSU Email: kimha2@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date:8/15/23
# Description: Implement a HashMap class by completing the code down below.
# # Use dynamic array to store your hash table and implement chaining for collision resolution using singly linked list.


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Updates the key/value pair in the hash map.
        If key already exists, value must be replaced with the new value.
        If key is not in the hash map, a new key/value pair must be added.
        Table must be resized to double its current capacity and the current load factor of table is greater than or equal to 1

        """

        # resize table to double its current capacity
        if self.table_load() >= 1:
            self.resize_table(2 * self._capacity)

        index = self._hash_function(key) % self._capacity
        bucket = self._buckets.get_at_index(index)  # linked list

        # if key is not in hash map, add key/value pair
        if bucket.length() is None:
            bucket.insert(key, value)
            self._size += 1

        # iterate through linked list to see if key exists
        for i in bucket:
            if i.key == key:
                bucket.remove(key)  # remove
                bucket.insert(key, value)  # and replace
                return
        bucket.insert(key, value)
        self._size += 1

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in hash table

        """

        # initialize number of empty buckets to 0
        empty_buckets = 0

        for i in range(self._capacity):
            if self._buckets.get_at_index(i).length() == 0:  # if empty
                empty_buckets += 1  # increment empty buckets
        return empty_buckets

    def table_load(self) -> float:
        """
        Returns the current hash table load factor.
        Load factor = total number of elements stored in table / number of buckets

        """
        return self._size / self._capacity

    def clear(self) -> None:
        """
        Clears the contents of the hash map.
        Does not change the underlying hash table capacity.

        """
        self._buckets = DynamicArray()
        for i in range(self._capacity):
            self._buckets.append(LinkedList())
        self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the internal hash table.
        All existing key/value pairs remain in new hash map and all hash table links must be rehashed.

        First check that new_capacity is not less than 1; if so, method does nothing.
        If new_capacity is 1 or more, make sure it is a prime number. If not, change to next highest prime number.

        """
        # make new hash map with new capacity
        new_map = HashMap(new_capacity, self._hash_function)

        # check that new_capacity is not less than 1; if so, do nothing
        if new_capacity < 1:
            return

        # if new_capacity is 1 or more, must be a prime number. If not, change to next highest prime num
        else:
            if new_capacity == 2:
                new_map._capacity = 2
            elif new_capacity != self._is_prime(new_capacity):
                new_capacity = self._next_prime(new_capacity)

        # move key/value pairs to the new hash map
        for i in range(self._capacity):
            chain_key = self._buckets.get_at_index(i)

            for j in chain_key:
                new_map.put(j.key, j.value)

        # reassign
        self._buckets = new_map._buckets
        self._capacity = new_map._capacity
        self._size = new_map._size

    def get(self, key: str):
        """
        Returns the value associated with given key.
        If key is not in hash map, method returns None.

        """

        # gets the index on hash table
        hash_index = self._hash_function(key) % self._capacity
        # linked list
        chain_key = self._buckets.get_at_index(hash_index)

        for i in chain_key:
            if i.key == key:
                return i.value

        # if key not in hash map, return None
        if chain_key.length() == 0:
            return None

    def contains_key(self, key: str) -> bool:
        """
        Returns True if given key is in hash map, otherwise returns False.

        """

        # gets the index on hash table
        hash_index = self._hash_function(key) % self._capacity
        chain_key = self._buckets.get_at_index(hash_index)

        # go to that index and search through entire linked list
        for i in chain_key:
            if i.key == key:
                return True
        return False

    def remove(self, key: str) -> None:
        """
        Removes the given key and its associated value from hash map.
        If key is not in hash map, method does nothing.

        """

        # gets the index on hash table
        hash_index = self._hash_function(key) % self._capacity
        chain_key = self._buckets.get_at_index(hash_index)

        # go to that index and search through entire linked list
        for j in chain_key:
            if j.key == key:
                chain_key.remove(key)
                self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a dynamic array where each index contains a tuple of key/value pair stored in hash map.
        Order of keys in dynamic array does not matter.

        """

        new_da = DynamicArray()

        for i in range(self._capacity):
            for j in self._buckets.get_at_index(i):
                new_da.append((j.key, j.value))
        return new_da


def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
    """
    A standalone function that return a tuple containing a dynamic array comprising the mode value of given array,
    and integer representing highest frequency of occurrence for mode value.

    If there is more than one value with the highest frequency, all values at that frequency should be included.
    If there is only one mode, the dynamic array will contain that value.

    Implemented with O(n) time complexity.

    """
    # if you'd like to use a hash map,
    # use this instance of your Separate Chaining HashMap
    map = HashMap()

    # initialize frequency to 0
    mode = 0
    # make a new Dynamic Array to return
    new_arr = DynamicArray()

    # add to map
    for i in range(0, da.length()):
        key = da.get_at_index(i)
        if map.contains_key(key):
            value = map.get(key) + 1
        else:
            value = 1
        map.put(key, value)

    # make a new hash map
    new_map = map.get_keys_and_values()

    # update mode
    for i in range(0, new_map.length()):
        # if value(index) is greater than current mode, update mode to this value
        if new_map.get_at_index(i)[1] > mode:
            mode = new_map.get_at_index(i)[1]

    # add to new_arr
    for i in range(0, new_map.length()):
        # if value(index) of map at that index is equal to mode:
        if new_map.get_at_index(i)[1] == mode:
            # add the key to new_arr
            new_arr.append(new_map.get_at_index(i)[0])

    return new_arr, mode


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(53, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
