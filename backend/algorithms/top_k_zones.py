"""
Top K Zones Algorithm - Manual Implementation
Find the K busiest pickup/dropoff zones without using built-in sort functions

This is required for the assignment - no heapq, no sorted(), etc.
"""

class TopKZones:
    """Find top K zones by trip count using manual heap implementation"""
    
    def __init__(self, k=10):
        self.k = k
    
    def find_top_k_pickups(self, zone_counts):
        """
        Find top K zones by pickup count
        
        Args:
            zone_counts: dict of {zone_id: count}
        
        Returns:
            list of tuples: [(zone_id, count), ...]
        
        Time Complexity: O(n log k) where n = number of zones
        Space Complexity: O(k) for the heap
        """
        # convert dict to list of tuples
        items = [(zone_id, count) for zone_id, count in zone_counts.items()]
        
        # use manual min-heap to keep top K
        # heap maintains K largest elements, smallest at root
        top_k = self._manual_top_k(items, self.k)
        
        # sort top K in descending order (manual sort)
        sorted_result = self._manual_sort_descending(top_k)
        
        return sorted_result
    
    def _manual_top_k(self, items, k):
        """
        Manual implementation of finding top K elements
        Uses min-heap approach but implemented from scratch
        
        Algorithm:
        1. Take first k elements as initial top k
        2. For remaining elements, if larger than smallest in top k, replace it
        3. Maintain heap property after each replacement
        """
        if len(items) <= k:
            return items
        
        # initialize heap with first k items
        heap = items[:k]
        self._build_min_heap(heap)
        
        # process remaining items
        for i in range(k, len(items)):
            zone_id, count = items[i]
            # if current item is larger than smallest in heap
            if count > heap[0][1]:
                heap[0] = (zone_id, count)  # replace root
                self._heapify_down(heap, 0)  # restore heap property
        
        return heap
    
    def _build_min_heap(self, arr):
        """Build min heap from array - manual implementation"""
        n = len(arr)
        # start from last non-leaf node and heapify down
        for i in range(n // 2 - 1, -1, -1):
            self._heapify_down(arr, i)
    
    def _heapify_down(self, arr, idx):
        """
        Heapify down operation for min heap
        Compare with children and swap with smaller one if needed
        """
        n = len(arr)
        smallest = idx
        left = 2 * idx + 1
        right = 2 * idx + 2
        
        # compare with left child
        if left < n and arr[left][1] < arr[smallest][1]:
            smallest = left
        
        # compare with right child
        if right < n and arr[right][1] < arr[smallest][1]:
            smallest = right
        
        # if smallest is not current node, swap and continue heapifying
        if smallest != idx:
            arr[idx], arr[smallest] = arr[smallest], arr[idx]
            self._heapify_down(arr, smallest)
    
    def _manual_sort_descending(self, arr):
        """
        Manual quicksort implementation - descending order
        No using sorted() or .sort()
        """
        if len(arr) <= 1:
            return arr
        
        # quicksort with manual partitioning
        return self._quicksort(arr, 0, len(arr) - 1)
    
    def _quicksort(self, arr, low, high):
        """Quicksort implementation"""
        if low < high:
            # partition and get pivot index
            pi = self._partition(arr, low, high)
            
            # recursively sort left and right
            self._quicksort(arr, low, pi - 1)
            self._quicksort(arr, pi + 1, high)
        
        return arr
    
    def _partition(self, arr, low, high):
        """
        Partition for quicksort - descending order
        Elements larger than pivot go left, smaller go right
        """
        pivot = arr[high][1]  # use count as pivot
        i = low - 1
        
        for j in range(low, high):
            # for descending order, check if current > pivot
            if arr[j][1] > pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1
    
    def find_top_k_by_revenue(self, zone_revenue):
        """
        Find top K zones by total revenue
        Same algorithm, different metric
        """
        items = [(zone_id, revenue) for zone_id, revenue in zone_revenue.items()]
        top_k = self._manual_top_k(items, self.k)
        return self._manual_sort_descending(top_k)
    
    def find_top_routes(self, route_counts, k=None):
        """
        Find top K routes (pickup -> dropoff pairs)
        
        Args:
            route_counts: dict of {(pickup_id, dropoff_id): count}
        """
        k = k or self.k
        items = [(route, count) for route, count in route_counts.items()]
        top_k = self._manual_top_k(items, k)
        return self._manual_sort_descending(top_k)


# helper function for easy use
def get_top_zones(zone_data, k=10, metric='count'):
    """
    Convenience function to get top K zones
    
    Args:
        zone_data: dict of zone_id -> value
        k: number of top zones to return
        metric: 'count' or 'revenue'
    
    Returns:
        list of (zone_id, value) tuples in descending order
    """
    finder = TopKZones(k)
    
    if metric == 'revenue':
        return finder.find_top_k_by_revenue(zone_data)
    else:
        return finder.find_top_k_pickups(zone_data)