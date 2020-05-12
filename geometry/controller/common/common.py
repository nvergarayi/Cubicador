# -*- coding: utf-8 -*-
def checkSign(num):
    '''
    Funcion para determinar el signo de un numero dado.
    '''
    if num < 0: return 1
    elif num > 0: return 2
    else: return 0
    
def checkIntervalClosed(a, b, x):
    '''
    Determina si x se encuentra en el intervalo cerrado a, b
    @param a: float
    @param b: float
    @param x: float
    @return: boolean
    '''
    if x >= min(a,b) and x <= max(a,b): 
        return True 
    return False

def checkIntervalOpen(a, b, x):
    '''
    Determina si x se encuentra en el intervalo abierto a, b
    @param a: float
    @param b: float
    @param x: float
    @return: boolean
    '''
    if x > min(a,b) and x < max(a,b):
        return True
    return False

def checkIntervalSemiopen(a, b, x):
    '''
    Determina si x se encuentra en el intervalo semiabierto a, b
    @param a: float
    @param b: float
    @param x: float
    @return boolean
    '''
    if x >= min(a,b) and x < max(a,b):
        return True
    return False

def checkIntervalSemiopen2(a, b, x):
    '''
        Determina si x se encuentra en el intervalo semiabierto a, b
        @param a: float
        @param b: float
        @param x: float
        @return boolean
        '''
    if x > min(a,b) and x <= max(a,b):
        return True
    return False

# '''
# Funcion para resolver el sistema de ecuaciones que permite la obtencion de
# las constantes del polinomio cuadratico de interpolacion.
# '''
def gaussianElimination(A,B):
    '''
    Resolucion del sistema de ecuaciones
    '''
    exchange = [0]*len(B)
    result = [0]*len(B)

    for k in range(len(B)-1):
        p = 0
        keep = 0
        pointer = []
        
        for i in range(k,len(B)):
            for j in range(k,len(B)):
                if (abs(A[i][j]) > exchange[i]):
                    exchange[i] = abs(A[i][j])
            if (exchange[i] == 0):
                return None
          
        for i in range(k,len(B)):
            if (abs(A[i][k])/exchange[i] > keep):
                keep = abs(A[i][k])/exchange[i]
                p = i
        
        if ((p != k) and (p != 0)):
            exchange = A[p]
            A[p] = A[k]
            A[k] = exchange
            keep = B[p]
            B[p] = B[k]
            B[k] = keep
        
        for j in range(k,len(B)):
            if (A[k][j] != 0):
                pointer.append(j)
        
        for i in range(k+1,len(B)):
            if (A[i][k] != 0):
                keep = A[i][k]/A[k][k]
                for j in range(len(pointer)):
                    A[i][pointer[j]] = A[i][pointer[j]]-A[k][pointer[j]]*keep
                B[i] = B[i]-B[k]*keep

    k = len(B)-1
    while k >= 0:
        result[k] = B[k]
        if (k < len(B)-1):
            for i in range(k+1,len(B)):
                result[k] = result[k]-A[k][i]*result[i]
        result[k] = result[k]/A[k][k]
        k -= 1
    
    return result

# # '''
# # Funcion para resolver el sistema de ecuaciones que permite la obtencion de
# # las constantes del polinomio cuadratico de interpolacion.
# # '''
# def gaussianElimination(A,B):
#     '''
#     Resolucion del sistema de ecuaciones
#     '''
#     exchange = [0]*len(B)
#     result = [0]*len(B)
# 
#     for k in range(len(B)-1):
#         p = 0
#         keep = 0
#         pointer = []
#         
#         for i in range(k,len(B)):
#             for j in range(k,len(B)):
#                 if (abs(A[i][j]) > exchange[i]):
#                     exchange[i] = abs(A[i][j])
#             if (exchange[i] == 0):
#                 return False,result
#           
#         for i in range(k,len(B)):
#             if (abs(A[i][k])/exchange[i] > keep):
#                 keep = abs(A[i][k])/exchange[i]
#                 p = i
#         
#         if ((p != k) and (p != 0)):
#             exchange = A[p]
#             A[p] = A[k]
#             A[k] = exchange
#             keep = B[p]
#             B[p] = B[k]
#             B[k] = keep
#         
#         for j in range(k,len(B)):
#             if (A[k][j] != 0):
#                 pointer.append(j)
#         
#         for i in range(k+1,len(B)):
#             if (A[i][k] != 0):
#                 keep = A[i][k]/A[k][k]
#                 for j in range(len(pointer)):
#                     A[i][pointer[j]] = A[i][pointer[j]]-A[k][pointer[j]]*keep
#                 B[i] = B[i]-B[k]*keep
# 
#     k = len(B)-1
#     while k >= 0:
#         result[k] = B[k]
#         if (k < len(B)-1):
#             for i in range(k+1,len(B)):
#                 result[k] = result[k]-A[k][i]*result[i]
#         result[k] = result[k]/A[k][k]
#         k -= 1
#     
#     return True,result
