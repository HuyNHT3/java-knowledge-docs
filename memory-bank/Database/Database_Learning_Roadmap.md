# Database Roadmap for Senior Software Engineer

## 1. Database Fundamentals
- [ ] Database concepts
- [ ] Relational Database (RDBMS)
- [ ] NoSQL overview
- [ ] ACID properties
- [ ] CAP theorem (basic)
- [ ] Database architecture
- [ ] OLTP vs OLAP

---

## 2. SQL Fundamentals
- [ ] SELECT
- [ ] INSERT
- [ ] UPDATE
- [ ] DELETE
- [ ] WHERE
- [ ] ORDER BY
- [ ] GROUP BY
- [ ] HAVING
- [ ] DISTINCT
- [ ] LIMIT / OFFSET
- [ ] CASE
- [ ] COALESCE
- [ ] NULL handling

---

## 3. SQL Joins
- [ ] INNER JOIN
- [ ] LEFT JOIN
- [ ] RIGHT JOIN
- [ ] FULL JOIN
- [ ] CROSS JOIN
- [ ] SELF JOIN

---

## 4. Advanced SQL
### 4.1 Subqueries
- [ ] Scalar Subquery
- [ ] Correlated Subquery
- [ ] EXISTS
- [ ] NOT EXISTS
- [ ] IN
- [ ] ANY / ALL

### 4.2 Common Table Expressions (CTE)
- [ ] WITH
- [ ] Recursive CTE

### 4.3 Window Functions
- [ ] ROW_NUMBER()
- [ ] RANK()
- [ ] DENSE_RANK()
- [ ] NTILE()
- [ ] LAG()
- [ ] LEAD()
- [ ] FIRST_VALUE()
- [ ] LAST_VALUE()

### 4.4 Set Operations
- [ ] UNION
- [ ] UNION ALL
- [ ] INTERSECT
- [ ] EXCEPT

---

## 5. Data Modeling
- [ ] ER Diagram
- [ ] Entity Relationship
- [ ] Primary Key
- [ ] Foreign Key
- [ ] Candidate Key
- [ ] Composite Key
- [ ] Surrogate Key

---

## 6. Database Normalization
- [ ] 1NF
- [ ] 2NF
- [ ] 3NF
- [ ] BCNF
- [ ] Denormalization

---

## 7. Constraints
- [ ] PRIMARY KEY
- [ ] FOREIGN KEY
- [ ] UNIQUE
- [ ] CHECK
- [ ] DEFAULT
- [ ] NOT NULL
- [ ] ON DELETE CASCADE
- [ ] ON UPDATE CASCADE

---

## 8. Indexing
### Basic
- [ ] Clustered Index
- [ ] Non-clustered Index
- [ ] Unique Index
- [ ] Composite Index

### Advanced
- [ ] Covering Index
- [ ] Partial Index
- [ ] Function Index
- [ ] Bitmap Index
- [ ] Hash Index
- [ ] B-Tree
- [ ] GiST
- [ ] GIN

---

## 9. Query Optimization
- [ ] EXPLAIN
- [ ] EXPLAIN ANALYZE
- [ ] Execution Plan
- [ ] Full Table Scan
- [ ] Index Scan
- [ ] Bitmap Scan
- [ ] Nested Loop
- [ ] Merge Join
- [ ] Hash Join
- [ ] Query Cost
- [ ] Statistics

---

## 10. Transactions
- [ ] BEGIN
- [ ] COMMIT
- [ ] ROLLBACK
- [ ] SAVEPOINT
- [ ] ACID Review

---

## 11. Transaction Isolation
- [ ] Read Uncommitted
- [ ] Read Committed
- [ ] Repeatable Read
- [ ] Serializable

### Anomalies
- [ ] Dirty Read
- [ ] Non-repeatable Read
- [ ] Phantom Read

---

## 12. Concurrency Control
- [ ] Shared Lock
- [ ] Exclusive Lock
- [ ] Row Lock
- [ ] Table Lock
- [ ] Deadlock
- [ ] Deadlock Detection
- [ ] Lock Escalation

---

## 13. MVCC
- [ ] Snapshot
- [ ] Undo Log
- [ ] Version Chain
- [ ] Visibility Rules

---

## 14. Database Objects
- [ ] Views
- [ ] Materialized Views
- [ ] Stored Procedures
- [ ] Functions
- [ ] Triggers
- [ ] Sequences

---

## 15. Partitioning
- [ ] Range Partition
- [ ] List Partition
- [ ] Hash Partition
- [ ] Composite Partition

---

## 16. Replication
- [ ] Primary-Replica
- [ ] Synchronous Replication
- [ ] Asynchronous Replication
- [ ] Semi-sync Replication
- [ ] Replication Lag
- [ ] Read Replica

---

## 17. Sharding
- [ ] Horizontal Sharding
- [ ] Vertical Sharding
- [ ] Shard Key
- [ ] Rebalancing
- [ ] Cross-shard Query

---

## 18. Backup & Recovery
- [ ] Full Backup
- [ ] Incremental Backup
- [ ] Differential Backup
- [ ] Point-in-Time Recovery
- [ ] Binary Log
- [ ] WAL
- [ ] Disaster Recovery

---

## 19. Security
- [ ] SQL Injection
- [ ] Prepared Statement
- [ ] Parameterized Query
- [ ] Encryption at Rest
- [ ] Encryption in Transit
- [ ] User Roles
- [ ] Permissions
- [ ] Row Level Security

---

## 20. NoSQL
### Document
- [ ] MongoDB

### Key-Value
- [ ] Redis

### Wide Column
- [ ] Cassandra

### Graph
- [ ] Neo4j

### Concepts
- [ ] Eventual Consistency
- [ ] BASE
- [ ] CAP Theorem (advanced)

---

## 21. Caching
- [ ] Cache Aside
- [ ] Write Through
- [ ] Write Back
- [ ] Write Around
- [ ] TTL
- [ ] Cache Invalidation
- [ ] Cache Stampede
- [ ] Cache Penetration
- [ ] Cache Avalanche

---

## 22. Distributed Data
- [ ] Distributed Transactions
- [ ] Two Phase Commit (2PC)
- [ ] Saga Pattern
- [ ] Outbox Pattern
- [ ] CDC (Change Data Capture)
- [ ] Debezium

---

## 23. Performance Tuning
- [ ] Slow Query Log
- [ ] Connection Pool
- [ ] Prepared Statement Cache
- [ ] Batch Processing
- [ ] Bulk Insert
- [ ] Bulk Update

---

## 24. Monitoring
- [ ] CPU Usage
- [ ] Memory Usage
- [ ] Disk I/O
- [ ] QPS
- [ ] TPS
- [ ] Replication Delay
- [ ] Deadlock Monitoring
- [ ] Slow Query Dashboard

---

## 25. ORM (Java)
- [ ] Hibernate
- [ ] JPA
- [ ] Entity Lifecycle
- [ ] Lazy Loading
- [ ] Eager Loading
- [ ] N+1 Query Problem
- [ ] First-level Cache
- [ ] Second-level Cache
- [ ] Optimistic Locking
- [ ] Pessimistic Locking
- [ ] Fetch Strategies
- [ ] Batch Fetching

---

# Master Level (System Design Perspective)
- [ ] Choosing SQL vs NoSQL
- [ ] Database selection strategy
- [ ] Read/Write splitting
- [ ] Multi-region database
- [ ] High Availability
- [ ] Disaster Recovery
- [ ] Scalability strategies
- [ ] Event-driven data architecture
- [ ] Database migration strategy
- [ ] Zero-downtime migration
- [ ] Data consistency patterns
- [ ] Large-scale database design