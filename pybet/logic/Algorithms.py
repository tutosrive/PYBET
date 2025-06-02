from typing import List, TypeVar

T = TypeVar('T')

class Algorithms:
    """
    Collection of classic algorithms: linear search, binary search,
    and simple sorting algorithms implemented from scratch, generic over type T.
    """

    @staticmethod
    def LinearSearch(data: List[T], target: T) -> int:
        """
        Scans the list from start to end looking for the target.

        Args:
            data (List[T]): The list to search.
            target (T): The value to find.

        Returns:
            int: The index of target if found; otherwise -1.
        """
        for index, value in enumerate(data):
            if value == target:
                return index
        return -1

    @staticmethod
    def BinarySearch(sorted_data: List[T], target: T) -> int:
        """
        Performs binary search on a sorted list.

        Args:
            sorted_data (List[T]): The sorted list to search.
            target (T): The value to find.

        Returns:
            int: The index of target if found; otherwise -1.
        """
        left, right = 0, len(sorted_data) - 1
        while left <= right:
            mid = (left + right) // 2
            if sorted_data[mid] == target:
                return mid
            if sorted_data[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        return -1

    @staticmethod
    def BubbleSort(data: List[T]) -> List[T]:
        """
        Sorts a list using the bubble sort algorithm.

        Args:
            data (List[T]): The list to sort.

        Returns:
            List[T]: A new list containing the sorted elements.
        """
        arr = data.copy()
        n = len(arr)
        for i in range(n):
            for j in range(0, n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        return arr

    @staticmethod
    def SelectionSort(data: List[T]) -> List[T]:
        """
        Sorts a list using the selection sort algorithm.

        Args:
            data (List[T]): The list to sort.

        Returns:
            List[T]: A new list containing the sorted elements.
        """
        arr = data.copy()
        n = len(arr)
        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                if arr[j] < arr[min_idx]:
                    min_idx = j
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
        return arr

    @staticmethod
    def InsertionSort(data: List[T]) -> List[T]:
        """
        Sorts a list using the insertion sort algorithm.

        Args:
            data (List[T]): The list to sort.

        Returns:
            List[T]: A new list containing the sorted elements.
        """
        arr = data.copy()
        for i in range(1, len(arr)):
            key = arr[i]
            j = i - 1
            while j >= 0 and arr[j] > key:
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = key
        return arr

    @staticmethod
    def MergeSort(data: List[T]) -> List[T]:
        """
        Sorts a list using the merge sort algorithm.

        Args:
            data (List[T]): The list to sort.

        Returns:
            List[T]: A new list containing the sorted elements.
        """
        def merge(left: List[T], right: List[T]) -> List[T]:
            merged: List[T] = []
            i = j = 0
            while i < len(left) and j < len(right):
                if left[i] <= right[j]:
                    merged.append(left[i])
                    i += 1
                else:
                    merged.append(right[j])
                    j += 1
            merged.extend(left[i:])
            merged.extend(right[j:])
            return merged

        if len(data) <= 1:
            return data.copy()
        mid = len(data) // 2
        left_sorted = Algorithms.MergeSort(data[:mid])
        right_sorted = Algorithms.MergeSort(data[mid:])
        return merge(left_sorted, right_sorted)