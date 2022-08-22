#!/usr/bin/env Rscrip
library("MOSAIC")

args = commandArgs(trailingOnly=TRUE)

## args[1] is .Rdata
# args[2] is ancestry number

load(args[1])

a = as.numeric(args[2])
fitcc=plot_coanccurves(acoancs,dr)
for (i in 1:a) {
    for (k in 1:a){
        message(target," ", fitcc$gens.matrix[i,k])
    }

}
