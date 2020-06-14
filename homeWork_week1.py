#删除重复数字
def removeDuplicates(nums):
    if not nums:
        return 0
    i = 0 
    for j in range(1, len(nums)):
        if nums[i] != nums[j]:
            i += 1
            nums[i] = nums[j]
    return i + 1

#数组平移K位
def rotate(nums, k):
        n = len(nums)
        k %= n
        nums[:] = nums[-k:] + nums[:-k]

        print(nums)

#找出和为target的两个数的下标
def twoSum(nums,target):
    d = {}
    n = len(nums)
    for x in range(n):
        if target - nums[x] in d:
            return d[target-nums[x]],x
        else:
            d[nums[x]] = x

#将数字0移到数组末尾
def moveZeroes(nums):
    if not nums:
        return 0
    j = 0
    for i in range(len(nums)):
        if nums[i]:
            nums[j],nums[i] = nums[i],nums[j]
            j += 1

    print(nums)


if __name__ == '__main__':
    nums = [5, 0, 7, 9, 0, 4, 8, 3, 2, 0, 6, 7, 4, 8, 0, 9, 3, 2, 1, 5, 0, 4, 6, 9, 8]

    #nums.sort()
    #length = removeDuplicates(nums)
    #print(length)

    #rotate(nums, 3)

    #x, y = twoSum(nums,8)
    #print(x, y)

    moveZeroes(nums)
