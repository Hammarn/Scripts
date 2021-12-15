setwd("/Users/rickardhammaren/test")
library(data.table)
fam = fread("kingunrelated.txt", sep = "\t", header= F)
library(dplyr)

new_df <- fam %>% group_by(V1) %>% slice_sample(n=30)
write.table(new_df, file="pygmy_30.fam", sep = " ", quote=FALSE, row.names = FALSE)


