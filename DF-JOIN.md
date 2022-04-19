# Dataframe join

There are 2 dataframes: df01, df02 with the following schemas:

**df01**
```
root
|— user_id: string
|— feature_1: long
|— feature_2: long
|— feature_3: long
```

**df02**
```
root
|— user_id: string
|— feature_4: long
|— feature_5: long
```

Assuming there is no duplicates on user_id on the two dataframes i.e.
```python
df01.count()= df01.select("user_id").distinct().count()
df02.count() = df02.select("user_id").distinct().count()
```
and assuming that df01 and df02 both have N rows.

## Complexity of join
```python
df01.join(df02, "user_id")
```
In Spark, there are several kinds of join:
- Shuffle sort-merge join
- Shuffle hash join
- Broadcast hash join
- Broadcast nested loop join

### Shuffle sort-merge join
This is the default join strategy in Spark. The join key ("user_id") needs to be sortable. It has 3 phases:
- Shuffle phase: shuffling of data to get the same join key with the same worker.
- Sort phase: sorting the data within each partition.
- Merge phase: merging the sorted and partitioned data by iterating over the elements and joining the rows having the same value for the join key

**So the complexity is O(N log N + N log N).**

### Shuffle hash join
The join key does not need to be sortable. It has 2 phases:
- Shuffle phase: moving data with the same value of join key in the same executor node.
- Hash join phase: creating a hash table based on the join key of smaller dataframe, then looping over larger dataframe to match the hashed join key values.

The cost to build a hash map is less than sorting the data, but maintaining a hash table requires memory and computation.

**The complexity is O(N + N).**

### Broadcast hash join
When one of the dataframes is small and fits in the memory, it will be broadcasted to all the executors, and a hash join will be performed.

It saves shuffling cost. But copy of the small dataframe is broadcasted over the network, so it could be a network-intensive operation.

**The complexity is O(N + N).**

### Broadcast nested loop join
It is a nested loop comparison of the both dataframe.

Different from above three types of join, broadcast nested loop join supports non-equi-joins ('≤=', '<', etc.) beside equi-joins ('=')

**The complexity is O(N ^ 2).**

## Optimize the join operation more efficiently
There are many things to consider when choosing a join strategy, such as dataframes' sizes, numbers of partitions, numbers of executors, numbers of unique join keys, .etc

e.g. if Spark driver and executors have enough memory to accommodate the df02, we can use broadcast hash join by a below hint
```python
join_df = df01.join(broadcast(df02), "user_id", "inner")
```