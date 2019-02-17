# Given a string, determine if it is a palindrome, considering only alphanumeric characters and ignoring cases.
# 
# Note: For the purpose of this problem, we define empty string as valid palindrome.
# 
# Example 1:
# 
# Input: "A man, a plan, a canal: Panama"
# Output: true
# Example 2:
# 
# Input: "race a car"
# Output: false


class Solution:
        def isPalindrome(self, s: 'str') -> 'bool':
            x = len(s)
            s = s.lower()
            out = False
            z = 0

            for n in range(x):
                if s[z] >= 'a' and s[z] <= 'z':
                    z += 1
                    continue
                else:
                    s1 = s[:z] + s[z+1:]
                    s = s1
                    z -= 1
                z += 1

            x = len(s)

            for i in range(len(s)):
                if i < x:
                    if s[i] == s[x-1]:
                        out = True
                    else:
                        out = False
                    x -= 1
                else:
                    break

            return out


y = Solution()
print(y.isPalindrome("A man, a plan, a canal: Panama"))
print(y.isPalindrome("Anita lava la tina"))
print(y.isPalindrome("Race a car"))
