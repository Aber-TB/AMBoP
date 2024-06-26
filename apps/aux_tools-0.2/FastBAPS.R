################################################################################
                       #FASTBAPS
################################################################################

library(fastbaps)
library(ggtree)
library(phytools)
library(ggplot2)

#Load in an alignment of SNPs in fasta format

fasta.file <- system.file("snp_sites.aln", package = "fastbaps")

sparse.data <- import_fasta_sparse_nt("snp_sites.aln")

#Then calculate an optimised prior that can be added to the sparse data file.

  #this empirically chooses the variance of the Dirichlet prior on the component 
  #mixtures.
  #Can change type to "baps"= unoptimised symmetric, or "hc" this is the BHC  
  #algorithm of Heller et al.

sparse.data <- optimise_prior(sparse.data, type = "optimise.symmetric")

#Then run the BAPS hierarchical clustering

  #k.init is initial number of clusters to start the Bayesian clustering from. 
  #By default this is no of seq/4 - it should be larger than number of clusters 
  #expected.

  #hc.method can either be "ward" or "genie"

baps.hc <-fast_baps(sparse.data, k.init=NULL, hc.method = "ward")

#Then partition the clustering data  

best.partition <- best_baps_partition(sparse.data, baps.hc)

#Then plot the output onto a tree

  #First import the pre-computed tree file in Newick format

iqtree <- phytools::read.newick("newick.txt")
plot.df <- data.frame(id = colnames(sparse.data$snp.matrix), 
                      fastbaps = best.partition, stringsAsFactors = FALSE)
gg <- ggtree(iqtree)

#Add tip labels to the figure:

gg <- ggtree(iqtree) + geom_tiplab()

#Then plot BAPs against the imported tree

f2 <- facet_plot(gg, 
                 panel = "fastbaps", 
                 data = plot.df, 
                 geom = geom_tile, 
                 aes(x = fastbaps), 
                 color = "black", 
                 fill = "cadetblue3")

# 2 levels of BAPS:

multi <- multi_res_baps(sparse.data)

plot.df <- data.frame(id = colnames(sparse.data$snp.matrix), 
                      fastbaps = multi$`Level 1`,  
                      fastbaps2 = multi$`Level 2`, 
                      stringsAsFactors = FALSE)

gg <- ggtree(iqtree)

f2 <- facet_plot(gg, 
                 panel = "fastbaps level 1", 
                 data = plot.df, 
                 geom = geom_tile, 
                 aes(x = fastbaps), 
                 color = "black", 
                 fill = "cadetblue3")
f2 <- facet_plot(f2, 
                 panel = "fastbaps level 2", 
                 data = plot.df, 
                 geom = geom_tile, 
                 aes(x = fastbaps2), 
                 color = "black", 
                 fill = "darkolivegreen2")


###############################################################################
           			#GENETIC DISTANCES- matrix and heatmap#
###############################################################################

library(pheatmap)
library(ape)
library(adegenet)
library(reshape2)
library(phytools)
library(ggtree)

#Convert alignment fasta file to DNAbin
  #fasta file needs to be saved as a .fas

BINfile <- fasta2DNAbin("fasta.fas")

##then calculate distance matrix
      # model can be: "raw", "N", "TS", "TV", "JC69", "K80" (the default), 
      #"F81", "K81", "F84", "BH87", "T92", "TN93", "GG95", "logdet", "paralin", 
      #"indel", or "indelblock"

distance_matrix <- dist.dna (BINfile, model= "N",  variance = FALSE,
          gamma = FALSE, pairwise.deletion = FALSE,
          base.freq = NULL, as.matrix = TRUE)

#Load in tree and convert it to a dendrogram format

iqtree <- phytools::read.newick("newick.txt")

#Convert tree to dendrogram but first test if tree is ultrametric:

is.ultrametric(iqtree)

  #if not ultrametric, then convert it: 

dendogram <-chronos(iqtree)
hc <- as.hclust.phylo(dendogram)

#Order distance matrix so it corresponds to tree labels:
ord.mat <- distance_matrix[hc$label, hc$label]

#Then make heatmap 
heatmap <-pheatmap(ord.mat, 
                   cluster_rows=hc, 
                   cluster_cols =hc, 
                   treeheight_col = 100, 
                   treeheight_row = 100, 
                   show_colnames= F, 
                   show_rownames = F)