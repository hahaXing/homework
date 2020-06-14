def removeDuplicates(nums):
    if not nums:
        return 0
    i = 0 
    for j in range(1, len(nums)):
        if nums[i] != nums[j]:
            i += 1
            nums[i] = nums[j]
    return i + 1


if __name__ == '__main__':
    nums = [5, 8, 7, 9, 3, 4, 8, 3, 2, 1, 6, 7, 4, 8, 5, 9, 3, 2, 1, 5, 7, 4, 6, 9, 8]
    nums.sort()
    length = removeDuplicates(nums)
    print(length)
