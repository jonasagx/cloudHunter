#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    CloudHunter -  cloud tracker based on satelites photos.
    Copyright (C) 2012, 2013 - Jonas Xavier

    This program is free software; you can redistribute it and/or
    modify it under the terms of the GNU General Public License
    as published by the Free Software Foundation; either version 2
    of the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
'''

import Image
import ImageOps
import numpy
import ImageFilter

class Point():
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    def __str__():
        return "%d %d %d" % self.x, self.y, self.z

def filtro(im_gray, mx, mi):
    '''Para valores dentre desses limites usa-se a cor 255(Branco) e para cores fora dos limtes 0(Preto)
    '''
    im_gray.flags.writeable = True
    for i in range( len(im_gray) ):
        for j in range( len(im_gray[0]) ):
            if( im_gray[i][j] < mi or im_gray[i][j] > mx):
                im_gray[i][j] = 0
            else:
                im_gray[i][j] = 255

def descript( im_gray, lim ):
    '''Descreve os objetos da imagem, no caso uma nuvem. É feita uma lista de listas para representar as nuvens, seus pontos, e suas coordenadas;
    '''
    im_gray.flags.writeable = True
    nuvens = []
    index = 0
    for i in range( len(im_gray) ):
        for j in range( len(im_gray[0]) ):
            if( im_gray[i][j] == 255 ):
                nuvens.append( [] )
                trackFill(i, j, im_gray, nuvens[index])
                index = index + 1

    n2 = [] # Novo vetor vazio para onde vão as nuvens filtradas

    '''Filtra os objetos menores que <lim> pontos.
    '''
    for i, value in enumerate(nuvens):
        n_points = len(value) 
        if n_points > lim:
            n2.append(value)
    nuvens = n2
    print "\tEncontradas %d nuvens nessa foto" % (len( nuvens ))
    return nuvens

def metadata( nuvens ):
    '''Descreve as nuvens em "metadados", um vetor
    de características:
        - N° de pontos;
        - Comprimento;
        - Largura;
        Retorna uma lista
    '''
    metadata = []
    for i in range( len(nuvens) ):
        dados = []
        widht = abs(max(nuvens[i])[0] - min(nuvens[i])[0]) + 1
        height = abs(max(nuvens[i])[1] - min(nuvens[i])[1]) + 1
        points = len(nuvens[i])
        ''' Armazenar o 'i' é útil para debbug;
            A área não precisa ser colocada na lista,
            pois pode ser facilmente calculada com widht e height
        '''
        metadata.append((points, widht, height))
    return metadata

def trackFill(i, j, im, stack):
    '''Algoritmo FloodFill implementado para seguir todos os pixels com um certo padrão de cor procurado. Recebe uma estrutura chamada stack, que armazena as nuvens e os pontos de cada nuvem.
    '''
    stack.append( [i, j] )

    im[i][j] = 0

    if ((j+1 < len(im[0]) ) and (im[i][j+1] == 255)):
        trackFill(i, j+1, im, stack)
    elif ((j-1 >= 0) and (im[i][j-1] == 255)):
        trackFill(i, j-1, im, stack)
    elif ((i-1 >= 0) and (im[i-1][j] == 255)):
        trackFill(i-1, j, im, stack)
    elif ((i+1 < len(im)) and (im[i+1][j] == 255)):
        trackFill(i+1, j, im, stack)
    else:
        return

def dWindow( metadata ):
    '''Desenha janela de cada nuvem
    '''
    m = numpy.zeros( shape=(500, 500), dtype = int)
    xMin, yMin = 0, 0
    for i in range( len(metadata) ):
        xMin = metadata[i][4][0]
        yMin = metadata[i][4][1]
        for j in range( metadata[i][2] ):
            for k in range( metadata[i][3] ):
                if xMin + j < len(m) and yMin + k < len(m[0]):
                    m[xMin + j][yMin + k] = 255
    return m

def  dilate( im ):
    '''Faz a dilatação de uma imagem.
    @im :  imagem (Image) a ser dilatada
    @k : máscara usada na dilatação
    '''
    k = (0, 255, 0, 255, 255, 255, 0, 255, 0)
    im = im.filter(ImageFilter.Kernel((3,3), k, scale=9))
    im = im.filter(ImageFilter.Kernel((3,3), k, scale=9))
#    im = im.filter(ImageFilter.Kernel((3,3), k, scale=9))

    return im

def drawPoint( hist ):
    '''Desenha pontos, que representam nuvens, numa imagem
    '''
    image = numpy.zeros( shape=(501, 522), dtype = int)

    for i in range( len(hist) ):
        image[ hist[i][4][0] ][ hist[i][4][1] ] = 255

    return Image.fromarray( numpy.uint8(image) )

def graph( metadados ):
    '''Cria o grafo relacionando nuvens de diferentes fotos.
    '''
    hist, m, index = [], 0, 0
    for i in range( len(metadados) ):
        for j in range( len(metadados[i]) ):
            if metadados[i][j][1] > m:
                m = metadados[i][j][1]
                index = j
        hist.append(metadados[i][index])
        print "Nuvem encontrada ", metadados[i][index]
    return hist

def track( metadados ):
	'''Relaciona nuvens de diferentes imagens a partir do cálculo de
	das diferenças quadráticas'''
	print "Relacionando nuvens"
	indexA, indexB, menorErro, i, j, somaErro = 0, 0, 0, 0, 0, 0.0
	hist = list()

	for i in range( len(metadados) ):
		for i in range( len(metadados[i]) - 1 ):
			somaErro += ( metadados[i][indeA] - metadados[i][j])
		if somaErro < menorErro:
			menorErro = somaErro
			indexB = i

def distance(pointA, pointB):
    '''Calcula a distência entre dois pontos dados pointA e pointB;'''
    pass

def minor_space(metadados):
    '''Conecta os pontos mais próximos entre si;'''
    for value_i, foto in enumerate(metadados):
        for value_j, nuvem in enumerate(foto):
            print nuvem, value_i, value_j
