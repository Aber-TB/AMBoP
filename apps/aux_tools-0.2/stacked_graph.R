library(ggplot2)
library(reshape2)
library(ggpubr)

#Read in the count table which has clade info and COG counts for the reference
dat <- read.delim("COG_count_table_per_sample_with_cladeinfo_and_ref.csv", 
                  check.names=FALSE, sep=",")

#Melt it into the correct format
dat1<- melt(dat, id=c("Samples", "Clade"))
#This 'melts' the data, turning it into a table like this:
#sample 1 group 1 variable 1 value 3
#sample 1 group 1 variable 2 value 1
#sample 2 group 1 variable 1 value 1
#sample 2 group 1 variable 2 value 5
#etc

#change data so that it's sum of all samples in the clade not per sample:
dat_per_clade <- aggregate(dat1$value, 
                           by = list(dat1$Clade, dat1$variable), 
                           FUN=sum)

#rename the columns so it's more apparent
names(dat_per_clade)[names(dat_per_clade) == "Group.1"] <- "Clade"
names(dat_per_clade)[names(dat_per_clade) == "Group.2"] <- "COG"

#Reshape them into a table to save:
dat_per_clade_tab <- dcast(dat_per_clade, Clade ~ COG, value.var = "x")
write.table(dat_per_clade_tab, 
            file = "COG_counts_per_clade.csv", 
            sep = ",", 
            row.names=FALSE)


#Assign colours (23 COG groups)
mycols <-c("navyblue", "lightskyblue1",   
           "chartreuse", "forestgreen", 
           "red1", "maroon",
           "yellow2", "moccasin", 
           "purple4", "magenta2", 
           "orange", "darkorange3", 
           "blue", "cyan3",
           "seagreen", "springgreen",
           "firebrick4", "coral1",
           "purple", "deeppink",
           "lemonchiffon", "gold1", 
           "azure4", "azure2")


#Make plot
stack<-ggplot(dat_per_clade, aes(x = Clade, y = x, fill = COG)) +
  geom_bar(position = "fill", stat = "identity") +
  scale_fill_manual(values = mycols)+
  guides(fill=guide_legend(title="COG group")) +
  #theme(axis.text.x = element_blank()) +
  labs(x = "Clades") +
  labs(y = "Percentage") +
  theme_bw() +
  scale_y_continuous(expand = c(0, 0.01), 
                     labels = scales::percent_format(accuracy = 1)) 

#Save figure
ggsave(plot=stack,"COGS_stackedgraph.png", device="png", dpi = 300)

