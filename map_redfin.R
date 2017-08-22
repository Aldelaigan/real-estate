# Alec Myres
# August 2017
# Redfin sale data mapping

# Packages needed
#install.packages("ggmap")
library(ggmap)

# Set path to folder with data file
setwd("~/Documents/Github/real-estate") 
dataSet <- read.csv("combined_results.csv")

# Histogram of days to sale
hist(dataSet$PRICE, xlab="Sale Prices", main="Histogram of UT Sales")

# Mapping of coordinates
dataSet$LOGPRICE = log(dataSet$PRICE)
len <- length(dataSet$LATITUDE)
mymarkers <- cbind.data.frame(lat  = (dataSet$LATITUDE),
                              lon  = (dataSet$LONGITUDE),
                              price = (dataSet$LOGPRICE),
                              size = rep("tiny", times = len),
                              col  = "red")
midPrice <- median(dataSet$LOGPRICE)                            
center <- c(median(dataSet$LONGITUDE), median(dataSet$LATITUDE) - .045)
hotmap <- get_map(location = center, zoom = 11)
hotmap <- ggmap(hotmap) + geom_point(data = mymarkers,
                                     aes(x = lon, y = lat, color = price),
                                     size = 1.5, alpha = 0.25,
                                     show.legend = FALSE) + 
          scale_color_gradient2(low="yellow", mid="orange", midpoint=midPrice, high="red", guide=FALSE)
