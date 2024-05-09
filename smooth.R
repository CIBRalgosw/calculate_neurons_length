library(nat)

args <- commandArgs(trailingOnly = TRUE)

n = read.neuron(args[1])
smooth = smooth_neuron(n, sigma=as.numeric(args[2]))
write.neuron(smooth,args[3])