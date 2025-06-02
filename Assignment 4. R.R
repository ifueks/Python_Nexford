install.packages("ggplot2")
library(ggplot2)
genre_data <- read.csv("C:/Users/eliri/Downloads/genre_counts.csv", header=TRUE)

# Rename columns 
colnames(genre_data) <- c("Genre", "Count")

# Plot
ggplot(genre_data, aes(x=reorder(Genre, Count), y=Count)) +
  geom_col(fill="steelblue") +
  coord_flip() +
  labs(title="Top 10 Most Frequent Genres on Netflix",
       x="Genre",
       y="Number of Titles") +
  theme_minimal()
