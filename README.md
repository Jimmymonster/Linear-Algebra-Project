# Linear-Algebra-Project
## About this project
This project use bruteforce to solve traveling salesman problem to find the path. Then use that path to calculate and compare the best path you should go using pearson similarity and covariance matrix. The algorithm is O(n!) if the case is complete graph also you can't travel back to visited node. (Maybe I could use all pair shortest path algorithm to make this problem can travel back to visited node!!!
## STILL WORK IN PROGRESS
# Update!!!
TSP1.py use bruteforce to solve TSP and can't go back to visited node. Input data is adjacency matrix. Time complexity is O(n!) \
TSP2.py use dynamic programming and dijkstra to solve modified TSP that can go back to visited Node. Input data is adjacenct list. Time complexity is O(n^2 * 2^n)
