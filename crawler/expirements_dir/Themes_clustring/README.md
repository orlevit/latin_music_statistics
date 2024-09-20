# Theme Clustering Attempts Analysis
## Number of Clusters
After analyzing the data, I determined that the optimal number of clusters is 20. While this configuration exhibits high frequencies in only a few themes with a long tail, the clusters at the beginning (high frequency) tend to be overly broad and general. In contrast, the clusters at the end are often too specific. The clusters positioned in the center offer a better balance between specificity and generality.

To refine the approach, I opted for iterative clustering. This method involves eliminating smaller clusters (those representing less than 2.5% of the data) and reapplying the clustering algorithm to achieve a more concise set of themes.

#### Iterative Clustering Results
Through iterative clustering, I observed a slight increase in specificity; however, this improvement came at the cost of discarding a significant amount of data (see the "Iterative Clustering" directory for details).

#### Selected Approach
In the final clustering strategy, I consolidated all clusters with less than 2.5% of the data into a single "Miscellaneous" category. This helps streamline the analysis and improves the relevance of the remaining clusters. Additionally, the specific artist clustering is significantly smaller, as each artist is associated with fewer samples. This leads to a high number of clusters, which results in overly specific themes.

## Matching Each Song to a Cluster
#### Clustering Embeddings
I employed several models for generating embeddings, including:

"all-MiniLM-L6-v2"
"bert-base-uncased"
"roberta-base"
OpenAI's "text-embedding-3-small" and "text-embedding-3-large"

#### Results
The initial clustering results indicated a high proportion of unsuitable samples.
To enhance accuracy, I decided to consult ChatGPT for insights on the general themes associated with each song.
This approach achieved more suitable cluster assignments.

