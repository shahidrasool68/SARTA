"""Curated question bank for common Job Description (JD) technical topics.

Covers key JD technologies:
- Python (core syntax, memory model, concurrency, async, data structures)
- SQL (relational algebra, indexing, transactions/ACID, window functions, query tuning)
- React (hooks, reconciliation, lifecycle, state management, suspense)
- Data Structures (arrays, lists, trees, graphs, hashing, complexity)
- Machine Learning (loss functions, regularization, metrics, transformers, gradient descent)
- Docker (images, container lifecycle, networks, multi-stage builds, orchestration)
- JavaScript (closures, prototypes, event loop, promises, ES6+)
"""

JD_QUESTION_BANK = {
    "Python": {
        "Easy": [
            {
                "question": "What is the output of `type([])` in Python 3?",
                "options": ["<class 'list'>", "<class 'array'>", "<class 'dict'>", "<class 'tuple'>"],
                "correct_answer": "<class 'list'>",
                "difficulty_score": 1.5
            },
            {
                "question": "Which keyword is used to define a function in Python?",
                "options": ["def", "func", "function", "lambda"],
                "correct_answer": "def",
                "difficulty_score": 1.0
            },
            {
                "question": "What is the result of `bool([])` and `bool([0])` in Python?",
                "options": ["False and True", "True and False", "False and False", "True and True"],
                "correct_answer": "False and True",
                "difficulty_score": 2.0
            },
            {
                "question": "Which built-in Python data type is immutable?",
                "options": ["tuple", "list", "dict", "set"],
                "correct_answer": "tuple",
                "difficulty_score": 1.5
            },
            {
                "question": "What does the expression `'hello'[::-1]` evaluate to?",
                "options": ["'olleh'", "'hello'", "SyntaxError", "IndexError"],
                "correct_answer": "'olleh'",
                "difficulty_score": 2.5
            },
            {
                "question": "How are variable keyword arguments collected into a function signature in Python?",
                "options": ["**kwargs", "*args", "kwargs[]", "&kwargs"],
                "correct_answer": "**kwargs",
                "difficulty_score": 2.0
            }
        ],
        "Medium": [
            {
                "question": "What is the average time complexity of looking up a key in a Python dictionary?",
                "options": ["O(1)", "O(log n)", "O(n)", "O(n log n)"],
                "correct_answer": "O(1)",
                "difficulty_score": 4.5
            },
            {
                "question": "What does a generator function return when invoked?",
                "options": ["A generator iterator object", "A list containing all yield values", "None", "The first yielded value"],
                "correct_answer": "A generator iterator object",
                "difficulty_score": 5.0
            },
            {
                "question": "In Python list comprehensions, what is the primary benefit over a traditional `for` loop with `.append()`?",
                "options": [
                    "Faster execution because the bytecode uses specialized C-level list creation (LIST_APPEND)",
                    "List comprehensions run in parallel across multiple CPU cores",
                    "List comprehensions consume zero heap memory",
                    "They allow modifying variables outside their scope automatically"
                ],
                "correct_answer": "Faster execution because the bytecode uses specialized C-level list creation (LIST_APPEND)",
                "difficulty_score": 5.5
            },
            {
                "question": "What is the difference between `is` and `==` in Python?",
                "options": [
                    "`is` checks for object identity (memory address); `==` checks for value equality",
                    "`==` checks for identity; `is` checks for equality",
                    "They are identical and interchangeable in modern Python",
                    "`is` can only be used with numeric types"
                ],
                "correct_answer": "`is` checks for object identity (memory address); `==` checks for value equality",
                "difficulty_score": 4.0
            },
            {
                "question": "How does the `__slots__` attribute optimize a Python class?",
                "options": [
                    "Replaces the per-instance `__dict__` with a fixed-size array, drastically reducing memory overhead",
                    "Enables multi-threading without the GIL",
                    "Automatically caches method return values in memory",
                    "Makes all class attributes private"
                ],
                "correct_answer": "Replaces the per-instance `__dict__` with a fixed-size array, drastically reducing memory overhead",
                "difficulty_score": 6.5
            },
            {
                "question": "What happens when you pass a mutable default argument (like `def fn(items=[])`) in Python?",
                "options": [
                    "The default list is created once at function definition time and mutated across subsequent calls",
                    "A new empty list is created every time the function is called",
                    "Python raises a `TypeError` at compile time",
                    "The list is reset to empty after every invocation"
                ],
                "correct_answer": "The default list is created once at function definition time and mutated across subsequent calls",
                "difficulty_score": 5.5
            }
        ],
        "Hard": [
            {
                "question": "How does Python's GIL (Global Interpreter Lock) affect multi-threaded CPU-bound programs on multi-core CPUs?",
                "options": [
                    "Prevents true parallel byte-code execution across cores",
                    "Distributes threads automatically across physical cores",
                    "Doubles the execution speed via thread-level parallelism",
                    "Disables memory garbage collection during threading"
                ],
                "correct_answer": "Prevents true parallel byte-code execution across cores",
                "difficulty_score": 8.0
            },
            {
                "question": "In Python metaclasses, which method is invoked to allocate the new class instance before `__init__`?",
                "options": ["__new__", "__call__", "__prepare__", "__build__"],
                "correct_answer": "__new__",
                "difficulty_score": 8.5
            },
            {
                "question": "In Python's `asyncio` event loop, what occurs when a blocking synchronous call (e.g. `time.sleep(5)`) is executed inside an `async def` coroutine?",
                "options": [
                    "It blocks the entire event loop thread, preventing all other scheduled coroutines from running",
                    "Asyncio automatically offloads it to a background thread pool",
                    "The event loop raises an `AsyncBlockedException`",
                    "The coroutine yields execution automatically via cooperative multitasking"
                ],
                "correct_answer": "It blocks the entire event loop thread, preventing all other scheduled coroutines from running",
                "difficulty_score": 8.5
            },
            {
                "question": "What is the Method Resolution Order (MRO) algorithm used by Python 3 for multiple inheritance?",
                "options": ["C3 Linearization algorithm", "Depth-First Search (DFS)", "Breadth-First Search (BFS)", "Dijkstra's Algorithm"],
                "correct_answer": "C3 Linearization algorithm",
                "difficulty_score": 9.0
            },
            {
                "question": "How does CPython's cyclic garbage collector detect circular references that cannot be freed by standard reference counting?",
                "options": [
                    "It isolates container objects in generation lists and simulates decrementing their reference counts to find unreachable subgraphs",
                    "It periodically scans all physical RAM for dangling pointers",
                    "It pauses execution and re-reads the source AST",
                    "Circular references are never freed in CPython and cause permanent memory leaks"
                ],
                "correct_answer": "It isolates container objects in generation lists and simulates decrementing their reference counts to find unreachable subgraphs",
                "difficulty_score": 9.5
            },
            {
                "question": "In Python descriptor protocol, what differentiates a 'data descriptor' from a 'non-data descriptor'?",
                "options": [
                    "A data descriptor implements both `__get__` and `__set__` (or `__delete__`); it takes precedence over an instance's `__dict__`",
                    "A data descriptor only works with primitive types like integers and strings",
                    "Non-data descriptors can only be invoked asynchronously",
                    "Data descriptors cannot access `self`"
                ],
                "correct_answer": "A data descriptor implements both `__get__` and `__set__` (or `__delete__`); it takes precedence over an instance's `__dict__`",
                "difficulty_score": 9.0
            }
        ]
    },
    "SQL": {
        "Easy": [
            {
                "question": "Which SQL clause is used to filter rows returned by a SELECT query?",
                "options": ["WHERE", "ORDER BY", "GROUP BY", "HAVING"],
                "correct_answer": "WHERE",
                "difficulty_score": 1.0
            },
            {
                "question": "Which SQL command is used to remove all records from a table without logging individual row deletions?",
                "options": ["TRUNCATE TABLE", "DELETE FROM", "DROP TABLE", "REMOVE ALL"],
                "correct_answer": "TRUNCATE TABLE",
                "difficulty_score": 2.5
            },
            {
                "question": "Which constraint uniquely identifies each record in a database table?",
                "options": ["PRIMARY KEY", "FOREIGN KEY", "UNIQUE", "CHECK"],
                "correct_answer": "PRIMARY KEY",
                "difficulty_score": 1.5
            },
            {
                "question": "What is the default sorting order when using the `ORDER BY` clause in SQL?",
                "options": ["ASC (Ascending)", "DESC (Descending)", "Random", "Table insertion order"],
                "correct_answer": "ASC (Ascending)",
                "difficulty_score": 1.0
            },
            {
                "question": "Which SQL aggregate function returns the total count of non-null values in a specified column?",
                "options": ["COUNT(column_name)", "SUM(column_name)", "TOTAL(column_name)", "ROW_COUNT()"],
                "correct_answer": "COUNT(column_name)",
                "difficulty_score": 2.0
            },
            {
                "question": "Which SQL operator is used to search for a specified pattern in a column?",
                "options": ["LIKE", "BETWEEN", "IN", "MATCHES"],
                "correct_answer": "LIKE",
                "difficulty_score": 1.5
            }
        ],
        "Medium": [
            {
                "question": "What is the primary difference between WHERE and HAVING clauses in SQL?",
                "options": [
                    "WHERE filters individual rows before grouping; HAVING filters aggregated groups after GROUP BY",
                    "WHERE operates only on indexed columns; HAVING operates on unindexed columns",
                    "HAVING is used exclusively with subqueries",
                    "There is no difference; they are interchangeable aliases"
                ],
                "correct_answer": "WHERE filters individual rows before grouping; HAVING filters aggregated groups after GROUP BY",
                "difficulty_score": 5.0
            },
            {
                "question": "What does a LEFT OUTER JOIN return?",
                "options": [
                    "All rows from the left table, plus matched rows from the right table (with NULLs where no match exists)",
                    "Only rows that match in both tables",
                    "All rows from the right table, plus matched rows from the left table",
                    "The Cartesian product of both tables"
                ],
                "correct_answer": "All rows from the left table, plus matched rows from the right table (with NULLs where no match exists)",
                "difficulty_score": 4.5
            },
            {
                "question": "What is a database transaction's ACID property that guarantees changes persist even after a system crash?",
                "options": ["Durability", "Atomicity", "Consistency", "Isolation"],
                "correct_answer": "Durability",
                "difficulty_score": 4.0
            },
            {
                "question": "How does a B-Tree index accelerate SQL query performance?",
                "options": [
                    "Keeps keys in sorted order to allow binary search in O(log N) disk block accesses",
                    "Compresses entire tables into gzip format",
                    "Converts relational tables into in-memory hash tables only",
                    "Pre-executes every possible SQL query at server startup"
                ],
                "correct_answer": "Keeps keys in sorted order to allow binary search in O(log N) disk block accesses",
                "difficulty_score": 6.0
            },
            {
                "question": "What is the purpose of a Database View in SQL?",
                "options": [
                    "A virtual table based on the result-set of a SQL statement that simplifies complex queries and enhances security",
                    "A physical copy of the table stored on a separate backup server",
                    "A temporary cache stored on the client browser",
                    "An index that automatically partitions large tables"
                ],
                "correct_answer": "A virtual table based on the result-set of a SQL statement that simplifies complex queries and enhances security",
                "difficulty_score": 5.0
            },
            {
                "question": "What is a 'correlated subquery' in SQL?",
                "options": [
                    "A subquery that references columns from the outer query, evaluated once for each row processed by the outer query",
                    "A subquery that executes once independently before the outer query runs",
                    "A subquery that joins two identical tables on their primary keys",
                    "A recursive Common Table Expression (CTE)"
                ],
                "correct_answer": "A subquery that references columns from the outer query, evaluated once for each row processed by the outer query",
                "difficulty_score": 6.5
            }
        ],
        "Hard": [
            {
                "question": "How does the window function DENSE_RANK() differ from RANK() in SQL when handling tied values?",
                "options": [
                    "DENSE_RANK does not skip subsequent ranking numbers after ties; RANK leaves gaps",
                    "RANK does not skip numbers; DENSE_RANK leaves gaps",
                    "DENSE_RANK only works with partitioned tables",
                    "RANK can only be used with numeric sorting"
                ],
                "correct_answer": "DENSE_RANK does not skip subsequent ranking numbers after ties; RANK leaves gaps",
                "difficulty_score": 8.0
            },
            {
                "question": "Under ANSI SQL transaction isolation levels, what phenomenon is prevented by 'SERIALIZABLE' that 'REPEATABLE READ' allows in standard implementations?",
                "options": [
                    "Phantom Reads",
                    "Dirty Reads",
                    "Non-Repeatable Reads",
                    "Dirty Writes"
                ],
                "correct_answer": "Phantom Reads",
                "difficulty_score": 8.5
            },
            {
                "question": "What is a 'covering index' in SQL optimization?",
                "options": [
                    "An index that contains all columns required by a query, allowing the database engine to satisfy the query entirely from the index without reading table pages (index-only scan)",
                    "An index that covers all tables in a schema simultaneously",
                    "An index that automatically encrypts table data at rest",
                    "A clustered index placed on every foreign key"
                ],
                "correct_answer": "An index that contains all columns required by a query, allowing the database engine to satisfy the query entirely from the index without reading table pages (index-only scan)",
                "difficulty_score": 9.0
            },
            {
                "question": "In PostgreSQL and MySQL (InnoDB), how does Multi-Version Concurrency Control (MVCC) achieve lock-free consistent reads?",
                "options": [
                    "By storing row versions with creation and expiration transaction IDs (xmin/xmax or undo log records), enabling readers to view snapshots without blocking writers",
                    "By locking entire tables with exclusive row locks for all transactions",
                    "By aborting all concurrent transactions and retrying them sequentially",
                    "By moving modified records to Redis in real time"
                ],
                "correct_answer": "By storing row versions with creation and expiration transaction IDs (xmin/xmax or undo log records), enabling readers to view snapshots without blocking writers",
                "difficulty_score": 9.5
            },
            {
                "question": "In query execution plans, when is a Hash Join preferred over a Nested Loop Join by the query optimizer?",
                "options": [
                    "When joining large, unsorted datasets without relevant indexes on the join predicate",
                    "When the outer table has only 1 row and has an indexed primary key",
                    "When the query contains an `ORDER BY` clause on the inner table",
                    "When executing full-text search queries"
                ],
                "correct_answer": "When joining large, unsorted datasets without relevant indexes on the join predicate",
                "difficulty_score": 8.5
            },
            {
                "question": "What is the primary trade-off of Table Partitioning (range, list, or hash) in high-throughput databases?",
                "options": [
                    "Improves query pruning on partition keys, but cross-partition queries and global index maintenance become more expensive",
                    "Eliminates the need for transaction logging completely",
                    "Guarantees sub-millisecond latency for all queries regardless of WHERE clause",
                    "Disables ACID constraints for improved write speeds"
                ],
                "correct_answer": "Improves query pruning on partition keys, but cross-partition queries and global index maintenance become more expensive",
                "difficulty_score": 8.0
            }
        ]
    },
    "React": {
        "Easy": [
            {
                "question": "Which React hook is used to manage local component state in functional components?",
                "options": ["useState", "useEffect", "useMemo", "useContext"],
                "correct_answer": "useState",
                "difficulty_score": 1.0
            },
            {
                "question": "What is JSX in the React ecosystem?",
                "options": [
                    "A syntax extension for JavaScript that looks similar to HTML and compiles to React.createElement calls",
                    "A standalone database query language for React",
                    "A CSS preprocessor built into Vite",
                    "A replacement for TypeScript"
                ],
                "correct_answer": "A syntax extension for JavaScript that looks similar to HTML and compiles to React.createElement calls",
                "difficulty_score": 1.5
            },
            {
                "question": "How are properties (props) passed from a parent component to a child component in React?",
                "options": [
                    "As attributes in the JSX tag (<Child title='Hello' />)",
                    "Via global browser cookies",
                    "By calling `window.setProp()`",
                    "Props can only be shared via Redux"
                ],
                "correct_answer": "As attributes in the JSX tag (<Child title='Hello' />)",
                "difficulty_score": 1.0
            },
            {
                "question": "Which hook is used to perform side effects (such as data fetching or subscriptions) in React functional components?",
                "options": ["useEffect", "useState", "useRef", "useCallback"],
                "correct_answer": "useEffect",
                "difficulty_score": 2.0
            },
            {
                "question": "Why should you pass a unique `key` prop when rendering a list of elements in React?",
                "options": [
                    "To help React's virtual DOM identify which items changed, were added, or removed",
                    "To apply unique CSS styles to list items",
                    "To enable automatic caching in localStorage",
                    "It is purely optional and has no performance benefit"
                ],
                "correct_answer": "To help React's virtual DOM identify which items changed, were added, or removed",
                "difficulty_score": 2.5
            }
        ],
        "Medium": [
            {
                "question": "What is the primary difference between `useMemo` and `useCallback` in React?",
                "options": [
                    "`useMemo` memoizes the computed return value; `useCallback` memoizes the callback function instance itself",
                    "`useCallback` runs synchronously before rendering; `useMemo` runs asynchronously",
                    "`useMemo` is for class components; `useCallback` is for functional components",
                    "They are identical and interchangeable aliases"
                ],
                "correct_answer": "`useMemo` memoizes the computed return value; `useCallback` memoizes the callback function instance itself",
                "difficulty_score": 5.0
            },
            {
                "question": "When does the cleanup function returned by `useEffect` execute?",
                "options": [
                    "Before the effect re-runs on dependency changes, and when the component unmounts",
                    "Only once when the browser window closes",
                    "Immediately before the component mounts for the first time",
                    "Every time any state variable in the entire app changes"
                ],
                "correct_answer": "Before the effect re-runs on dependency changes, and when the component unmounts",
                "difficulty_score": 5.5
            },
            {
                "question": "What problem does the React Context API solve?",
                "options": [
                    "Prop drilling by allowing data to be shared across the component tree without passing props down at every level",
                    "Automated database normalization",
                    "Compiling JavaScript into WebAssembly",
                    "Eliminating the need for CSS"
                ],
                "correct_answer": "Prop drilling by allowing data to be shared across the component tree without passing props down at every level",
                "difficulty_score": 4.5
            },
            {
                "question": "What is the difference between an uncontrolled component and a controlled component in React form inputs?",
                "options": [
                    "In a controlled component, form data is handled by React state (`value` and `onChange`); in an uncontrolled component, form data is handled by the DOM itself via `ref`",
                    "Uncontrolled components cannot have CSS styles",
                    "Controlled components cannot be rendered on the server",
                    "There is no difference"
                ],
                "correct_answer": "In a controlled component, form data is handled by React state (`value` and `onChange`); in an uncontrolled component, form data is handled by the DOM itself via `ref`",
                "difficulty_score": 5.5
            },
            {
                "question": "How does `React.memo()` optimize component rendering?",
                "options": [
                    "Performs a shallow comparison of props and skips rendering if props haven't changed",
                    "Caches component HTML in the browser's Service Worker",
                    "Renders the component in a Web Worker thread",
                    "Disables state updates inside the component"
                ],
                "correct_answer": "Performs a shallow comparison of props and skips rendering if props haven't changed",
                "difficulty_score": 6.0
            }
        ],
        "Hard": [
            {
                "question": "When does the callback inside `useLayoutEffect` execute relative to browser painting?",
                "options": [
                    "Synchronously after DOM mutations but before the browser paints",
                    "Asynchronously after the browser has completed painting",
                    "Before any reconciliation process starts",
                    "Inside a web worker thread"
                ],
                "correct_answer": "Synchronously after DOM mutations but before the browser paints",
                "difficulty_score": 8.0
            },
            {
                "question": "In React 18, what is the primary role of the Fiber architecture's concurrent renderer (`startTransition`, `useDeferredValue`)?",
                "options": [
                    "Enables interruptible rendering, allowing high-priority user interactions (typing/clicking) to interrupt non-urgent background render trees",
                    "Translates JSX directly into WebGL canvas instructions",
                    "Replaces the JavaScript event loop with native OS threads",
                    "Automatically memoizes every function component without manual hooks"
                ],
                "correct_answer": "Enables interruptible rendering, allowing high-priority user interactions (typing/clicking) to interrupt non-urgent background render trees",
                "difficulty_score": 9.0
            },
            {
                "question": "What causes an 'infinite re-render loop' when setting state inside `useEffect` without an appropriate dependency array?",
                "options": [
                    "Updating state triggers a re-render, which re-runs the effect, which updates state again unconditionally",
                    "React's garbage collector enters an infinite loop",
                    "The browser limits HTTP requests to 5 per second",
                    "The component unmounts and remounts continuously"
                ],
                "correct_answer": "Updating state triggers a re-render, which re-runs the effect, which updates state again unconditionally",
                "difficulty_score": 7.5
            },
            {
                "question": "How does React Suspense coordinate asynchronous data boundaries with Server-Side Rendering (SSR)?",
                "options": [
                    "Streams HTML chunks as they become ready while preserving client-side selective hydration for interactive parts of the page",
                    "Freezes the client browser until all database queries on the server finish",
                    "Replaces React with static HTML snapshots with zero client JavaScript",
                    "Executes client-side promises inside WebAssembly"
                ],
                "correct_answer": "Streams HTML chunks as they become ready while preserving client-side selective hydration for interactive parts of the page",
                "difficulty_score": 9.0
            },
            {
                "question": "What is the key rule regarding hook invocations in React components?",
                "options": [
                    "Hooks must only be called at the top level of React functions, never inside loops, conditions, or nested functions",
                    "Hooks must always be called inside a `try/catch` block",
                    "Hooks can only be called from class component `render` methods",
                    "A component cannot invoke more than 3 hooks total"
                ],
                "correct_answer": "Hooks must only be called at the top level of React functions, never inside loops, conditions, or nested functions",
                "difficulty_score": 7.5
            }
        ]
    },
    "Docker": {
        "Easy": [
            {
                "question": "What is the primary command used to start a new container from a Docker image?",
                "options": ["docker run", "docker start", "docker init", "docker launch"],
                "correct_answer": "docker run",
                "difficulty_score": 1.0
            },
            {
                "question": "What is the default filename used by Docker to build container images?",
                "options": ["Dockerfile", "Containerfile.yml", "docker-compose.json", "Imagefile"],
                "correct_answer": "Dockerfile",
                "difficulty_score": 1.0
            },
            {
                "question": "Which Docker instruction sets the base image for subsequent instructions in a Dockerfile?",
                "options": ["FROM", "BASE", "IMAGE", "ORIGIN"],
                "correct_answer": "FROM",
                "difficulty_score": 1.5
            },
            {
                "question": "Which flag is passed to `docker run` to run a container in the background (detached mode)?",
                "options": ["-d", "-b", "--async", "-bg"],
                "correct_answer": "-d",
                "difficulty_score": 1.5
            },
            {
                "question": "Which command lists all currently running Docker containers?",
                "options": ["docker ps", "docker list", "docker show", "docker status"],
                "correct_answer": "docker ps",
                "difficulty_score": 1.0
            }
        ],
        "Medium": [
            {
                "question": "What is the difference between the `CMD` and `ENTRYPOINT` instructions in a Dockerfile?",
                "options": [
                    "`ENTRYPOINT` defines the fixed executable, while `CMD` provides default arguments that can be overridden at runtime via `docker run`",
                    "`CMD` runs during `docker build`, while `ENTRYPOINT` runs during `docker run`",
                    "`ENTRYPOINT` is for root users only; `CMD` is for non-root users",
                    "They are identical and have no functional difference"
                ],
                "correct_answer": "`ENTRYPOINT` defines the fixed executable, while `CMD` provides default arguments that can be overridden at runtime via `docker run`",
                "difficulty_score": 5.0
            },
            {
                "question": "How do Docker volumes provide persistent storage compared to bind mounts?",
                "options": [
                    "Volumes are managed entirely by Docker inside `/var/lib/docker/volumes/` and are isolated from the host filesystem structure",
                    "Volumes are stored entirely in RAM and lost upon restart",
                    "Volumes can only be used with read-only containers",
                    "Bind mounts are automatically encrypted while volumes are not"
                ],
                "correct_answer": "Volumes are managed entirely by Docker inside `/var/lib/docker/volumes/` and are isolated from the host filesystem structure",
                "difficulty_score": 5.5
            },
            {
                "question": "What is the primary benefit of multi-stage Docker builds?",
                "options": [
                    "Separates the build environment (compilers/SDKs) from the final runtime image, resulting in dramatically smaller and more secure images",
                    "Enables running multiple containers inside a single image",
                    "Allows a container to run on ARM and x86 simultaneously",
                    "Bypasses Docker daemon security restrictions"
                ],
                "correct_answer": "Separates the build environment (compilers/SDKs) from the final runtime image, resulting in dramatically smaller and more secure images",
                "difficulty_score": 6.0
            },
            {
                "question": "Why is it important to place `COPY package.json ./` and `RUN npm install` BEFORE `COPY . .` in a Node.js Dockerfile?",
                "options": [
                    "To leverage Docker's layer caching so dependency installation is skipped if dependencies haven't changed",
                    "Because npm will fail if other files are in the working directory",
                    "To force npm to install dependencies in global mode",
                    "It has no effect on build speed"
                ],
                "correct_answer": "To leverage Docker's layer caching so dependency installation is skipped if dependencies haven't changed",
                "difficulty_score": 4.5
            },
            {
                "question": "What is the default network driver assigned to a container when created without specifying `--network`?",
                "options": ["bridge", "host", "overlay", "macvlan"],
                "correct_answer": "bridge",
                "difficulty_score": 5.0
            }
        ],
        "Hard": [
            {
                "question": "Which Linux kernel features form the fundamental isolation and resource limitation primitives underlying Docker containers?",
                "options": [
                    "Namespaces (for process, mount, network isolation) and cgroups (control groups for CPU/memory resource limiting)",
                    "KVM (Kernel-based Virtual Machine) and QEMU",
                    "systemd unit files and AppArmor profiles exclusively",
                    "eBPF filters and POSIX signals"
                ],
                "correct_answer": "Namespaces (for process, mount, network isolation) and cgroups (control groups for CPU/memory resource limiting)",
                "difficulty_score": 8.5
            },
            {
                "question": "Why is running a containerized process as PID 1 without an init system (like `tini` or `dumb-init`) problematic when the process spawns child sub-processes?",
                "options": [
                    "PID 1 does not automatically reap orphaned zombie processes and fails to forward POSIX termination signals (SIGTERM/SIGINT) to children properly",
                    "PID 1 causes CPU utilization to spike to 100% permanently",
                    "Docker daemon immediately kills containers that reach PID 1",
                    "Sub-processes cannot access the network without an init system"
                ],
                "correct_answer": "PID 1 does not automatically reap orphaned zombie processes and fails to forward POSIX termination signals (SIGTERM/SIGINT) to children properly",
                "difficulty_score": 9.0
            },
            {
                "question": "How does the Copy-on-Write (CoW) storage driver (such as overlay2) handle file modifications inside a running container?",
                "options": [
                    "Copies the file from the read-only lower image layer up to the container's writable layer before applying modifications",
                    "Modifies the underlying base image layer in place for all containers",
                    "Creates an in-memory duplicate of the entire disk",
                    "Writes changes to the host swap space exclusively"
                ],
                "correct_answer": "Copies the file from the read-only lower image layer up to the container's writable layer before applying modifications",
                "difficulty_score": 8.0
            },
            {
                "question": "In Docker security best practices, why is granting the `--privileged` flag considered a severe vulnerability in production?",
                "options": [
                    "It gives the container root access to all host devices and disables nearly all kernel security protections, allowing host root breakout",
                    "It increases image build times by 10x",
                    "It forces all network traffic through an unencrypted HTTP proxy",
                    "It deletes all persistent volumes upon container shutdown"
                ],
                "correct_answer": "It gives the container root access to all host devices and disables nearly all kernel security protections, allowing host root breakout",
                "difficulty_score": 8.5
            },
            {
                "question": "In Docker Swarm or Kubernetes, how does an `overlay` network enable container-to-container communication across multiple physical cluster nodes?",
                "options": [
                    "Encapsulates layer 2 container traffic inside layer 4 UDP packets (typically VXLAN on port 4789) routed across the underlay network",
                    "Creates physical Ethernet cables between containers dynamically",
                    "Requires public IP addresses for every container in the cluster",
                    "Relies on SSH tunneling between all host machines"
                ],
                "correct_answer": "Encapsulates layer 2 container traffic inside layer 4 UDP packets (typically VXLAN on port 4789) routed across the underlay network",
                "difficulty_score": 9.0
            }
        ]
    },
    "Data Structures": {
        "Easy": [
            {
                "question": "Which data structure operates on a Last-In, First-Out (LIFO) basis?",
                "options": ["Stack", "Queue", "Binary Tree", "Linked List"],
                "correct_answer": "Stack",
                "difficulty_score": 1.0
            },
            {
                "question": "What is the time complexity to access an element by index in a contiguous dynamic array?",
                "options": ["O(1)", "O(n)", "O(log n)", "O(n^2)"],
                "correct_answer": "O(1)",
                "difficulty_score": 1.5
            },
            {
                "question": "Which data structure operates on a First-In, First-Out (FIFO) basis?",
                "options": ["Queue", "Stack", "Binary Search Tree", "Heap"],
                "correct_answer": "Queue",
                "difficulty_score": 1.0
            },
            {
                "question": "In a singly linked list, what does each node store besides its payload data?",
                "options": ["A pointer to the next node", "Pointers to both the next and previous nodes", "An array index", "The memory size of the entire list"],
                "correct_answer": "A pointer to the next node",
                "difficulty_score": 1.5
            },
            {
                "question": "What is the average time complexity of searching for a value in a balanced Binary Search Tree (BST)?",
                "options": ["O(log n)", "O(1)", "O(n)", "O(n log n)"],
                "correct_answer": "O(log n)",
                "difficulty_score": 2.5
            },
            {
                "question": "Which data structure is typically used to implement Breadth-First Search (BFS) in a graph?",
                "options": ["Queue", "Stack", "Heap", "Hash Set"],
                "correct_answer": "Queue",
                "difficulty_score": 2.0
            }
        ],
        "Medium": [
            {
                "question": "What is the worst-case time complexity of quicksort when poor pivots are chosen?",
                "options": ["O(n^2)", "O(n log n)", "O(n)", "O(log n)"],
                "correct_answer": "O(n^2)",
                "difficulty_score": 4.5
            },
            {
                "question": "What is the time complexity to insert a new element into a min-heap containing N elements?",
                "options": ["O(log N)", "O(1)", "O(N)", "O(N log N)"],
                "correct_answer": "O(log N)",
                "difficulty_score": 5.0
            },
            {
                "question": "In a hash table, what is the 'Separate Chaining' technique used for?",
                "options": [
                    "Resolving hash collisions by storing multiple key-value pairs at the same bucket index using a linked list or red-black tree",
                    "Encrypting passwords before hashing",
                    "Rehashing the table when load factor drops below 0.1",
                    "Linking multiple hash tables across different database nodes"
                ],
                "correct_answer": "Resolving hash collisions by storing multiple key-value pairs at the same bucket index using a linked list or red-black tree",
                "difficulty_score": 5.5
            },
            {
                "question": "What is the primary difference between a binary tree and a Trie (prefix tree)?",
                "options": [
                    "In a Trie, node keys are not stored directly in nodes; instead, their position in the tree defines the associated prefix key (ideal for string search)",
                    "A Trie can only store floating point numbers",
                    "A Trie has a maximum depth of 2",
                    "A Trie is strictly a binary search tree with at most 2 children"
                ],
                "correct_answer": "In a Trie, node keys are not stored directly in nodes; instead, their position in the tree defines the associated prefix key (ideal for string search)",
                "difficulty_score": 6.0
            },
            {
                "question": "What is the space complexity of an adjacency matrix representation of a graph with V vertices and E edges?",
                "options": ["O(V^2)", "O(V + E)", "O(E^2)", "O(V * E)"],
                "correct_answer": "O(V^2)",
                "difficulty_score": 4.5
            },
            {
                "question": "Which sorting algorithm is guaranteed to have O(N log N) time complexity in the worst case and is stable?",
                "options": ["Merge Sort", "Quick Sort", "Heap Sort", "Selection Sort"],
                "correct_answer": "Merge Sort",
                "difficulty_score": 5.0
            }
        ],
        "Hard": [
            {
                "question": "What is the amortized cost per operation for union and find in a Disjoint Set (Union-Find) with path compression and union by rank?",
                "options": ["O(α(n)) (Inverse Ackermann)", "O(log n)", "O(1) strict", "O(n)"],
                "correct_answer": "O(α(n)) (Inverse Ackermann)",
                "difficulty_score": 8.5
            },
            {
                "question": "In a Red-Black Tree, what invariant guarantees that the tree remains balanced such that search operations are bounded by O(log N)?",
                "options": [
                    "The path from root to farthest leaf is no more than twice as long as the path to nearest leaf (every path from root to leaf has same black depth)",
                    "Every node must have exactly two non-null children",
                    "All leaf nodes must be colored red",
                    "The tree is completely rebuilt whenever an odd number of insertions occur"
                ],
                "correct_answer": "The path from root to farthest leaf is no more than twice as long as the path to nearest leaf (every path from root to leaf has same black depth)",
                "difficulty_score": 9.0
            },
            {
                "question": "What is the time complexity of building a heap (Heapify) from an arbitrary unordered array of N elements?",
                "options": ["O(N)", "O(N log N)", "O(log N)", "O(N^2)"],
                "correct_answer": "O(N)",
                "difficulty_score": 8.0
            },
            {
                "question": "What is the space-efficient probabilistic data structure used to test whether an element is a member of a set with zero false negatives but possible false positives?",
                "options": ["Bloom Filter", "Skip List", "Fibonacci Heap", "Suffix Automaton"],
                "correct_answer": "Bloom Filter",
                "difficulty_score": 8.5
            },
            {
                "question": "What is the worst-case time complexity of Tarjan's strongly connected components algorithm on a directed graph with V vertices and E edges?",
                "options": ["O(V + E)", "O(V * E)", "O(V^2)", "O(E log V)"],
                "correct_answer": "O(V + E)",
                "difficulty_score": 9.0
            },
            {
                "question": "How does a Segment Tree with Lazy Propagation achieve O(log N) range updates and range queries?",
                "options": [
                    "Postpones updating children nodes until those children need to be accessed by subsequent queries",
                    "Compresses all tree nodes into an uncompressed binary hash",
                    "Converts range updates into sequential O(1) pointer updates",
                    "Reroutes queries to a secondary B-Tree"
                ],
                "correct_answer": "Postpones updating children nodes until those children need to be accessed by subsequent queries",
                "difficulty_score": 9.5
            }
        ]
    },
    "Machine Learning": {
        "Easy": [
            {
                "question": "Which type of machine learning uses labeled training datasets to learn mapping functions?",
                "options": ["Supervised Learning", "Unsupervised Learning", "Reinforcement Learning", "Self-Organizing Maps"],
                "correct_answer": "Supervised Learning",
                "difficulty_score": 1.0
            },
            {
                "question": "Which metric evaluates the proportion of true positives among all instances predicted as positive?",
                "options": ["Precision", "Recall", "Accuracy", "Specificity"],
                "correct_answer": "Precision",
                "difficulty_score": 2.0
            },
            {
                "question": "What is the main objective of unsupervised learning algorithms like K-Means?",
                "options": ["Discover hidden patterns or cluster unlabeled data into groups", "Predict a continuous target price label", "Train a reward-maximizing agent in a simulator", "Classify images into known label classes"],
                "correct_answer": "Discover hidden patterns or cluster unlabeled data into groups",
                "difficulty_score": 1.5
            },
            {
                "question": "What common activation function maps any real number to a value strictly between 0 and 1?",
                "options": ["Sigmoid", "ReLU", "Tanh", "Softplus"],
                "correct_answer": "Sigmoid",
                "difficulty_score": 1.5
            },
            {
                "question": "What is the purpose of splitting data into training and test sets in ML pipelines?",
                "options": ["To evaluate model generalization on unseen data and prevent undetected overfitting", "To speed up matrix multiplication", "To reduce the dataset size to save cloud storage costs", "To balance imbalanced class weights automatically"],
                "correct_answer": "To evaluate model generalization on unseen data and prevent undetected overfitting",
                "difficulty_score": 2.0
            }
        ],
        "Medium": [
            {
                "question": "What common problem does L1 regularization (Lasso) mitigate by driving feature coefficients to zero?",
                "options": [
                    "Overfitting by performing automatic feature selection",
                    "Vanishing gradients in deep neural networks",
                    "Class imbalance in binary classification",
                    "Exploding learning rates"
                ],
                "correct_answer": "Overfitting by performing automatic feature selection",
                "difficulty_score": 5.0
            },
            {
                "question": "In the Bias-Variance tradeoff, what symptom characterizes a model with high variance?",
                "options": [
                    "Low training error but significantly higher cross-validation / test error (overfitting)",
                    "High training error and high test error (underfitting)",
                    "Consistently stable predictions across diverse training subsets",
                    "Premature convergence during gradient descent"
                ],
                "correct_answer": "Low training error but significantly higher cross-validation / test error (overfitting)",
                "difficulty_score": 5.5
            },
            {
                "question": "Why is the ROC-AUC score preferred over raw Accuracy for evaluating models trained on highly imbalanced datasets (e.g. 99% negative, 1% positive)?",
                "options": [
                    "A naive classifier predicting the majority class gets 99% accuracy but 0.5 ROC-AUC; ROC-AUC is invariant to class distribution shifts",
                    "ROC-AUC can only be calculated on small datasets",
                    "Accuracy requires matrix inversions which fail on imbalanced data",
                    "ROC-AUC automatically balances class weights during backpropagation"
                ],
                "correct_answer": "A naive classifier predicting the majority class gets 99% accuracy but 0.5 ROC-AUC; ROC-AUC is invariant to class distribution shifts",
                "difficulty_score": 6.0
            },
            {
                "question": "How does Random Forest reduce model variance compared to a single decision tree?",
                "options": [
                    "By combining predictions of multiple decorrelated trees trained on bootstrap samples with random feature subsets (Bagging)",
                    "By boosting sequential errors using adaptive weights",
                    "By using L2 regularization on tree branch depths",
                    "By eliminating all non-linear splits"
                ],
                "correct_answer": "By combining predictions of multiple decorrelated trees trained on bootstrap samples with random feature subsets (Bagging)",
                "difficulty_score": 5.5
            },
            {
                "question": "What is the primary advantage of the Adam optimizer over standard Stochastic Gradient Descent (SGD)?",
                "options": [
                    "Combines adaptive learning rates per parameter (from RMSprop) with momentum to accelerate convergence across sparse gradients",
                    "Guarantees finding the global minimum in non-convex loss surfaces",
                    "Eliminates the need for backpropagation",
                    "Requires zero hyperparameter tuning"
                ],
                "correct_answer": "Combines adaptive learning rates per parameter (from RMSprop) with momentum to accelerate convergence across sparse gradients",
                "difficulty_score": 6.5
            }
        ],
        "Hard": [
            {
                "question": "What is the core mathematical formulation of the Scaled Dot-Product Attention mechanism in Transformer models?",
                "options": [
                    "Attention(Q, K, V) = softmax(Q * K^T / sqrt(d_k)) * V",
                    "Attention(Q, K, V) = sigmoid(Q * K) + V",
                    "Attention(Q, K, V) = ReLU(Q * V) * K",
                    "Attention(Q, K, V) = normalize(Q + K + V)"
                ],
                "correct_answer": "Attention(Q, K, V) = softmax(Q * K^T / sqrt(d_k)) * V",
                "difficulty_score": 8.5
            },
            {
                "question": "How does Batch Normalization mitigate the internal covariate shift during deep neural network training?",
                "options": [
                    "Normalizes layer inputs across mini-batch mean and variance, and applies learnable scale (gamma) and shift (beta) parameters",
                    "Scales the learning rate by batch size squared",
                    "Randomly drops layer activations with probability 0.5",
                    "Replaces negative weights with zero during backpropagation"
                ],
                "correct_answer": "Normalizes layer inputs across mini-batch mean and variance, and applies learnable scale (gamma) and shift (beta) parameters",
                "difficulty_score": 8.5
            },
            {
                "question": "In gradient-boosted decision trees (e.g. XGBoost, LightGBM), how is each new tree fitted in the sequence?",
                "options": [
                    "It is fitted to the pseudo-residuals (negative gradient of the loss function) with respect to the current ensemble's predictions",
                    "It is trained on a randomly shuffled subset of the original labels",
                    "It is trained to minimize the tree height of previous trees",
                    "It is initialized with random weights and never pruned"
                ],
                "correct_answer": "It is fitted to the pseudo-residuals (negative gradient of the loss function) with respect to the current ensemble's predictions",
                "difficulty_score": 9.0
            },
            {
                "question": "What is the Vanishing Gradient problem in Deep Recurrent Neural Networks (RNNs) and how do LSTMs resolve it?",
                "options": [
                    "Repeated matrix multiplications cause gradients to decay exponentially over time; LSTMs provide an additive constant-error carousel via the cell state",
                    "Gradients grow to infinity; LSTMs apply gradient clipping to 1.0",
                    "Neurons stop firing; LSTMs replace weights with biases",
                    "Data overflows float32 memory; LSTMs use int8 quantization"
                ],
                "correct_answer": "Repeated matrix multiplications cause gradients to decay exponentially over time; LSTMs provide an additive constant-error carousel via the cell state",
                "difficulty_score": 9.0
            },
            {
                "question": "What is the key difference between Self-Supervised Learning (e.g. BERT masked language modeling, SimCLR) and traditional Unsupervised Learning?",
                "options": [
                    "Self-supervised learning generates pseudo-labels automatically from input data structure itself to formulate a supervised pretext task without human labeling",
                    "Self-supervised learning requires active human feedback in real time",
                    "Self-supervised learning can only be applied to tabular CSV data",
                    "There is no difference; they are exact synonyms"
                ],
                "correct_answer": "Self-supervised learning generates pseudo-labels automatically from input data structure itself to formulate a supervised pretext task without human labeling",
                "difficulty_score": 9.5
            }
        ]
    },
    "JavaScript": {
        "Easy": [
            {
                "question": "Which keyword declares a block-scoped variable in modern ECMAScript?",
                "options": ["let", "var", "scope", "global"],
                "correct_answer": "let",
                "difficulty_score": 1.0
            },
            {
                "question": "What is the output of `typeof null` in JavaScript?",
                "options": ["'object'", "'null'", "'undefined'", "'number'"],
                "correct_answer": "'object'",
                "difficulty_score": 2.0
            },
            {
                "question": "Which array method creates a new array populated with the results of calling a provided function on every element?",
                "options": ["map()", "forEach()", "filter()", "reduce()"],
                "correct_answer": "map()",
                "difficulty_score": 1.5
            },
            {
                "question": "What is the difference between `==` and `===` in JavaScript?",
                "options": [
                    "`===` checks both value and type (strict equality); `==` performs type coercion before comparison",
                    "`==` checks value and type; `===` only checks value",
                    "They are identical in modern JavaScript engines",
                    "`===` only works with numbers"
                ],
                "correct_answer": "`===` checks both value and type (strict equality); `==` performs type coercion before comparison",
                "difficulty_score": 1.5
            },
            {
                "question": "Which keyword is used to handle asynchronous operations cleanly in modern JavaScript?",
                "options": ["async / await", "defer / resume", "spawn / join", "thread / yield"],
                "correct_answer": "async / await",
                "difficulty_score": 1.5
            }
        ],
        "Medium": [
            {
                "question": "What is a closure in JavaScript?",
                "options": [
                    "A function bundled together with references to its surrounding lexical environment (enabling access to outer variables even after the outer function has closed)",
                    "A function that automatically terminates after 100 milliseconds",
                    "A method that converts an object into a JSON string",
                    "A private variable declared with the `#` symbol"
                ],
                "correct_answer": "A function bundled together with references to its surrounding lexical environment (enabling access to outer variables even after the outer function has closed)",
                "difficulty_score": 5.0
            },
            {
                "question": "In the JavaScript Event Loop, what is the execution order of microtasks (e.g. `Promise.then`) and macrotasks (e.g. `setTimeout`)?",
                "options": [
                    "All pending microtasks run to completion before the next macrotask is dequeued and executed",
                    "Macrotasks always execute before microtasks",
                    "They alternate strictly 1-to-1",
                    "Order is non-deterministic and randomized by the browser engine"
                ],
                "correct_answer": "All pending microtasks run to completion before the next macrotask is dequeued and executed",
                "difficulty_score": 6.0
            },
            {
                "question": "What happens when you access a property on an object that does not exist directly on that object?",
                "options": [
                    "JavaScript traverses the prototype chain (`__proto__`) upward until the property is found or `null` is reached (returning `undefined`)",
                    "A `ReferenceError` is thrown immediately",
                    "The property is automatically created and assigned `null`",
                    "The browser crashes"
                ],
                "correct_answer": "JavaScript traverses the prototype chain (`__proto__`) upward until the property is found or `null` is reached (returning `undefined`)",
                "difficulty_score": 5.5
            },
            {
                "question": "What is the output of `[1, 2, 3] + [4, 5, 6]` in JavaScript?",
                "options": ["'1,2,34,5,6'", "[1, 2, 3, 4, 5, 6]", "NaN", "TypeError"],
                "correct_answer": "'1,2,34,5,6'",
                "difficulty_score": 5.0
            },
            {
                "question": "What is the difference between `call()`, `apply()`, and `bind()` on a JavaScript function?",
                "options": [
                    "`call()` invokes with comma-separated arguments; `apply()` invokes with an array of arguments; `bind()` returns a new function with `this` bound",
                    "`bind()` executes immediately; `call()` returns a promise",
                    "`apply()` only works in browser workers",
                    "They are identical aliases"
                ],
                "correct_answer": "`call()` invokes with comma-separated arguments; `apply()` invokes with an array of arguments; `bind()` returns a new function with `this` bound",
                "difficulty_score": 5.5
            }
        ],
        "Hard": [
            {
                "question": "In the V8 engine, how does Hidden Classes (Shapes) and Inline Caches (IC) optimize property access on JavaScript objects?",
                "options": [
                    "Objects with identical property layouts share hidden classes, allowing the JIT compiler to generate direct memory offset reads instead of dictionary lookups",
                    "Converts all objects into immutable flat strings",
                    "Executes all property accesses inside C++ shared libraries",
                    "Caches properties exclusively in localStorage"
                ],
                "correct_answer": "Objects with identical property layouts share hidden classes, allowing the JIT compiler to generate direct memory offset reads instead of dictionary lookups",
                "difficulty_score": 9.0
            },
            {
                "question": "How does `Promise.allSettled()` differ from `Promise.all()` in JavaScript?",
                "options": [
                    "`Promise.allSettled()` waits for all promises to either resolve or reject and returns an array of status objects; `Promise.all()` rejects immediately if any single promise rejects",
                    "`Promise.allSettled()` rejects if any promise takes more than 1 second",
                    "`Promise.all()` runs sequentially while `Promise.allSettled()` runs in parallel",
                    "`Promise.allSettled()` only works with fetch requests"
                ],
                "correct_answer": "`Promise.allSettled()` waits for all promises to either resolve or reject and returns an array of status objects; `Promise.all()` rejects immediately if any single promise rejects",
                "difficulty_score": 7.5
            },
            {
                "question": "What is the difference between a `WeakMap` and a standard `Map` in JavaScript regarding garbage collection?",
                "options": [
                    "Keys in a `WeakMap` must be objects and are held weakly: if no other references to a key object exist, it can be garbage collected along with its value",
                    "WeakMaps store data on disk instead of memory",
                    "WeakMaps can store primitive types as keys",
                    "WeakMaps prevent objects from being garbage collected"
                ],
                "correct_answer": "Keys in a `WeakMap` must be objects and are held weakly: if no other references to a key object exist, it can be garbage collected along with its value",
                "difficulty_score": 8.5
            },
            {
                "question": "What occurs when code attempts to mutate an object that was frozen with `Object.freeze()` in 'use strict' mode?",
                "options": [
                    "A `TypeError` is thrown",
                    "The mutation succeeds silently",
                    "The object is cloned into a mutable copy",
                    "A warning is logged to console but execution continues"
                ],
                "correct_answer": "A `TypeError` is thrown",
                "difficulty_score": 7.5
            },
            {
                "question": "In JavaScript generator functions (`function*`), what does `yield*` do?",
                "options": [
                    "Delegates iteration to another iterable or generator function",
                    "Terminates the generator permanently",
                    "Converts the generator into an asynchronous promise",
                    "Doubles the yielded numeric value"
                ],
                "correct_answer": "Delegates iteration to another iterable or generator function",
                "difficulty_score": 8.0
            }
        ]
    }
}

