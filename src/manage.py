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

from utils import *
import sys
import time
import Image
import numpy
import ImageOps

def main():
    '''Abre uma sequência de imagens e transforma cada uma dalas.
    '''

    assert len(sys.argv) > 1, ("Passe alguma imagem, no formato" +
    " .png, como parâmetro na chamado do programa.")

    imList, im = [], []

    try:
        for i in range(1, len(sys.argv), 1):
            imList.append( Image.open(sys.argv[i]) )
    except Exception, e:
        print "Erro ao abrir arquivo ", e

    print "Quantidade de imagens lidas:\t %d" % ( len(sys.argv) - 1 )

    print "Cortando as imagens"
    for i in range( len(imList) ):
        imList[i] = imList[i].crop( (0, 22, 500, 521) )
        #print imList[i]

    print "Convertendo para cinza"
    for i, value in enumerate(imList):
        imList[i] = ImageOps.grayscale(imList[i])
        im.append(numpy.asarray(imList[i]))

    print "Filtrando cores"
    for i in im:
        filtro( i, 90, 80 )

    #Opcional
    print "Dilatando nuvens acontradas"
    for i, value in enumerate(im):
        image = Image.fromarray(im[i])
        image.save("pre_dilate.png", "PNG")
        dilate(image).save("after_dilate.png", "PNG")
        im[i] = numpy.asarray(image)

    nuvens = []
    print "Descrevendo cada imagem"
    for i, value in enumerate(im):
        print "\t", i+1,
        nuvens.append( descript(im[i], 20) )
    del im

    metadados = list()
    print "Buscando metadados de cada nuvem"
    for i in range( len(nuvens) ):
        metadados.append( metadata(nuvens[i]) )
#    minor_space(metadados)

    f = open("nuvens.csv", "w")
    f.write("np;l;c\n")
    for nuvens in metadados:
        for nuvem in nuvens:
            f.write("%d;%d;%d\n" % (nuvem[0], nuvem[1], nuvem[2]))
    f.close()
#    return metadados

if __name__ == "__main__":
    #print "Running ..."
    start = time.time()
    main()
    end = time.time()
    print "Time running: %.3fs" % ( end - start )
