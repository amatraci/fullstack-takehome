# Answers to Concept Questions

## 1. Complexity

Big-O, Big-Ω, and Big-Θ describe how an algorithm grows as the input size increases.

- **Big-O** gives an upper bound. It tells us the worst-case growth rate, or at least a limit the algorithm will not exceed asymptotically.
- **Big-Ω** gives a lower bound. It describes the best-case or minimum growth rate asymptotically.
- **Big-Θ** gives a tight bound. It means the algorithm grows at that exact asymptotic rate from both above and below.

In practice, `O(n log n)` is much more scalable than `O(n^2)`. For small inputs, the difference may not be dramatic, but as `n` becomes large, quadratic growth becomes expensive very quickly. For example, sorting algorithms like merge sort or heap sort are `O(n log n)`, while a simple nested-loop comparison approach is often `O(n^2)`. With large datasets, the `O(n log n)` solution will usually remain usable much longer.

That said, complexity alone is not the whole story. Constant factors, memory usage, and implementation details also matter. For very small inputs, an `O(n^2)` solution can sometimes be acceptable or even simpler. But for systems expected to scale, `O(n log n)` is generally the much safer choice.

---

## 2. Data Structures

I would choose a data structure based on the access pattern, update pattern, and performance requirements.

### Array / List
I would use an array or list when I need fast indexed access and the data is stored in sequence. It is a strong default choice when reads by position are common.

**Trade-off:** inserting or deleting elements in the middle can be expensive because other elements may need to shift.

### Linked List
I would choose a linked list when I expect frequent insertions and deletions, especially if they happen near known positions and I do not need fast random access.

**Trade-off:** random access is slow because elements must be traversed one by one.

### Hash Map
I would use a hash map when I need very fast lookup by key, such as caching, indexing by ID, or counting frequencies.

**Trade-off:** it does not preserve order naturally, and performance depends on a good hash function and collision handling.

### Tree
I would choose a tree when I need ordered data, hierarchical data, or efficient range queries. Balanced trees are useful when I need sorted inserts, deletes, and lookups.

**Trade-off:** trees are more complex than arrays or hash maps, and they usually have higher overhead in both implementation and memory.

---

## 3. Immutability & State

Mutable data can be changed after it is created. Immutable data cannot.

For example, if an object is mutable, one part of the program can change it and other parts will observe that new state. If it is immutable, its value stays stable and any “change” requires creating a new value instead.

Immutability simplifies reasoning because it reduces surprise. A function receiving immutable input can trust that the value will not change unexpectedly somewhere else. This makes code easier to debug, easier to test, and easier to reason about over time.

It is also helpful in concurrency. Shared mutable state is one of the main sources of race conditions. If data is immutable, multiple threads or processes can read it safely without locks, because nobody can change it underneath them. That does not remove every concurrency problem, but it greatly reduces a major class of bugs.

In practice, I usually prefer immutability for shared state, configuration, messages, and values that do not need in-place updates. Mutable state is still useful, but I try to keep it local and controlled.

---

## 4. Memory Model

The **stack** and the **heap** are two different memory areas used by programs.

The **stack** is typically used for function call frames, local variables, and control flow. It is usually very fast, automatically managed, and has a clear lifetime tied to function execution.

The **heap** is used for dynamically allocated memory. Objects stored there can outlive a single function call and have more flexible lifetimes, but allocation and deallocation are generally more expensive.

### Scope vs Lifetime
- **Scope** means where in the program a variable can be accessed.
- **Lifetime** means how long the variable or object exists in memory.

A local variable inside a function usually has limited scope and a short lifetime tied to that function call. Heap-allocated objects may have a wider useful lifetime, depending on references and memory management.

In higher-level languages like Python, developers do not manage stack and heap directly in the same way as in C or C++, but the conceptual distinction still matters. Understanding lifetime and allocation helps explain performance, memory usage, and why some objects remain alive longer than expected.

---

## 5. OOP Basics

### Encapsulation
Encapsulation means bundling data and behavior together and controlling access to internal state. In practice, this means exposing a clean public interface and hiding unnecessary implementation details.

### Inheritance
Inheritance allows one class to reuse or extend the behavior of another. It is useful when there is a genuine “is-a” relationship.

### Polymorphism
Polymorphism means different objects can be used through the same interface while providing different implementations. For example, two different classes can implement the same method name but behave differently.

### When composition is preferable to inheritance
Composition is often better when I want flexibility and loose coupling. Instead of forcing a class hierarchy, I can build behavior by combining smaller objects. This makes the system easier to change and reduces the risk of deep inheritance trees that are hard to maintain.

I generally prefer composition when behavior may vary, when relationships are not truly hierarchical, or when reuse is better expressed as “has-a” rather than “is-a”.

---

## 6. APIs & Contracts

An **idempotent API operation** is one that can be repeated multiple times with the same effect as performing it once.

For example:
- `GET /users/123` is idempotent because calling it repeatedly does not change the resource.
- `PUT /users/123` is typically idempotent because replacing the resource with the same payload multiple times leads to the same final state.
- `POST /users` is usually **not** idempotent because each call may create a new resource.

This matters because idempotent operations are safer for retries. In distributed systems, timeouts and network failures happen. If the client retries an idempotent request, the result is predictable. If the operation is non-idempotent, retries can accidentally duplicate actions such as charges, orders, or records.

So, a common HTTP comparison is:
- **Idempotent:** `GET`, usually `PUT`, often `DELETE`
- **Non-idempotent:** usually `POST`

---

## 7. Concurrency vs Parallelism

**Concurrency** means multiple tasks are in progress during overlapping periods of time. It is about coordinating many tasks efficiently, even if they are not literally executing at the exact same instant.

**Parallelism** means multiple tasks are executing at the same time, usually on different CPU cores or workers.

So, concurrency is more about structure and coordination, while parallelism is about actual simultaneous execution.

### Race conditions
A race condition happens when the outcome depends on the timing or ordering of operations on shared state. This can lead to inconsistent or incorrect results.

### Deadlocks
A deadlock happens when two or more threads or processes wait on each other indefinitely, so none of them can continue.

### Mitigation
To reduce these problems, I would:
- minimize shared mutable state
- use immutable data where possible
- use locks carefully and consistently
- enforce lock ordering to avoid deadlocks
- prefer message passing or queues instead of direct shared state
- keep critical sections small

In many systems, good design reduces the need for heavy synchronization in the first place.

---

## 8. Databases

I would choose **SQL** when:
- data is relational
- consistency is important
- transactions matter
- joins and strong schemas are valuable

I would choose **NoSQL** when:
- schema flexibility is important
- horizontal scalability is a priority
- the access patterns are simpler
- I want to optimize for large volumes of semi-structured or distributed data

### Indexes
Indexes are data structures that make lookups faster, especially for filtering, joins, and sorting on frequently queried fields.

### How indexes help
Indexes can improve read performance significantly because the database does not need to scan every row.

### How indexes hurt
Indexes also have a cost:
- they consume storage
- they slow down writes, because inserts, updates, and deletes must also update the index
- too many indexes can confuse optimization and increase maintenance overhead

So I would add indexes based on actual query patterns, not automatically on every field.

---

## 9. Testing

### Unit tests
Unit tests verify small, isolated pieces of logic, such as a single function or class method. They are fast and helpful for catching logic bugs early.

### Integration tests
Integration tests verify that components work together correctly, for example API + database, or service + queue.

### End-to-end tests
End-to-end tests validate the full workflow from the user’s perspective. They are the closest to real usage, but they are usually slower and more fragile.

### When to mock
I would mock when:
- the dependency is external
- the dependency is slow
- the dependency is expensive or non-deterministic
- I want to isolate the unit under test

Examples include payment providers, email services, third-party APIs, or background infrastructure.

### Risks of over-mocking
Over-mocking can make tests unrealistic. A test can pass because the mocks are too idealized, while the real integration still fails. Too many mocks can also lock tests too tightly to implementation details instead of behavior.

So I try to keep a balance:
- unit tests with mocks where appropriate
- integration tests for real interactions
- a smaller number of end-to-end tests for confidence in the full flow

---

## 10. Version Control

### Merge
A merge combines branches and preserves the full history, including the branch structure. It is straightforward and safe for shared branches.

### Rebase
A rebase rewrites commits onto a new base, creating a cleaner and more linear history. It can make commit history easier to read.

### When I would favor one over the other
I would use **rebase** when working on my own local feature branch and I want to clean up the history before merging. It keeps the commit history linear and easier to follow.

I would use **merge** when working on shared branches or when preserving the exact history of collaboration matters. Merge is safer when commits have already been pushed and used by others, because rebasing shared history can create confusion.

In general:
- **Rebase** for clean local history
- **Merge** for preserving collaboration history safely

I focused on keeping the implementation clean, readable, and easy to run locally, while still showing how the system could scale in a real-world scenario.
