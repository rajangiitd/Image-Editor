# min heap in name of magic list
class MagicList:
    def __init__(self):
        self.data = [0]

    def findMin(self):
        M = self.data
        ''' find and return the smallest
            element in MagicList
        '''
        L = len(M)
        if (L == 0 or L == 1):
            return None
        else:
            return M[1]

    def insert(self, E):
        M = self.data
        ''' insert E in MagicList M,Return M after inserting E into M
        '''
        L = len(M)
        M.append(E)
        while (L > 1):
            if (M[L // 2] > M[L]):
                t = M[L // 2]
                M[L // 2] = M[L]
                M[L] = t
                L = L // 2
            else:
                break

    def deleteMin(self):
        M = self.data
        ''' delete the minimum element in MagicList M,Return M after deleting the minimum element.
        '''

        def minichild(M, i):
            L = len(M) - 1
            if (L >= (2 * i) + 1):
                if (M[i] < M[2 * i] and M[i] < M[(2 * i) + 1]):
                    return None
                elif (M[2 * i] <= M[2 * i + 1]):
                    return 2 * i
                else:
                    return 2 * i + 1
            elif (L == (2 * i)):
                if (M[2 * i] < M[i]):
                    return 2 * i
                else:
                    return None
            else:
                return None

        L = len(M)
        if (L == 0):
            return M
        elif (L == 1):
            return [0]
        else:
            L = L - 1
            M[1] = M[L]
            M.pop()
            f = 1
            while (minichild(M, f) != None):
                x = minichild(M, f)
                t = M[x]
                M[x] = M[f]
                M[f] = t
                f = x
            return M


def K_sum(L, K):
    ''' find the sum of smallest K elements
        of L using a MagicList. Return the sum.
    '''
    M = MagicList()
    for i in L:
        M.insert(i)
    sum = 0
    for _ in range(K):
        sum = sum + M.findMin()
        M.deleteMin()
    return sum

